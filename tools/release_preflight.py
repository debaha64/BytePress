#!/usr/bin/env python3
"""Read-only release evidence. Semantic owner: docs/technical/release-evidence.md.

Only preflight/readback are public CLI operations. No write, retry, shell,
release engine, implicit authorization or generic-checker integration.
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tarfile
import zipfile


class PreflightError(ValueError):
    """Fixed, non-secret error code; external stderr is never forwarded."""


SETTINGS = ('allow_merge_commit', 'allow_squash_merge', 'allow_rebase_merge',
            'allow_auto_merge', 'delete_branch_on_merge')
REPO_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}\Z')
LOGIN_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9-]{0,38}\Z')
SHA_RE = re.compile(r'[0-9a-f]{40}\Z')
REF_RE = re.compile(r'refs/(heads|tags)/[A-Za-z0-9][A-Za-z0-9._/-]*\Z')
PR_PARAMETERS = frozenset(('allowed_merge_methods', 'dismiss_stale_reviews_on_push',
                          'require_code_owner_review', 'require_last_push_approval',
                          'required_approving_review_count', 'required_review_thread_resolution',
                          'require_extra_approval_for_unattributed_changes', 'required_reviewers'))
SECRET_KEYS = frozenset(('token', 'access_token', 'password', 'secret', 'credentials',
                        'credential', 'environment', 'env', 'authorization_header'))
SECRET_KEY_RE = re.compile(r'(?:^|_)(?:token|secret|password|credentials?|private_key)(?:_|$)', re.I)
SECRET_RE = re.compile(r'(?:gh[pousr]_[A-Za-z0-9_]{16,}|github_pat_[A-Za-z0-9_]+|Bearer\s+\S+)', re.I)
WRITE_PERMISSIONS = frozenset(('write', 'maintain', 'admin'))
MAX_PAGES = 20
MAX_BYTES = 128 * 1024 * 1024


def _safe(value):
    # Validate structure and credential syntax, independent of environment values.
    def visit(item):
        if isinstance(item, dict):
            for key, val in item.items():
                if not isinstance(key, str) or key.lower() in SECRET_KEYS or SECRET_KEY_RE.search(key):
                    raise PreflightError('UNSAFE_EVIDENCE')
                visit(key); visit(val)
        elif isinstance(item, (list, tuple)):
            for val in item: visit(val)
        elif isinstance(item, str):
            if SECRET_RE.search(item):
                raise PreflightError('UNSAFE_EVIDENCE')
        elif item is not None and type(item) not in (bool, int, float):
            raise PreflightError('INVALID_DATA_TYPE')
    visit(value)


def canonical(value):
    _safe(value)
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + '\n'
    except (ValueError, UnicodeError, TypeError):
        raise PreflightError('INVALID_JSON') from None


def digest(value):
    try: return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()
    except UnicodeError: raise PreflightError('INVALID_UNICODE') from None


def _decode(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result: raise PreflightError('DUPLICATE_JSON_KEY')
            result[k] = v
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(PreflightError('INVALID_JSON')))
    except (ValueError, TypeError, UnicodeError):
        raise PreflightError('INVALID_JSON') from None


def _identity(actor):
    return {k: actor[k] for k in ('login', 'id')}


def _policy(rule):
    return {k: v for k, v in rule.items() if k not in ('bypass_actors', 'current_user_can_bypass')}


def _ordered(items):
    return sorted(items, key=canonical)


def _ref(value):
    if not isinstance(value, str) or not REF_RE.fullmatch(value) or '..' in value or '//' in value or value.endswith('/'):
        raise PreflightError('INVALID_REF')
    return value


def _contract(contract):
    _safe(contract)
    required = {'schema_version', 'gate_id', 'repository', 'expected_actor', 'refs', 'settings',
                'rulesets', 'chain', 'candidate', 'pr_numbers'}
    if set(contract) != required or contract['schema_version'] != 1:
        raise PreflightError('INVALID_CONTRACT')
    repo = contract['repository']
    if set(repo) != {'full_name', 'id', 'visibility', 'default_branch'} or not REPO_RE.fullmatch(repo['full_name']):
        raise PreflightError('INVALID_REPOSITORY')
    if type(repo['id']) is not int or repo['id'] <= 0 or repo['visibility'] not in ('public', 'private', 'internal'):
        raise PreflightError('INVALID_REPOSITORY')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,199}', contract['gate_id']):
        raise PreflightError('INVALID_GATE')
    if set(contract['settings']) != set(SETTINGS) or any(type(v) is not bool for v in contract['settings'].values()):
        raise PreflightError('INVALID_SETTINGS')
    chain = contract['chain']
    if set(chain) != {'pr_author', 'last_pusher', 'approvers', 'merger', 'publisher',
                      'source_ref', 'base_ref', 'working_ref', 'merge_method'}:
        raise PreflightError('INVALID_CHAIN')
    names = [chain[k] for k in ('pr_author', 'last_pusher', 'merger', 'publisher')] + chain['approvers']
    if not names or not all(isinstance(n, str) and LOGIN_RE.fullmatch(n) for n in names):
        raise PreflightError('INVALID_ACTOR')
    if len(set(chain['approvers'])) != len(chain['approvers']): raise PreflightError('DUPLICATE_APPROVER')
    if set(contract['expected_actor']) != {'login', 'id'} or not LOGIN_RE.fullmatch(contract['expected_actor']['login']):
        raise PreflightError('INVALID_ACTOR')
    for key in ('source_ref', 'base_ref', 'working_ref'):
        _ref(chain[key])
        if not chain[key].startswith('refs/heads/'): raise PreflightError('CHAIN_REQUIRES_BRANCH_REFS')
    if type(contract['expected_actor']['id']) is not int or contract['expected_actor']['id'] <= 0: raise PreflightError('INVALID_ACTOR_ID')
    if chain['merge_method'] not in ('merge', 'squash', 'rebase'): raise PreflightError('INVALID_MERGE_METHOD')
    for ref, entry in contract['refs'].items():
        _ref(ref)
        if set(entry) != {'sha', 'type'} or not SHA_RE.fullmatch(entry['sha']) or entry['type'] not in ('tag', 'commit'):
            raise PreflightError('INVALID_REF_OBJECT')
    for key in ('source_ref', 'base_ref'):
        if chain[key] not in contract['refs']: raise PreflightError('MISSING_EXPECTED_REF')
    candidate = contract['candidate']
    if set(candidate) != {'kind', 'ref', 'sha'} or candidate['kind'] != 'ref':
        raise PreflightError('INVALID_CANDIDATE')
    if candidate['ref'] != chain['source_ref'] or candidate['sha'] != contract['refs'][chain['source_ref']]['sha']:
        raise PreflightError('CANDIDATE_REF_MISMATCH')
    if not isinstance(contract['pr_numbers'], list) or any(type(n) is not int or n <= 0 for n in contract['pr_numbers']):
        raise PreflightError('INVALID_PR_SELECTION')


def _observation(observation, contract):
    """Reject incomplete evidence before any positive verdict can be derived."""
    _safe(observation)
    try:
        required = {'schema_version', 'observed_at', 'repository', 'actor', 'refs', 'rulesets',
                    'protections', 'permissions', 'pulls', 'releases'}
        if set(observation) - {'open_pr_numbers'} != required or observation['schema_version'] != 1: raise PreflightError('INVALID_OBSERVATION')
        timestamp = datetime.fromisoformat(observation['observed_at'].replace('Z', '+00:00'))
        if timestamp.tzinfo is None or timestamp.utcoffset().total_seconds() != 0: raise PreflightError('OBSERVATION_TIME_NOT_UTC')
        repository = observation['repository']
        if set(repository) != {'full_name', 'id', 'visibility', 'archived', 'default_branch', 'settings'}: raise PreflightError('INCOMPLETE_REPOSITORY')
        if type(repository['archived']) is not bool or type(repository['id']) is not int: raise PreflightError('INVALID_REPOSITORY_TYPES')
        if set(repository['settings']) != set(SETTINGS) or any(type(v) is not bool for v in repository['settings'].values()): raise PreflightError('INVALID_SETTINGS_TYPES')
        actor = observation['actor']
        if set(actor) != {'login', 'id', 'type'} or type(actor['id']) is not int or actor['id'] <= 0: raise PreflightError('INVALID_ACTOR_ID')
        actor_ids = set()
        for name, permission in observation['permissions'].items():
            if set(permission) != {'login', 'id', 'type', 'permission'} or permission['login'] != name or type(permission['id']) is not int:
                raise PreflightError('INVALID_PERMISSION_OBSERVATION')
            if permission['id'] <= 0 or permission['id'] in actor_ids: raise PreflightError('ACTOR_IDENTITY_COLLISION')
            actor_ids.add(permission['id'])
        authenticated_permission = observation['permissions'].get(actor['login'])
        if authenticated_permission is None or _identity(authenticated_permission) != _identity(actor): raise PreflightError('ACTOR_PERMISSION_IDENTITY_MISMATCH')
        for ref, value in observation['refs'].items():
            _ref(ref)
            if set(value) != {'sha', 'type'} or not SHA_RE.fullmatch(value['sha']) or value['type'] not in ('commit', 'tag'): raise PreflightError('INVALID_REF_OBJECT')
        targets = {contract['chain'][k] for k in ('source_ref', 'base_ref')}
        if set(observation['protections']) != targets: raise PreflightError('INCOMPLETE_CLASSIC_OBSERVATION')
        for protection in observation['protections'].values():
            if protection.get('state') not in ('ABSENT', 'PRESENT', 'UNKNOWN'): raise PreflightError('INVALID_CLASSIC_STATE')
            if protection['state'] == 'ABSENT' and protection.get('source') != 'admin-api': raise PreflightError('CLASSIC_ABSENCE_NOT_PROVED')
        seen = set()
        for rule in observation['rulesets']:
            required = {'id', 'name', 'target', 'source', 'source_type', 'enforcement', 'conditions', 'rules'}
            if not required <= rule.keys() or set(rule) - required - {'bypass_actors', 'current_user_can_bypass'}: raise PreflightError('INVALID_RULESET_SCHEMA')
            if type(rule['id']) is not int or rule['id'] <= 0 or rule['id'] in seen: raise PreflightError('DUPLICATE_RULESET')
            seen.add(rule['id'])
            if not isinstance(rule['rules'], list): raise PreflightError('INVALID_RULE_LIST')
        if 'open_pr_numbers' in observation:
            numbers = observation['open_pr_numbers']
            if not isinstance(numbers, list) or any(type(n) is not int or n <= 0 for n in numbers) or len(set(numbers)) != len(numbers):
                raise PreflightError('INVALID_OPEN_PR_INVENTORY')
        if not isinstance(observation['pulls'], dict) or not isinstance(observation['releases'], dict): raise PreflightError('INVALID_OBJECT_INVENTORY')
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        if isinstance(exc, PreflightError): raise
        raise PreflightError('INVALID_OBSERVATION') from None


class GitHubReader:
    """One fixed host, closed endpoint set, explicit GET and bounded pagination."""
    def __init__(self, repository, *, timeout=30, runner=None):
        if not REPO_RE.fullmatch(repository): raise PreflightError('INVALID_REPOSITORY')
        if type(timeout) not in (float, int) or not math.isfinite(timeout) or timeout <= 0:
            raise PreflightError('INVALID_TIMEOUT')
        self.repository = repository
        self.prefix = 'repos/' + repository
        self.timeout = timeout
        self.runner = runner or subprocess.run

    def get(self, endpoint, *, method='GET'):
        base, separator, query = endpoint.partition('?')
        suffix = base[len(self.prefix):] if base.startswith(self.prefix) else None
        valid = base == 'user' or suffix == '' or (suffix is not None and bool(re.fullmatch(
            r'/(?:git/matching-refs/(?:heads|tags)|rulesets(?:/[1-9][0-9]*)?|'
            r'collaborators/[A-Za-z0-9-]+/permission|'
            r'branches/[A-Za-z0-9._/-]+/protection|pulls(?:/[1-9][0-9]*(?:/reviews)?)?|'
            r'git/commits/[0-9a-f]{40}|releases)', suffix)))
        if method != 'GET' or not valid or '..' in base or '//' in base:
            raise PreflightError('GET_BOUNDARY_REJECTED')
        if separator and not re.fullmatch(r'(?:state=open&)?(?:includes_parents=true&)?per_page=100&page=[1-9][0-9]*', query):
            raise PreflightError('GET_BOUNDARY_REJECTED')
        argv = ['gh', 'api', '--hostname', 'github.com', '--method', 'GET',
                '-H', 'Accept: application/vnd.github+json', endpoint]
        try:
            result = self.runner(argv, shell=False, timeout=self.timeout, stdin=subprocess.DEVNULL,
                                 capture_output=True, text=True,
                                 env={**os.environ, 'GH_DEBUG': '', 'NO_COLOR': '1', 'GH_PROMPT_DISABLED': '1'})
        except (OSError, subprocess.SubprocessError):
            raise PreflightError('READ_ONLY_ACCESS_UNAVAILABLE') from None
        if len(result.stdout) > MAX_BYTES: raise PreflightError('API_RESPONSE_TOO_LARGE')
        data = _decode(result.stdout)
        if result.returncode:
            if suffix and suffix.endswith('/protection') and data.get('status') == '404':
                return {'_http_status': 404}
            raise PreflightError('READ_ONLY_ACCESS_UNAVAILABLE')
        return data

    def pages(self, suffix, query=''):
        results = []
        for page in range(1, MAX_PAGES + 1):
            part = self.get(f'{self.prefix}{suffix}?{query}per_page=100&page={page}')
            if not isinstance(part, list): raise PreflightError('INVALID_API_LIST')
            results.extend(part)
            if len(part) < 100: return results
        raise PreflightError('INCOMPLETE_ENUMERATION')


def observe(contract, *, runner=None, timeout=30):
    """Fresh normalized snapshot. No cached observation is accepted as live."""
    _contract(contract)
    api = GitHubReader(contract['repository']['full_name'], runner=runner, timeout=timeout)
    raw_actor = api.get('user'); raw_repo = api.get(api.prefix)
    actor = {k: raw_actor[k] for k in ('login', 'id', 'type')}
    repository = {k: raw_repo[k] for k in ('full_name', 'id', 'visibility', 'archived', 'default_branch')}
    repository['settings'] = {k: raw_repo[k] for k in SETTINGS}
    if _identity(actor) != contract['expected_actor'] or repository['full_name'] != contract['repository']['full_name'] or repository['id'] != contract['repository']['id']:
        raise PreflightError('LIVE_IDENTITY_MISMATCH')
    chain = contract['chain']
    names = sorted(set([chain[k] for k in ('pr_author', 'last_pusher', 'merger', 'publisher')]
                       + chain['approvers'] + [actor['login']]))
    permissions = {}
    for name in names:
        data = api.get(api.prefix + '/collaborators/' + name + '/permission')
        permissions[name] = {**_identity(data['user']), 'type': data['user']['type'], 'permission': data['permission']}
    refs = {}
    for kind in ('heads', 'tags'):
        for entry in api.pages('/git/matching-refs/' + kind):
            ref = _ref(entry['ref'])
            if ref in refs: raise PreflightError('DUPLICATE_REF')
            refs[ref] = {k: entry['object'][k] for k in ('sha', 'type')}
    rulesets = []
    seen = set()
    for summary in api.pages('/rulesets', 'includes_parents=true&'):
        ident = summary['id']
        if type(ident) is not int or ident <= 0 or ident in seen: raise PreflightError('INVALID_RULESET_ID')
        seen.add(ident)
        data = api.get(api.prefix + '/rulesets/' + str(ident))
        if any(data.get(k) != summary.get(k) for k in ('id', 'name', 'target', 'enforcement', 'source', 'source_type')):
            raise PreflightError('RULESET_IDENTITY_DRIFT')
        rule = {k: data[k] for k in ('id', 'name', 'target', 'enforcement', 'source', 'source_type', 'conditions', 'rules')}
        rule['rules'] = _ordered(rule['rules'])
        for key in ('bypass_actors', 'current_user_can_bypass'):
            if key in data: rule[key] = data[key]
        rulesets.append(rule)
    protections = {}
    for ref in sorted(set((chain['source_ref'], chain['base_ref']))):
        data = api.get(api.prefix + '/branches/' + ref.removeprefix('refs/heads/') + '/protection')
        if data.get('_http_status') == 404:
            # API 404 alone cannot distinguish absent policy from hidden policy.
            protections[ref] = {'state': 'UNKNOWN', 'source': 'api', 'http_status': 404}
        else:
            keys = ('required_status_checks', 'enforce_admins', 'required_pull_request_reviews',
                    'restrictions', 'required_linear_history', 'allow_force_pushes', 'allow_deletions',
                    'block_creations', 'required_conversation_resolution', 'lock_branch')
            protections[ref] = {'state': 'PRESENT', 'source': 'api', 'http_status': 200,
                                'rules': {k: data[k] for k in keys if k in data}}
    pulls = {}
    selected = contract['pr_numbers']
    if len(selected) > 1: raise PreflightError('AMBIGUOUS_PR_SELECTION')
    open_numbers = [p['number'] for p in api.pages('/pulls', 'state=open&')]
    if any(type(n) is not int or n <= 0 for n in open_numbers) or len(set(open_numbers)) != len(open_numbers):
        raise PreflightError('INVALID_OPEN_PR_INVENTORY')
    for number in selected:
        endpoint = api.prefix + '/pulls/' + str(number)
        p = _pull(api.get(endpoint), number)
        reviews = api.pages('/pulls/' + str(number) + '/reviews')
        normalized = []
        for raw in reviews:
            # Missing fields remain unknown; neither body nor raw errors enter evidence.
            user = raw.get('user') or {}
            normalized.append({**{k: raw.get(k) for k in ('id', 'state', 'commit_id', 'submitted_at')},
                               'user': {k: user.get(k) for k in ('login', 'id', 'type')}})
        if _pull(api.get(endpoint), number) != p: raise PreflightError('PR_CHANGED_DURING_REVIEW_OBSERVATION')
        p['reviews'] = normalized
        if p['merged']:
            merge_sha = p['merge_commit_sha']
            if not isinstance(merge_sha, str) or not SHA_RE.fullmatch(merge_sha): raise PreflightError('INVALID_MERGE_SHA')
            commit = api.get(api.prefix + '/git/commits/' + merge_sha)
            if commit['sha'] != merge_sha: raise PreflightError('MERGE_OBJECT_MISMATCH')
            p['merge_parents'] = [x['sha'] for x in commit['parents']]
        pulls[str(number)] = p
    releases = {}
    for raw in api.pages('/releases'):
        r = {k: raw[k] for k in ('id', 'tag_name', 'target_commitish', 'draft', 'prerelease')}
        r['author'] = _identity(raw['author'])
        r['assets'] = sorted([{k: a.get(k) for k in ('id', 'name', 'size', 'digest')} for a in raw['assets']], key=lambda a: a['id'])
        if str(r['id']) in releases: raise PreflightError('DUPLICATE_RELEASE')
        releases[str(r['id'])] = r
    result = {'schema_version': 1, 'observed_at': datetime.now(timezone.utc).isoformat(),
              'repository': repository, 'actor': actor, 'refs': refs, 'rulesets': sorted(rulesets, key=lambda r: r['id']),
              'protections': protections, 'permissions': permissions, 'pulls': pulls, 'releases': releases,
              'open_pr_numbers': sorted(open_numbers)}
    _safe(result)
    return result



def _pull(raw, number):
    """Normalize one selected object; endpoint number never replaces observed identity."""
    if type(raw.get('number')) is not int or raw['number'] != number:
        raise PreflightError('SELECTED_PR_IDENTITY_MISMATCH')
    p = {k: raw[k] for k in ('number', 'state', 'draft', 'merged', 'merge_commit_sha')}
    p.update(author=_identity(raw['user']), merged_by=_identity(raw['merged_by']) if raw['merged_by'] else None,
             mergeable=raw.get('mergeable'))
    for side in ('head', 'base'):
        obj = raw[side]; repo = obj.get('repo')
        p[side + '_ref'] = obj['ref']; p[side + '_sha'] = obj['sha']
        p[side + '_repository'] = {k: repo[k] for k in ('id', 'full_name')} if repo else None
    return p

def _human(observation, contract, human):
    if human is None: return {'verdict': 'NOT_PROVIDED', 'reasons': []}
    try:
        _safe(human)
        if set(human) != {'schema_version', 'source', 'observed_date', 'observer', 'gate_id', 'repository', 'rulesets', 'classic_protection'}:
            raise PreflightError('HUMAN_SCHEMA')
        if human['schema_version'] != 1 or human['source'] != 'owner-admin-github-web-settings': raise PreflightError('HUMAN_SOURCE')
        if human['gate_id'] != contract['gate_id'] or human['observed_date'] != observation['observed_at'][:10]: raise PreflightError('HUMAN_GATE_OR_DATE')
        if human['repository'] != {k: observation['repository'][k] for k in ('full_name', 'id')}: raise PreflightError('HUMAN_REPOSITORY')
        permission = observation['permissions'].get(human['observer']['login'], {})
        if permission.get('permission') != 'admin' or _identity(permission) != human['observer']: raise PreflightError('HUMAN_ADMIN_IDENTITY')
        rules = {r['id']: r for r in observation['rulesets']}
        if len(human['rulesets']) != len(rules) or {r['id'] for r in human['rulesets']} != set(rules): raise PreflightError('HUMAN_RULESET_SET')
        for h in human['rulesets']:
            r = rules[h['id']]
            if set(h) != {'id', 'name', 'target', 'enforcement', 'conditions', 'bypass_actors'}: raise PreflightError('HUMAN_RULESET_SCHEMA')
            if any(h[k] != r[k] for k in ('id', 'name', 'target', 'enforcement', 'conditions')): raise PreflightError('HUMAN_RULESET_BINDING')
            if h['bypass_actors'] != [] or ('bypass_actors' in r and r['bypass_actors'] != []): raise PreflightError('HUMAN_BYPASS_CONFLICT')
        if human['classic_protection'] != 'ABSENT' or any(p['state'] == 'PRESENT' for p in observation['protections'].values()): raise PreflightError('HUMAN_CLASSIC_CONFLICT')
        return {'verdict': 'PASS', 'reasons': [], 'evidence': copy.deepcopy(human)}
    except (KeyError, TypeError, PreflightError):
        return {'verdict': 'FAIL', 'reasons': ['HUMAN_POLICY_NOT_BOUND']}


def _applies(rule, ref, default_branch):
    conditions = rule.get('conditions', {})
    if set(conditions) != {'ref_name'}: raise PreflightError('UNSUPPORTED_RULE_CONDITION')
    names = conditions['ref_name']
    if set(names) != {'include', 'exclude'}: raise PreflightError('UNSUPPORTED_RULE_CONDITION')
    def match(pattern):
        if pattern == '~ALL': return True
        if pattern == '~DEFAULT_BRANCH': return ref == 'refs/heads/' + default_branch
        # No approximation of GitHub fnmatch/FNM_PATHNAME semantics.
        if any(c in pattern for c in '*?['): raise PreflightError('UNSUPPORTED_RULE_PATTERN')
        return pattern == ref
    return any(match(p) for p in names['include']) and not any(match(p) for p in names['exclude'])


def _feasibility(observation, contract, human):
    chain = contract['chain']; reasons = []; requirements = []
    names = [chain[k] for k in ('pr_author', 'last_pusher', 'merger', 'publisher')] + chain['approvers']
    for name in names:
        p = observation['permissions'].get(name, {})
        if p.get('login') != name or p.get('permission') not in WRITE_PERMISSIONS or p.get('type') != 'User': reasons.append('ACTOR_PERMISSION_OR_TYPE_UNKNOWN')
    if chain['pr_author'] in chain['approvers']: reasons.append('SELF_REVIEW_NOT_ALLOWED')
    method_setting = {'merge': 'allow_merge_commit', 'squash': 'allow_squash_merge', 'rebase': 'allow_rebase_merge'}
    if observation['repository']['settings'][method_setting[chain['merge_method']]] is not True: reasons.append('MERGE_METHOD_DISABLED')
    if chain['source_ref'] == chain['base_ref']: reasons.append('SOURCE_BASE_SEPARATION_REQUIRED')
    if chain['working_ref'] == chain['base_ref']: reasons.append('WORKING_BASE_SEPARATION_REQUIRED')
    if chain['working_ref'] in observation['refs']:
        if observation['refs'][chain['working_ref']] != observation['refs'].get(chain['source_ref']): reasons.append('WORKING_REF_NOT_FROZEN_CANDIDATE')
    for protection in observation['protections'].values():
        if protection['state'] == 'PRESENT': reasons.append('CLASSIC_POLICY_REVIEW_REQUIRED')
        elif protection['state'] == 'UNKNOWN' and human['verdict'] != 'PASS': reasons.append('CLASSIC_POLICY_UNKNOWN')
    for rule in observation['rulesets']:
        if rule['enforcement'] != 'active':
            if rule['enforcement'] not in ('disabled', 'evaluate'): reasons.append('UNKNOWN_ENFORCEMENT')
            continue
        if rule.get('bypass_actors') != [] and human['verdict'] != 'PASS': reasons.append('BYPASS_NOT_PROVED_EMPTY')
        if rule.get('bypass_actors') == [] and rule.get('current_user_can_bypass') not in (None, 'never'):
            reasons.append('BYPASS_POLICY_CONTRADICTION')
        if rule['target'] != 'branch': reasons.append('TAG_OR_PUSH_POLICY_REVIEW_REQUIRED'); continue
        try:
            on_base = _applies(rule, chain['base_ref'], observation['repository']['default_branch'])
            on_work = _applies(rule, chain['working_ref'], observation['repository']['default_branch'])
        except PreflightError:
            reasons.append('UNSUPPORTED_POLICY_CONDITION'); continue
        for item in rule['rules']:
            kind = item.get('type')
            if kind not in ('deletion', 'non_fast_forward', 'required_linear_history', 'pull_request'):
                reasons.append('UNKNOWN_BLOCKING_RULE'); continue
            if kind != 'pull_request' and set(item) != {'type'}: reasons.append('UNKNOWN_RULE_PARAMETERS')
            if kind == 'pull_request':
                p = item.get('parameters', {})
                if set(item) != {'type', 'parameters'} or set(p) - PR_PARAMETERS:
                    reasons.append('UNKNOWN_RULE_PARAMETERS'); continue
                required = PR_PARAMETERS - {'require_extra_approval_for_unattributed_changes', 'required_reviewers'}
                if not required <= p.keys(): reasons.append('MISSING_REVIEW_PARAMETERS'); continue
                booleans = required - {'allowed_merge_methods', 'required_approving_review_count'}
                booleans |= {'require_extra_approval_for_unattributed_changes'} & p.keys()
                if any(type(p[k]) is not bool for k in booleans) or type(p['required_approving_review_count']) is not int or not 0 <= p['required_approving_review_count'] <= 10:
                    reasons.append('INVALID_REVIEW_PARAMETER_TYPES'); continue
                if not isinstance(p['allowed_merge_methods'], list) or not p['allowed_merge_methods'] or set(p['allowed_merge_methods']) - {'merge', 'squash', 'rebase'}:
                    reasons.append('INVALID_REVIEW_MERGE_METHODS'); continue
                if on_work and chain['working_ref'] != chain['source_ref']: reasons.append('WORKING_BRANCH_REQUIRES_PR')
                if on_base:
                    requirements.append(p)
                    if chain['merge_method'] not in p['allowed_merge_methods']: reasons.append('RULE_MERGE_METHOD_CONFLICT')
                    if p['require_last_push_approval'] and not set(chain['approvers']) - {chain['last_pusher']}:
                        reasons.append('LAST_PUSH_APPROVAL_ACTOR_CONFLICT')
                    if type(p['required_approving_review_count']) is not int or p['required_approving_review_count'] > len(chain['approvers']): reasons.append('INSUFFICIENT_APPROVERS')
                    if p['require_code_owner_review'] or p.get('required_reviewers'): reasons.append('DESIGNATED_REVIEWER_UNPROVED')
            if on_base and kind == 'required_linear_history' and chain['merge_method'] == 'merge': reasons.append('LINEAR_HISTORY_MERGE_CONFLICT')
    return {'verdict': 'BLOCKED' if reasons else 'PASS', 'reasons': sorted(set(reasons)),
            'sequence': copy.deepcopy(chain), 'review_requirements': requirements,
            'scope': 'potential-route-only; exact push/head/reviews must be observed at future gate'}



def _pr_binding(observation, contract):
    """Bind exactly one selected live PR; actor expectations are never observations."""
    numbers = contract['pr_numbers']; pulls = observation['pulls']
    if len(numbers) != 1: return ['EXACTLY_ONE_SELECTED_PR_REQUIRED']
    if set(pulls) != {str(numbers[0])}: return ['SELECTED_PR_INVENTORY_MISMATCH']
    p = pulls[str(numbers[0])]; chain = contract['chain']; failures = []
    if not isinstance(p, dict): return ['SELECTED_PR_METADATA_MISSING']
    repo = {k: observation['repository'][k] for k in ('full_name', 'id')}
    expected_repo = {k: contract['repository'][k] for k in ('full_name', 'id')}
    author = observation['permissions'].get(chain['pr_author'], {})
    if type(p.get('number')) is not int or p['number'] != numbers[0]: failures.append('SELECTED_PR_IDENTITY_MISMATCH')
    if p.get('state') != 'open': failures.append('SELECTED_PR_NOT_OPEN')
    if p.get('draft') is not False: failures.append('SELECTED_PR_DRAFT_OR_UNKNOWN')
    if p.get('merged') is not False or 'merged_by' not in p or p['merged_by'] is not None:
        failures.append('SELECTED_PR_ALREADY_MERGED_OR_UNKNOWN')
    if p.get('author') != {k: author.get(k) for k in ('login', 'id')}: failures.append('SELECTED_PR_AUTHOR_MISMATCH')
    for side, ref in (('head', chain['working_ref']), ('base', chain['base_ref'])):
        sha = contract['candidate']['sha'] if side == 'head' else contract['refs'][ref]['sha']
        if p.get(side + '_ref') != ref.removeprefix('refs/heads/'): failures.append('SELECTED_PR_' + side.upper() + '_REF_MISMATCH')
        if p.get(side + '_sha') != sha or observation['refs'].get(ref) != {'sha': sha, 'type': 'commit'}:
            failures.append('SELECTED_PR_' + side.upper() + '_SHA_MISMATCH')
        if p.get(side + '_repository') != repo or repo != expected_repo:
            failures.append('SELECTED_PR_' + side.upper() + '_REPOSITORY_MISMATCH')
    return failures


def _reviews(pull, observation, contract):
    """Count distinct current-head terminal approvals from observed review records."""
    reviews = pull.get('reviews'); findings = []; latest = {}; seen = set()
    if not isinstance(reviews, list): return [], ['PR_REVIEWS_NOT_OBSERVED']
    previous_time = None
    for review in reviews:
        try:
            if set(review) != {'id', 'user', 'state', 'commit_id', 'submitted_at'}:
                raise ValueError()
            user = review['user']; state = review['state']; ident = review['id']
            if type(ident) is not int or ident <= 0 or ident in seen: raise ValueError()
            seen.add(ident)
            if set(user) != {'login', 'id', 'type'} or type(user['id']) is not int or user['id'] <= 0:
                raise ValueError()
            if not isinstance(user['login'], str) or not LOGIN_RE.fullmatch(user['login']) or user['type'] != 'User':
                raise ValueError()
            if state not in ('APPROVED', 'CHANGES_REQUESTED', 'COMMENTED', 'DISMISSED', 'PENDING'): raise ValueError()
            if state == 'PENDING': continue
            if not isinstance(review['commit_id'], str) or not SHA_RE.fullmatch(review['commit_id']): raise ValueError()
            when = datetime.fromisoformat(review['submitted_at'].replace('Z', '+00:00'))
            observed_at = datetime.fromisoformat(observation['observed_at'].replace('Z', '+00:00'))
            if when.tzinfo is None or when > observed_at or (previous_time is not None and when < previous_time): raise ValueError()
            previous_time = when
            if state == 'COMMENTED': continue
            name = user['login']; permission = observation['permissions'].get(name, {})
            if {k: permission.get(k) for k in ('login', 'id', 'type')} != user or permission.get('permission') not in WRITE_PERMISSIONS:
                findings.append('REVIEWER_IDENTITY_OR_PERMISSION_UNPROVED')
            # API order is chronological; a later terminal state supersedes approval.
            latest[user['id']] = review
        except (KeyError, TypeError, ValueError, AttributeError):
            findings.append('REVIEW_STATE_UNKNOWN')
    valid = []
    for review in latest.values():
        name = review['user']['login']
        if review['state'] == 'CHANGES_REQUESTED': findings.append('PR_CHANGES_REQUESTED')
        if review['state'] != 'APPROVED': continue
        if review['commit_id'] != pull['head_sha']:
            findings.append('APPROVAL_NOT_CURRENT_HEAD'); continue
        if name == contract['chain']['pr_author'] or name not in contract['chain']['approvers']:
            findings.append('APPROVER_NOT_SEPARATE_OR_PLANNED'); continue
        permission = observation['permissions'].get(name, {})
        if {k: permission.get(k) for k in ('login', 'id', 'type')} != review['user'] or permission.get('permission') not in WRITE_PERMISSIONS:
            continue
        valid.append(name)
    return sorted(set(valid)), findings


def _exact_pr_gate(observation, contract, chain):
    if not contract['pr_numbers']:
        reasons = ['UNSELECTED_PR_OBSERVATION'] if observation['pulls'] else []
        return {'verdict': 'FAIL' if reasons else 'NOT_YET_OBSERVED', 'pr_binding': 'NOT_ASSESSED',
                'reasons': reasons, 'valid_approvers': [], 'latest_reviewable_pusher': 'UNKNOWN'}
    failures = _pr_binding(observation, contract)
    result = {'pr_binding': 'FAIL' if failures else 'PASS', 'valid_approvers': [],
              'latest_reviewable_pusher': 'UNKNOWN', 'pr_numbers': list(contract['pr_numbers'])}
    if failures: return {**result, 'verdict': 'FAIL', 'reasons': sorted(set(failures))}
    pull = observation['pulls'][str(contract['pr_numbers'][0])]
    valid, findings = _reviews(pull, observation, contract)
    if pull.get('mergeable') is False: failures.append('PR_MERGE_CONFLICT')
    elif pull.get('mergeable') is not True: findings.append('PR_MERGEABILITY_UNKNOWN')
    for policy in chain['review_requirements']:
        if len(valid) < policy['required_approving_review_count']: findings.append('INSUFFICIENT_CURRENT_HEAD_APPROVALS')
        # REST reviews do not identify the latest reviewable pusher or resolved threads.
        # No contract field, commit author or undocumented mergeable_state is proof.
        if policy['require_last_push_approval']: findings.append('LATEST_REVIEWABLE_PUSH_UNPROVED')
        if policy['required_review_thread_resolution']: findings.append('CONVERSATION_RESOLUTION_UNPROVED')
        if policy['require_code_owner_review'] or policy.get('required_reviewers'): findings.append('DESIGNATED_REVIEWER_UNPROVED')
    findings.extend(chain['reasons'])
    return {**result, 'valid_approvers': valid, 'verdict': 'FAIL' if failures else 'OWNER_ACTION_REQUIRED' if findings else 'PASS',
            'reasons': sorted(set(failures + findings))}

def _result(operation, observation, contract, verdict, findings, chain, human=None, **extra):
    result = {'schema_version': 1, 'operation': operation, 'verdict': verdict,
              'observation': copy.deepcopy(observation), 'contract': copy.deepcopy(contract),
              'observation_digest': digest(observation), 'findings': sorted(set(findings)),
              'actor_chain': chain, 'human_reconciliation': human or {'verdict': 'NOT_PROVIDED', 'reasons': []},
              'write_authorized': False, 'external_writes': 0,
              'product_acceptance': 'not-performed', 'release_authorization': 'not-performed', **extra}
    result['evidence_digest'] = digest(result)
    return result


def preflight(observation, contract, human_policy=None):
    _contract(contract); _observation(observation, contract)
    findings = []; failures = []
    if observation.get('schema_version') != 1: raise PreflightError('INVALID_OBSERVATION')
    for key, value in contract['repository'].items():
        if observation['repository'].get(key) != value: failures.append('REPOSITORY_' + key.upper() + '_MISMATCH')
    if observation['repository']['archived'] is not False: failures.append('REPOSITORY_ARCHIVED')
    if _identity(observation['actor']) != contract['expected_actor']: failures.append('AUTHENTICATED_ACTOR_MISMATCH')
    if observation['refs'] != contract['refs']: failures.append('REF_INVENTORY_OR_SHA_DRIFT')
    if observation['repository']['settings'] != contract['settings']: failures.append('SETTINGS_DRIFT')
    expected = copy.deepcopy(contract['rulesets']); actual = [_policy(r) for r in observation['rulesets']]
    for rules in (expected, actual):
        for r in rules: r['rules'] = _ordered(r['rules'])
    if _ordered(actual) != _ordered(expected): failures.append('RULESET_STRUCTURE_DRIFT')
    human = _human(observation, contract, human_policy)
    if human['verdict'] == 'FAIL': failures.append('HUMAN_POLICY_NOT_BOUND')
    if any(r.get('bypass_actors') != [] for r in observation['rulesets']): findings.append('BYPASS_POLICY_UNKNOWN_OR_NONEMPTY')
    if any(p['state'] != 'ABSENT' for p in observation['protections'].values()): findings.append('CLASSIC_POLICY_UNKNOWN_OR_PRESENT')
    chain = _feasibility(observation, contract, human)
    findings.extend(chain['reasons'])
    gate = _exact_pr_gate(observation, contract, chain)
    if gate['verdict'] == 'FAIL': failures.extend(gate['reasons'])
    elif gate['verdict'] == 'OWNER_ACTION_REQUIRED': findings.extend(gate['reasons'])
    if failures: verdict = 'FAIL'
    elif findings: verdict = 'OWNER_ACTION_REQUIRED'
    else: verdict = 'PASS'
    return _result('preflight', observation, contract, verdict, findings + failures, chain, human,
                   scope='exact-pr-gate' if contract['pr_numbers'] else 'potential-route-only', exact_pr_gate=gate)


def readback(before, delta, observation):
    """Pure comparison of independently collected post-state; never a write."""
    _safe(before); _safe(delta); _safe(observation)
    contract = before['contract']; _contract(contract)
    findings = []; actual = copy.deepcopy(observation); expected = copy.deepcopy(before['observation'])
    try:
        _observation(observation, contract); _observation(before['observation'], contract)
        if set(delta) != {'schema_version', 'gate_id', 'pre_digest', 'action', 'actor', 'merge_method', 'changes'} or delta['schema_version'] != 1: raise PreflightError('INVALID_DELTA')
        if delta['pre_digest'] != digest(expected) or before['observation_digest'] != digest(expected): raise PreflightError('PRE_OBSERVATION_DIGEST_MISMATCH')
        unsigned = {k: v for k, v in before.items() if k != 'evidence_digest'}
        if digest(unsigned) != before['evidence_digest']: raise PreflightError('PRE_EVIDENCE_DIGEST_MISMATCH')
        if delta['gate_id'] != contract['gate_id']: raise PreflightError('GATE_MISMATCH')
        if delta['action'] not in ('observe', 'merge', 'release', 'tag', 'push', 'pr'): raise PreflightError('UNSUPPORTED_ACTION')
        actor = delta['actor']
        permission = observation['permissions'].get(actor.get('login'), {})
        if not permission or _identity(permission) != actor: raise PreflightError('DELTA_ACTOR_IDENTITY_MISMATCH')
        if delta['action'] != 'observe' and permission['permission'] not in WRITE_PERMISSIONS: raise PreflightError('DELTA_ACTOR_PERMISSION_MISMATCH')
        role = {'release': 'publisher', 'tag': 'publisher', 'merge': 'merger', 'pr': 'pr_author', 'push': 'last_pusher'}.get(delta['action'])
        if role and actor['login'] != contract['chain'][role]: raise PreflightError('FROZEN_ACTOR_CHAIN_MISMATCH')
        if delta['action'] == 'observe' and (delta['changes'] or delta['actor'] != _identity(expected['actor'])): raise PreflightError('OBSERVE_IS_NOT_WRITE')
        if delta['action'] != 'observe' and not delta['changes']: raise PreflightError('NOOP_WRITE')
        if delta['action'] == 'release' and any(c.get('collection') != 'releases' for c in delta['changes']): raise PreflightError('RELEASE_CANNOT_PROVE_REF_WRITE')
        if delta['action'] == 'merge':
            if _pr_binding(before['observation'], contract): raise PreflightError('MERGE_PRESTATE_PR_NOT_BOUND')
            if delta['merge_method'] != contract['chain']['merge_method']: raise PreflightError('FROZEN_MERGE_METHOD_MISMATCH')
            for change in delta['changes']:
                if change.get('collection') == 'pulls' and change.get('key') != str(contract['pr_numbers'][0]):
                    raise PreflightError('MERGE_SELECTED_PR_MISMATCH')
                if change.get('collection') == 'refs':
                    if change.get('key') not in (contract['chain']['base_ref'], contract['chain']['working_ref']): raise PreflightError('MERGE_UNRELATED_REF')
                    if change['key'] == contract['chain']['working_ref'] and change.get('after') is not None: raise PreflightError('MERGE_UNEXPECTED_HEAD_PUSH')
                elif change.get('collection') != 'pulls': raise PreflightError('MERGE_UNRELATED_OBJECT')
        seen = set()
        for change in delta['changes']:
            if set(change) != {'collection', 'key', 'before', 'after'}: raise PreflightError('INVALID_OBJECT_DELTA')
            collection, key = change['collection'], change['key']
            if collection not in ('refs', 'pulls', 'releases') or (collection, key) in seen: raise PreflightError('UNAUTHORIZED_OBJECT_KIND')
            if collection == 'refs': _ref(key)
            else:
                ident = 'number' if collection == 'pulls' else 'id'
                if any(value is not None and str(value.get(ident)) != key for value in (change['before'], change['after'])):
                    raise PreflightError('EXTERNAL_OBJECT_IDENTITY_MISMATCH')
            seen.add((collection, key))
            if change['before'] == change['after'] or expected[collection].get(key) != change['before']: raise PreflightError('NOOP_OR_PRESTATE_MISMATCH')
            if change['after'] is None: expected[collection].pop(key)
            else: expected[collection][key] = copy.deepcopy(change['after'])
        # Open inventory changes are justified only by independently read selected
        # PR state transitions in the exact delta; unrelated numbers stay frozen.
        if 'open_pr_numbers' in expected:
            open_numbers = set(expected['open_pr_numbers'])
            for change in delta['changes']:
                if change['collection'] != 'pulls': continue
                number = int(change['key']); old = change['before']; new = change['after']
                if bool(old and old.get('state') == 'open') != (number in open_numbers):
                    raise PreflightError('PRE_OPEN_PR_INVENTORY_MISMATCH')
                if new and new.get('state') == 'open': open_numbers.add(number)
                else: open_numbers.discard(number)
            expected['open_pr_numbers'] = sorted(open_numbers)
        expected.pop('observed_at', None); actual.pop('observed_at', None)
        if actual != expected: raise PreflightError('UNEXPECTED_OR_PARTIAL_EXTERNAL_DELTA')
    except (KeyError, TypeError, PreflightError) as exc:
        code = str(exc) if isinstance(exc, PreflightError) else 'INVALID_READBACK_INPUT'
        return _result('readback', observation, contract, 'FAIL', [code], {'verdict': 'NOT_ASSESSED'}, comparison_verdict='FAIL')
    action = delta['action']; actor = delta['actor']
    if action == 'release':
        changed = [c['after'] for c in delta['changes'] if c['collection'] == 'releases' and c['after']]
        if len(changed) != 1 or changed[0].get('author') != actor: findings.append('RELEASE_ACTOR_OR_IDENTITY_MISMATCH')
    elif action == 'merge':
        changes = [c for c in delta['changes'] if c['collection'] == 'pulls' and c['after']]
        if len(changes) != 1: findings.append('MERGE_PR_IDENTITY_MISMATCH')
        else:
            old, merged = changes[0]['before'], changes[0]['after']
            if merged.get('merged') is not True or merged.get('merged_by') != actor or merged.get('state') != 'closed': findings.append('MERGE_ACTOR_OR_STATE_MISMATCH')
            if not old or any(merged.get(k) != old.get(k) for k in ('number', 'author', 'head_ref', 'head_sha', 'base_ref', 'head_repository', 'base_repository')):
                findings.append('MERGE_PR_BINDING_MISMATCH')
            if delta['merge_method'] != 'merge': findings.append('MERGE_METHOD_NOT_INDEPENDENTLY_OBSERVABLE')
            elif not old or merged.get('merge_parents') != [old.get('base_sha'), old.get('head_sha')]: findings.append('MERGE_PARENT_PROOF_MISMATCH')
            target = observation['refs'].get(contract['chain']['base_ref'], {})
            if target.get('sha') != merged.get('merge_commit_sha'): findings.append('MERGE_REF_MISMATCH')
    elif action in ('tag', 'push', 'pr'):
        findings.append('ACTION_ACTOR_NOT_INDEPENDENTLY_OBSERVABLE')
    failures = [f for f in findings if f.endswith('MISMATCH')]
    if any(r.get('bypass_actors') != [] for r in observation['rulesets']): findings.append('BYPASS_POLICY_UNKNOWN_OR_NONEMPTY')
    if any(p['state'] != 'ABSENT' for p in observation['protections'].values()): findings.append('CLASSIC_POLICY_UNKNOWN_OR_PRESENT')
    verdict = 'FAIL' if failures else 'OWNER_ACTION_REQUIRED' if findings else 'PASS'
    return _result('readback', observation, contract, verdict, findings, {'verdict': 'NOT_ASSESSED'},
                   comparison_verdict='PASS', expected_delta_digest=digest(delta))


def format_report(result, level='owner'):
    if level == 'machine': return canonical(result)
    repo = result['observation']['repository']; candidate = result['contract']['candidate']
    lines = [f"Verdict: {result['verdict']}", f"Target: {repo['full_name']} (ID {repo['id']}); {result['contract']['gate_id']}",
             f"Candidate: {candidate['ref']}@{candidate['sha']}", f"Actor-chain: {result['actor_chain']['verdict']}",
             f"Scope: {result.get('scope', 'independent-readback')}; exact PR gate: {result.get('exact_pr_gate', {}).get('verdict', 'NOT_ASSESSED')}",
             'Blockers: ' + (', '.join(result['findings'][:5]) or 'none') + ('; остальные в engineering evidence' if len(result['findings']) > 5 else ''),
             'Owner action: ' + ('рассмотреть exact gate evidence; write не разрешён' if result['verdict'] == 'PASS' else 'разрешить findings; обновить gate observation; write не разрешён')]
    if level == 'engineering':
        lines += ['Actor: ' + result['observation']['actor']['login'],
                  'Refs: ' + ', '.join(ref + '@' + data['sha'] for ref, data in sorted(result['observation']['refs'].items()) if ref.startswith('refs/heads/')),
                  'Settings: ' + canonical(repo['settings']).strip(),
                  'Rulesets: ' + ', '.join(str(r['id']) + '/' + r['name'] + '/' + r['enforcement'] for r in result['observation']['rulesets']),
                  'Findings: ' + ', '.join(result['findings']),
                  'Human reconciliation: ' + result['human_reconciliation']['verdict'],
                  'OBSERVATION_SHA256: ' + result['observation_digest'], 'EVIDENCE_SHA256: ' + result['evidence_digest']]
    elif level != 'owner': raise PreflightError('INVALID_REPORT_FORMAT')
    text = '\n'.join(lines) + '\n'; _safe(text); return text


def _entry(kind, mode, content=None):
    return {'type': kind, 'mode': mode, 'sha256': hashlib.sha256(content).hexdigest() if content is not None else None}


def _archive_path(name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or '\x00' in name or '//' in name:
        raise PreflightError('UNSAFE_ARCHIVE_PATH')
    if name.rstrip('/') != p.as_posix(): raise PreflightError('NONCANONICAL_ARCHIVE_PATH')
    return p


def transport_manifest(path, transport, *, zip_posix=False):
    path = Path(path); result = {}
    if transport in ('filesystem', 'git-checkout'):
        if not path.is_dir() or path.is_symlink(): raise PreflightError('UNSAFE_FILESYSTEM_ROOT')
        for current, dirs, files in os.walk(path, followlinks=False):
            if transport == 'git-checkout' and Path(current) == path:
                # Checkout service metadata is not a Git tree entry; never read it.
                dirs[:] = [n for n in dirs if n != '.git']
                files[:] = [n for n in files if n != '.git']
            for child in [Path(current)] + [Path(current) / n for n in dirs + files]:
                s = child.lstat(); key = child.relative_to(path).as_posix()
                if stat.S_ISDIR(s.st_mode): result[key] = _entry('directory', stat.S_IMODE(s.st_mode))
                elif stat.S_ISREG(s.st_mode) and s.st_nlink == 1:
                    if s.st_size > MAX_BYTES: raise PreflightError('ARTIFACT_TOO_LARGE')
                    result[key] = _entry('file', stat.S_IMODE(s.st_mode), child.read_bytes())
                else: raise PreflightError('LINK_OR_SPECIAL_NODE')
        if transport == 'git-checkout':
            result = {k: {**v, 'mode': '100755' if v['mode'] & 0o111 else '100644'} for k, v in result.items() if v['type'] == 'file'}
        return result
    if path.is_symlink() or not path.is_file(): raise PreflightError('UNSAFE_ARCHIVE_FILE')
    roots = set(); seen = set(); total = 0
    def add(name, kind, mode, content=None):
        p = _archive_path(name); roots.add(p.parts[0])
        key = p.relative_to(p.parts[0]).as_posix()
        if key in seen: raise PreflightError('DUPLICATE_ARCHIVE_PATH')
        seen.add(key); result[key] = _entry(kind, mode, content)
    try:
        if transport == 'tar.gz':
            with tarfile.open(path, 'r:gz') as tf:
                for m in tf:
                    if not (m.isdir() or m.isfile()) or m.linkname: raise PreflightError('LINK_OR_SPECIAL_NODE')
                    total += m.size
                    if total > MAX_BYTES: raise PreflightError('ARTIFACT_TOO_LARGE')
                    add(m.name, 'directory' if m.isdir() else 'file', m.mode & 0o7777, tf.extractfile(m).read() if m.isfile() else None)
        elif transport == 'zip':
            with zipfile.ZipFile(path) as zf:
                for info in zf.infolist():
                    mode = info.external_attr >> 16; kind = stat.S_IFMT(mode)
                    if kind not in (0, stat.S_IFDIR, stat.S_IFREG): raise PreflightError('LINK_OR_SPECIAL_NODE')
                    if kind and (kind == stat.S_IFDIR) != info.is_dir(): raise PreflightError('ZIP_NODE_TYPE_CONFLICT')
                    if info.flag_bits & 1: raise PreflightError('ENCRYPTED_ARCHIVE')
                    if zip_posix and (info.create_system != 3 or kind == 0): raise PreflightError('ZIP_POSIX_NOT_PROVED')
                    total += info.file_size
                    if total > MAX_BYTES: raise PreflightError('ARTIFACT_TOO_LARGE')
                    add(info.filename, 'directory' if info.is_dir() else 'file', stat.S_IMODE(mode) if zip_posix else None,
                        None if info.is_dir() else zf.read(info))
        else: raise PreflightError('UNSUPPORTED_TRANSPORT')
    except (tarfile.TarError, zipfile.BadZipFile, OSError, EOFError): raise PreflightError('INVALID_ARCHIVE') from None
    if len(roots) != 1 or result.get('.', {}).get('type') != 'directory': raise PreflightError('UNSAFE_SINGLE_ROOT')
    for key in result:
        for parent in PurePosixPath(key).parents:
            if parent.as_posix() in result and result[parent.as_posix()]['type'] != 'directory': raise PreflightError('ARCHIVE_PARENT_TYPE_CONFLICT')
    return result


def git_tree_manifest(entries):
    result = {}
    for entry in entries:
        path = _archive_path(entry['path']).as_posix()
        if path == '.' or path in result or entry['mode'] not in ('100644', '100755'): raise PreflightError('UNSUPPORTED_GIT_TREE_ENTRY')
        result[path] = _entry('file', entry['mode'], entry['content'])
    for path in result:
        if any(p.as_posix() in result for p in PurePosixPath(path).parents): raise PreflightError('GIT_PATH_TYPE_CONFLICT')
    return result


def compare_candidate(expected, artifact, transport, *, zip_posix=False):
    actual = transport_manifest(artifact, transport, zip_posix=zip_posix)
    wanted = copy.deepcopy(expected)
    if transport == 'zip' and not zip_posix:
        wanted = {k: {**v, 'mode': None} for k, v in wanted.items()}
    equal = wanted == actual
    return {'transport': transport, 'equal': equal, 'properties': 'path/type/content/mode' if transport != 'zip' or zip_posix else 'path/type/content',
            'expected_digest': digest(wanted), 'actual_digest': digest(actual)}


def verify_release_asset(path, name, sha256, expected_manifest, archive_format):
    path = Path(path)
    if path.name != name or path.is_symlink() or not path.is_file(): raise PreflightError('ASSET_IDENTITY_MISMATCH')
    if hashlib.sha256(path.read_bytes()).hexdigest() != sha256: raise PreflightError('DOWNLOADED_ASSET_CHECKSUM_MISMATCH')
    return compare_candidate(expected_manifest, path, archive_format)


def _load(path):
    p = Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size > MAX_BYTES: raise PreflightError('UNSAFE_INPUT_FILE')
    value = _decode(p.read_text(encoding='utf-8')); _safe(value); return value


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        # argparse normally echoes rejected user input, which may be a credential.
        self.exit(2, 'FAIL: INVALID_CLI_ARGUMENTS; external_writes=0\n')


def main(argv=None):
    parser = _Parser(description='Read-only release evidence; external write и authorization отсутствуют.')
    commands = parser.add_subparsers(dest='operation', required=True)
    for operation in ('preflight', 'readback'):
        p = commands.add_parser(operation)
        p.add_argument('--contract', required=True)
        p.add_argument('--timeout', type=float, default=30)
        p.add_argument('--format', choices=('owner', 'engineering', 'machine'), default='owner')
        if operation == 'preflight': p.add_argument('--human-policy')
        else:
            p.add_argument('--before', required=True)
            p.add_argument('--delta', required=True)
    args = parser.parse_args(argv)
    try:
        contract = _load(args.contract)
        observation = observe(contract, timeout=args.timeout)
        if args.operation == 'preflight': result = preflight(observation, contract, _load(args.human_policy) if args.human_policy else None)
        else:
            before = _load(args.before)
            if before['contract'] != contract: raise PreflightError('READBACK_CONTRACT_MISMATCH')
            result = readback(before, _load(args.delta), observation)
        print(format_report(result, args.format), end='')
        return 0 if result['verdict'] == 'PASS' else 2 if result['verdict'] == 'OWNER_ACTION_REQUIRED' else 1
    except (PreflightError, OSError, ValueError, KeyError, TypeError, UnicodeError):
        print('FAIL: RELEASE_EVIDENCE_INPUT_OR_OBSERVATION; external_writes=0')
        return 1


if __name__ == '__main__': raise SystemExit(main())

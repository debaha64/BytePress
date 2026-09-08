"""REQ-REL-001..009 / SCN-REL-001..012: isolated release evidence contracts."""

import copy
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
A = '1' * 40
B = '2' * 40
C = '3' * 40


def fixture(working_ref='refs/heads/develop'):
    pr = {'type': 'pull_request', 'parameters': {
        'allowed_merge_methods': ['merge'], 'dismiss_stale_reviews_on_push': False,
        'require_code_owner_review': False, 'require_last_push_approval': True,
        'required_approving_review_count': 1, 'required_review_thread_resolution': True,
        'require_extra_approval_for_unattributed_changes': True, 'required_reviewers': []}}
    rule = {'id': 10, 'name': 'stable', 'target': 'branch', 'enforcement': 'active',
            'source': 'example/Project', 'source_type': 'Repository',
            'conditions': {'ref_name': {'include': ['refs/heads/main'], 'exclude': []}},
            'rules': [{'type': 'deletion'}, {'type': 'non_fast_forward'}, pr],
            'bypass_actors': [], 'current_user_can_bypass': 'never'}
    settings = {'allow_merge_commit': True, 'allow_squash_merge': True,
                'allow_rebase_merge': False, 'allow_auto_merge': False,
                'delete_branch_on_merge': True}
    repository = {'full_name': 'example/Project', 'id': 100, 'visibility': 'public',
                  'archived': False, 'default_branch': 'develop', 'settings': settings}
    refs = {'refs/heads/main': {'sha': A, 'type': 'commit'},
            'refs/heads/develop': {'sha': B, 'type': 'commit'}}
    chain = {'pr_author': 'writer', 'last_pusher': 'writer', 'approvers': ['owner'],
             'merger': 'owner', 'publisher': 'owner', 'source_ref': 'refs/heads/develop',
             'base_ref': 'refs/heads/main', 'working_ref': working_ref,
             'merge_method': 'merge'}
    policy_rule = {k: v for k, v in rule.items() if k not in ('bypass_actors', 'current_user_can_bypass')}
    contract = {'schema_version': 1, 'gate_id': 'GATE-EXAMPLE-RECON',
                'repository': {k: repository[k] for k in ('full_name', 'id', 'visibility', 'default_branch')},
                'expected_actor': {'login': 'writer', 'id': 101}, 'refs': refs,
                'settings': settings, 'rulesets': [policy_rule], 'chain': chain,
                'candidate': {'kind': 'ref', 'ref': 'refs/heads/develop', 'sha': B},
                'pr_numbers': []}
    observation = {'schema_version': 1, 'observed_at': '2026-09-05T12:00:00Z',
                   'repository': repository, 'actor': {'login': 'writer', 'id': 101, 'type': 'User'},
                   'refs': refs, 'rulesets': [rule],
                   'protections': {r: {'state': 'ABSENT', 'source': 'admin-api', 'http_status': 404}
                                   for r in ('refs/heads/main', 'refs/heads/develop')},
                   'permissions': {'writer': {'login': 'writer', 'id': 101, 'type': 'User', 'permission': 'write'},
                                   'owner': {'login': 'owner', 'id': 102, 'type': 'User', 'permission': 'admin'}},
                   'pulls': {}, 'releases': {}}
    return copy.deepcopy(observation), copy.deepcopy(contract)


def human_policy(observation, contract):
    return {'schema_version': 1, 'source': 'owner-admin-github-web-settings',
            'observed_date': '2026-09-05', 'observer': {'login': 'owner', 'id': 102},
            'gate_id': contract['gate_id'], 'repository': {'full_name': 'example/Project', 'id': 100},
            'rulesets': [{k: copy.deepcopy(r[k]) for k in ('id', 'name', 'target', 'enforcement', 'conditions', 'bypass_actors')}
                        for r in observation['rulesets']], 'classic_protection': 'ABSENT'}


class IntegrationRedTests(unittest.TestCase):
    def test_public_cli_has_exact_readonly_operations(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/release_preflight.py'), '--help'],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, 'missing release-preflight CLI capability')
        self.assertIn('{preflight,readback}', result.stdout)

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.rp = importlib.import_module('release_preflight')
        self.obs, self.contract = fixture()

    def run_preflight(self, human=None):
        return self.rp.preflight(self.obs, self.contract, human)

    def test_identity_positive(self):
        result = self.run_preflight()
        self.assertEqual(result['verdict'], 'PASS')
        self.assertEqual(result['actor_chain']['verdict'], 'PASS')
        self.assertFalse(result['write_authorized'])
        self.assertEqual(result['product_acceptance'], 'not-performed')
        self.assertEqual(result['release_authorization'], 'not-performed')

    def test_incomplete_or_mistyped_observation_never_passes(self):
        for mutate in [lambda o: o.update(protections={}), lambda o: o.pop('permissions'),
                       lambda o: o['repository']['settings'].update(allow_merge_commit='true'),
                       lambda o: o['actor'].update(id=True),
                       lambda o: o['rulesets'].append(copy.deepcopy(o['rulesets'][0]))]:
            self.obs, self.contract = fixture(); mutate(self.obs)
            try: result = self.run_preflight()
            except self.rp.PreflightError: continue
            self.assertNotEqual(result['verdict'], 'PASS')

    def test_review_parameter_types_and_negative_count_rejected(self):
        for key, value in [('required_approving_review_count', -1), ('require_last_push_approval', 'false'),
                           ('required_review_thread_resolution', None)]:
            self.obs, self.contract = fixture()
            self.obs['rulesets'][0]['rules'][-1]['parameters'][key] = value
            self.contract['rulesets'][0]['rules'][-1]['parameters'][key] = value
            try: result = self.run_preflight()
            except self.rp.PreflightError: continue
            self.assertNotEqual(result['verdict'], 'PASS')

    def test_readback_release_does_not_prove_unrelated_push_actor(self):
        before = self.run_preflight()
        release = {'id': 9, 'author': {'login': 'owner', 'id': 102}, 'assets': []}
        delta = {'schema_version': 1, 'gate_id': self.contract['gate_id'], 'pre_digest': before['observation_digest'],
                 'action': 'release', 'actor': {'login': 'owner', 'id': 102}, 'merge_method': None,
                 'changes': [{'collection': 'releases', 'key': '9', 'before': None, 'after': release},
                             {'collection': 'refs', 'key': 'refs/heads/main', 'before': self.obs['refs']['refs/heads/main'],
                              'after': {'sha': C, 'type': 'commit'}}]}
        after = copy.deepcopy(self.obs); after['releases']['9'] = release; after['refs']['refs/heads/main']['sha'] = C
        self.assertNotEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')

    def test_readback_actor_change_invalidates_frozen_chain(self):
        before = self.run_preflight()
        release = {'id': 9, 'tag_name': '1.0', 'author': {'login': 'writer', 'id': 101}, 'assets': []}
        delta = {'schema_version': 1, 'gate_id': self.contract['gate_id'], 'pre_digest': before['observation_digest'],
                 'action': 'release', 'actor': {'login': 'writer', 'id': 101}, 'merge_method': None,
                 'changes': [{'collection': 'releases', 'key': '9', 'before': None, 'after': release}]}
        after = copy.deepcopy(self.obs); after['releases']['9'] = release
        self.assertNotEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')

    def test_identity_missing_ref_and_drift_matrix(self):
        mutations = [lambda o: o['repository'].update(id=101),
                     lambda o: o['repository'].update(full_name='wrong/Project'),
                     lambda o: o['repository'].update(archived=True),
                     lambda o: o['repository'].update(default_branch='main'),
                     lambda o: o['refs'].pop('refs/heads/main'),
                     lambda o: o['refs']['refs/heads/develop'].update(sha=C),
                     lambda o: o['actor'].update(login='owner', id=102)]
        for change in mutations:
            with self.subTest(change=change):
                self.obs, self.contract = fixture(); change(self.obs)
                self.assertEqual(self.run_preflight()['verdict'], 'FAIL')

    def test_policy_unknown_rules_parameters_and_merge_conflict(self):
        for change in [lambda o: o['rulesets'][0]['rules'].append({'type': 'new_blocker'}),
                       lambda o: o['rulesets'][0]['rules'][-1]['parameters'].update(new_requirement=True),
                       lambda o: o['repository']['settings'].update(allow_merge_commit=False),
                       lambda o: o['rulesets'][0]['rules'].append({'type': 'required_linear_history'})]:
            self.obs, self.contract = fixture(); change(self.obs)
            self.assertNotEqual(self.run_preflight()['verdict'], 'PASS')

    def test_same_last_pusher_approver_rejected_without_bypass(self):
        self.contract['chain']['approvers'] = ['writer']
        self.assertEqual(self.run_preflight()['actor_chain']['verdict'], 'BLOCKED')

    def test_unknown_approver_and_insufficient_permissions_blocked(self):
        for change in [lambda o: o['permissions'].pop('owner'),
                       lambda o: o['permissions']['owner'].update(permission='read'),
                       lambda o: o['permissions']['writer'].update(permission='read')]:
            self.obs, self.contract = fixture(); change(self.obs)
            self.assertEqual(self.run_preflight()['actor_chain']['verdict'], 'BLOCKED')

    def test_bypass_empty_is_not_omission(self):
        self.assertEqual(self.run_preflight()['verdict'], 'PASS')
        del self.obs['rulesets'][0]['bypass_actors']
        result = self.run_preflight()
        self.assertEqual(result['verdict'], 'OWNER_ACTION_REQUIRED')
        self.assertNotIn('bypass_actors', result['observation']['rulesets'][0])

    def test_nonempty_bypass_never_ordinary_positive(self):
        self.obs['rulesets'][0]['bypass_actors'] = [{'actor_type': 'RepositoryRole', 'actor_id': 5, 'bypass_mode': 'always'}]
        self.assertEqual(self.run_preflight()['verdict'], 'OWNER_ACTION_REQUIRED')

    def test_404_never_absent_and_human_gate_completion_is_separate(self):
        human = human_policy(self.obs, self.contract)
        del self.obs['rulesets'][0]['bypass_actors']
        self.obs['protections'] = {k: {'state': 'UNKNOWN', 'source': 'api', 'http_status': 404} for k in self.obs['protections']}
        result = self.run_preflight(human)
        self.assertEqual(result['verdict'], 'OWNER_ACTION_REQUIRED')
        self.assertEqual(result['human_reconciliation']['verdict'], 'PASS')
        self.assertEqual(result['actor_chain']['verdict'], 'PASS')
        self.assertEqual(result['observation']['protections']['refs/heads/main']['state'], 'UNKNOWN')

    def test_human_policy_wrong_gate_date_id_target_or_admin_rejected(self):
        for change in [lambda h: h.update(gate_id='FUTURE-RELEASE'),
                       lambda h: h.update(observed_date='2026-09-04'),
                       lambda h: h['rulesets'][0].update(id=11),
                       lambda h: h['rulesets'][0].update(name='other'),
                       lambda h: h['rulesets'][0]['conditions']['ref_name'].update(include=['refs/heads/other']),
                       lambda h: h['observer'].update(login='writer', id=101)]:
            self.obs, self.contract = fixture(); h = human_policy(self.obs, self.contract)
            del self.obs['rulesets'][0]['bypass_actors']; change(h)
            self.assertNotEqual(self.run_preflight(h)['human_reconciliation']['verdict'], 'PASS')

    def test_classic_protection_contradiction_rejected(self):
        self.obs['protections']['refs/heads/main'] = {'state': 'PRESENT', 'source': 'api', 'http_status': 200,
                                                     'rules': {'required_linear_history': {'enabled': True}}}
        self.assertNotEqual(self.run_preflight()['verdict'], 'PASS')
        self.assertNotEqual(self.run_preflight(human_policy(*fixture()))['human_reconciliation']['verdict'], 'PASS')

    def test_deterministic_serialization_and_compact_owner_report(self):
        first = self.run_preflight(); self.obs = dict(reversed(list(self.obs.items())))
        self.assertEqual(self.rp.canonical(first), self.rp.canonical(self.run_preflight()))
        report = self.rp.format_report(first, 'owner')
        self.assertLessEqual(len(report.splitlines()), 8)
        self.assertLess(len(report), 1500)
        self.assertNotIn('bypass_actors', report)
        self.assertNotIn('permissions', report)
        self.assertIn('example/Project', report)

    def test_no_secret_values_in_evidence_or_errors(self):
        for key in ('token', 'access_token', 'password', 'secret', 'credentials',
                    'credential', 'environment', 'env', 'authorization_header',
                    'PRIVATE_KEY', 'EXAMPLE_SECRET_TOKEN'):
            with self.subTest(key=key):
                self.obs, self.contract = fixture()
                self.obs['repository'][key] = 'synthetic-sensitive-value'
                with self.assertRaises(self.rp.PreflightError) as error:
                    self.run_preflight()
                self.assertEqual(str(error.exception), 'UNSAFE_EVIDENCE')
        for secret in (*('gh' + kind + '_' + 'a' * 36 for kind in 'pousr'),
                       'github_pat_' + 'b' * 40, 'Bearer sensitivecredential123'):
            with self.assertRaises(self.rp.PreflightError): self.rp.canonical({'value': secret})

    def test_unrelated_secret_environment_collision_is_deterministic(self):
        # Entire synthetic environments: no dependency on host secrets.
        with mock.patch.dict(os.environ, {}, clear=True):
            before = self.run_preflight()
            encoded = self.rp.canonical(before)
        with mock.patch.dict(os.environ, {'EXAMPLE_SECRET_TOKEN': 'admin'}, clear=True):
            after = self.run_preflight()
            self.assertEqual(after['observation']['permissions']['owner']['permission'], 'admin')
            self.assertEqual(after['verdict'], 'PASS')
            self.assertEqual(after['evidence_digest'], before['evidence_digest'])
            self.assertEqual(self.rp.canonical(after), encoded)
            for form in ('owner', 'engineering', 'machine'):
                self.assertEqual(self.rp.format_report(after, form), self.rp.format_report(before, form))
            self.assertNotIn('EXAMPLE_SECRET_TOKEN', self.rp.canonical(after))

    def test_environment_object_is_not_evidence(self):
        with mock.patch.dict(os.environ, {'EXAMPLE_SECRET_TOKEN': 'synthetic-value'}, clear=True):
            for payload in (os.environ, {'value': os.environ},
                            {'environment': dict(os.environ)}, dict(os.environ)):
                with self.assertRaises(self.rp.PreflightError): self.rp.canonical(payload)

    def test_direct_source_to_base_route_is_feasible_without_writes(self):
        self.obs, self.contract = fixture('refs/heads/develop')
        before = copy.deepcopy((self.obs, self.contract))
        with mock.patch.object(self.rp.subprocess, 'run') as run, mock.patch('builtins.open') as opened, \
                mock.patch.object(Path, 'open') as path_open, mock.patch.object(Path, 'mkdir') as mkdir:
            result = self.run_preflight()
        for operation in (run, opened, path_open, mkdir): operation.assert_not_called()
        self.assertEqual(result['verdict'], 'PASS')
        self.assertEqual(result['actor_chain']['verdict'], 'PASS')
        self.assertEqual((self.obs, self.contract), before)
        self.assertEqual(result['external_writes'], 0)
        self.assertFalse(result['write_authorized'])

    def test_frozen_direct_source_with_pr_rules_needs_no_new_source_push(self):
        rule = copy.deepcopy(self.obs['rulesets'][0]); rule.update(id=11, name='source')
        rule['conditions']['ref_name']['include'] = ['refs/heads/develop']
        self.obs['rulesets'].append(rule)
        self.contract['rulesets'].append({k: v for k, v in rule.items()
                                         if k not in ('bypass_actors', 'current_user_can_bypass')})
        self.assertEqual(self.run_preflight()['actor_chain']['verdict'], 'PASS')

    def test_conditional_missing_release_branch_is_potential_only(self):
        self.obs, self.contract = fixture('refs/heads/release/1.0')
        before = copy.deepcopy((self.obs, self.contract))
        with mock.patch.object(self.rp.subprocess, 'run') as run, mock.patch.object(Path, 'mkdir') as mkdir:
            result = self.run_preflight()
        run.assert_not_called(); mkdir.assert_not_called()
        self.assertEqual(result['verdict'], 'PASS')
        self.assertEqual((self.obs, self.contract), before)
        self.assertNotIn('refs/heads/release/1.0', result['observation']['refs'])
        self.assertTrue(result['actor_chain']['scope'].startswith('potential-route-only'))
        self.assertFalse(result['write_authorized'])
        self.assertEqual(result['external_writes'], 0)
        self.assertEqual(result['release_authorization'], 'not-performed')

    def test_existing_release_branch_exact_frozen_candidate(self):
        self.obs, self.contract = fixture('refs/heads/release/1.0')
        for refs in (self.obs['refs'], self.contract['refs']):
            refs['refs/heads/release/1.0'] = {'sha': B, 'type': 'commit'}
        self.assertEqual(self.run_preflight()['verdict'], 'PASS')

    def test_existing_release_branch_drift_is_blocked(self):
        self.obs, self.contract = fixture('refs/heads/release/1.0')
        for refs in (self.obs['refs'], self.contract['refs']):
            refs['refs/heads/release/1.0'] = {'sha': C, 'type': 'commit'}
        result = self.run_preflight()
        self.assertEqual(result['actor_chain']['verdict'], 'BLOCKED')
        self.assertIn('WORKING_REF_NOT_FROZEN_CANDIDATE', result['actor_chain']['reasons'])

    def test_working_ref_equal_to_base_is_blocked(self):
        self.contract['chain']['working_ref'] = self.contract['chain']['base_ref']
        result = self.run_preflight()
        self.assertEqual(result['actor_chain']['verdict'], 'BLOCKED')
        self.assertNotEqual(result['verdict'], 'PASS')

    def test_source_ref_equal_to_base_is_blocked(self):
        self.obs, self.contract = fixture('refs/heads/release/1.0')
        self.contract['chain']['base_ref'] = self.contract['chain']['source_ref']
        self.obs['protections'].pop('refs/heads/main')
        result = self.run_preflight()
        self.assertEqual(result['actor_chain']['verdict'], 'BLOCKED')
        self.assertIn('SOURCE_BASE_SEPARATION_REQUIRED', result['actor_chain']['reasons'])

    def test_get_boundary_timeout_no_shell_and_sanitized_errors(self):
        calls = []
        def runner(argv, **kwargs):
            calls.append((argv, kwargs))
            return subprocess.CompletedProcess(argv, 0, '{"login":"writer","id":101,"type":"User"}', '')
        api = self.rp.GitHubReader('example/Project', timeout=2, runner=runner)
        api.get('user')
        argv, opts = calls[0]
        self.assertEqual(argv[argv.index('--method') + 1], 'GET')
        self.assertEqual(argv[argv.index('--hostname') + 1], 'github.com')
        self.assertIs(opts['shell'], False)
        self.assertGreater(opts['timeout'], 0)
        for endpoint in ('https://evil.example/user', 'repos/wrong/Project', 'repos/example/Project/issues', 'user;touch sentinel'):
            with self.assertRaises(self.rp.PreflightError): api.get(endpoint)
        with self.assertRaises(self.rp.PreflightError): api.get('user', method='POST')
        self.assertEqual(len(calls), 1)
        for timeout in (0, -1, float('inf'), float('nan')):
            with self.assertRaises(self.rp.PreflightError): self.rp.GitHubReader('example/Project', timeout=timeout)
        def denied(argv, **kwargs): return subprocess.CompletedProcess(argv, 1, '{"status":"403"}', 'token leaked here')
        with self.assertRaises(self.rp.PreflightError) as error:
            self.rp.GitHubReader('example/Project', runner=denied).get('user')
        self.assertNotIn('token', str(error.exception))

    def test_mocked_live_get_normalization_hidden_fields_and_secret_filtering(self):
        observed, contract = fixture(); requests = []
        def runner(argv, **kwargs):
            endpoint = argv[-1].split('?')[0]; requests.append(endpoint)
            self.assertEqual(argv[argv.index('--method') + 1], 'GET')
            prefix = 'repos/example/Project'
            if endpoint == 'user': data = observed['actor']
            elif endpoint == prefix:
                data = {**{k: v for k, v in observed['repository'].items() if k != 'settings'},
                        **observed['repository']['settings'], 'token': 'ghp_' + 'z' * 36}
            elif '/collaborators/' in endpoint:
                login = endpoint.split('/')[-2]; p = observed['permissions'][login]
                data = {'permission': p['permission'], 'user': {k: p[k] for k in ('login', 'id', 'type')}}
            elif '/git/matching-refs/' in endpoint:
                kind = endpoint.split('/')[-1]
                data = [{'ref': ref, 'object': entry} for ref, entry in observed['refs'].items() if ref.startswith('refs/' + kind + '/')]
            elif endpoint.endswith('/rulesets'): data = [{k: r[k] for k in ('id', 'name', 'target', 'enforcement', 'source', 'source_type')} for r in observed['rulesets']]
            elif '/rulesets/' in endpoint: data = {k: v for k, v in observed['rulesets'][0].items() if k != 'bypass_actors'}
            elif endpoint.endswith('/protection'): return subprocess.CompletedProcess(argv, 1, '{"status":"404"}', 'Not Found')
            elif endpoint.endswith('/pulls') or endpoint.endswith('/releases'): data = []
            else: self.fail('unexpected endpoint')
            return subprocess.CompletedProcess(argv, 0, json.dumps(data), '')
        actual = self.rp.observe(contract, runner=runner, timeout=2)
        self.assertNotIn('bypass_actors', actual['rulesets'][0])
        self.assertEqual(actual['protections']['refs/heads/main']['state'], 'UNKNOWN')
        self.assertNotIn('ghp_', self.rp.canonical(actual))
        self.assertEqual(actual['actor'], observed['actor'])
        self.assertEqual(self.rp.preflight(actual, contract)['verdict'], 'OWNER_ACTION_REQUIRED')
        self.assertGreater(len(requests), 8)

    def test_bounded_pagination_refuses_incomplete_observation(self):
        calls = []
        def runner(argv, **kwargs):
            calls.append(argv)
            return subprocess.CompletedProcess(argv, 0, json.dumps([{'id': n} for n in range(100)]), '')
        api = self.rp.GitHubReader('example/Project', timeout=2, runner=runner)
        with self.assertRaises(self.rp.PreflightError): api.pages('/releases')
        self.assertEqual(len(calls), self.rp.MAX_PAGES)

    def test_same_actor_id_under_different_names_and_tag_working_ref_rejected(self):
        self.obs['permissions']['owner']['id'] = 101
        try: result = self.run_preflight()
        except self.rp.PreflightError: result = {'verdict': 'FAIL'}
        self.assertNotEqual(result['verdict'], 'PASS')
        self.obs, self.contract = fixture(); self.contract['chain']['working_ref'] = 'refs/tags/1.0'
        with self.assertRaises(self.rp.PreflightError): self.run_preflight()

    def test_cli_usage_error_does_not_echo_credentials(self):
        for marker in ('arbitrary-sensitive-cli-argument', 'ghp_' + 'q' * 36):
            p = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/release_preflight.py'), marker],
                               capture_output=True, text=True, timeout=10)
            self.assertNotEqual(p.returncode, 0)
            self.assertNotIn(marker, p.stdout + p.stderr)

    def test_no_change_readback_and_unexpected_state_matrix(self):
        before = self.run_preflight()
        delta = {'schema_version': 1, 'gate_id': self.contract['gate_id'], 'pre_digest': before['observation_digest'],
                 'action': 'observe', 'actor': {'login': 'writer', 'id': 101}, 'merge_method': None, 'changes': []}
        after = copy.deepcopy(self.obs); after['observed_at'] = '2026-09-05T12:01:00Z'
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')
        for group, key, value in [('refs', 'refs/heads/surprise', {'sha': C, 'type': 'commit'}),
                                  ('releases', '9', {'id': 9}), ('pulls', '42', {'number': 42})]:
            changed = copy.deepcopy(after); changed[group][key] = value
            self.assertEqual(self.rp.readback(before, delta, changed)['verdict'], 'FAIL')
        after['repository']['settings']['allow_auto_merge'] = True
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'FAIL')

    def test_release_readback_exact_actor_assets_partial_and_noop(self):
        before = self.run_preflight()
        release = {'id': 9, 'tag_name': '1.0', 'author': {'login': 'owner', 'id': 102},
                   'assets': [{'id': 7, 'name': 'product.tar.gz', 'size': 9, 'digest': 'sha256:' + 'a' * 64}]}
        delta = {'schema_version': 1, 'gate_id': self.contract['gate_id'], 'pre_digest': before['observation_digest'],
                 'action': 'release', 'actor': {'login': 'owner', 'id': 102}, 'merge_method': None,
                 'changes': [{'collection': 'releases', 'key': '9', 'before': None, 'after': release}]}
        after = copy.deepcopy(self.obs); after['releases']['9'] = copy.deepcopy(release)
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')
        self.assertEqual(self.rp.readback(before, delta, self.obs)['verdict'], 'FAIL')
        after['releases']['9']['assets'] = []
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'FAIL')
        after['releases']['9'] = release; delta['actor']['login'] = 'writer'
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'FAIL')

    def test_merge_readback_requires_independent_actor_and_parent_proof(self):
        self.obs, self.contract = exact_fixture()
        before = self.run_preflight()
        merged = copy.deepcopy(self.obs['pulls']['7'])
        merged.update(state='closed', merged=True, merged_by={'login': 'owner', 'id': 102},
                      merge_commit_sha=C, merge_parents=[A, B])
        delta = {'schema_version': 1, 'gate_id': self.contract['gate_id'], 'pre_digest': before['observation_digest'],
                 'action': 'merge', 'actor': {'login': 'owner', 'id': 102}, 'merge_method': 'merge', 'changes': [
                     {'collection': 'pulls', 'key': '7', 'before': self.obs['pulls']['7'], 'after': merged},
                     {'collection': 'refs', 'key': 'refs/heads/main', 'before': self.obs['refs']['refs/heads/main'],
                      'after': {'sha': C, 'type': 'commit'}}]}
        after = copy.deepcopy(self.obs); after['pulls']['7'] = merged; after['refs']['refs/heads/main']['sha'] = C
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')
        delta['merge_method'] = 'squash'
        self.assertNotEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')
        delta['merge_method'] = 'merge'; after['pulls']['7']['merge_parents'] = [A]
        self.assertNotEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')

    def test_readback_rejects_digest_tampering_noop_and_unobservable_tag_actor(self):
        before = self.run_preflight()
        delta = {'schema_version': 1, 'gate_id': self.contract['gate_id'], 'pre_digest': '0' * 64,
                 'action': 'tag', 'actor': {'login': 'owner', 'id': 102}, 'merge_method': None, 'changes': []}
        self.assertEqual(self.rp.readback(before, delta, self.obs)['verdict'], 'FAIL')
        delta['pre_digest'] = before['observation_digest']
        self.assertEqual(self.rp.readback(before, delta, self.obs)['verdict'], 'FAIL')
        delta['changes'] = [{'collection': 'refs', 'key': 'refs/tags/1.0', 'before': None,
                             'after': {'sha': A, 'type': 'commit'}}]
        after = copy.deepcopy(self.obs); after['refs']['refs/tags/1.0'] = {'sha': A, 'type': 'commit'}
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'OWNER_ACTION_REQUIRED')


class TransportTests(unittest.TestCase):
    def setUp(self): self.rp = importlib.import_module('release_preflight')

    def test_tar_path_content_modes_and_safe_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'payload'; root.mkdir(mode=0o755)
            file = root / 'run'; file.write_bytes(b'hello'); file.chmod(0o755)
            expected = self.rp.transport_manifest(root, 'filesystem')
            archive = Path(td) / 'asset.tar.gz'
            with tarfile.open(archive, 'w:gz') as tf: tf.add(root, arcname='payload')
            self.assertTrue(self.rp.compare_candidate(expected, archive, 'tar.gz')['equal'])
            file.chmod(0o644)
            self.assertFalse(self.rp.compare_candidate(self.rp.transport_manifest(root, 'filesystem'), archive, 'tar.gz')['equal'])
            for names in (['payload', 'payload/../escape'], ['payload', 'other/file'], ['payload', 'payload/a', 'payload/a']):
                with tarfile.open(archive, 'w:gz') as tf:
                    for name in names:
                        entry = tarfile.TarInfo(name); entry.type = tarfile.DIRTYPE if name == 'payload' else tarfile.REGTYPE
                        tf.addfile(entry, io.BytesIO(b''))
                with self.assertRaises(self.rp.PreflightError): self.rp.transport_manifest(archive, 'tar.gz')

    def test_archive_links_specials_and_filesystem_hardlinks_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / 'asset.tar.gz'
            for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE):
                with tarfile.open(archive, 'w:gz') as tf:
                    root = tarfile.TarInfo('payload'); root.type = tarfile.DIRTYPE; tf.addfile(root)
                    entry = tarfile.TarInfo('payload/link'); entry.type = kind; entry.linkname = '/etc/passwd'; tf.addfile(entry)
                with self.assertRaises(self.rp.PreflightError): self.rp.transport_manifest(archive, 'tar.gz')
            root = Path(td) / 'tree'; root.mkdir(); (root / 'one').write_bytes(b'x'); os.link(root / 'one', root / 'two')
            with self.assertRaises(self.rp.PreflightError): self.rp.transport_manifest(root, 'filesystem')

    def test_zip_modes_conditional_and_downloaded_asset_checksum(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / 'payload'; root.mkdir(); (root / 'run').write_bytes(b'hello'); (root / 'run').chmod(0o755)
            expected = self.rp.transport_manifest(root, 'filesystem')
            archive = Path(td) / 'asset.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('payload/', b''); z.writestr('payload/run', b'hello')
            self.assertTrue(self.rp.compare_candidate(expected, archive, 'zip')['equal'])
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            self.assertTrue(self.rp.verify_release_asset(archive, 'asset.zip', digest, expected, 'zip')['equal'])
            with self.assertRaises(self.rp.PreflightError): self.rp.verify_release_asset(archive, 'asset.zip', '0' * 64, expected, 'zip')
            with self.assertRaises(self.rp.PreflightError): self.rp.verify_release_asset(archive, 'wrong.zip', digest, expected, 'zip')

    def test_git_tree_and_checkout_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / 'run').write_bytes(b'hello'); (root / 'run').chmod(0o775)
            tree = self.rp.git_tree_manifest([{'path': 'run', 'mode': '100755', 'content': b'hello'}])
            self.assertTrue(self.rp.compare_candidate(tree, root, 'git-checkout')['equal'])
            (root / 'run').chmod(0o644)
            self.assertFalse(self.rp.compare_candidate(tree, root, 'git-checkout')['equal'])
            with self.assertRaises(self.rp.PreflightError): self.rp.git_tree_manifest([{'path': 'link', 'mode': '120000', 'content': b'target'}])

    def test_git_checkout_excludes_root_service_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / 'file').write_bytes(b'x'); (root / 'file').chmod(0o644)
            (root / '.git').mkdir(); (root / '.git/config').write_text('fixture-only')
            tree = self.rp.git_tree_manifest([{'path': 'file', 'mode': '100644', 'content': b'x'}])
            self.assertTrue(self.rp.compare_candidate(tree, root, 'git-checkout')['equal'])

    def test_zip_type_contradiction_and_git_path_collision(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / 'bad.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                info = zipfile.ZipInfo('payload/'); info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16; z.writestr(info, b'')
            with self.assertRaises(self.rp.PreflightError): self.rp.transport_manifest(archive, 'zip')
        with self.assertRaises(self.rp.PreflightError): self.rp.git_tree_manifest([
            {'path': 'a', 'mode': '100644', 'content': b'x'}, {'path': 'a/b', 'mode': '100644', 'content': b'y'}])




def exact_fixture(strict=False, working_ref='refs/heads/develop'):
    obs, contract = fixture(working_ref)
    contract['pr_numbers'] = [7]
    if working_ref != contract['chain']['source_ref']:
        for refs in (obs['refs'], contract['refs']): refs[working_ref] = {'sha': B, 'type': 'commit'}
    if not strict:
        for rules in (obs['rulesets'], contract['rulesets']):
            rules[0]['rules'][-1]['parameters'].update(
                require_last_push_approval=False, required_review_thread_resolution=False,
                require_extra_approval_for_unattributed_changes=False)
    repo = {'full_name': 'example/Project', 'id': 100}
    obs['pulls']['7'] = {
        'number': 7, 'state': 'open', 'draft': False, 'merged': False,
        'merge_commit_sha': C, 'merged_by': None, 'mergeable': True,
        'author': {'login': 'writer', 'id': 101},
        'head_ref': working_ref.removeprefix('refs/heads/'), 'head_sha': B,
        'base_ref': 'main', 'base_sha': A, 'head_repository': repo.copy(),
        'base_repository': repo.copy(), 'reviews': [
            {'id': 8, 'user': {'login': 'owner', 'id': 102, 'type': 'User'},
             'state': 'APPROVED', 'commit_id': B, 'submitted_at': '2026-09-05T11:59:00Z'}]}
    return obs, contract


class ExactPRTests(unittest.TestCase):
    def setUp(self):
        self.rp = importlib.import_module('release_preflight')
        self.obs, self.contract = exact_fixture()

    def result(self):
        return self.rp.preflight(self.obs, self.contract)

    def change_policy(self, **values):
        for rules in (self.obs['rulesets'], self.contract['rulesets']):
            rules[0]['rules'][-1]['parameters'].update(values)

    def test_original_selected_pr_bypass(self):
        self.obs, self.contract = exact_fixture(strict=True)
        self.obs['pulls']['7'].update(author={'login': 'owner', 'id': 102},
                                      head_ref='wrong-head', head_sha=C)
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_selected_author_mismatch(self):
        self.obs['pulls']['7']['author'] = {'login': 'owner', 'id': 102}
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_selected_head_sha_mismatch(self):
        self.obs['pulls']['7']['head_sha'] = C
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_selected_head_branch_mismatch(self):
        self.obs['pulls']['7']['head_ref'] = 'other'
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_selected_base_binding_mismatch(self):
        for values in ({'base_ref': 'develop'}, {'base_sha': C}):
            self.obs, self.contract = exact_fixture(); self.obs['pulls']['7'].update(values)
            self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_selected_draft_fails(self):
        self.obs['pulls']['7']['draft'] = True
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_selected_closed_or_merged_fails(self):
        for values in ({'state': 'closed'}, {'merged': True}, {'merged_by': {'login': 'owner', 'id': 102}}):
            self.obs, self.contract = exact_fixture(); self.obs['pulls']['7'].update(values)
            self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_selected_ambiguity_and_missing_fail(self):
        for numbers in ([7, 8], [7, 7], [8]):
            self.obs, self.contract = exact_fixture(); self.contract['pr_numbers'] = numbers
            self.assertEqual(self.result()['verdict'], 'FAIL')
        self.obs, self.contract = exact_fixture(); self.obs['pulls']['7']['number'] = 8
        self.assertEqual(self.result()['verdict'], 'FAIL')
        self.obs, self.contract = exact_fixture(); self.obs['pulls']['8'] = copy.deepcopy(self.obs['pulls']['7'])
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_exact_metadata_and_current_approval_pass(self):
        result = self.result()
        self.assertEqual(result['scope'], 'exact-pr-gate')
        self.assertEqual(result['exact_pr_gate']['pr_binding'], 'PASS')
        self.assertEqual(result['exact_pr_gate']['valid_approvers'], ['owner'])
        self.assertEqual(result['exact_pr_gate']['verdict'], 'PASS')
        self.assertEqual(result['verdict'], 'PASS')
        self.assertFalse(result['write_authorized'])

    def test_potential_route_has_no_exact_readiness(self):
        self.obs, self.contract = fixture()
        result = self.result()
        self.assertEqual(result['verdict'], 'PASS')
        self.assertEqual(result['scope'], 'potential-route-only')
        self.assertEqual(result['exact_pr_gate']['verdict'], 'NOT_YET_OBSERVED')
        self.assertFalse(result['write_authorized'])
        self.assertIn('potential-route-only', self.rp.format_report(result))

    def test_unselected_observed_pr_is_not_ignored(self):
        self.contract['pr_numbers'] = []
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_conditional_route_requires_exact_existing_working_ref(self):
        self.obs, self.contract = exact_fixture(working_ref='refs/heads/release/1.0')
        self.assertEqual(self.result()['verdict'], 'PASS')
        self.obs['pulls']['7']['head_ref'] = 'develop'
        self.assertEqual(self.result()['verdict'], 'FAIL')
        self.obs, self.contract = exact_fixture(working_ref='refs/heads/release/1.0')
        for refs in (self.obs['refs'], self.contract['refs']): refs.pop('refs/heads/release/1.0')
        self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_fork_or_author_identity_collision_fails(self):
        for change in (lambda p: p['head_repository'].update(id=200),
                       lambda p: p['base_repository'].update(full_name='wrong/Project'),
                       lambda p: p['author'].update(id=102)):
            self.obs, self.contract = exact_fixture(); change(self.obs['pulls']['7'])
            self.assertEqual(self.result()['verdict'], 'FAIL')

    def test_no_approval_is_not_pass(self):
        self.obs['pulls']['7']['reviews'] = []
        self.assertNotEqual(self.result()['verdict'], 'PASS')

    def test_old_head_approval_is_not_pass(self):
        self.obs['pulls']['7']['reviews'][0]['commit_id'] = A
        self.assertNotEqual(self.result()['verdict'], 'PASS')

    def test_contract_last_pusher_is_not_live_proof(self):
        self.change_policy(require_last_push_approval=True)
        result = self.result()
        self.assertEqual(result['verdict'], 'OWNER_ACTION_REQUIRED')
        self.assertIn('LATEST_REVIEWABLE_PUSH_UNPROVED', result['findings'])
        self.assertEqual(result['exact_pr_gate']['latest_reviewable_pusher'], 'UNKNOWN')
        self.contract['chain']['last_pusher'] = 'owner'
        self.assertNotEqual(self.result()['verdict'], 'PASS')

    def test_rejected_commented_dismissed_pending_do_not_count(self):
        for state in ('CHANGES_REQUESTED', 'COMMENTED', 'DISMISSED', 'PENDING'):
            self.obs, self.contract = exact_fixture(); self.obs['pulls']['7']['reviews'][0]['state'] = state
            self.assertNotEqual(self.result()['verdict'], 'PASS')

    def test_head_change_invalidates_old_gate_approval(self):
        self.assertEqual(self.result()['verdict'], 'PASS')
        self.obs['pulls']['7']['head_sha'] = C
        for refs in (self.obs['refs'], self.contract['refs']): refs['refs/heads/develop']['sha'] = C
        self.contract['candidate']['sha'] = C
        self.assertNotEqual(self.result()['verdict'], 'PASS')

    def test_required_count_and_duplicate_actor(self):
        self.change_policy(required_approving_review_count=2)
        # Structural potential has two possible actors; only one actually approved.
        self.contract['chain']['approvers'].append('reviewer')
        self.obs['permissions']['reviewer'] = {'login': 'reviewer', 'id': 103, 'type': 'User', 'permission': 'write'}
        review = copy.deepcopy(self.obs['pulls']['7']['reviews'][0]); review.update(id=9, submitted_at='2026-09-05T11:59:01Z')
        self.obs['pulls']['7']['reviews'].append(review)
        self.assertNotEqual(self.result()['verdict'], 'PASS')
        review['user'] = {'login': 'reviewer', 'id': 103, 'type': 'User'}
        self.assertEqual(self.result()['verdict'], 'PASS')

    def test_unknown_or_incomplete_review_state_requires_owner(self):
        for change in (lambda r: r.update(state='FUTURE_STATE'), lambda r: r.pop('commit_id'),
                       lambda r: r.update(submitted_at=None), lambda r: r['user'].update(id=500),
                       lambda r: r.update(submitted_at='2026-09-06T12:00:00Z')):
            self.obs, self.contract = exact_fixture(); change(self.obs['pulls']['7']['reviews'][0])
            self.assertEqual(self.result()['verdict'], 'OWNER_ACTION_REQUIRED')

    def test_latest_decisive_review_and_duplicate_id(self):
        reviews = self.obs['pulls']['7']['reviews']
        later = copy.deepcopy(reviews[0]); later.update(id=9, state='CHANGES_REQUESTED', submitted_at='2026-09-05T11:59:01Z')
        reviews.append(later)
        self.assertNotEqual(self.result()['verdict'], 'PASS')
        later['state'] = 'DISMISSED'
        self.assertNotEqual(self.result()['verdict'], 'PASS')
        later['state'] = 'COMMENTED'
        self.assertEqual(self.result()['verdict'], 'PASS')
        later.update(id=8, state='APPROVED')
        self.assertEqual(self.result()['verdict'], 'OWNER_ACTION_REQUIRED')

    def test_actual_review_identity_permission_and_self_review(self):
        for user in ({'login': 'writer', 'id': 101, 'type': 'User'},
                     {'login': 'owner', 'id': 101, 'type': 'User'},
                     {'login': 'owner', 'id': 102, 'type': 'Bot'},
                     {'login': 'unknown', 'id': 103, 'type': 'User'}):
            self.obs, self.contract = exact_fixture(); self.obs['pulls']['7']['reviews'][0]['user'] = user
            self.assertNotEqual(self.result()['verdict'], 'PASS')

    def test_conversation_designated_and_status_requirements_fail_closed(self):
        for policy in ({'required_review_thread_resolution': True}, {'require_code_owner_review': True},
                       {'required_reviewers': [{'reviewer': 'owner'}]}):
            self.obs, self.contract = exact_fixture(); self.change_policy(**policy)
            self.assertEqual(self.result()['verdict'], 'OWNER_ACTION_REQUIRED')
        self.obs, self.contract = exact_fixture()
        for rules in (self.obs['rulesets'], self.contract['rulesets']): rules[0]['rules'].append({'type': 'required_status_checks'})
        self.assertNotEqual(self.result()['verdict'], 'PASS')

    def test_mergeable_is_only_conflict_proof(self):
        self.obs['pulls']['7']['mergeable'] = None
        self.assertEqual(self.result()['verdict'], 'OWNER_ACTION_REQUIRED')
        self.obs['pulls']['7']['mergeable'] = False
        self.assertEqual(self.result()['verdict'], 'FAIL')
        self.obs, self.contract = exact_fixture(strict=True)
        self.assertEqual(self.result()['exact_pr_gate']['pr_binding'], 'PASS')
        self.assertEqual(self.result()['verdict'], 'OWNER_ACTION_REQUIRED')
        human = human_policy(self.obs, self.contract)
        self.assertEqual(self.rp.preflight(self.obs, self.contract, human)['verdict'], 'OWNER_ACTION_REQUIRED')

    def merge_readback_fixture(self):
        self.obs['open_pr_numbers'] = [7, 99]
        before = self.result(); after = copy.deepcopy(self.obs)
        after['open_pr_numbers'] = [99]
        after['pulls']['7'].update(state='closed', merged=True, merged_by={'login': 'owner', 'id': 102},
                                  merge_commit_sha=C, merge_parents=[A, B])
        after['refs']['refs/heads/main']['sha'] = C
        delta = {'schema_version': 1, 'gate_id': self.contract['gate_id'], 'pre_digest': before['observation_digest'],
                 'action': 'merge', 'actor': {'login': 'owner', 'id': 102}, 'merge_method': 'merge',
                 'changes': [{'collection': group, 'key': key, 'before': copy.deepcopy(self.obs[group][key]),
                              'after': copy.deepcopy(after[group][key])} for group, key in (('pulls', '7'), ('refs', 'refs/heads/main'))]}
        return before, delta, after

    def test_merge_readback_tracks_only_selected_open_inventory_change(self):
        before, delta, after = self.merge_readback_fixture()
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'PASS')
        after['open_pr_numbers'] = []
        self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'FAIL')

    def test_merge_readback_rejects_unselected_and_unbound_prestate(self):
        for mutate in (lambda c, o: c.update(pr_numbers=[]),
                       lambda c, o: c.update(pr_numbers=[8]),
                       lambda c, o: o['pulls']['7'].update(head_ref='other')):
            self.obs, self.contract = exact_fixture(); mutate(self.contract, self.obs)
            before, delta, after = self.merge_readback_fixture()
            # Omit optional open inventory to expose identity-only bypass on old reader.
            for obs in (before['observation'], after): obs.pop('open_pr_numbers')
            before['observation_digest'] = self.rp.digest(before['observation'])
            before['evidence_digest'] = self.rp.digest({k: v for k, v in before.items() if k != 'evidence_digest'})
            delta['pre_digest'] = before['observation_digest']
            self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'FAIL')

    def test_merge_readback_independent_actor_head_parent_and_target(self):
        for mutation in (lambda o: o['pulls']['7'].update(merged_by={'login': 'writer', 'id': 101}),
                         lambda o: o['pulls']['7'].update(head_sha=A),
                         lambda o: o['pulls']['7'].update(merge_parents=[B, A]),
                         lambda o: o['refs']['refs/heads/main'].update(sha=B)):
            self.obs, self.contract = exact_fixture(); before, delta, after = self.merge_readback_fixture()
            mutation(after)
            for change in delta['changes']: change['after'] = copy.deepcopy(after[change['collection']][change['key']])
            self.assertEqual(self.rp.readback(before, delta, after)['verdict'], 'FAIL')

    def observe_runner(self, *, head_drift=False, unrelated=False):
        obs = self.obs; prefix = 'repos/example/Project'; calls = []; pr_reads = 0
        def runner(argv, **kwargs):
            nonlocal pr_reads
            calls.append(argv[-1]); endpoint = argv[-1].split('?')[0]
            self.assertEqual(argv[argv.index('--method') + 1], 'GET'); self.assertIs(kwargs['shell'], False)
            if endpoint == 'user': data = obs['actor']
            elif endpoint == prefix:
                data = {**{k: v for k, v in obs['repository'].items() if k != 'settings'}, **obs['repository']['settings']}
            elif '/collaborators/' in endpoint:
                p = obs['permissions'][endpoint.split('/')[-2]]
                data = {'permission': p['permission'], 'user': {k: p[k] for k in ('login', 'id', 'type')}}
            elif '/git/matching-refs/' in endpoint:
                kind = endpoint.split('/')[-1]
                data = [{'ref': r, 'object': v} for r, v in obs['refs'].items() if r.startswith('refs/' + kind + '/')]
            elif endpoint.endswith('/rulesets'): data = obs['rulesets']
            elif '/rulesets/' in endpoint: data = obs['rulesets'][0]
            elif endpoint.endswith('/protection'): return subprocess.CompletedProcess(argv, 1, '{"status":"404"}', '')
            elif endpoint.endswith('/pulls'): data = [{'number': n} for n in ([7, 99] if unrelated else [7])]
            elif endpoint.endswith('/pulls/7/reviews'):
                data = [{**r, 'body': 'unrelated-private-review-body'} for r in obs['pulls']['7']['reviews']]
            elif endpoint.endswith('/pulls/7'):
                pr_reads += 1; p = obs['pulls']['7']
                data = {k: p[k] for k in ('number', 'state', 'draft', 'merged', 'merge_commit_sha', 'merged_by', 'mergeable')}
                data.update(user=p['author'], head={'ref': p['head_ref'], 'sha': C if head_drift and pr_reads > 1 else p['head_sha'], 'repo': p['head_repository']},
                            base={'ref': p['base_ref'], 'sha': p['base_sha'], 'repo': p['base_repository']})
            elif endpoint.endswith('/releases'): data = []
            else: self.fail('unrelated endpoint: ' + endpoint)
            return subprocess.CompletedProcess(argv, 0, json.dumps(data), '')
        return runner, calls

    def test_live_reader_observes_selected_reviews_only_and_rereads_pr(self):
        runner, calls = self.observe_runner(unrelated=True)
        obs = self.rp.observe(self.contract, runner=runner)
        self.assertEqual(set(obs['pulls']), {'7'})
        self.assertEqual(obs['open_pr_numbers'], [7, 99])
        self.assertEqual(obs['pulls']['7']['reviews'], self.obs['pulls']['7']['reviews'])
        self.assertEqual(calls.count('repos/example/Project/pulls/7'), 2)
        self.assertTrue(any('/pulls/7/reviews?' in x for x in calls))
        self.assertFalse(any('/pulls/99' in x for x in calls))
        self.assertNotIn('unrelated-private-review-body', self.rp.canonical(obs))

    def test_reader_detects_head_push_during_review_read(self):
        runner, _ = self.observe_runner(head_drift=True)
        with self.assertRaises(self.rp.PreflightError): self.rp.observe(self.contract, runner=runner)

    def test_reviews_get_allowlist_remains_closed(self):
        runner = mock.Mock(return_value=subprocess.CompletedProcess([], 0, '[]', ''))
        api = self.rp.GitHubReader('example/Project', runner=runner)
        api.pages('/pulls/7/reviews')
        for suffix in ('/pulls/7/timeline', '/pulls/7/comments', '/issues/7/events', '/pulls/7/reviews/9', '/pulls/7/reviews/../x'):
            with self.assertRaises(self.rp.PreflightError): api.get(api.prefix + suffix)
        for method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            with self.assertRaises(self.rp.PreflightError): api.get(api.prefix + '/pulls/7/reviews', method=method)
        self.assertEqual(runner.call_count, 1)


if __name__ == '__main__': unittest.main()

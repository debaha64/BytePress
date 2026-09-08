"""BytePress-specific qualification without a public qualification executable.

REQ-CHECK/VERSION/BOUNDARY/SDD; INV-004/010/011/013; SCN-010/013/014.
"""

import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock
import zipfile
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "tools"))
import new_project


EXPECTED_TOOL_FILES = {
    "README.md", "bp_clean.py", "check_product.py", "check_workspace.py",
    "new_project.py", "project_profile.py", "release_preflight.py",
}
EXPECTED_TEST_FILES = {
    "README.md", "test_check_product.py", "test_check_workspace.py",
    "test_harness.py", "test_new_project.py", "test_project_profile.py", "test_release_preflight.py", "test_workspace_update.py",
}
EXPECTED_DISTRIBUTION_FILES = 142
EXPECTED_DISTRIBUTION_DIRECTORIES = 13
EXPECTED_DEPLOY_FILES = 111
EXPECTED_DEPLOY_MANIFEST_SHA256 = "8ba826c6eee9063f8c42db14abd7b1ea1174e56728ea212f378b9b7dd22fb60e"
DISPOSABLE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
DISPOSABLE_SUFFIXES = (".pyc", ".pyo", ".tmp", ".temp", ".orig")


def regular_files(root):
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    )


def local_targets(text):
    for match in re.finditer(r"!?\[[^]]*\]\(([^)]+)\)", text):
        value = match.group(1).strip().strip("<>")
        if " " in value:
            value = value.split(" ", 1)[0]
        if value and not value.startswith(("#", "http://", "https://", "mailto:", "codexlog:")):
            yield value.split("#", 1)[0]



def documentation_issues(root):
    """Objective Product docs scope: README and all docs/*.md topics.

    Templates, SOP, roles, generated instance entries and internal artifacts are
    outside the user entry graph. All shipped docs are user-facing, including
    readable machine contracts; no file-count-based orphan heuristic is used.
    """
    from urllib.parse import unquote
    import check_workspace
    root = root.resolve()
    issues = []
    pages = {root / 'README.md', *(root / 'docs').rglob('*.md')}
    graph = {p: set() for p in pages}
    glossary = root / 'docs/terminology/glossary.md'
    contract = glossary.read_text() if glossary.exists() else ''
    aliases = []
    section = contract.partition('## Deprecated aliases')[2].split('\n## ', 1)[0]
    for line in section.splitlines():
        match = re.fullmatch(r'\| `([^`]+)` \| `([^`]+)` \| `(sot-mode-title)` \|', line)
        if match:
            aliases.append(match.groups())
    if not aliases:
        issues.append('missing approved deprecated terminology contract')
    for source in sorted(root.rglob('*.md')):
        text = source.read_text(encoding='utf-8')
        # Fenced examples and quotations cannot become live prose consumers.
        prose = re.sub(r'(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*$', '', text)
        prose = re.sub(r'(?m)^>.*$', '', prose)
        for target in check_workspace._markdown_targets(prose):
            if not target or target.startswith(('http://', 'https://', 'mailto:', 'codexlog:')):
                continue
            name, _, anchor = unquote(target).partition('#')
            candidate = (source.parent / name).resolve() if name else source
            try:
                candidate.relative_to(root)
                if not candidate.exists():
                    raise ValueError('missing')
            except ValueError:
                issues.append(f'link: {source.relative_to(root)} -> {target}')
                continue
            if anchor and candidate.is_file() and anchor not in check_workspace._anchors(candidate):
                issues.append(f'anchor: {source.relative_to(root)} -> {target}')
            if source in graph and candidate in pages:
                graph[source].add(candidate)
        if source in pages and re.search(r'sot_mode|sot_files|sot_git|sot_github', prose):
            title = re.search(r'(?m)^# (.+)$', prose)
            if title:
                for alias, canonical, scope in aliases:
                    if title.group(1) == alias:
                        issues.append(f'deprecated: {source.relative_to(root)} -> {canonical}')
    seen = set(); pending = [root / 'README.md']
    while pending:
        page = pending.pop()
        if page in seen:
            continue
        seen.add(page); pending.extend(graph.get(page, ()))
    for page in sorted(pages - seen):
        issues.append(f'orphan: {page.relative_to(root)}')
    for page in sorted(pages):
        if page.name != 'README.md' and page not in graph.get(page.parent / 'README.md', set()):
            issues.append(f'index: {page.relative_to(root)}')
    return issues


class BytePressQualificationTests(unittest.TestCase):
    def test_documentation_deployment_consumer_closure(self):
        import check_workspace
        with tempfile.TemporaryDirectory() as td:
            inputs = dict(source_distribution=SOURCE_ROOT, destination_parent=Path(td), slug='DocProbe',
                          display_name='Проверка документации', product_mode='new', wroad='Проверить документацию.',
                          existing_product=None, exclude_vcs_paths=())
            preview = new_project.build_preview(**inputs)
            new_project.apply_project(**inputs, authorization_sha256=preview['preview_sha256'])
            deployed = Path(td) / 'WS_DocProbe'
            self.assertIsNone(check_workspace._check_links(deployed, 'DocProbe'))
            for old in ('docs/architecture/input-output-contract.md', 'docs/user/operating-mode.md',
                        'docs/technical/language-support.md', 'templates/session-record.md',
                        'templates/docs-product-jtbd.md', 'templates/docs-product-dods.md',
                        'templates/docs-technical-architecture.md'):
                self.assertFalse((deployed / old).exists(), old)
            mode = (deployed / 'docs/user/source-of-truth-mode.md').read_text()
            self.assertTrue(mode.startswith('# Режим источника истины\n'))
            self.assertFalse(list((deployed / 'plans/active').glob('WPLAN-*.md')))
            for relative in new_project.DEPLOY_COPY_FILES:
                self.assertEqual((deployed / relative).read_bytes(), (SOURCE_ROOT / relative).read_bytes())

    def test_documentation_entry_graph_anchors_and_approved_terms(self):
        self.assertEqual(documentation_issues(SOURCE_ROOT), [])

    def test_documentation_negative_fixtures_are_objective_and_scope_bounded(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'docs/terminology').mkdir(parents=True)
            (root / 'templates').mkdir()
            (root / 'README.md').write_text('# Entry\n[Docs](docs/README.md)\n')
            (root / 'docs/README.md').write_text('# Docs\n[Terms](terminology/README.md)\n[Topic](topic.md#result)\n')
            (root / 'docs/terminology/README.md').write_text('# Terms\n[Glossary](glossary.md)\n')
            (root / 'docs/terminology/glossary.md').write_text('# Glossary\n\n## Deprecated aliases\n\n'
                '| `Операционный режим` | `Режим источника истины` | `sot-mode-title` |\n')
            topic = root / 'docs/topic.md'
            valid = '# Режим источника истины\n\n`sot_mode`\n\n## Result\n\n'
            topic.write_text(valid + '```text\nОперационный режим\n```\n> Операционный режим\n')
            (root / 'templates/internal.md').write_text('# Internal form\n')
            self.assertEqual(documentation_issues(root), [])
            topic.write_text(valid.replace('## Result', '## Changed'))
            self.assertTrue(any(x.startswith('anchor:') for x in documentation_issues(root)))
            topic.write_text(valid.replace('# Режим источника истины', '# Операционный режим'))
            self.assertTrue(any(x.startswith('deprecated:') for x in documentation_issues(root)))
            topic.write_text(valid)
            (root / 'docs/orphan.md').write_text('# Unlinked topic\n')
            self.assertTrue(any(x.startswith('orphan:') for x in documentation_issues(root)))

    def test_owner_decision_schema_consumers_and_family_separation(self):
        consumers = {
            relative: (SOURCE_ROOT / relative).read_text(encoding="utf-8")
            for relative in (
                "templates/decision-record.md", "sops/record-decision.md",
                "sops/project-management.md", "docs/terminology/glossary.md",
            )
        }
        for relative, document in consumers.items():
            with self.subTest(consumer=relative):
                self.assertIn("decommissioning_authorization", document)
                self.assertIn("retirement_authorization", document)
                self.assertIn("PA-*", document)
                self.assertIn("Release Authorization", document)
        template = consumers["templates/decision-record.md"]
        self.assertIn("DECISION_KIND: implementation | decommissioning_authorization | retirement_authorization", template)
        plan_template = (SOURCE_ROOT / "templates/workspace-plan-active.md").read_text(encoding="utf-8")
        self.assertNotRegex(plan_template, r"(?m)^REQUIRED_OWNER_DECISION_KIND:")
        self.assertIn("только из `docs/technical/phase-gates.md`", plan_template)


    def test_product_acceptance_role_and_sop_ownership(self):
        review = (SOURCE_ROOT / "roles/13-review-coordinator.md").read_text(encoding="utf-8")
        acceptance = (SOURCE_ROOT / "roles/14-product-acceptance-coordinator.md").read_text(encoding="utf-8")
        procedure = (SOURCE_ROOT / "sops/project-management.md").read_text(encoding="utf-8")
        self.assertIn("создавать Product Acceptance вместо владельца", review)
        self.assertIn("После передачи `owner-open` получить полномочия фазы", acceptance)
        self.assertIn("Заранее принятый `PA-*`", acceptance)
        self.assertIn("owner-review -> product-acceptance", procedure)
        self.assertIn("product-acceptance -> release-readiness", procedure)


    def test_real_deployment_includes_preflight_without_autorun(self):
        self.assertIn('tools/release_preflight.py', new_project.DEPLOY_COPY_FILES)
        with tempfile.TemporaryDirectory() as td:
            inputs = dict(source_distribution=SOURCE_ROOT, destination_parent=Path(td), slug='Probe', display_name='Проверка',
                          product_mode='new', wroad='Проверить поставляемую возможность.', existing_product=None, exclude_vcs_paths=())
            plan = new_project.build_preview(**inputs)
            with mock.patch('subprocess.run', side_effect=AssertionError('Project Start executed commands')):
                new_project.apply_project(**inputs, authorization_sha256=plan['preview_sha256'])
            deployed = Path(td) / 'WS_Probe'
            self.assertTrue((deployed / 'tools/release_preflight.py').is_file())
            commands = [[sys.executable, '-B', str(deployed / 'tools' / checker), '--workspace', str(deployed)]
                        for checker in ('check_workspace.py', 'check_product.py')]
            commands.append([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_release_preflight.py'])
            for command in commands:
                p = subprocess.run(command, cwd=deployed, capture_output=True, text=True, timeout=15,
                                   env={**os.environ, 'PATH': '', 'PYTHONPATH': '', 'PYTHONDONTWRITEBYTECODE': '1'})
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    maxDiff = None

    def copy_unit(self):
        temporary = tempfile.TemporaryDirectory(prefix="bytepress-qualification-")
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name) / "BytePress"
        shutil.copytree(SOURCE_ROOT, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        return target

    def assert_distribution_identity(self, root):
        files = regular_files(root)
        directories = [path for path in root.rglob("*") if path.is_dir() and not path.is_symlink()]
        self.assertEqual(len(files), EXPECTED_DISTRIBUTION_FILES)
        self.assertEqual(len(directories) + 1, EXPECTED_DISTRIBUTION_DIRECTORIES)
        self.assertEqual((root / "VERSION").read_bytes(), b"0.5.2\n")
        self.assertEqual({path.name for path in (root / "tools").iterdir() if path.is_file()}, EXPECTED_TOOL_FILES)
        self.assertEqual({path.name for path in (root / "tests").iterdir() if path.is_file()}, EXPECTED_TEST_FILES)
        for forbidden in ("plans", "logs", "research", "src"):
            self.assertFalse((root / forbidden).exists(), forbidden)
        self.assertFalse(any(root.glob("*.profile")))
        self.assertFalse((root / "tools/bp_check.py").exists())

    def test_exact_distribution_composition_count_version_and_clean_break(self):
        self.assert_distribution_identity(SOURCE_ROOT)

    def test_bytepress_fingerprint_violation_fails_qualification(self):
        root = self.copy_unit()
        (root / "VERSION").write_text("9.9.9\n", encoding="utf-8")
        with self.assertRaises(AssertionError):
            self.assert_distribution_identity(root)
        generic = (root / "tools/check_product.py").read_text(encoding="utf-8")
        self.assertNotIn("0.5.2", generic)
        self.assertNotIn(str(EXPECTED_DISTRIBUTION_FILES), generic)

    def test_project_start_manifest_has_new_checkers_and_no_legacy_checker(self):
        paths = tuple(sorted(new_project.DEPLOY_COPY_FILES))
        self.assertEqual(len(paths), EXPECTED_DEPLOY_FILES)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn("tools/check_workspace.py", paths)
        self.assertIn("tools/check_product.py", paths)
        self.assertIn("tests/test_check_workspace.py", paths)
        self.assertNotIn("tools/bp_check.py", paths)
        digest = hashlib.sha256(("\n".join(paths) + "\n").encode()).hexdigest()
        self.assertEqual(digest, EXPECTED_DEPLOY_MANIFEST_SHA256)

    def test_required_docs_sops_roles_templates_and_tools_exist(self):
        required = {
            "AGENTS.md", "SYSTEM.md", "README.md", "LICENSE", "VERSION",
            "docs/architecture/project-profile.md", "docs/technical/testing.md",
            "docs/technical/security.md", "sops/change-management.md", "sops/sot.md",
            "sops/verify-work.md", "roles/12-verification-engineer.md",
            "templates/codex-task.md", "templates/codex-report.md",
            "templates/docs-product-prd.md", "tools/check_workspace.py",
            "tools/check_product.py", "tools/project_profile.py", "tools/new_project.py",
        }
        self.assertEqual([path for path in sorted(required) if not (SOURCE_ROOT / path).is_file()], [])

    def test_distribution_has_no_links_special_nodes_or_runtime_residue(self):
        residue = []
        for current, directories, files in os.walk(SOURCE_ROOT, topdown=True, followlinks=False):
            base = Path(current)
            for name in directories:
                path = base / name
                self.assertFalse(path.is_symlink(), path)
                if name in DISPOSABLE_DIRS:
                    residue.append(path.relative_to(SOURCE_ROOT).as_posix())
            for name in files:
                path = base / name
                info = path.lstat()
                self.assertTrue(stat.S_ISREG(info.st_mode), path)
                if name.endswith(DISPOSABLE_SUFFIXES) or name.endswith(":Zone.Identifier"):
                    residue.append(path.relative_to(SOURCE_ROOT).as_posix())
        self.assertEqual(residue, [])

    def test_all_local_markdown_links_are_contained_and_exist(self):
        root = SOURCE_ROOT.resolve()
        failures = []
        for source in root.rglob("*.md"):
            for target in local_targets(source.read_text(encoding="utf-8")):
                candidate = source.parent / target
                try:
                    candidate.resolve(strict=True).relative_to(root)
                except (OSError, ValueError):
                    failures.append(f"{source.relative_to(root)} -> {target}")
        self.assertEqual(failures, [])

    def test_product_distribution_contains_no_current_workspace_route(self):
        current = re.compile(r"\b(?:WPLAN-000148|WBACK-000061|WBACK-000062)\b")
        findings = []
        for path in SOURCE_ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py"} and "tests" not in path.relative_to(SOURCE_ROOT).parts:
                if current.search(path.read_text(encoding="utf-8")):
                    findings.append(path.relative_to(SOURCE_ROOT).as_posix())
        self.assertEqual(findings, [])

    def test_generic_checker_sources_have_no_bytepress_identity_or_route(self):
        workspace_source = (SOURCE_ROOT / "tools/check_workspace.py").read_text(encoding="utf-8")
        product_source = (SOURCE_ROOT / "tools/check_product.py").read_text(encoding="utf-8")
        self.assertNotIn("BytePress", workspace_source)
        self.assertNotIn("check_product", workspace_source)
        for marker in ("BytePress", "WROAD", "WBACK", "WPLAN", ".sln"):
            self.assertNotIn(marker, product_source)
        self.assertNotIn(str(EXPECTED_DISTRIBUTION_FILES), workspace_source + product_source)

    def test_no_third_public_checker_or_runner_executable(self):
        public = {
            path.name for path in (SOURCE_ROOT / "tools").glob("*.py")
            if "check" in path.name or "runner" in path.name or "qualif" in path.name
        }
        self.assertEqual(public, {"check_product.py", "check_workspace.py"})

    def test_transport_capabilities_are_not_equalized(self):
        with tempfile.TemporaryDirectory(prefix="bytepress-transport-") as td:
            root = Path(td)
            source = root / "tree"; source.mkdir(mode=0o750)
            regular = source / "regular"; regular.write_text("same\n", encoding="utf-8"); regular.chmod(0o640)
            executable = source / "executable"; executable.write_text("#!/bin/sh\n", encoding="utf-8"); executable.chmod(0o755)
            archive = root / "tree.tar.gz"
            with tarfile.open(archive, "w:gz") as stream:
                stream.add(source, arcname="tree")
            with tarfile.open(archive, "r:gz") as stream:
                modes = {item.name: stat.S_IMODE(item.mode) for item in stream.getmembers()}
            self.assertEqual(modes["tree/regular"], 0o640)
            self.assertEqual(modes["tree/executable"], 0o755)
            zipped = root / "tree.zip"
            with zipfile.ZipFile(zipped, "w") as stream:
                info = zipfile.ZipInfo("executable")
                info.create_system = 3
                info.external_attr = 0o100755 << 16
                stream.writestr(info, executable.read_bytes())
            with zipfile.ZipFile(zipped) as stream:
                info = stream.getinfo("executable")
                self.assertEqual((info.external_attr >> 16) & 0o777, 0o755)
            if shutil.which("git"):
                repository = root / "repository"; repository.mkdir()
                subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repository, check=True)
                shutil.copy2(regular, repository / "regular")
                shutil.copy2(executable, repository / "executable")
                subprocess.run(["git", "add", "regular", "executable"], cwd=repository, check=True)
                tree = subprocess.run(
                    ["git", "ls-files", "--stage"], cwd=repository, check=True,
                    stdout=subprocess.PIPE, text=True,
                    env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
                ).stdout
                self.assertIn("100644", tree)
                self.assertIn("100755", tree)
                self.assertNotIn("040750", tree)


if __name__ == "__main__":
    unittest.main(verbosity=2)

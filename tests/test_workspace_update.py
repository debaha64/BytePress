"""REQ-VERSION/SOT/BOUNDARY; INV-001/004/011; SCN-011/014.

Neutral tests execute the bounded manual Workspace Update sequence. This is
test-owned fixture preparation, not a public migration executable or framework.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

import test_check_workspace as fixtures

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE / "tools"))
import project_profile


class WorkspaceUpdateTests(unittest.TestCase):
    fixture = fixtures.WorkspaceCheckerTests.fixture
    run_checker = fixtures.WorkspaceCheckerTests.run_checker
    assert_pass = fixtures.WorkspaceCheckerTests.assert_pass
    assert_fail = fixtures.WorkspaceCheckerTests.assert_fail
    maxDiff = None

    def command(self, root, *args):
        result = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"},
            stdin=subprocess.DEVNULL, timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def old_fixture(self, mode="sot_files", service=False):
        root = self.fixture()
        (root / "Example.profile").unlink()
        repository = "SOT_GITHUB_REPOSITORY: owner/repository\n" if mode == "sot_github" else ""
        (root / "AGENTS.md").write_text("# Legacy 0.5.1 input\nSOT_MODE: " + mode + "\n" + repository)
        (root / "Example/VERSION").write_bytes(b"0.5.2\n")
        (root / "Example/private.txt").write_bytes(b"Product content\n")
        (root / "plans/completed/WPLAN-000099-history.md").write_bytes(b"immutable completed history\n")
        (root / "skills/private.md").write_bytes(b"private overlay\n")
        (root / "research/private.md").write_bytes(b"private research\n")
        (root / "logs/history.md").write_bytes(b"append-only history prefix\n")
        if mode == "sot_files":
            if service:
                (root / ".git").mkdir()
        else:
            self.command(root, "init", "-b", "main")
            self.command(root, "config", "user.name", "Neutral fixture")
            self.command(root, "config", "user.email", "fixture@example.invalid")
            self.command(root, "add", ".")
            self.command(root, "commit", "-m", "legacy fixture")
            if mode == "sot_github":
                bare = root.parent / "owner/repository.git"
                bare.parent.mkdir()
                self.command(root, "init", "--bare", "-b", "main", str(bare))
                self.command(root, "remote", "add", "origin", str(bare))
                # Local filesystem transport only; there is no GitHub/network.
                self.command(root, "push", "-u", "origin", "main")
                self.command(root, "remote", "set-head", "origin", "main")
        return root

    def protected(self, root):
        paths = ("Example", "plans", "research", "skills", "logs")
        return {
            p.relative_to(root).as_posix(): (p.stat().st_mode & 0o7777, hashlib.sha256(p.read_bytes()).hexdigest())
            for prefix in paths for p in (root / prefix).rglob("*") if p.is_file()
        }

    def represent_previous_version(self, root):
        agents = root / "AGENTS.md"
        text = agents.read_text()
        modes = re.findall(r"(?m)^SOT_MODE: (sot_files|sot_git|sot_github)$", text)
        self.assertEqual(len(modes), 1)
        # Execution is suspended across this bounded no-owner interval.
        agents.write_text(re.sub(r"(?m)^SOT_MODE: .*\n", "", text))
        self.assertFalse(list(root.glob("*.profile")))
        document = dict(schema_version=1, harness_version="0.5.1", sot_mode=modes[0], display_name="Example")
        (root / "Example.profile").write_bytes(project_profile.serialize_project_profile("Example.profile", document))
        return document

    def commit_fixture(self, root, mode, message):
        if mode != "sot_files":
            self.command(root, "add", "AGENTS.md", "Example.profile")
            self.command(root, "commit", "-m", message)

    def migration(self, mode, service=False):
        root = self.old_fixture(mode, service)
        before = self.protected(root)
        git_before = (root / ".git").stat() if service else None
        topology = None
        if mode == "sot_github":
            topology = tuple(self.command(root, *a) for a in (
                ("remote", "-v"), ("rev-parse", "--abbrev-ref", "@{upstream}"),
                ("symbolic-ref", "refs/remotes/origin/HEAD"),
            ))
        self.assert_fail(self.run_checker(root), "project-profile")
        document = self.represent_previous_version(root)
        self.commit_fixture(root, mode, "bounded update readback before version cutover")
        # A newer Product VERSION alone cannot advance deployed Harness version.
        self.assertEqual((root / "Example/VERSION").read_bytes(), b"0.5.2\n")
        self.assertEqual(json.loads((root / "Example.profile").read_text())["harness_version"], "0.5.1")
        self.assert_pass(self.run_checker(root))
        self.assertEqual(self.protected(root), before)
        document["harness_version"] = "0.5.2"
        (root / "Example.profile").write_bytes(project_profile.serialize_project_profile("Example.profile", document))
        self.commit_fixture(root, mode, "verified harness version cutover")
        self.assert_pass(self.run_checker(root))
        self.assertEqual(self.protected(root), before)
        self.assertNotRegex((root / "AGENTS.md").read_text(), r"(?m)^SOT_MODE")
        if mode == "sot_git":
            self.assertEqual(self.command(root, "remote"), "")
        if topology:
            self.assertEqual(topology, tuple(self.command(root, *a) for a in (
                ("remote", "-v"), ("rev-parse", "--abbrev-ref", "@{upstream}"),
                ("symbolic-ref", "refs/remotes/origin/HEAD"),
            )))
            self.assertIn("SOT_GITHUB_REPOSITORY: owner/repository", (root / "AGENTS.md").read_text())
        if service:
            after = (root / ".git").stat()
            self.assertEqual((git_before.st_mode, git_before.st_mtime_ns, git_before.st_ctime_ns),
                             (after.st_mode, after.st_mtime_ns, after.st_ctime_ns))
            self.assertEqual(list((root / ".git").iterdir()), [])
        return root

    def test_sot_files_migration_without_git(self):
        self.migration("sot_files")

    def test_sot_files_migration_with_non_authoritative_service_git(self):
        self.migration("sot_files", service=True)

    def test_sot_git_migration_local_clean_no_remote(self):
        self.migration("sot_git")

    def test_sot_github_migration_offline_preserves_origin_upstream_identity(self):
        self.migration("sot_github")

    def test_failed_readback_does_not_advance_deployed_version(self):
        root = self.old_fixture()
        self.represent_previous_version(root)
        (root / "Example").rename(root / "example")
        self.assert_fail(self.run_checker(root), "project-profile")
        self.assertEqual(json.loads((root / "Example.profile").read_text())["harness_version"], "0.5.1")

    def test_final_legacy_projection_is_competing_owner(self):
        root = self.fixture()
        (root / "AGENTS.md").write_text("SOT_MODE: sot_files\n")
        self.assert_fail(self.run_checker(root), "workspace-sot")

    def test_explicit_competing_git_owner_is_rejected(self):
        root = self.fixture()
        (root / ".git").mkdir()
        (root / "AGENTS.md").write_text("SOT_MODE: sot_git\n")
        self.assert_fail(self.run_checker(root), "workspace-sot")

    def test_profile_mode_does_not_infer_git_from_presence(self):
        root = self.fixture()
        (root / ".git").mkdir()
        env = {**os.environ, "PATH": "", "PYTHONPATH": ""}
        self.assert_pass(self.run_checker(root, env=env))

    def test_snapshot_service_exclusions_preserve_private_content(self):
        root = self.migration("sot_files", service=True)
        for name in (".agents", ".codex"):
            (root / name).mkdir()
        archive = root.parent / "fixture.tar.gz"
        with tarfile.open(archive, "w:gz") as target:
            for path in (root, *sorted(root.rglob("*"))):
                rel = path.relative_to(root)
                if rel.parts and rel.parts[0] in {".git", ".agents", ".codex"}:
                    continue
                target.add(path, arcname=str(Path(root.name) / rel), recursive=False)
        with tarfile.open(archive) as source:
            names = source.getnames()
        self.assertFalse(any(set(Path(name).parts) & {".git", ".agents", ".codex"} for name in names))
        self.assertIn(root.name + "/skills/private.md", names)

    def test_static_product_cleaner_needs_no_workspace_sot_owner(self):
        with tempfile.TemporaryDirectory() as temporary:
            product = Path(temporary) / "BytePress"
            shutil.copytree(SOURCE, product)
            agents = product / "AGENTS.md"
            agents.write_text(re.sub(r"(?m)^SOT_MODE: .*\n", "", agents.read_text()))
            probe = "import sys; from pathlib import Path; sys.path.insert(0, 'tools'); import bp_clean; error = bp_clean.product_unit_root_error(Path.cwd()); assert error is None, error"
            result = subprocess.run([sys.executable, "-B", "-c", probe],
                                    cwd=product, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

"""REQ-VERSION/SOT/BOUNDARY; INV-001/004/011; SCN-011/014.

Neutral tests execute the bounded manual Workspace Update sequence. This is
test-owned fixture preparation, not a public migration executable or framework.
"""

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

import test_check_workspace as fixtures
import test_new_project as project_start

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE / "tools"))
import project_profile


class WorkspaceUpdateTests(unittest.TestCase):
    fixture = fixtures.WorkspaceCheckerTests.fixture
    run_checker = fixtures.WorkspaceCheckerTests.run_checker
    assert_pass = fixtures.WorkspaceCheckerTests.assert_pass
    assert_fail = fixtures.WorkspaceCheckerTests.assert_fail
    maxDiff = None

    def released_workspace(self):
        """Frozen output of the real released 0.5.2 generator, never VERSION spoofing."""
        directory = SOURCE / "tests/fixtures"
        provenance = json.loads((directory / "deployed-0.5.2.json").read_text())
        archive = directory / "deployed-0.5.2.tar.gz"
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), provenance["archive_sha256"])
        temporary = tempfile.TemporaryDirectory(prefix="bytepress-released-052-")
        self.addCleanup(temporary.cleanup)
        parent = Path(temporary.name)
        with tarfile.open(archive) as stream:
            members = stream.getmembers()
            names = [item.name for item in members]
            self.assertEqual(len(names), len(set(names)))
            for item in members:
                self.assertTrue(item.name == "WS_Example" or item.name.startswith("WS_Example/"))
                self.assertNotIn("..", Path(item.name).parts)
                self.assertTrue(item.isdir() or item.isfile())
                path = parent / item.name
                if item.isdir():
                    path.mkdir(parents=True, exist_ok=True)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(stream.extractfile(item).read())
                path.chmod(item.mode)
        root = parent / "WS_Example"
        observed = project_start.tree_manifest(root)
        observed["."] = ("directory", root.stat().st_mode & 0o7777, "")
        expected = {p: (x["type"], int(x["mode"], 8), x["sha256"] or "")
                    for p, x in provenance["manifest"].items()}
        self.assertEqual(observed, expected)
        self.assertEqual(hashlib.sha256((root / "tools/check_workspace.py").read_bytes()).hexdigest(),
                         provenance["checker_sha256"])
        return root

    def test_patch_old_fixture_uses_released_checker_bytes(self):
        released = self.released_workspace()
        old = self.patch_old_workspace()
        self.assertEqual((old / "tools/check_workspace.py").read_bytes(),
                         (released / "tools/check_workspace.py").read_bytes())

    def test_patch_generated_project_start_contract_is_deployed(self):
        old = self.released_workspace()
        reference, preview = self.patch_reference()
        self.assertNotEqual((old / "docs/technical/project-start.md").read_bytes(),
                            (reference / "docs/technical/project-start.md").read_bytes())
        rows = self.patch_disposition(reference, preview)
        self.apply_patch_contracts(old, reference, preview, authorization=self.authorize_update(old, reference, rows), rows=rows)
        self.assertEqual((old / "docs/technical/project-start.md").read_bytes(),
                         (reference / "docs/technical/project-start.md").read_bytes())


    def patch_reference(self):
        temporary = tempfile.TemporaryDirectory(prefix="bytepress-patch-reference-")
        self.addCleanup(temporary.cleanup)
        inputs = dict(source_distribution=SOURCE, destination_parent=Path(temporary.name), slug="Example",
                      display_name="Example", product_mode="new", wroad="Neutral reference", existing_product=None,
                      exclude_vcs_paths=())
        preview = project_start.new_project.build_preview(**inputs)
        result = project_start.new_project.apply_project(**inputs, authorization_sha256=preview["preview_sha256"])
        return Path(result["target_workspace"]), preview

    def patch_old_workspace(self):
        root = self.released_workspace()
        # Only neutral project state is added; all released Harness bytes stay exact.
        with (root / "SYSTEM.md").open("a") as stream:
            stream.write("\nPrivate system meaning preserved.\n")
        (root / "Example/private.txt").write_bytes(b"neutral Product code and data\n")
        (root / "Example/private.txt").chmod(0o640)
        (root / "logs/history.md").write_bytes(b"immutable history\n")
        (root / "plans/completed/WPLAN-000099-history.md").write_bytes(b"completed history\n")
        return root

    def changed_deployed_paths(self, reference):
        old = self.released_workspace()
        before, after = project_start.tree_manifest(old), project_start.tree_manifest(reference)
        return {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}

    def patch_disposition(self, reference, preview):
        # A bounded patch qualification driver, not a shipped updater capability.
        actions = {row["path"]: row["action"] for row in preview["authorization_payload"]["actions"]}
        generated = {
            "Example.profile": ("GENERATED_MERGE", "Preserve composition and SoT; version cutover last."),
            "SYSTEM.md": ("GENERATED_MERGE", "Merge generated contract; preserve stronger private rules."),
            "docs/technical/project-start.md": ("GENERATED_MERGE", "Rendered Project Start contract, not a COPY action."),
            "docs/user/README.md": ("GENERATED_MERGE", "Rendered instance navigation."),
            "docs/user/first-start.md": ("GENERATED_MERGE", "Rendered instance onboarding."),
            "logs/changes.md": ("PRESERVE", "Initial Project Start fact is historical; never import reference history."),
        }
        rows = []
        for path in sorted(self.changed_deployed_paths(reference)):
            if actions.get(path) == "COPY":
                kind, reason = "COPY", "Exact copied Harness contract without private overlay."
            else:
                self.assertIn(path, generated, "Changed generated contract needs explicit disposition: " + path)
                kind, reason = generated[path]
            rows.append({"path": path, "disposition": kind, "reason": reason})
        return rows

    def validate_disposition(self, reference, preview, rows):
        required = self.patch_disposition(reference, preview)
        self.assertEqual(len(rows), len({row["path"] for row in rows}), "Duplicate disposition")
        self.assertEqual({row["path"] for row in rows}, self.changed_deployed_paths(reference),
                         "Changed downstream contract missing from disposition")
        expected = {row["path"]: row["disposition"] for row in required}
        for row in rows:
            self.assertTrue(row["reason"].strip(), "Disposition requires a reason")
            self.assertEqual(row["disposition"], expected[row["path"]],
                             "Mandatory changed contract cannot be silently preserved or excluded")

    def update_digest(self, root, reference, rows):
        payload = {"target": str(root.resolve()), "before": self.patch_tree(root),
                   "distribution": project_start.tree_manifest(SOURCE),
                   "reference": project_start.tree_manifest(reference), "disposition": rows}
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def authorize_update(self, root, reference, rows):
        """Simulated owner response to exact prepared backup/disposition in a neutral test."""
        before = self.patch_tree(root)
        self.assertTrue(all(value[0] in {"file", "directory"} for value in before.values()))
        with tempfile.NamedTemporaryFile(dir=root.parent, suffix=".tar.gz", delete=False) as stream:
            backup = Path(stream.name)
        with tarfile.open(backup, "w:gz") as archive:
            for relative in [".", *sorted(before)]:
                archive.add(root / relative, arcname=str(Path(root.name) / relative), recursive=False)
        self.assertEqual(self.patch_tree(root), before, "Workspace changed while creating backup")
        return {"snapshot": str(backup), "snapshot_sha256": hashlib.sha256(backup.read_bytes()).hexdigest(),
                "digest": self.update_digest(root, reference, rows)}

    def verify_backup(self, root, authorization):
        backup = Path(authorization["snapshot"])
        self.assertTrue(backup.is_file(), "Exact backup required")
        self.assertEqual(hashlib.sha256(backup.read_bytes()).hexdigest(), authorization["snapshot_sha256"])
        observed = {}
        with tarfile.open(backup) as archive:
            members = archive.getmembers()
            self.assertEqual(len(members), len({item.name for item in members}))
            for item in members:
                self.assertTrue(item.name == root.name or item.name.startswith(root.name + "/"))
                self.assertNotIn("..", Path(item.name).parts)
                self.assertTrue(item.isdir() or item.isfile())
                if item.name == root.name:
                    self.assertEqual(item.mode, root.stat().st_mode & 0o7777)
                    continue
                relative = Path(item.name).relative_to(root.name).as_posix()
                observed[relative] = ("directory" if item.isdir() else "file", item.mode,
                                     "" if item.isdir() else hashlib.sha256(archive.extractfile(item).read()).hexdigest())
        self.assertEqual(observed, self.patch_tree(root), "Backup must match frozen target bytes/types/modes")

    def patch_tree(self, root):
        """Permanent target surface; sot_files service projections are never traversed."""
        result = {}
        for folder, directories, files in os.walk(root, followlinks=False):
            if Path(folder) == root:
                directories[:] = [name for name in directories if name not in {".git", ".agents", ".codex", "temp"}]
            for path in [Path(folder) / name for name in directories + files]:
                mode = path.lstat().st_mode
                kind = "file" if stat.S_ISREG(mode) else "directory" if stat.S_ISDIR(mode) else "unsafe"
                result[path.relative_to(root).as_posix()] = (kind, stat.S_IMODE(mode),
                    hashlib.sha256(path.read_bytes()).hexdigest() if kind == "file" else "")
        return result

    def apply_patch_contracts(self, root, reference, preview, *, authorization=None, rows=None):
        self.assertFalse(list((root / "plans/active").glob("WPLAN-*.md")), "Update requires quiescent Workspace")
        self.assertIn("NON_EXECUTING_CHECKPOINT:", (root / "plans/backlog.md").read_text())
        self.assertIsNotNone(rows, "Exact disposition required")
        self.validate_disposition(reference, preview, rows)
        self.assertIsNotNone(authorization, "Explicit owner authorization required")
        self.assertEqual(authorization["digest"], self.update_digest(root, reference, rows), "Frozen inputs/authorization mismatch")
        self.verify_backup(root, authorization)
        self.assertTrue(all(x[0] in {"file", "directory"} for x in self.patch_tree(root).values()))
        self.assert_pass(self.run_checker(root))  # Real old checker; no research or synthetic OD.
        released = self.released_workspace()
        # Stop before writes if a copied contract has an unreviewed private overlay.
        for row in rows:
            if row["disposition"] != "PRESERVE" and row["path"] not in {"SYSTEM.md", "Example.profile"}:
                self.assertEqual((root / row["path"]).read_bytes(), (released / row["path"]).read_bytes(),
                                 "Private contract overlay needs explicit merge: " + row["path"])
                self.assertEqual((root / row["path"]).stat().st_mode & 0o7777,
                                 (released / row["path"]).stat().st_mode & 0o7777)
        old_system = (released / "SYSTEM.md").read_bytes()
        self.assertTrue((root / "SYSTEM.md").read_bytes().startswith(old_system), "SYSTEM requires reviewed semantic merge")
        for row in rows:
            path = row["path"]
            if path == "Example.profile" or row["disposition"] == "PRESERVE":
                continue
            if path == "SYSTEM.md":
                private = (root / path).read_bytes()[len(old_system):]
                merged = (reference / path).read_bytes().replace(b"deployed Harness version: `0.5.3`", b"deployed Harness version: `0.5.2`")
                (root / path).write_bytes(merged + private)
            else:
                shutil.copy2(reference / path, root / path)
        return rows

    def patch_readback(self, root, reference, rows, protected):
        self.assertEqual(self.protected(root), protected)
        self.assertEqual(json.loads((root / "Example.profile").read_text())["harness_version"], "0.5.2")
        for row in rows:
            path = row["path"]
            if path in {"Example.profile", "SYSTEM.md"} or row["disposition"] == "PRESERVE":
                continue
            actual, expected = root / path, reference / path
            self.assertEqual(actual.read_bytes(), expected.read_bytes(), path)
            self.assertEqual(actual.stat().st_mode & 0o7777, expected.stat().st_mode & 0o7777, path)
        expected_system = (reference / "SYSTEM.md").read_bytes().replace(b"deployed Harness version: `0.5.3`", b"deployed Harness version: `0.5.2`")
        self.assertTrue((root / "SYSTEM.md").read_bytes().startswith(expected_system))
        self.assert_pass(self.run_checker(root))  # New checker, previous version claim.

    def test_patch_052_to_053_deployment_readback_then_first_research(self):
        """External authorized deployment over real quiescent 0.5.2; cutover last."""
        root = self.patch_old_workspace()
        before, profile = self.protected(root), (root / "Example.profile").read_bytes()
        reference, preview = self.patch_reference()
        rows = self.patch_disposition(reference, preview)
        authorization = self.authorize_update(root, reference, rows)  # Simulated explicit owner response.
        self.apply_patch_contracts(root, reference, preview, authorization=authorization, rows=rows)
        self.patch_readback(root, reference, rows, before)
        self.assertEqual((root / "Example.profile").read_bytes(), profile)
        self.assertFalse(list((root / "plans/active").glob("WPLAN-*.md")))
        self.assertIn(b"Private system meaning preserved.", (root / "SYSTEM.md").read_bytes())
        # Verify first research on an isolated read-back copy before cutover.
        probe = root.parent / "probe" / "WS_Example"
        shutil.copytree(root, probe, copy_function=shutil.copy2)
        fixtures.open_first_research(probe)
        self.assert_pass(self.run_checker(probe))
        document = json.loads(profile)
        document["harness_version"] = "0.5.3"
        system = root / "SYSTEM.md"
        system.write_bytes(system.read_bytes().replace(b"deployed Harness version: `0.5.2`", b"deployed Harness version: `0.5.3`"))
        (root / "Example.profile").write_bytes(project_profile.serialize_project_profile("Example.profile", document))
        self.assert_pass(self.run_checker(root))
        self.assertEqual(self.protected(root), before)
        self.assertEqual({k: v for k, v in json.loads((root / "Example.profile").read_text()).items() if k != "harness_version"},
                         {k: v for k, v in json.loads(profile).items() if k != "harness_version"})
        # Successful deployment evidence is appended after cutover, under the same bounded operation.
        original_log = (root / "logs/changes.md").read_bytes()
        with (root / "logs/changes.md").open("a") as stream:
            stream.write("\nWorkspace Update 0.5.2 -> 0.5.3: owner-authorized disposition/read-back PASS.\n")
        self.assertTrue((root / "logs/changes.md").read_bytes().startswith(original_log))
        fixtures.open_first_research(root)
        self.assert_pass(self.run_checker(root))
        self.assertEqual((root / "Example/private.txt").read_bytes(), b"neutral Product code and data\n")
        self.assertEqual((root / "Example/private.txt").stat().st_mode & 0o7777, 0o640)
        self.assertNotIn("DECISION_KIND: implementation", (root / "logs/decisions.md").read_text())

    def test_patch_failed_deployment_readback_keeps_052(self):
        root = self.patch_old_workspace()
        before = self.protected(root)
        reference, preview = self.patch_reference()
        rows = self.patch_disposition(reference, preview)
        self.apply_patch_contracts(root, reference, preview, authorization=self.authorize_update(root, reference, rows), rows=rows)
        target = root / "docs/technical/project-start.md"
        target.write_text(target.read_text() + "\nInjected incomplete generated contract\n")
        with self.assertRaises(AssertionError):
            self.patch_readback(root, reference, rows, before)
        self.assertEqual(json.loads((root / "Example.profile").read_text())["harness_version"], "0.5.2")

    def test_patch_all_changed_paths_require_one_disposition(self):
        reference, preview = self.patch_reference()
        rows = self.patch_disposition(reference, preview)
        self.assertIn("docs/technical/project-start.md", {row["path"] for row in rows})
        for omitted in rows:
            with self.subTest(path=omitted["path"]), self.assertRaises(AssertionError):
                self.validate_disposition(reference, preview, [row for row in rows if row != omitted])
        with self.assertRaises(AssertionError):
            self.validate_disposition(reference, preview, rows + [rows[0]])
        wrong = [dict(row, disposition="NOT_APPLICABLE") if row["path"] == "docs/technical/project-start.md" else row for row in rows]
        with self.assertRaises(AssertionError):
            self.validate_disposition(reference, preview, wrong)

    def test_patch_authority_and_quiescence_fail_before_mutation(self):
        for condition in ("no-authorization", "stale-authorization", "active-plan", "missing-generated", "missing-backup", "private-overlay"):
            with self.subTest(condition=condition):
                root = self.patch_old_workspace()
                reference, preview = self.patch_reference()
                rows = self.patch_disposition(reference, preview)
                authorization = self.authorize_update(root, reference, rows)
                if condition == "no-authorization":
                    authorization = None
                elif condition == "stale-authorization":
                    (root / "Example/private.txt").write_bytes(b"owner changed Product since freeze\n")
                elif condition == "active-plan":
                    fixtures.open_first_research(root)
                elif condition == "missing-generated":
                    rows = [row for row in rows if row["path"] != "docs/technical/project-start.md"]
                elif condition == "missing-backup":
                    Path(authorization["snapshot"]).unlink()
                else:
                    with (root / "sops/research.md").open("a") as stream:
                        stream.write("\nPrivate copied overlay\n")
                    authorization = self.authorize_update(root, reference, rows)
                before = project_start.tree_manifest(root)
                with self.assertRaises(AssertionError):
                    self.apply_patch_contracts(root, reference, preview, authorization=authorization, rows=rows)
                self.assertEqual(project_start.tree_manifest(root), before)

    def test_real_052_checker_blocks_research_but_quiescent_start_passes(self):
        root = self.released_workspace()
        self.assert_pass(self.run_checker(root))
        fixtures.open_first_research(root)
        result = self.run_checker(root)
        self.assert_fail(result, "sdlc-transition")
        self.assertIn("owner decision must be projected", str(result[1]["errors"]))
        self.assertNotIn("DECISION_KIND: implementation", (root / "logs/decisions.md").read_text())

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

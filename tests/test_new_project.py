"""Project Start v1 regression.

Traceability: REQ-COMP/SLUG/PROFILE/SOT/PRODUCT/PART/NATIVE/START/SEED/TAS/
VERSION/BOUNDARY-001; INV-001–013/015/016; SCN-001–010.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


SOURCE_ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = SOURCE_ROOT / "tools" / "new_project.py"
if not TOOL_PATH.is_file():
    raise RuntimeError("TDD RED: tools/new_project.py отсутствует")

sys.path.insert(0, str(SOURCE_ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location("bytepress_new_project", TOOL_PATH)
assert SPEC is not None and SPEC.loader is not None
new_project = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = new_project
SPEC.loader.exec_module(new_project)


def tree_manifest(root: Path):
    result = {}
    if not root.exists():
        return result
    for base, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        directories.sort()
        filenames.sort()
        for name in directories + filenames:
            path = Path(base) / name
            relative = path.relative_to(root).as_posix()
            info = path.lstat()
            mode = stat.S_IMODE(info.st_mode)
            if stat.S_ISDIR(info.st_mode):
                value = ("directory", mode, "")
            elif stat.S_ISREG(info.st_mode):
                value = ("file", mode, hashlib.sha256(path.read_bytes()).hexdigest())
            elif stat.S_ISLNK(info.st_mode):
                value = ("symlink", mode, os.readlink(path))
            else:
                value = ("special", mode, "")
            result[relative] = value
    return result


class ProjectStartCase(unittest.TestCase):
    """Shared isolated fixture; no Product command is executed by the tool."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="bytepress-project-start-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.destination = self.base / "dest"
        self.destination.mkdir()
        self.defaults = {
            "source_distribution": SOURCE_ROOT,
            "destination_parent": self.destination,
            "slug": "Example",
            "display_name": "Пример продукта",
            "product_mode": "new",
            "wroad": "Создать полезный продукт в управляемом Workspace.",
            "existing_product": None,
            "exclude_vcs_paths": (),
        }

    def preview(self, **updates):
        values = {**self.defaults, **updates}
        return new_project.build_preview(**values)

    def apply(self, preview=None, **updates):
        preview = preview or self.preview(**updates)
        values = {**self.defaults, **updates}
        return new_project.apply_project(
            **values,
            authorization_sha256=preview["preview_sha256"],
        )

    def existing(self, name="existing"):
        root = self.base / name
        root.mkdir()
        return root

    def distribution_copy(self):
        root = self.base / "distribution"
        shutil.copytree(SOURCE_ROOT, root, copy_function=shutil.copy2)
        return root

    def staging_paths(self, destination=None, slug="Example"):
        destination = destination or self.destination
        return sorted(destination.glob(f".WS_{slug}.project-start.*.staging"))


class PreviewTests(ProjectStartCase):
    """REQ-START/SLUG/BOUNDARY; INV-001/002/007/013; SCN-003/004/009."""

    def test_preview_is_read_only_and_stable(self):
        """REQ-START-001; INV-007; SCN-003: preview has zero writes and stable bytes."""
        source_before = tree_manifest(SOURCE_ROOT)
        destination_before = tree_manifest(self.destination)
        first = self.preview()
        time.sleep(0.01)
        second = self.preview()
        self.assertEqual(first, second)
        self.assertEqual(source_before, tree_manifest(SOURCE_ROOT))
        self.assertEqual(destination_before, tree_manifest(self.destination))
        self.assertFalse(self.staging_paths())
        self.assertFalse((self.destination / "WS_Example").exists())

    def test_digest_coverage_and_transient_exclusion(self):
        """REQ-START-001; INV-007: covered input changes digest; time/staging never does."""
        baseline = self.preview()
        self.assertEqual(baseline["preview_sha256"], self.preview()["preview_sha256"])
        variants = (
            {"display_name": "Другой продукт"},
            {"wroad": "Другая точная формулировка."},
            {"slug": "Other"},
        )
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertNotEqual(
                    baseline["preview_sha256"], self.preview(**variant)["preview_sha256"]
                )
        self.assertNotIn("staging", baseline["authorization_payload"]["target"])
        volatile_keys = {"time", "timestamp", "created_at", "staging_path"}

        def assert_no_volatile_keys(value):
            if isinstance(value, dict):
                self.assertTrue(volatile_keys.isdisjoint(value))
                for child in value.values():
                    assert_no_volatile_keys(child)
            elif isinstance(value, list):
                for child in value:
                    assert_no_volatile_keys(child)

        assert_no_volatile_keys(baseline["authorization_payload"])

    def test_preview_contains_canonical_machine_and_human_contract(self):
        """REQ-START/PROFILE/VERSION-001; INV-003/007/011; SCN-003."""
        preview = self.preview()
        payload = preview["authorization_payload"]
        self.assertEqual(preview["state"], "PREVIEW_READY")
        self.assertEqual(payload["preview_schema_version"], 1)
        self.assertEqual(payload["operation"], "project_start")
        self.assertEqual(payload["initial_sot"], "sot_files")
        self.assertIn("generated_readme", payload)
        self.assertIn("profile", payload)
        self.assertIn("verification_plan", payload)
        self.assertIn("Project Start", preview["human_readable"])
        self.assertIn("## Лицензия BytePress Harness", preview["human_readable"])
        canonical = new_project.canonical_payload_bytes(payload)
        self.assertTrue(canonical.endswith(b"\n"))
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), preview["preview_sha256"])

    def test_invalid_and_reserved_slug_fail_without_mutation(self):
        """REQ-SLUG-001; INV-002/007; SCN-004."""
        for slug in ("1Bad", "Bad.Name", "Bad Name", "Тест", "CON", "lpt9"):
            with self.subTest(slug=slug), self.assertRaises(new_project.InputError):
                self.preview(slug=slug)
        self.assertEqual(tree_manifest(self.destination), {})

    def test_destination_collision_and_case_collision_fail(self):
        """REQ-COMP/SLUG/START-001; INV-001/002/007; SCN-004/009."""
        (self.destination / "WS_Example").mkdir()
        with self.assertRaises(new_project.InspectionError):
            self.preview()
        (self.destination / "WS_Example").rmdir()
        (self.destination / "ws_example").mkdir()
        with self.assertRaises(new_project.InspectionError):
            self.preview()

    def test_source_destination_overlap_fails(self):
        """REQ-START/BOUNDARY-001; INV-007/013; SCN-009."""
        distribution = self.distribution_copy()
        nested_destination = distribution / "destination"
        nested_destination.mkdir()
        with self.assertRaises(new_project.InspectionError):
            self.preview(source_distribution=distribution, destination_parent=nested_destination)

    def test_cross_platform_risk_warns_but_invalid_unicode_path_fails(self):
        """REQ-START/BOUNDARY-001; INV-004/007/013; SCN-002/003/009."""
        existing = self.existing()
        (existing / "windows:risk.txt").write_text("opaque", encoding="utf-8")
        preview = self.preview(
            product_mode="existing",
            existing_product=existing,
        )
        self.assertTrue(any(item["path"] == "windows:risk.txt" for item in preview["warnings"]))
        bad = self.existing("invalid-unicode")
        file_descriptor = os.open(os.path.join(os.fsencode(bad), b"bad-\xff"), os.O_WRONLY | os.O_CREAT, 0o600)
        os.close(file_descriptor)
        with self.assertRaises(new_project.InspectionError):
            self.preview(product_mode="existing", existing_product=bad)

    def test_read_only_known_target_component_limit_fails_before_authorization(self):
        """REQ-START/BOUNDARY-001; INV-007/013; SCN-009."""
        existing = self.existing()
        (existing / ("x" * 21)).write_text("opaque", encoding="utf-8")

        def target_limits(_path, name):
            return 20 if name == "PC_NAME_MAX" else 4096

        with mock.patch.object(new_project.os, "pathconf", side_effect=target_limits):
            with self.assertRaises(new_project.InspectionError):
                self.preview(product_mode="existing", existing_product=existing)
        self.assertEqual(tree_manifest(self.destination), {})

    def test_known_missing_atomic_commit_primitive_fails_in_preview(self):
        """REQ-START/BOUNDARY-001; INV-007/013; SCN-003/009."""
        with mock.patch.object(new_project.sys, "platform", "darwin"):
            with self.assertRaises(new_project.InspectionError):
                self.preview()
        self.assertEqual(tree_manifest(self.destination), {})


class NewProductTests(ProjectStartCase):
    """REQ-COMP/PROFILE/SOT/START/SEED/TAS/BOUNDARY; INV-001/003/006–009/013."""

    def test_new_product_exact_composition_profile_and_wroad_only(self):
        """REQ-COMP/PROFILE/START/SEED-001; INV-001/003/008/009; SCN-001/006."""
        result = self.apply()
        root = Path(result["target_workspace"])
        product = root / "Example"
        self.assertEqual(result["state"], "OWNER_PLANNING")
        self.assertTrue(product.is_dir())
        self.assertEqual(list(product.iterdir()), [])
        profiles = list(root.glob("*.profile"))
        self.assertEqual([path.name for path in profiles], ["Example.profile"])
        document = json.loads(profiles[0].read_text(encoding="utf-8"))
        self.assertEqual(
            document,
            {
                "display_name": "Пример продукта",
                "harness_version": "0.5.2",
                "schema_version": 1,
                "sot_mode": "sot_files",
            },
        )
        self.assertEqual(list((root / "plans" / "active").iterdir()), [])
        self.assertFalse(any((root / "plans").rglob("WBACK-*.md")))
        self.assertFalse(any((root / "plans").rglob("WPLAN-*.md")))
        backlog = (root / "plans" / "backlog.md").read_text(encoding="utf-8")
        roadmap = (root / "plans" / "roadmap.md").read_text(encoding="utf-8")
        self.assertIn("WROAD-000001-OWNER-PLANNING", backlog)
        self.assertIn("WROAD-000001", roadmap)
        self.assertNotIn("WBACK-000001", roadmap + backlog)
        self.assertNotIn("WPLAN-000001", roadmap + backlog)

    def test_workspace_readme_has_terminal_exact_license_and_no_license_artifact(self):
        """REQ-START/BOUNDARY-001; INV-001/013; SCN-001."""
        root = Path(self.apply()["target_workspace"])
        data = (root / "README.md").read_bytes()
        expected_tail = b"## \xd0\x9b\xd0\xb8\xd1\x86\xd0\xb5\xd0\xbd\xd0\xb7\xd0\xb8\xd1\x8f BytePress Harness\n\n" + (SOURCE_ROOT / "LICENSE").read_bytes()
        self.assertTrue(data.endswith(expected_tail))
        self.assertFalse((root / "LICENSE").exists())
        self.assertFalse((root / "BYTEPRESS-LICENSE.txt").exists())
        self.assertFalse((root / "licenses").exists())
        self.assertFalse((root / "Example" / "LICENSE").exists())

    def test_harness_is_outside_empty_product_and_uses_workspace_templates(self):
        """REQ-SEED/TAS/BOUNDARY-001; INV-006/009/013; SCN-006/010."""
        preview = self.preview()
        root = Path(self.apply(preview)["target_workspace"])
        product = root / "Example"
        for forbidden in ("AGENTS.md", "SYSTEM.md", "tools", "templates", "plans", "docs", "tests", "research", "src"):
            self.assertFalse((product / forbidden).exists(), forbidden)
        self.assertTrue((root / "AGENTS.md").is_file())
        self.assertTrue((root / "SYSTEM.md").is_file())
        self.assertTrue((root / "templates" / "workspace-roadmap.md").is_file())
        self.assertEqual(
            (root / "plans" / "completed" / "README.md").read_bytes(),
            (SOURCE_ROOT / "templates" / "workspace-plan-completed-readme.md").read_bytes(),
        )
        actions = preview["authorization_payload"]["actions"]
        self.assertTrue(any(item["path"] == "plans/roadmap.md" for item in actions))
        self.assertFalse(any(item["path"].startswith("Example/") and item["path"] != "Example" for item in actions))

    def test_real_project_start_materializes_and_runs_both_generic_checkers(self):
        """REQ-CHECK/START-001; INV-001/010/012/013; SCN-001/007/008."""
        root = Path(self.apply()["target_workspace"])
        workspace_checker = root / "tools/check_workspace.py"
        product_checker = root / "tools/check_product.py"
        self.assertTrue(workspace_checker.is_file())
        self.assertTrue(product_checker.is_file())
        self.assertFalse((root / "tools/bp_check.py").exists())
        self.assertFalse((root / "research/archives").exists())
        for checker in (workspace_checker, product_checker):
            completed = subprocess.run(
                [sys.executable, "-B", str(checker), "--workspace", str(root), "--format", "json"],
                cwd=root, stdin=subprocess.DEVNULL, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["status"], "PASS")

    def test_new_and_existing_deploy_durable_product_acceptance_checker(self):
        for mode in ("new", "existing"):
            with self.subTest(product_mode=mode):
                existing = self.existing() if mode == "existing" else None
                if existing:
                    (existing / "opaque.bin").write_bytes(b"\x00Product stays opaque\xff")
                updates = {"slug": "Fresh" + mode.title(), "product_mode": mode, "existing_product": existing}
                root = Path(self.apply(**updates)["target_workspace"])
                for relative in ("tools/check_workspace.py", "tests/test_check_workspace.py"):
                    self.assertEqual((root / relative).read_bytes(), (SOURCE_ROOT / relative).read_bytes())
                environment = dict(os.environ)
                environment.pop("PYTHONPATH", None)
                environment["PYTHONDONTWRITEBYTECODE"] = "1"
                completed = subprocess.run(
                    [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests",
                     "-p", "test_check_workspace.py", "-k", "durable_product_acceptance_in_later_release_wplan"],
                    cwd=root, env=environment, stdin=subprocess.DEVNULL,
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertIn("Ran 1 test", completed.stderr)
                if existing:
                    self.assertEqual((root / updates["slug"] / "opaque.bin").read_bytes(), (existing / "opaque.bin").read_bytes())

    def test_fresh_workspace_first_plan_executes_sdlc_authority_and_delta_contract(self):
        """REQ-SDLC-TRANSITION/EVIDENCE/DELTA-001; INV-SDLC-002..008; SCN-SDLC-001..012."""
        root = Path(self.apply()["target_workspace"])
        checker = root / "tools/check_workspace.py"

        def run_checker(*extra):
            environment = dict(os.environ)
            environment.pop("PYTHONPATH", None)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            completed = subprocess.run(
                [sys.executable, "-B", str(checker), "--workspace", str(root), "--format", "json", *map(str, extra)],
                cwd=root, env=environment, stdin=subprocess.DEVNULL, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            return completed, json.loads(completed.stdout)

        def assert_status(expected, result, check_id=None):
            completed, payload = result
            expected_code = 0 if expected == "PASS" else 1
            self.assertEqual(completed.returncode, expected_code, completed.stdout + completed.stderr)
            self.assertEqual(payload["status"], expected)
            if check_id:
                self.assertIn(check_id, {item["id"] for item in payload["checks"] if item["status"] == "FAIL"})
            return payload

        initial = assert_status("PASS", run_checker())
        self.assertIn("WROAD-000001-OWNER-PLANNING", initial["checks"][2]["value"]["checkpoint"])

        plan_template = (root / "templates/workspace-plan-active.md").read_text(encoding="utf-8")
        for required_contract in (
            "INTERVIEW_EVIDENCE_REF:", "OWNER_DECISION_REFS:", "ALLOWED_SURFACES:",
            "EVIDENCE_KIND:", "### CREATE", "### UPDATE", "### PRESERVE", "### REMOVE",
            "file:mode", "content,mode,type",
        ):
            self.assertIn(required_contract, plan_template)
        for relative in ("sops/verify-work.md", "tools/README.md"):
            deployed_consumer = (root / relative).read_text(encoding="utf-8")
            self.assertIn("required owner decision kind", deployed_consumer)
            self.assertIn("docs/technical/phase-gates.md", deployed_consumer)

        plan = root / "plans/active/WPLAN-000001-fixture.md"
        (root / "plans/backlog.md").write_text(
            "WROAD-000001 active\nWBACK-000001 active\nactive WPLAN count 1\n"
            "CHECKPOINT: `WBACK-000001-WORK-IN-PROGRESS`.\n",
            encoding="utf-8",
        )
        with (root / "logs/decisions.md").open("a", encoding="utf-8") as stream:
            stream.write(
                "\nRELEASE_AUTHORIZATION_FIXTURE: authorized\nWPLAN_ID: WPLAN-000001\n\n"
                "RECORD_TYPE: owner_decision\nRECORD_ID: OD-000001\nWPLAN_ID: WPLAN-000001\n"
                "DECISION_KIND: implementation\nDECISION_VALUE: approved\nEVIDENCE_REF: IE-000001\n"
                "ROUTE_REF: WBACK-000001\nSTATUS: active\n\n"
                "RECORD_TYPE: owner_decision\nRECORD_ID: OD-000002\nWPLAN_ID: WPLAN-000001\n"
                "DECISION_KIND: decommissioning_authorization\nDECISION_VALUE: approved\nEVIDENCE_REF: IE-000001\n"
                "ROUTE_REF: WBACK-000001\nSTATUS: active\n\n"
                "RECORD_TYPE: owner_decision\nRECORD_ID: OD-000003\nWPLAN_ID: WPLAN-000001\n"
                "DECISION_KIND: retirement_authorization\nDECISION_VALUE: approved\nEVIDENCE_REF: IE-000001\n"
                "ROUTE_REF: WBACK-000001\nSTATUS: active\n"
            )
        with (root / "logs/sessions.md").open("a", encoding="utf-8") as stream:
            stream.write(
                "\nRECORD_TYPE: interview_evidence\nRECORD_ID: IE-000001\n"
                "WPLAN_ID: WPLAN-000001\nSTATUS: complete\n"
            )

        def set_field(document, label, value):
            document, count = re.subn(
                rf"(?m)^{re.escape(label)}\s*:.*$", f"{label}: {value}", document
            )
            self.assertEqual(count, 1, label)
            return document

        plan_text = plan_template.replace("# WPLAN-<ID>-<slug>", "# WPLAN-000001-fixture", 1)
        fields = {
            "WPLAN ID": "WPLAN-000001", "WROAD": "WROAD-000001", "WBACK": "WBACK-000001",
            "Фаза SDLC": "implementation", "Операционный режим": "system-editing",
            "Класс изменения": "S2", "Disposition": "affected",
            "Owners": "docs/technical/phase-gates.md", "Reason": "Проверка fixture перехода.",
            "Текущая контрольная отметка": "WBACK-000001-WORK-IN-PROGRESS",
            "INTERVIEW_EVIDENCE_REF": "IE-000001", "OWNER_DECISION_REFS": "OD-000001",
            "ALLOWED_SURFACES": "tests/evidence.md,logs/sessions.md,logs/decisions.md",
            "TRANSITION_STATE": "in-progress", "FROM_PHASE": "implementation",
            "FROM_ROLE": "roles/11-developer.md", "PHASE_COMPLETION": "pending",
            "EVIDENCE_KIND": "implementation-red-green-delta", "EVIDENCE_REFS": "none",
            "TRANSITION_CHECKPOINT": "WBACK-000001-WORK-IN-PROGRESS", "HANDOFF_REF": "none",
            "TO_PHASE": "verification", "TO_ROLE": "roles/12-verification-engineer.md",
            "FROM_ROLE_AUTHORITY": "active", "TO_ROLE_AUTHORITY": "withheld",
            "AUTHORITY_REF": "OD-000001", "OWNER_GATE": "none",
            "OWNER_GATE_STATUS": "not-applicable", "OWNER_GATE_REF": "none",
            "VERIFICATION_STATUS": "pending", "VERIFICATION_REF": "none",
            "VALIDATION_STATUS": "not-performed", "VALIDATION_REF": "none",
            "PRODUCT_ACCEPTANCE_STATUS": "not-performed", "PRODUCT_ACCEPTANCE_REF": "none",
            "RELEASE_AUTHORIZATION_STATUS": "not-performed", "RELEASE_AUTHORIZATION_REF": "none",
        }
        for label, value in fields.items():
            plan_text = set_field(plan_text, label, value)
        surface_sections = {
            "### CREATE — <count>\n\n1. `<relative path>` — `<file:mode | directory:mode>`.":
                "### CREATE — 1\n\n1. `tests/evidence.md` — `file:0644`.",
            "### UPDATE — <count>\n\n1. `<relative path>` — `<непустое подмножество content,mode,type>`.":
                "### UPDATE — 3\n\n1. `plans/active/WPLAN-000001-fixture.md` — `content`.\n"
                "2. `logs/sessions.md` — `content`.\n"
                "3. `logs/decisions.md` — `content`.",
            "### PRESERVE — <count>\n\n1. `<relative path | relative tree/**>`.":
                "### PRESERVE — 1\n\n1. `SYSTEM.md`.",
            "### REMOVE — <count>\n\n1. `<relative path>` — `<file | directory>`.":
                "### REMOVE — 0",
        }
        for placeholder, concrete in surface_sections.items():
            self.assertIn(placeholder, plan_text)
            plan_text = plan_text.replace(placeholder, concrete, 1)
        plan.write_text(plan_text, encoding="utf-8")
        in_progress = plan.read_text(encoding="utf-8")
        assert_status("PASS", run_checker())
        plan.write_text(in_progress.replace("TO_ROLE_AUTHORITY: withheld", "TO_ROLE_AUTHORITY: granted", 1), encoding="utf-8")
        assert_status("FAIL", run_checker(), "sdlc-transition")
        plan.write_text(
            in_progress.replace("AUTHORITY_REF: OD-000001", "AUTHORITY_REF: logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE", 1),
            encoding="utf-8",
        )
        assert_status("FAIL", run_checker(), "sdlc-transition")
        plan.write_text(in_progress, encoding="utf-8")

        baseline = self.base / "first-plan-baseline.tsv"
        (root / "tests/arbitrary.md").write_text("BANANA\n", encoding="utf-8")
        before_baseline = tree_manifest(root)
        baseline_result = subprocess.run(
            [sys.executable, "-B", str(checker), "--workspace", str(root), "--print-baseline-manifest"],
            cwd=root, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        self.assertEqual(baseline_result.returncode, 0, baseline_result.stdout + baseline_result.stderr)
        self.assertTrue(baseline_result.stdout.startswith("manifest\t1\tcomplete\t.\n"))
        self.assertEqual(tree_manifest(root), before_baseline)
        baseline.write_text(baseline_result.stdout, encoding="utf-8")
        product_before = tree_manifest(root / "Example")
        history_before = (root / "logs/history.md").read_bytes()

        (root / "tests/evidence.md").write_text("EVIDENCE-FIXTURE\n", encoding="utf-8")
        with (root / "logs/sessions.md").open("a", encoding="utf-8") as stream:
            stream.write("\nHANDOFF-IMPLEMENTATION\nHANDOFF-VERIFICATION\n")
        owner_review = in_progress
        replacements = {
            "Фаза SDLC: implementation": "Фаза SDLC: owner-review",
            "FROM_PHASE: implementation": "FROM_PHASE: verification",
            "FROM_ROLE: roles/11-developer.md": "FROM_ROLE: roles/12-verification-engineer.md",
            "TO_PHASE: verification": "TO_PHASE: owner-review",
            "TO_ROLE: roles/12-verification-engineer.md": "TO_ROLE: roles/13-review-coordinator.md",
            "TRANSITION_STATE: in-progress": "TRANSITION_STATE: complete",
            "PHASE_COMPLETION: pending": "PHASE_COMPLETION: complete",
            "EVIDENCE_KIND: implementation-red-green-delta": "EVIDENCE_KIND: technical-verdict-and-traceability",
            "EVIDENCE_REFS: none": "EVIDENCE_REFS: tests/evidence.md#EVIDENCE-FIXTURE",
            "HANDOFF_REF: none": "HANDOFF_REF: logs/sessions.md#HANDOFF-VERIFICATION",
            "FROM_ROLE_AUTHORITY: active": "FROM_ROLE_AUTHORITY: relinquished",
            "TO_ROLE_AUTHORITY: withheld": "TO_ROLE_AUTHORITY: granted",
            "OWNER_GATE: none": "OWNER_GATE: GATE-OWNER-FIXTURE",
            "OWNER_GATE_STATUS: not-applicable": "OWNER_GATE_STATUS: pending",
            "VERIFICATION_STATUS: pending": "VERIFICATION_STATUS: pass",
            "VERIFICATION_REF: none": "VERIFICATION_REF: tests/evidence.md#EVIDENCE-FIXTURE",
        }
        for old, new in replacements.items():
            self.assertIn(old, owner_review)
            owner_review = owner_review.replace(old, new, 1)
        evidence = root / "tests/evidence.md"
        evidence.write_text(
            "EVIDENCE_ID: EVIDENCE-FIXTURE\nWPLAN_ID: WPLAN-000001\n"
            "EVIDENCE_KIND: technical-verdict-and-traceability\n",
            encoding="utf-8",
        )
        plan.write_text(owner_review, encoding="utf-8")
        assert_status("PASS", run_checker())

        plan.write_text(owner_review.replace("EVIDENCE_REFS: tests/evidence.md#EVIDENCE-FIXTURE", "EVIDENCE_REFS: none", 1), encoding="utf-8")
        assert_status("FAIL", run_checker(), "sdlc-transition")
        plan.write_text(
            owner_review.replace(
                "EVIDENCE_REFS: tests/evidence.md#EVIDENCE-FIXTURE",
                "EVIDENCE_REFS: tests/arbitrary.md#BANANA",
                1,
            ),
            encoding="utf-8",
        )
        assert_status("FAIL", run_checker(), "sdlc-transition")
        plan.write_text(owner_review.replace("OWNER_GATE_STATUS: pending", "OWNER_GATE_STATUS: satisfied", 1), encoding="utf-8")
        assert_status("FAIL", run_checker(), "sdlc-transition")
        wrong_gate = owner_review.replace("OWNER_GATE_STATUS: pending", "OWNER_GATE_STATUS: satisfied", 1).replace(
            "OWNER_GATE_REF: none", "OWNER_GATE_REF: logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE", 1
        )
        plan.write_text(wrong_gate, encoding="utf-8")
        assert_status("FAIL", run_checker(), "sdlc-transition")

        def lifecycle_plan(
            source, source_role, target, target_role, evidence_kind,
            gate_kind, gate_ref, decision_refs, product_acceptance=False,
        ):
            document = owner_review
            projections = {
                "Фаза SDLC": target,
                "FROM_PHASE": source,
                "FROM_ROLE": source_role,
                "EVIDENCE_KIND": evidence_kind,
                "TO_PHASE": target,
                "TO_ROLE": target_role,
                "TO_ROLE_AUTHORITY": "not-applicable" if target == "retired" else "granted",
                "OWNER_GATE": f"GATE-OWNER-FIXTURE-{gate_kind}",
                "OWNER_GATE_STATUS": "satisfied",
                "OWNER_GATE_REF": gate_ref,
                "OWNER_DECISION_REFS": decision_refs,
                "PRODUCT_ACCEPTANCE_STATUS": "accepted" if product_acceptance else "not-performed",
                "PRODUCT_ACCEPTANCE_REF": "PA-000001" if product_acceptance else "none",
            }
            for label, value in projections.items():
                document = set_field(document, label, value)
            evidence.write_text(
                "EVIDENCE_ID: EVIDENCE-FIXTURE\nWPLAN_ID: WPLAN-000001\n"
                f"EVIDENCE_KIND: {evidence_kind}\n",
                encoding="utf-8",
            )
            return document

        product_acceptance_entry = owner_review
        for label, value in {
            "Фаза SDLC": "product-acceptance",
            "FROM_PHASE": "owner-review",
            "FROM_ROLE": "roles/13-review-coordinator.md",
            "EVIDENCE_KIND": "owner-review-decision",
            "TO_PHASE": "product-acceptance",
            "TO_ROLE": "roles/14-product-acceptance-coordinator.md",
            "OWNER_GATE": "GATE-OWNER-FIXTURE-PRODUCT-ACCEPTANCE-PHASE",
            "OWNER_GATE_STATUS": "pending",
            "OWNER_GATE_REF": "none",
            "PRODUCT_ACCEPTANCE_STATUS": "not-performed",
            "PRODUCT_ACCEPTANCE_REF": "none",
        }.items():
            product_acceptance_entry = set_field(product_acceptance_entry, label, value)
        evidence.write_text(
            "EVIDENCE_ID: EVIDENCE-FIXTURE\nWPLAN_ID: WPLAN-000001\n"
            "EVIDENCE_KIND: owner-review-decision\n",
            encoding="utf-8",
        )
        plan.write_text(product_acceptance_entry, encoding="utf-8")
        assert_status("PASS", run_checker())
        self.assertNotIn("RECORD_ID: PA-", (root / "logs/decisions.md").read_text(encoding="utf-8"))
        self.assertIn("PRODUCT_ACCEPTANCE_STATUS: not-performed", plan.read_text(encoding="utf-8"))

        product_acceptance_exit = lifecycle_plan(
            "product-acceptance", "roles/14-product-acceptance-coordinator.md",
            "release-readiness", "roles/15-release-readiness-reviewer.md",
            "product-acceptance-decision", "PRODUCT-ACCEPTANCE",
            "PA-000001", "OD-000001", product_acceptance=True,
        )
        plan.write_text(product_acceptance_exit, encoding="utf-8")
        assert_status("FAIL", run_checker(), "sdlc-transition")
        with (root / "logs/decisions.md").open("a", encoding="utf-8") as stream:
            stream.write(
                "\nRECORD_TYPE: product_acceptance\nRECORD_ID: PA-000001\n"
                "WPLAN_ID: WPLAN-000001\nDECISION_VALUE: accepted\n"
            )
        assert_status("PASS", run_checker())

        wrong_product_acceptance_substitutions = (
            ("IMPLEMENTATION-AUTHORIZATION", "OD-000001", "OD-000001", False),
            ("RELEASE-AUTHORIZATION", "logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE", "OD-000001", False),
            ("DECOMMISSIONING-AUTHORIZATION", "OD-000002", "OD-000001,OD-000002", False),
            ("RETIREMENT-AUTHORIZATION", "OD-000003", "OD-000001,OD-000003", False),
            ("PRODUCT-ACCEPTANCE", "tests/evidence.md#EVIDENCE-FIXTURE", "OD-000001", True),
        )
        for gate_kind, gate_ref, decision_refs, product_acceptance in wrong_product_acceptance_substitutions:
            plan.write_text(
                lifecycle_plan(
                    "product-acceptance", "roles/14-product-acceptance-coordinator.md",
                    "release-readiness", "roles/15-release-readiness-reviewer.md",
                    "product-acceptance-decision", gate_kind, gate_ref, decision_refs,
                    product_acceptance=product_acceptance,
                ),
                encoding="utf-8",
            )
            assert_status("FAIL", run_checker(), "sdlc-transition")

        decommissioning = lifecycle_plan(
            "retrospective", "roles/20-retrospective-facilitator.md",
            "decommissioning", "roles/21-decommissioning-engineer.md",
            "retrospective-and-decommission-authorization", "DECOMMISSIONING-AUTHORIZATION",
            "OD-000002", "OD-000001,OD-000002",
        )
        plan.write_text(decommissioning, encoding="utf-8")
        assert_status("PASS", run_checker())
        plan.write_text(
            lifecycle_plan(
                "retrospective", "roles/20-retrospective-facilitator.md",
                "decommissioning", "roles/21-decommissioning-engineer.md",
                "retrospective-and-decommission-authorization", "IMPLEMENTATION-AUTHORIZATION",
                "OD-000001", "OD-000001",
            ),
            encoding="utf-8",
        )
        assert_status("FAIL", run_checker(), "sdlc-transition")

        retirement = lifecycle_plan(
            "decommissioning", "roles/21-decommissioning-engineer.md",
            "retired", "none", "decommissioning-evidence",
            "RETIREMENT-AUTHORIZATION", "OD-000003", "OD-000001,OD-000003",
        )
        plan.write_text(retirement, encoding="utf-8")
        assert_status("PASS", run_checker())
        plan.write_text(
            lifecycle_plan(
                "decommissioning", "roles/21-decommissioning-engineer.md",
                "retired", "none", "decommissioning-evidence",
                "PRODUCT-ACCEPTANCE", "PA-000001", "OD-000001",
                product_acceptance=True,
            ),
            encoding="utf-8",
        )
        assert_status("FAIL", run_checker(), "sdlc-transition")

        evidence.write_text(
            "EVIDENCE_ID: EVIDENCE-FIXTURE\nWPLAN_ID: WPLAN-000001\n"
            "EVIDENCE_KIND: technical-verdict-and-traceability\n",
            encoding="utf-8",
        )
        plan.write_text(owner_review, encoding="utf-8")

        system = root / "SYSTEM.md"
        protected = system.read_bytes()
        system.write_bytes(protected + b"\nfixture mutation\n")
        assert_status("FAIL", run_checker("--baseline-manifest", baseline), "actual-delta")
        system.write_bytes(protected)
        final_payload = assert_status("PASS", run_checker("--baseline-manifest", baseline))
        self.assertEqual(next(item for item in final_payload["checks"] if item["id"] == "actual-delta")["value"]["PROTECTED"], 1)
        self.assertEqual(next(item for item in final_payload["checks"] if item["id"] == "runtime-residue")["status"], "PASS")
        self.assertEqual(tree_manifest(root / "Example"), product_before)
        self.assertEqual((root / "logs/history.md").read_bytes(), history_before)

    def test_declared_parts_and_native_checks_are_explicit_after_project_start(self):
        """REQ-PART/NATIVE/CHECK/START-001; INV-005/006/012; SCN-005/008."""
        root = Path(self.apply()["target_workspace"])
        product = root / "Example"
        (product / "Core").mkdir()
        sentinel = product / "native-ran"
        (product / "native.py").write_text(
            f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\nprint('native pass')\n",
            encoding="utf-8",
        )
        profile_path = root / "Example.profile"
        profile_path.write_bytes(new_project.serialize_project_profile(profile_path.name, {
            "schema_version": 1,
            "harness_version": "0.5.2",
            "sot_mode": "sot_files",
            "display_name": "Example Product",
            "product_parts": {"Core": {"responsibility": "Neutral core"}},
            "product_native_checks": {
                "unit": {"command": ["python3", "native.py"], "working_directory": "."}
            },
        }))
        checker = root / "tools/check_product.py"
        composition = subprocess.run(
            [sys.executable, "-B", str(checker), "--workspace", str(root), "--format", "json"],
            cwd=root, stdin=subprocess.DEVNULL, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(composition.returncode, 0, composition.stdout + composition.stderr)
        self.assertFalse(sentinel.exists())
        native = subprocess.run(
            [sys.executable, "-B", str(checker), "--workspace", str(root),
             "--run-native-checks", "--timeout-seconds", "3", "--format", "json"],
            cwd=root, stdin=subprocess.DEVNULL, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(native.returncode, 0, native.stdout + native.stderr)
        self.assertTrue(sentinel.is_file())

    def test_deployment_uses_a_frozen_per_file_manifest(self):
        """REQ-COMP/START-001; INV-001/013; SCN-001: no broad-tree copy."""
        distribution = self.distribution_copy()
        extension = distribution / "sops" / "undeclared-extension.md"
        extension.write_text("Не входит в Project Start v1 deployment manifest.\n", encoding="utf-8")
        preview = self.preview(source_distribution=distribution)
        deployed = {item["path"] for item in preview["authorization_payload"]["actions"]}
        self.assertNotIn("sops/undeclared-extension.md", deployed)


class ExistingProductTests(ProjectStartCase):
    """REQ-PRODUCT/SOT/NATIVE/START/BOUNDARY; INV-004/007/012/013; SCN-002/008/009."""

    def make_opaque_product(self):
        product = self.existing()
        (product / ".hidden").write_bytes(b"hidden\x00bytes")
        (product / ".gitignore").write_text("build/\n", encoding="utf-8")
        (product / ".gitattributes").write_text("* text=auto\n", encoding="utf-8")
        script = product / "never-run.py"
        script.write_text("raise SystemExit('must never execute')\n", encoding="utf-8")
        script.chmod(0o751)
        nested = product / "nested"
        nested.mkdir(mode=0o750)
        (nested / "data.bin").write_bytes(b"\x00\x01opaque")
        return product

    def test_copy_only_preserves_hidden_bytes_modes_and_never_executes(self):
        """REQ-PRODUCT/NATIVE/START-001; INV-004/012/013; SCN-002/008."""
        product = self.make_opaque_product()
        sentinel = self.base / "executed"
        hook = product / "hook.py"
        hook.write_text(f"from pathlib import Path; Path({str(sentinel)!r}).write_text('bad')\n", encoding="utf-8")
        hook.chmod(0o755)
        before = tree_manifest(product)
        result = self.apply(product_mode="existing", existing_product=product)
        target = Path(result["target_workspace"]) / "Example"
        self.assertEqual(tree_manifest(product), before)
        self.assertEqual(tree_manifest(target), before)
        self.assertFalse(sentinel.exists())
        self.assertEqual(stat.S_IMODE((target / "never-run.py").stat().st_mode), 0o751)
        self.assertEqual(stat.S_IMODE((target / "nested").stat().st_mode), 0o750)

    def test_targeted_tas_like_src_and_plans_remain_product_only(self):
        """REQ-TAS/START-001; INV-004/006/013; SCN-010."""
        product = self.existing()
        (product / "src/TAS.Core").mkdir(parents=True)
        (product / "plans").mkdir()
        (product / "plans/strategy.md").write_text("Product-owned plan\n", encoding="utf-8")
        (product / "src/TAS.Core/model.cs").write_text("namespace TAS.Core;\n", encoding="utf-8")
        target = Path(self.apply(product_mode="existing", existing_product=product)["target_workspace"])
        copied = target / "Example"
        self.assertTrue((copied / "src/TAS.Core/model.cs").is_file())
        self.assertTrue((copied / "plans/strategy.md").is_file())
        self.assertFalse((copied / "tools/check_workspace.py").exists())
        self.assertTrue((target / "tools/check_workspace.py").is_file())
        self.assertTrue((target / "tools/check_product.py").is_file())

    def test_git_directory_exact_exclusion_and_ordinary_hidden_copy(self):
        """REQ-SOT/START-001; INV-004/007/013; SCN-002/003."""
        product = self.make_opaque_product()
        git = product / ".git"
        git.mkdir()
        (git / "config").write_text("opaque git metadata", encoding="utf-8")
        before = tree_manifest(product)
        preview = self.preview(
            product_mode="existing", existing_product=product, exclude_vcs_paths=(".git",)
        )
        self.assertEqual(preview["vcs_exclusions"][0]["classification"], "git-directory")
        self.assertTrue(any(item["path"] == ".git/config" for item in preview["authorization_payload"]["exclusions"]))
        target = Path(self.apply(preview, product_mode="existing", existing_product=product, exclude_vcs_paths=(".git",))["target_workspace"]) / "Example"
        self.assertFalse((target / ".git").exists())
        self.assertTrue((target / ".gitignore").is_file())
        self.assertTrue((target / ".gitattributes").is_file())
        self.assertEqual(tree_manifest(product), before)

    def test_valid_gitfile_and_nested_hg_svn_exact_exclusions(self):
        """REQ-SOT/START-001; INV-004/007/013; SCN-002/003."""
        product = self.make_opaque_product()
        (product / ".git").write_text("gitdir: ../metadata/worktree\n", encoding="utf-8")
        (product / "nested" / ".hg").mkdir()
        (product / "nested" / ".svn").mkdir()
        exclusions = (".git", "nested/.hg", "nested/.svn")
        preview = self.preview(product_mode="existing", existing_product=product, exclude_vcs_paths=exclusions)
        classes = {item["path"]: item["classification"] for item in preview["vcs_exclusions"]}
        self.assertEqual(classes, {".git": "gitfile", "nested/.hg": "hg-directory", "nested/.svn": "svn-directory"})
        target = Path(self.apply(preview, product_mode="existing", existing_product=product, exclude_vcs_paths=exclusions)["target_workspace"]) / "Example"
        for relative in exclusions:
            self.assertFalse((target / relative).exists())

    def test_malformed_or_unauthorized_vcs_metadata_fails(self):
        """REQ-SOT/START-001; INV-004/007/013; SCN-002/009."""
        malformed = self.existing("malformed")
        (malformed / ".git").write_text("not a gitfile\n", encoding="utf-8")
        with self.assertRaises(new_project.InspectionError):
            self.preview(product_mode="existing", existing_product=malformed, exclude_vcs_paths=(".git",))
        unauthorized = self.existing("unauthorized")
        (unauthorized / ".git").mkdir()
        with self.assertRaises(new_project.InspectionError):
            self.preview(product_mode="existing", existing_product=unauthorized)
        regular_hg = self.existing("regular-hg")
        (regular_hg / ".hg").write_text("unsupported", encoding="utf-8")
        with self.assertRaises(new_project.InspectionError):
            self.preview(product_mode="existing", existing_product=regular_hg, exclude_vcs_paths=(".hg",))

    def test_symlink_hardlink_and_special_nodes_fail_closed(self):
        """REQ-PRODUCT/START-001; INV-004/013; SCN-002/009."""
        symlink_product = self.existing("symlink")
        (symlink_product / "file").write_text("data", encoding="utf-8")
        (symlink_product / "link").symlink_to("file")
        hardlink_product = self.existing("hardlink")
        (hardlink_product / "one").write_text("data", encoding="utf-8")
        os.link(hardlink_product / "one", hardlink_product / "two")
        fifo_product = self.existing("fifo")
        os.mkfifo(fifo_product / "pipe")
        for product in (symlink_product, hardlink_product, fifo_product):
            with self.subTest(product=product.name), self.assertRaises(new_project.InspectionError):
                self.preview(product_mode="existing", existing_product=product)

    def test_vcs_drift_or_changed_exclusions_invalidates_authorization(self):
        """REQ-SOT/START-001; INV-004/007/013; SCN-003/009."""
        product = self.existing()
        (product / ".git").mkdir()
        preview = self.preview(product_mode="existing", existing_product=product, exclude_vcs_paths=(".git",))
        (product / ".git" / "config").write_text("drift", encoding="utf-8")
        with self.assertRaises(new_project.InspectionError):
            self.apply(preview, product_mode="existing", existing_product=product, exclude_vcs_paths=(".git",))
        self.assertFalse(self.staging_paths())
        self.assertFalse((self.destination / "WS_Example").exists())

    def test_existing_content_and_exclusion_set_drift_fail_before_staging(self):
        """REQ-PRODUCT/SOT/START-001; INV-004/007/013; SCN-003/009."""
        product = self.existing()
        (product / "content.txt").write_text("before", encoding="utf-8")
        (product / ".git").mkdir()
        (product / ".hg").mkdir()
        exclusions = (".git", ".hg")
        preview = self.preview(
            product_mode="existing", existing_product=product, exclude_vcs_paths=exclusions
        )
        with self.assertRaises(new_project.InspectionError):
            self.apply(
                preview,
                product_mode="existing",
                existing_product=product,
                exclude_vcs_paths=(".git",),
            )
        (product / "content.txt").write_text("after", encoding="utf-8")
        with self.assertRaises(new_project.AuthorizationError):
            self.apply(
                preview,
                product_mode="existing",
                existing_product=product,
                exclude_vcs_paths=tuple(reversed(exclusions)),
            )
        self.assertFalse(self.staging_paths())


class AuthorizationAndRecoveryTests(ProjectStartCase):
    """REQ-START-001; INV-001/007/008/013; SCN-001/003/009."""

    def test_exact_digest_pass_and_wrong_digest_has_zero_mutation(self):
        """REQ-START-001; INV-007/008; SCN-001/003."""
        preview = self.preview()
        with self.assertRaises(new_project.AuthorizationError):
            new_project.apply_project(**self.defaults, authorization_sha256="0" * 64)
        self.assertFalse(self.staging_paths())
        self.assertFalse((self.destination / "WS_Example").exists())
        self.assertEqual(self.apply(preview)["state"], "OWNER_PLANNING")

    def test_distribution_or_destination_drift_changes_digest_before_mutation(self):
        """REQ-START/VERSION-001; INV-007/011/013; SCN-003/009."""
        distribution = self.distribution_copy()
        preview = self.preview(source_distribution=distribution)
        (distribution / "README.md").write_text("drift\n", encoding="utf-8")
        with self.assertRaises(new_project.AuthorizationError):
            self.apply(preview, source_distribution=distribution)
        other_destination = self.base / "other-destination"
        other_destination.mkdir()
        stable = self.preview(source_distribution=SOURCE_ROOT)
        with self.assertRaises(new_project.AuthorizationError):
            self.apply(stable, destination_parent=other_destination)
        self.assertFalse(self.staging_paths(other_destination))

    def test_staging_failure_rolls_back_and_preserves_sources(self):
        """REQ-START/BOUNDARY-001; INV-004/007/013; SCN-009."""
        product = self.make_existing_for_failure()
        distribution_before = tree_manifest(SOURCE_ROOT)
        product_before = tree_manifest(product)
        preview = self.preview(product_mode="existing", existing_product=product)
        with mock.patch.object(new_project, "_copy_regular_file", side_effect=PermissionError("denied")):
            with self.assertRaises(new_project.ApplyAborted):
                self.apply(preview, product_mode="existing", existing_product=product)
        self.assertFalse((self.destination / "WS_Example").exists())
        self.assertFalse(self.staging_paths())
        self.assertEqual(tree_manifest(SOURCE_ROOT), distribution_before)
        self.assertEqual(tree_manifest(product), product_before)

    def make_existing_for_failure(self):
        product = self.existing()
        (product / "opaque.txt").write_text("data", encoding="utf-8")
        return product

    def test_staging_representation_failure_has_no_final_target(self):
        """REQ-START/BOUNDARY-001; INV-007/013; SCN-009."""
        preview = self.preview()
        with mock.patch.object(new_project, "_verify_staging_representation", side_effect=new_project.StagingError("representation")):
            with self.assertRaises(new_project.ApplyAborted):
                self.apply(preview)
        self.assertFalse((self.destination / "WS_Example").exists())
        self.assertFalse(self.staging_paths())

    def test_interruption_before_commit_then_matching_apply_rebuilds_safely(self):
        """REQ-START-001; INV-007/008; SCN-009."""
        preview = self.preview()
        with mock.patch.object(new_project, "_materialize_workspace", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.apply(preview)
        staging = self.staging_paths()
        self.assertEqual(len(staging), 1)
        marker = json.loads((staging[0] / new_project.TRANSACTION_MARKER).read_text(encoding="utf-8"))
        self.assertEqual(marker["transaction_state"], "STAGING")
        for field in (
            "preview_schema_version", "authorization_digest", "normalized_inputs",
            "destination_identity", "expected_final_root", "actions_sha256",
        ):
            self.assertIn(field, marker)
        result = self.apply(preview)
        self.assertEqual(result["state"], "OWNER_PLANNING")
        self.assertFalse(self.staging_paths())

    def test_mismatched_digest_or_unknown_state_requires_recovery(self):
        """REQ-START-001; INV-001/007; SCN-009."""
        preview = self.preview()
        with mock.patch.object(new_project, "_materialize_workspace", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.apply(preview)
        changed = self.preview(display_name="Другое имя")
        with self.assertRaises(new_project.RecoveryRequired):
            self.apply(changed, display_name="Другое имя")
        staging = self.staging_paths()[0]
        marker_path = staging / new_project.TRANSACTION_MARKER
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        marker["transaction_state"] = "UNKNOWN"
        marker_path.write_text(json.dumps(marker, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        with self.assertRaises(new_project.RecoveryRequired):
            self.apply(preview)
        self.assertTrue(staging.exists())
        self.assertFalse((self.destination / "WS_Example").exists())

    def test_interruption_after_commit_finalizes_only_matching_target(self):
        """REQ-START-001; INV-007/008/013; SCN-009."""
        preview = self.preview()
        real_finalize = new_project._finalize_committed
        with mock.patch.object(new_project, "_finalize_committed", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.apply(preview)
        target = self.destination / "WS_Example"
        self.assertTrue((target / new_project.TRANSACTION_MARKER).is_file())
        with mock.patch.object(new_project, "_finalize_committed", wraps=real_finalize):
            result = self.apply(preview)
        self.assertEqual(result["state"], "OWNER_PLANNING")
        self.assertFalse((target / new_project.TRANSACTION_MARKER).exists())

    def test_concurrent_commit_collision_never_overwrites_foreign_target(self):
        """REQ-COMP/START-001; INV-001/007/013; SCN-009."""
        preview = self.preview()
        foreign = self.destination / "WS_Example"

        def collision(_staging, _target):
            foreign.mkdir()
            (foreign / "foreign.txt").write_text("preserve", encoding="utf-8")
            raise FileExistsError("concurrent target")

        with mock.patch.object(new_project, "_commit_staging", side_effect=collision):
            with self.assertRaises(new_project.ApplyAborted):
                self.apply(preview)
        self.assertEqual((foreign / "foreign.txt").read_text(encoding="utf-8"), "preserve")

    def test_repeat_after_success_and_unexpected_target_content_fail_closed(self):
        """REQ-COMP/START-001; INV-001/007; SCN-009."""
        preview = self.preview()
        root = Path(self.apply(preview)["target_workspace"])
        before = tree_manifest(root)
        with self.assertRaises(new_project.InspectionError):
            self.apply(preview)
        self.assertEqual(tree_manifest(root), before)
        (root / "unexpected").write_text("foreign", encoding="utf-8")
        with self.assertRaises(new_project.InspectionError):
            self.apply(preview)
        self.assertTrue((root / "unexpected").is_file())


class CliTests(ProjectStartCase):
    """REQ-START/PART/NATIVE/SOT-001; INV-005/007/012; SCN-003/006/008/009."""

    def cli(self, operation, *extra):
        args = [
            sys.executable,
            "-B",
            str(TOOL_PATH),
            operation,
            "--source-distribution", str(SOURCE_ROOT),
            "--destination-parent", str(self.destination),
            "--slug", "Example",
            "--display-name", "Example Product",
            "--wroad", "Create an example product.",
            "--product", "new",
            *map(str, extra),
        ]
        return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    def test_public_operations_are_only_preview_and_apply(self):
        """REQ-START-001; INV-007; SCN-003/009."""
        help_result = subprocess.run(
            [sys.executable, "-B", str(TOOL_PATH), "--help"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("preview", help_result.stdout)
        self.assertIn("apply", help_result.stdout)
        for forbidden in ("recover", "run-product-checks", "product-parts", "product-native-checks", "sot-mode", "github"):
            self.assertNotIn(forbidden, help_result.stdout.lower())
        rejected = self.cli("recover")
        self.assertEqual(rejected.returncode, 2)
        self.assertFalse(self.staging_paths())

    def test_cli_preview_apply_and_authorization_validation(self):
        """REQ-START-001; INV-007/008; SCN-001/003."""
        preview_result = self.cli("preview")
        self.assertEqual(preview_result.returncode, 0, preview_result.stderr)
        preview = json.loads(preview_result.stdout)
        self.assertEqual(preview["state"], "PREVIEW_READY")
        missing = self.cli("apply")
        self.assertEqual(missing.returncode, 2)
        invalid = self.cli("apply", "--authorization-sha256", "not-a-digest")
        self.assertEqual(invalid.returncode, 2)
        self.assertFalse(self.staging_paths())
        success = self.cli("apply", "--authorization-sha256", preview["preview_sha256"])
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertEqual(json.loads(success.stdout)["state"], "OWNER_PLANNING")


if __name__ == "__main__":
    unittest.main(verbosity=2)

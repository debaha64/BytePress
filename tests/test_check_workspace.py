"""REQ-CHECK/COMP/SOT/BOUNDARY; INV-001/010/015; SCN-001/005/007.

Tests-first contracts for the generic Workspace checker.  Every fixture is
neutral, self-created and non-authoritative.
"""

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
CHECKER_SOURCE = SOURCE_ROOT / "tools" / "check_workspace.py"
PARSER_SOURCE = SOURCE_ROOT / "tools" / "project_profile.py"
SDLC_SOURCE = SOURCE_ROOT / "docs" / "technical" / "sdlc.md"
PHASE_GATES_SOURCE = SOURCE_ROOT / "docs" / "technical" / "phase-gates.md"


class WorkspaceCheckerTests(unittest.TestCase):
    maxDiff = None

    def test_documentation_impact_required_only_for_semantic_classes(self):
        for kind in ('S1', 'S2'):
            with self.subTest(kind=kind):
                root = self.fixture(active=True)
                plan = root / 'plans/active/WPLAN-000001-example.md'
                original = plan.read_text() + f'\nКласс изменения: {kind}\n'
                plan.write_text(original)
                self.assert_fail(self.run_checker(root), 'documentation-impact')
                for block in ('', 'Disposition: affected\nOwners: docs/technical/sdlc.md\nReason: ',
                              'Disposition: maybe\nOwners: docs/technical/sdlc.md\nReason: test',
                              'Disposition: affected\nOwners: ../escape.md\nReason: test'):
                    plan.write_text(original + '\n## Documentation Impact\n\n' + block + '\n')
                    self.assert_fail(self.run_checker(root), 'documentation-impact')
                for disposition in ('affected', 'not affected'):
                    plan.write_text(original + '\n## Documentation Impact\n\nDisposition: ' + disposition
                                    + '\nOwners: docs/technical/sdlc.md\nReason: Проверены затронутые границы.\n')
                    self.assert_pass(self.run_checker(root))
        root = self.fixture(active=True)
        plan = root / 'plans/active/WPLAN-000001-example.md'
        plan.write_text(plan.read_text() + '\nКласс изменения: S0\n')
        self.assert_pass(self.run_checker(root))

    def test_unrelated_historical_decision_block_cannot_poison_current_authority(self):
        root = self.fixture(active=True)
        path = root / 'logs/decisions.md'
        path.write_text(path.read_text() + '\nRECORD_TYPE: owner_decision\nRECORD_ID: OD-000099\n'
                        'WPLAN_ID: WPLAN-000099\n\n## Historical closeout\nWPLAN_ID: WPLAN-000099\n')
        self.assert_pass(self.run_checker(root))
        path.write_text(path.read_text().replace('RECORD_ID: OD-000001\n', 'RECORD_ID: OD-000001\nWPLAN_ID: WPLAN-000001\n', 1))
        self.assert_fail(self.run_checker(root), 'sdlc-transition')

    def test_documentation_move_requires_live_consumer_closure_without_stub(self):
        root = self.fixture()
        old = root / 'docs/old.md'; new = root / 'docs/new.md'
        old.write_text('# Контракт\n')
        consumer = root / 'research/accepted.md'
        before = '# Принятый факт\n\nОбъект: [старый документ](../docs/old.md). Вывод сохранён.\n'
        consumer.write_text(before)
        self.assert_pass(self.run_checker(root))
        old.rename(new)
        self.assert_fail(self.run_checker(root), 'markdown-links')
        after = before.replace('(../docs/old.md)', '(../docs/new.md)')
        consumer.write_text(after)
        self.assertEqual(after.replace('(../docs/new.md)', '(../docs/old.md)'), before)
        self.assert_pass(self.run_checker(root))
        self.assertFalse(old.exists())
        # A split preserves the source label without inventing a single successor.
        consumer.write_text(before.replace('[старый документ](../docs/old.md)', '`docs/old.md`'))
        self.assert_pass(self.run_checker(root))


    def test_final_profile_rejects_every_legacy_sot_machine_projection(self):
        """REQ-SOT-001; SCN-014: one Profile owner, no compatibility projection."""
        for field in ("SOT_MODE: sot_files", "SOT_MODE = sot_files", "SOT_MODE: sot_git"):
            with self.subTest(field=field):
                root = self.fixture()
                (root / "AGENTS.md").write_text(field + "\n", encoding="utf-8")
                self.assert_fail(self.run_checker(root), "workspace-sot")

    def fixture(self, *, active=False, profile=None):
        temporary = tempfile.TemporaryDirectory(prefix="bytepress-check-workspace-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "WS_Example"
        for relative in (
            "Example", "docs", "logs", "research", "roles", "skills", "sops",
            "templates", "tests", "tools", "plans/active", "plans/completed",
        ):
            (root / relative).mkdir(parents=True, exist_ok=True)
        (root / "docs/technical").mkdir()
        shutil.copy2(PARSER_SOURCE, root / "tools/project_profile.py")
        shutil.copy2(CHECKER_SOURCE, root / "tools/check_workspace.py")
        sdlc_table = "\n".join(
            line for line in SDLC_SOURCE.read_text(encoding="utf-8").splitlines()
            if line.startswith("|")
        ) + "\n"
        (root / "docs/technical/sdlc.md").write_text(sdlc_table, encoding="utf-8")
        phase_gate_table = "\n".join(
            line for line in PHASE_GATES_SOURCE.read_text(encoding="utf-8").splitlines()
            if line.startswith("|")
        ) + "\n"
        (root / "docs/technical/phase-gates.md").write_text(phase_gate_table, encoding="utf-8")
        for relative in re.findall(r"\(\.\./\.\./(roles/[^)]+)\)", sdlc_table):
            (root / relative).write_text("# Neutral role fixture\n", encoding="utf-8")
        document = profile or {
            "schema_version": 1,
            "harness_version": "0.5.2",
            "sot_mode": "sot_files",
            "display_name": "Example",
        }
        (root / "Example.profile").write_text(
            json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (root / "AGENTS.md").write_text("# Agent map\n", encoding="utf-8")
        (root / "SYSTEM.md").write_text("# System\n", encoding="utf-8")
        (root / "logs/decisions.md").write_text(
            "RELEASE_AUTHORIZATION_FIXTURE: authorized\nWPLAN_ID: WPLAN-000001\n\n"
            "RECORD_TYPE: owner_decision\nRECORD_ID: OD-000001\nWPLAN_ID: WPLAN-000001\n"
            "DECISION_KIND: implementation\nDECISION_VALUE: approved\nEVIDENCE_REF: IE-000001\n"
            "ROUTE_REF: WBACK-000001\nSTATUS: active\n\n"
            "RECORD_TYPE: owner_decision\nRECORD_ID: OD-000002\nWPLAN_ID: WPLAN-000001\n"
            "DECISION_KIND: decommissioning_authorization\nDECISION_VALUE: approved\n"
            "EVIDENCE_REF: IE-000001\nROUTE_REF: WBACK-000001\nSTATUS: active\n\n"
            "RECORD_TYPE: owner_decision\nRECORD_ID: OD-000003\nWPLAN_ID: WPLAN-000001\n"
            "DECISION_KIND: retirement_authorization\nDECISION_VALUE: approved\n"
            "EVIDENCE_REF: IE-000001\nROUTE_REF: WBACK-000001\nSTATUS: active\n\n"
            "RECORD_TYPE: product_acceptance\nRECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000001\n"
            "DECISION_VALUE: accepted\n",
            encoding="utf-8",
        )
        (root / "logs/sessions.md").write_text("# Sessions\n", encoding="utf-8")
        (root / "logs/quality.md").write_text("# Quality\n", encoding="utf-8")
        (root / "research/00-index.md").write_text(
            "# Исследования\n\nСледующий research ID: `01`.\n", encoding="utf-8"
        )
        (root / "plans/roadmap.md").write_text(
            "| ID | Статус |\n|---|---|\n| WROAD-000001 | active |\n", encoding="utf-8"
        )
        if active:
            (root / "plans/backlog.md").write_text(
                "WROAD-000001 active\nWBACK-000001 active\nactive WPLAN count 1\n"
                "CHECKPOINT: `WBACK-000001-WORK-IN-PROGRESS`.\n",
                encoding="utf-8",
            )
            (root / "plans/active/WPLAN-000001-example.md").write_text(
                "# WPLAN\nСтатус: active\nWPLAN ID: WPLAN-000001\n"
                "WROAD: WROAD-000001\nWBACK: WBACK-000001\n"
                "Фаза SDLC: implementation\n"
                "INTERVIEW_EVIDENCE_REF: IE-000001\n"
                "OWNER_DECISION_REFS: OD-000001\n"
                "ALLOWED_SURFACES: tests/transition-evidence.md,logs/sessions.md\n"
                "Текущая контрольная отметка: WBACK-000001-WORK-IN-PROGRESS\n"
                "SDLC_TRANSITION: v1\n"
                "TRANSITION_STATE: in-progress\n"
                "FROM_PHASE: implementation\n"
                "FROM_ROLE: roles/11-developer.md\n"
                "PHASE_COMPLETION: pending\n"
                "EVIDENCE_KIND: implementation-red-green-delta\n"
                "EVIDENCE_REFS: none\n"
                "TRANSITION_CHECKPOINT: WBACK-000001-WORK-IN-PROGRESS\n"
                "HANDOFF_REF: none\n"
                "TO_PHASE: verification\n"
                "TO_ROLE: roles/12-verification-engineer.md\n"
                "FROM_ROLE_AUTHORITY: active\n"
                "TO_ROLE_AUTHORITY: withheld\n"
                "AUTHORITY_REF: OD-000001\n"
                "OWNER_GATE: none\n"
                "OWNER_GATE_STATUS: not-applicable\n"
                "OWNER_GATE_REF: none\n"
                "VERIFICATION_STATUS: pending\n"
                "VERIFICATION_REF: none\n"
                "VALIDATION_STATUS: not-performed\n"
                "VALIDATION_REF: none\n"
                "PRODUCT_ACCEPTANCE_STATUS: not-performed\n"
                "PRODUCT_ACCEPTANCE_REF: none\n"
                "RELEASE_AUTHORIZATION_STATUS: not-performed\n"
                "RELEASE_AUTHORIZATION_REF: none\n",
                encoding="utf-8",
            )
        else:
            (root / "plans/backlog.md").write_text(
                "WROAD-000001 active\nactive WBACK count 0\nactive WPLAN count 0\n"
                "NON_EXECUTING_CHECKPOINT: `WROAD-000001-OWNER-PLANNING`.\n",
                encoding="utf-8",
            )
        return root

    def complete_transition(self, root):
        plan = root / "plans/active/WPLAN-000001-example.md"
        (root / "tests/transition-evidence.md").write_text(
            "EVIDENCE_ID: EVIDENCE-FIXTURE\nWPLAN_ID: WPLAN-000001\n"
            "EVIDENCE_KIND: implementation-red-green-delta\n",
            encoding="utf-8",
        )
        with (root / "logs/sessions.md").open("a", encoding="utf-8") as stream:
            stream.write("\nHANDOFF-FIXTURE\n")
        text = plan.read_text(encoding="utf-8")
        replacements = {
            "Фаза SDLC: implementation": "Фаза SDLC: verification",
            "TRANSITION_STATE: in-progress": "TRANSITION_STATE: complete",
            "PHASE_COMPLETION: pending": "PHASE_COMPLETION: complete",
            "EVIDENCE_REFS: none": "EVIDENCE_REFS: tests/transition-evidence.md#EVIDENCE-FIXTURE",
            "HANDOFF_REF: none": "HANDOFF_REF: logs/sessions.md#HANDOFF-FIXTURE",
            "FROM_ROLE_AUTHORITY: active": "FROM_ROLE_AUTHORITY: relinquished",
            "TO_ROLE_AUTHORITY: withheld": "TO_ROLE_AUTHORITY: granted",
        }
        for old, new in replacements.items():
            self.assertIn(old, text)
            text = text.replace(old, new, 1)
        plan.write_text(text, encoding="utf-8")
        return plan

    def phase_gate_rows(self, root):
        pattern = re.compile(
            r"^\| `([a-z][a-z-]*)` \| `([a-z][a-z-]*)` \| `([a-z][a-z0-9-]*)` \| "
            r"`(none|owner-open|owner-decision)` \| "
            r"`(none|implementation|product_acceptance|release_authorization|decommissioning_authorization|retirement_authorization)` \|$"
        )
        return [
            match.groups()
            for line in (root / "docs/technical/phase-gates.md").read_text(encoding="utf-8").splitlines()
            if (match := pattern.fullmatch(line))
        ]

    def materialize_transition(self, root, row, supplied_kind=None):
        source, target, evidence_kind, policy, required_kind = row
        supplied_kind = supplied_kind or required_kind
        plan = root / "plans/active/WPLAN-000001-example.md"
        plan_text = plan.read_text(encoding="utf-8")
        sdlc = (root / "docs/technical/sdlc.md").read_text(encoding="utf-8")
        roles = {
            phase: role
            for phase, role in re.findall(
                r"^\| `?\d{2}`? \| [^|]+ \| `([a-z][a-z-]*)` \| [^|]+ \| \[[^]]+\]\(\.\./\.\./(roles/[^)]+)\) \|$",
                sdlc,
                re.MULTILINE,
            )
        }

        def set_field(document, label, value):
            document, count = re.subn(
                rf"(?m)^{re.escape(label)}\s*:.*$", f"{label}: {value}", document
            )
            self.assertEqual(count, 1, label)
            return document

        fields = {
            "Фаза SDLC": target,
            "TRANSITION_STATE": "complete",
            "FROM_PHASE": source,
            "FROM_ROLE": roles[source],
            "PHASE_COMPLETION": "complete",
            "EVIDENCE_KIND": evidence_kind,
            "EVIDENCE_REFS": "tests/transition-evidence.md#EVIDENCE-FIXTURE",
            "HANDOFF_REF": "logs/sessions.md#HANDOFF-FIXTURE",
            "TO_PHASE": target,
            "TO_ROLE": roles.get(target, "none"),
            "FROM_ROLE_AUTHORITY": "relinquished",
            "TO_ROLE_AUTHORITY": "not-applicable" if target == "retired" else "granted",
            "OWNER_GATE": "none",
            "OWNER_GATE_STATUS": "not-applicable",
            "OWNER_GATE_REF": "none",
            "PRODUCT_ACCEPTANCE_STATUS": "not-performed",
            "PRODUCT_ACCEPTANCE_REF": "none",
            "RELEASE_AUTHORIZATION_STATUS": "not-performed",
            "RELEASE_AUTHORIZATION_REF": "none",
            "OWNER_DECISION_REFS": "OD-000001",
        }
        if policy == "owner-open":
            fields.update({
                "OWNER_GATE": "GATE-OWNER-WPLAN-000001-PENDING",
                "OWNER_GATE_STATUS": "pending",
            })
        elif policy == "owner-decision":
            records = {
                "implementation": ("IMPLEMENTATION-AUTHORIZATION", "OD-000001"),
                "product_acceptance": ("PRODUCT-ACCEPTANCE", "PA-000001"),
                "release_authorization": (
                    "RELEASE-AUTHORIZATION", "logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE",
                ),
                "decommissioning_authorization": ("DECOMMISSIONING-AUTHORIZATION", "OD-000002"),
                "retirement_authorization": ("RETIREMENT-AUTHORIZATION", "OD-000003"),
            }
            marker, reference = records[supplied_kind]
            fields.update({
                "OWNER_GATE": f"GATE-OWNER-WPLAN-000001-{marker}",
                "OWNER_GATE_STATUS": "satisfied",
                "OWNER_GATE_REF": reference,
            })
            if reference.startswith("OD-"):
                fields["OWNER_DECISION_REFS"] = "OD-000001" if reference == "OD-000001" else f"OD-000001,{reference}"
            if supplied_kind == "product_acceptance":
                fields.update({
                    "PRODUCT_ACCEPTANCE_STATUS": "accepted",
                    "PRODUCT_ACCEPTANCE_REF": reference,
                })
            if supplied_kind == "release_authorization":
                fields.update({
                    "RELEASE_AUTHORIZATION_STATUS": "authorized",
                    "RELEASE_AUTHORIZATION_REF": reference,
                })
        for label, value in fields.items():
            plan_text = set_field(plan_text, label, value)
        (root / "tests/transition-evidence.md").write_text(
            "EVIDENCE_ID: EVIDENCE-FIXTURE\nWPLAN_ID: WPLAN-000001\n"
            f"EVIDENCE_KIND: {evidence_kind}\n",
            encoding="utf-8",
        )
        with (root / "logs/sessions.md").open("a", encoding="utf-8") as stream:
            stream.write("\nHANDOFF-FIXTURE\n")
        plan.write_text(plan_text, encoding="utf-8")
        return plan

    def write_baseline_manifest(self, root):
        rows = ["manifest\t1\tcomplete\t.\n"]
        for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix().encode("utf-8")):
            relative = path.relative_to(root).as_posix()
            info = path.lstat()
            mode = stat.S_IMODE(info.st_mode)
            if stat.S_ISDIR(info.st_mode):
                rows.append(f"d\t{mode:04o}\t-\t{relative}\n")
            elif stat.S_ISREG(info.st_mode):
                rows.append(f"f\t{mode:04o}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\t{relative}\n")
            else:
                self.fail(f"unexpected fixture type: {relative}")
        manifest = root.parent / "baseline.tsv"
        manifest.write_text("".join(rows), encoding="utf-8")
        return manifest

    def run_checker(self, root, *extra, env=None):
        completed = subprocess.run(
            [sys.executable, "-B", str(root / "tools/check_workspace.py"),
             "--workspace", str(root), "--format", "json", *map(str, extra)],
            cwd=root,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            self.fail(f"invalid JSON ({completed.returncode}):\n{completed.stdout}\n{completed.stderr}")
        return completed, payload

    def assert_pass(self, result):
        completed, payload = result
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["fail_count"], 0)
        self.assertEqual(payload["warn_count"], 0)

    def assert_fail(self, result, check_id=None):
        completed, payload = result
        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        self.assertEqual(payload["status"], "FAIL")
        if check_id:
            self.assertIn(check_id, {item["id"] for item in payload["checks"] if item["status"] == "FAIL"})

    def test_minimal_wroad_only_and_absent_archives_pass(self):
        root = self.fixture()
        before = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
        completed, payload = self.run_checker(root)
        self.assert_pass((completed, payload))
        self.assertEqual(payload["archive_state"], "ABSENT")
        self.assertEqual(payload["preservation"], "NOT_REQUESTED")
        self.assertFalse((root / "research/archives").exists())
        self.assertEqual(before, sorted(p.relative_to(root).as_posix() for p in root.rglob("*")))

    def test_partial_archive_lifecycle_fails(self):
        variants = ("directory", "catalog", "manifest-only", "empty")
        for variant in variants:
            with self.subTest(variant=variant):
                root = self.fixture()
                if variant in {"directory", "manifest-only", "empty"}:
                    (root / "research/archives").mkdir()
                if variant == "catalog":
                    with (root / "research/00-index.md").open("a", encoding="utf-8") as stream:
                        stream.write("\n## Архивы\n\n1. `research/archives/01_one.zip`.\n")
                if variant == "manifest-only":
                    (root / "research/archives/MANIFEST.sha256").write_text("", encoding="utf-8")
                self.assert_fail(self.run_checker(root), "research-archives")

    def test_complete_archive_lifecycle_passes_without_fixed_count(self):
        root = self.fixture()
        archives = root / "research/archives"
        archives.mkdir()
        payload = archives / "07_fact.zip"
        payload.write_bytes(b"neutral archive bytes")
        digest = hashlib.sha256(payload.read_bytes()).hexdigest()
        (archives / "MANIFEST.sha256").write_text(
            f"{digest}  research/archives/{payload.name}\n", encoding="utf-8"
        )
        (archives / "README.md").write_text(
            f"# Архивы\n\n1. `{payload.name}`.\n", encoding="utf-8"
        )
        index = root / "research/00-index.md"
        index.write_text(
            index.read_text(encoding="utf-8").replace("`01`", "`08`"), encoding="utf-8"
        )
        with index.open("a", encoding="utf-8") as stream:
            stream.write(f"\n## Архивы\n\n1. `research/archives/{payload.name}`.\n")
        self.assert_pass(self.run_checker(root))

        # A prose citation is history, not a second inventory declaration.
        with (archives / "README.md").open("a", encoding="utf-8") as stream:
            stream.write(f"\n## History\n\nOriginal evidence is inside `{payload.name}`.\n")
        self.assert_pass(self.run_checker(root))
        with (archives / "README.md").open("a", encoding="utf-8") as stream:
            stream.write(f"\n2. `{payload.name}`.\n")
        self.assert_fail(self.run_checker(root), "research-archives")

    def test_markdown_heading_anchors_preserve_literal_underscores(self):
        """REQ-CHECK/BOUNDARY; SCN-014: preserve valid immutable history links."""
        root = self.fixture()
        (root / "logs/history.md").write_text(
            "## RELEASE_EVIDENCE_ACCEPTANCE\n\n"
            "## 2026-09-05 — candidate `_28`\n\n"
            "[decision](#release_evidence_acceptance)\n"
            "[candidate](#2026-09-05--candidate-_28)\n",
            encoding="utf-8",
        )
        self.assert_pass(self.run_checker(root))
        with (root / "logs/history.md").open("a", encoding="utf-8") as stream:
            stream.write("[missing](#releaseevidenceacceptance)\n")
        self.assert_fail(self.run_checker(root), "markdown-links")

    def test_research_next_id_is_monotonic(self):
        """REQ-CHECK-W-008: the next research ID cannot collide with a live domain."""
        root = self.fixture()
        (root / "research/01_neutral_domain").mkdir()
        self.assert_fail(self.run_checker(root), "research-registry")
        (root / "research/00-index.md").write_text(
            "# Исследования\n\nСледующий research ID: `02`.\n", encoding="utf-8"
        )
        self.assert_pass(self.run_checker(root))

    def test_active_wplan_consistency_and_checkpoint(self):
        root = self.fixture(active=True)
        self.assert_pass(self.run_checker(root))
        backlog = root / "plans/backlog.md"
        backlog.write_text(backlog.read_text(encoding="utf-8").replace("WORK-IN-PROGRESS", "OTHER"), encoding="utf-8")
        self.assert_fail(self.run_checker(root), "checkpoint")

    def test_completed_transition_requires_evidence_checkpoint_handoff_and_authority(self):
        """REQ-SDLC-TRANSITION/EVIDENCE-001; INV-SDLC-002/003/004."""
        root = self.fixture(active=True)
        plan = self.complete_transition(root)
        self.assert_pass(self.run_checker(root))

        cases = {
            "missing-evidence": ("EVIDENCE_REFS: tests/transition-evidence.md#EVIDENCE-FIXTURE", "EVIDENCE_REFS: none"),
            "skipped-checkpoint": ("TRANSITION_CHECKPOINT: WBACK-000001-WORK-IN-PROGRESS", "TRANSITION_CHECKPOINT: WBACK-000001-SKIPPED"),
            "missing-handoff": ("HANDOFF_REF: logs/sessions.md#HANDOFF-FIXTURE", "HANDOFF_REF: none"),
            "retained-prior-authority": ("FROM_ROLE_AUTHORITY: relinquished", "FROM_ROLE_AUTHORITY: active"),
        }
        valid = plan.read_text(encoding="utf-8")
        for name, (old, new) in cases.items():
            with self.subTest(name=name):
                plan.write_text(valid.replace(old, new, 1), encoding="utf-8")
                self.assert_fail(self.run_checker(root), "sdlc-transition")
        plan.write_text(valid, encoding="utf-8")

    def test_wrong_evidence_kind_is_rejected(self):
        """Corrective RED A: an arbitrary existing token is not transition evidence."""
        root = self.fixture(active=True)
        plan = self.complete_transition(root)
        (root / "tests/arbitrary.md").write_text("BANANA\n", encoding="utf-8")
        valid = plan.read_text(encoding="utf-8")
        plan.write_text(
            valid.replace(
                "EVIDENCE_REFS: tests/transition-evidence.md#EVIDENCE-FIXTURE",
                "EVIDENCE_REFS: tests/arbitrary.md#BANANA",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_wrong_authority_scope_is_rejected(self):
        """Corrective RED B: release authorization is not implementation authority."""
        root = self.fixture(active=True)
        plan = self.complete_transition(root)
        valid = plan.read_text(encoding="utf-8")
        plan.write_text(
            valid.replace("AUTHORITY_REF: OD-000001", "AUTHORITY_REF: logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE", 1),
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_wrong_owner_gate_decision_is_rejected(self):
        """Corrective RED C: release authorization is not implementation acceptance."""
        root = self.fixture(active=True)
        plan = self.complete_transition(root)
        valid = plan.read_text(encoding="utf-8")
        owner_review = valid
        replacements = {
            "FROM_PHASE: implementation": "FROM_PHASE: verification",
            "FROM_ROLE: roles/11-developer.md": "FROM_ROLE: roles/12-verification-engineer.md",
            "TO_PHASE: verification": "TO_PHASE: owner-review",
            "TO_ROLE: roles/12-verification-engineer.md": "TO_ROLE: roles/13-review-coordinator.md",
            "Фаза SDLC: verification": "Фаза SDLC: owner-review",
            "OWNER_GATE: none": "OWNER_GATE: GATE-OWNER-FIXTURE-IMPLEMENTATION-ACCEPTANCE",
            "OWNER_GATE_STATUS: not-applicable": "OWNER_GATE_STATUS: satisfied",
            "OWNER_GATE_REF: none": "OWNER_GATE_REF: logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE",
        }
        for old, new in replacements.items():
            owner_review = owner_review.replace(old, new, 1)
        owner_review = owner_review.replace(
            "EVIDENCE_KIND: implementation-red-green-delta",
            "EVIDENCE_KIND: technical-verdict-and-traceability",
            1,
        )
        evidence = root / "tests/transition-evidence.md"
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace(
                "EVIDENCE_KIND: implementation-red-green-delta",
                "EVIDENCE_KIND: technical-verdict-and-traceability",
                1,
            ),
            encoding="utf-8",
        )
        plan.write_text(owner_review, encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_implementation_decision_cannot_authorize_decommissioning_start(self):
        """Lifecycle RED A: the transition contract must require decommissioning_authorization."""
        root = self.fixture(active=True)
        plan = self.complete_transition(root)
        transition = plan.read_text(encoding="utf-8")
        replacements = {
            "Фаза SDLC: verification": "Фаза SDLC: decommissioning",
            "FROM_PHASE: implementation": "FROM_PHASE: retrospective",
            "FROM_ROLE: roles/11-developer.md": "FROM_ROLE: roles/20-retrospective-facilitator.md",
            "TO_PHASE: verification": "TO_PHASE: decommissioning",
            "TO_ROLE: roles/12-verification-engineer.md": "TO_ROLE: roles/21-decommissioning-engineer.md",
            "EVIDENCE_KIND: implementation-red-green-delta": "EVIDENCE_KIND: retrospective-and-decommission-authorization",
            "OWNER_GATE: none": "OWNER_GATE: GATE-OWNER-WPLAN-000001-IMPLEMENTATION-AUTHORIZATION",
            "OWNER_GATE_STATUS: not-applicable": "OWNER_GATE_STATUS: satisfied",
            "OWNER_GATE_REF: none": "OWNER_GATE_REF: OD-000001",
        }
        for old, new in replacements.items():
            transition = transition.replace(old, new, 1)
        evidence = root / "tests/transition-evidence.md"
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace(
                "EVIDENCE_KIND: implementation-red-green-delta",
                "EVIDENCE_KIND: retrospective-and-decommission-authorization",
                1,
            ),
            encoding="utf-8",
        )
        plan.write_text(transition, encoding="utf-8")
        completed, payload = self.run_checker(root)
        self.assert_fail((completed, payload), "sdlc-transition")
        self.assertIn(
            "required decision kind = decommissioning_authorization",
            next(item["message"] for item in payload["checks"] if item["id"] == "sdlc-transition"),
        )

    def test_product_acceptance_cannot_authorize_retirement(self):
        """Lifecycle RED B: the transition contract must require retirement_authorization."""
        root = self.fixture(active=True)
        plan = self.complete_transition(root)
        transition = plan.read_text(encoding="utf-8")
        replacements = {
            "Фаза SDLC: verification": "Фаза SDLC: retired",
            "FROM_PHASE: implementation": "FROM_PHASE: decommissioning",
            "FROM_ROLE: roles/11-developer.md": "FROM_ROLE: roles/21-decommissioning-engineer.md",
            "TO_PHASE: verification": "TO_PHASE: retired",
            "TO_ROLE: roles/12-verification-engineer.md": "TO_ROLE: none",
            "TO_ROLE_AUTHORITY: granted": "TO_ROLE_AUTHORITY: not-applicable",
            "EVIDENCE_KIND: implementation-red-green-delta": "EVIDENCE_KIND: decommissioning-evidence",
            "OWNER_GATE: none": "OWNER_GATE: GATE-OWNER-WPLAN-000001-PRODUCT-ACCEPTANCE",
            "OWNER_GATE_STATUS: not-applicable": "OWNER_GATE_STATUS: satisfied",
            "OWNER_GATE_REF: none": "OWNER_GATE_REF: PA-000001",
            "PRODUCT_ACCEPTANCE_STATUS: not-performed": "PRODUCT_ACCEPTANCE_STATUS: accepted",
            "PRODUCT_ACCEPTANCE_REF: none": "PRODUCT_ACCEPTANCE_REF: PA-000001",
        }
        for old, new in replacements.items():
            transition = transition.replace(old, new, 1)
        evidence = root / "tests/transition-evidence.md"
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace(
                "EVIDENCE_KIND: implementation-red-green-delta", "EVIDENCE_KIND: decommissioning-evidence", 1
            ),
            encoding="utf-8",
        )
        plan.write_text(transition, encoding="utf-8")
        completed, payload = self.run_checker(root)
        self.assert_fail((completed, payload), "sdlc-transition")
        self.assertIn(
            "required decision kind = retirement_authorization",
            next(item["message"] for item in payload["checks"] if item["id"] == "sdlc-transition"),
        )

    def test_all_21_transition_rows_and_exact_decision_kinds(self):
        canonical = self.fixture(active=True)
        rows = self.phase_gate_rows(canonical)
        self.assertEqual(len(rows), 21)
        self.assertEqual(len({(source, target) for source, target, *_rest in rows}), 21)
        self.assertEqual(sum(policy == "owner-decision" for *_prefix, policy, _kind in rows), 5)
        self.assertEqual(sum(policy == "owner-open" for *_prefix, policy, _kind in rows), 3)
        for row in rows:
            with self.subTest(transition=row[:2]):
                root = self.fixture(active=True)
                self.materialize_transition(root, row)
                self.assert_pass(self.run_checker(root))

    def test_product_acceptance_phase_opens_without_pa(self):
        """Entering product-acceptance is owner-open and does not require PA."""
        entry = (
            "owner-review", "product-acceptance", "owner-review-decision",
            "owner-open", "none",
        )
        root = self.fixture(active=True)
        self.materialize_transition(root, entry)
        self.assert_pass(self.run_checker(root))

    def later_product_acceptance_fixture(self, *, acceptance_gate=False):
        """A later WPLAN consumes an unchanged PA from WPLAN-000001."""
        root = self.fixture(active=True)
        plan = root / "plans/active/WPLAN-000001-example.md"
        if acceptance_gate:
            self.materialize_transition(root, (
                "product-acceptance", "release-readiness", "product-acceptance-decision",
                "owner-decision", "product_acceptance",
            ))
        else:
            text = plan.read_text(encoding="utf-8")
            for old, new in (
                ("Фаза SDLC: implementation", "Фаза SDLC: release-readiness"),
                ("FROM_PHASE: implementation", "FROM_PHASE: release-readiness"),
                ("FROM_ROLE: roles/11-developer.md", "FROM_ROLE: roles/15-release-readiness-reviewer.md"),
                ("TO_PHASE: verification", "TO_PHASE: release"),
                ("TO_ROLE: roles/12-verification-engineer.md", "TO_ROLE: roles/16-release-engineer.md"),
                ("EVIDENCE_KIND: implementation-red-green-delta", "EVIDENCE_KIND: release-readiness-evidence"),
                ("OWNER_GATE: none", "OWNER_GATE: GATE-OWNER-RELEASE-AUTHORIZATION"),
                ("OWNER_GATE_STATUS: not-applicable", "OWNER_GATE_STATUS: pending"),
                ("PRODUCT_ACCEPTANCE_STATUS: not-performed", "PRODUCT_ACCEPTANCE_STATUS: accepted"),
                ("PRODUCT_ACCEPTANCE_REF: none", "PRODUCT_ACCEPTANCE_REF: PA-000001"),
            ):
                self.assertIn(old, text)
                text = text.replace(old, new, 1)
            plan.write_text(text, encoding="utf-8")
        for path in (plan, root / "tests/transition-evidence.md"):
            if path.exists():
                path.write_text(path.read_text(encoding="utf-8").replace("WPLAN-000001", "WPLAN-000002"), encoding="utf-8")
        decisions = root / "logs/decisions.md"
        before, pa = decisions.read_text(encoding="utf-8").split("RECORD_TYPE: product_acceptance", 1)
        decisions.write_text(before.replace("WPLAN-000001", "WPLAN-000002") + "RECORD_TYPE: product_acceptance" + pa, encoding="utf-8")
        later_plan = plan.with_name("WPLAN-000002-example.md")
        plan.rename(later_plan)
        return root, later_plan

    def test_durable_product_acceptance_in_later_release_wplan(self):
        root, plan = self.later_product_acceptance_fixture()
        decisions = (root / "logs/decisions.md").read_bytes()
        self.assert_pass(self.run_checker(root))
        self.assertEqual((root / "logs/decisions.md").read_bytes(), decisions)
        self.assertIn("RECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000001", decisions.decode())
        self.assertIn("WPLAN ID: WPLAN-000002", plan.read_text())
        self.assertIn("RELEASE_AUTHORIZATION_STATUS: not-performed", plan.read_text())

    def test_later_product_acceptance_gate_still_requires_its_own_pa(self):
        root, _ = self.later_product_acceptance_fixture(acceptance_gate=True)
        result = self.run_checker(root)
        self.assert_fail(result, "sdlc-transition")
        self.assertIn("product acceptance WPLAN_ID mismatch", result[0].stdout)
        decisions = root / "logs/decisions.md"
        decisions.write_text(decisions.read_text().replace(
            "RECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000001",
            "RECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000002", 1,
        ))
        self.assert_pass(self.run_checker(root))

    def test_durable_product_acceptance_rejects_invalid_records_and_projections(self):
        root, plan = self.later_product_acceptance_fixture()
        decisions = root / "logs/decisions.md"
        valid_plan = plan.read_text()
        valid_decisions = decisions.read_text()
        before, pa = valid_decisions.split("RECORD_TYPE: product_acceptance", 1)
        pa = "RECORD_TYPE: product_acceptance" + pa
        variants = {
            "missing-record": (before, valid_plan),
            "wrong-type": (before + pa.replace("product_acceptance", "owner_decision", 1), valid_plan),
            "wrong-id": (before + pa.replace("PA-000001", "PA-000099", 1), valid_plan),
            "pending": (before + pa.replace("accepted", "pending", 1), valid_plan),
            "rejected": (before + pa.replace("accepted", "rejected", 1), valid_plan),
            "missing-provenance": (before + pa.replace("WPLAN_ID: WPLAN-000001\n", "", 1), valid_plan),
            "malformed-provenance": (before + pa.replace("WPLAN_ID: WPLAN-000001", "WPLAN_ID: other", 1), valid_plan),
            "duplicate-record": (valid_decisions + "\n" + pa, valid_plan),
            "duplicate-field": (before + pa.replace("DECISION_VALUE: accepted", "DECISION_VALUE: accepted\nDECISION_VALUE: accepted", 1), valid_plan),
            "malformed-reference": (valid_decisions, valid_plan.replace("PRODUCT_ACCEPTANCE_REF: PA-000001", "PRODUCT_ACCEPTANCE_REF: PA-1", 1)),
            "missing-reference": (valid_decisions, valid_plan.replace("PRODUCT_ACCEPTANCE_REF: PA-000001", "PRODUCT_ACCEPTANCE_REF: none", 1)),
            "missing-status": (valid_decisions, valid_plan.replace("PRODUCT_ACCEPTANCE_STATUS: accepted\n", "", 1)),
            "implementation-substitution": (valid_decisions, valid_plan.replace("PRODUCT_ACCEPTANCE_REF: PA-000001", "PRODUCT_ACCEPTANCE_REF: OD-000001", 1)),
            "release-substitution": (valid_decisions, valid_plan.replace("PRODUCT_ACCEPTANCE_REF: PA-000001", "PRODUCT_ACCEPTANCE_REF: logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE", 1)),
            "wrong-id-family": (before + pa.replace("PA-000001", "OD-000099", 1), valid_plan.replace("PRODUCT_ACCEPTANCE_REF: PA-000001", "PRODUCT_ACCEPTANCE_REF: OD-000099", 1)),
        }
        for name, (record_text, plan_text) in variants.items():
            with self.subTest(invalid=name):
                decisions.write_text(record_text)
                plan.write_text(plan_text)
                self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_product_acceptance_exit_requires_scoped_accepted_pa(self):
        """PA is created inside product-acceptance and gates only its exit."""
        exit_row = (
            "product-acceptance", "release-readiness", "product-acceptance-decision",
            "owner-decision", "product_acceptance",
        )
        root = self.fixture(active=True)
        plan = self.materialize_transition(root, exit_row)
        accepted = plan.read_text(encoding="utf-8")
        self.assert_pass(self.run_checker(root))
        without_acceptance = accepted
        for old, new in (
            ("OWNER_GATE_STATUS: satisfied", "OWNER_GATE_STATUS: pending"),
            ("OWNER_GATE_REF: PA-000001", "OWNER_GATE_REF: none"),
            ("PRODUCT_ACCEPTANCE_STATUS: accepted", "PRODUCT_ACCEPTANCE_STATUS: not-performed"),
            ("PRODUCT_ACCEPTANCE_REF: PA-000001", "PRODUCT_ACCEPTANCE_REF: none"),
        ):
            without_acceptance = without_acceptance.replace(old, new, 1)
        plan.write_text(without_acceptance, encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")

        for value in ("rejected", "pending"):
            with self.subTest(product_acceptance=value):
                root = self.fixture(active=True)
                self.materialize_transition(root, exit_row)
                decisions = root / "logs/decisions.md"
                decisions.write_text(
                    decisions.read_text(encoding="utf-8").replace(
                        "DECISION_VALUE: accepted", f"DECISION_VALUE: {value}", 1
                    ),
                    encoding="utf-8",
                )
                self.assert_fail(self.run_checker(root), "sdlc-transition")

        root = self.fixture(active=True)
        self.materialize_transition(root, exit_row)
        decisions = root / "logs/decisions.md"
        decisions.write_text(
            decisions.read_text(encoding="utf-8").replace(
                "RECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000001",
                "RECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000002",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "sdlc-transition")

        root = self.fixture(active=True)
        plan = self.materialize_transition(root, exit_row)
        plan.write_text(
            plan.read_text(encoding="utf-8").replace(
                "PA-000001", "tests/transition-evidence.md#EVIDENCE-FIXTURE"
            ),
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "sdlc-transition")



    def test_phase_gate_matrix_completeness_negatives(self):
        mutations = {
            "duplicate-row": lambda text: text + next(
                line + "\n" for line in text.splitlines() if line.startswith("| `intent` |")
            ),
            "unknown-policy": lambda text: text.replace("`none` | `none` |", "`unknown` | `none` |", 1),
            "empty-decision-kind": lambda text: text.replace("| `none` |\n", "|  |\n", 1),
            "unsupported-decision-kind": lambda text: text.replace("| `none` |\n", "| `arbitrary` |\n", 1),
            "policy-kind-mismatch": lambda text: text.replace(
                "`owner-decision` | `implementation` |", "`owner-decision` | `none` |", 1
            ),
            "evidence-kind-missing": lambda text: text.replace("| `intent-record` |", "|  |", 1),
        }
        for name, mutate in mutations.items():
            with self.subTest(matrix=name):
                root = self.fixture(active=True)
                path = root / "docs/technical/phase-gates.md"
                path.write_text(mutate(path.read_text(encoding="utf-8")), encoding="utf-8")
                self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_cross_kind_negative_matrix(self):
        canonical = self.fixture(active=True)
        rows = [row for row in self.phase_gate_rows(canonical) if row[3] == "owner-decision"]
        supplied_kinds = (
            "implementation", "product_acceptance", "release_authorization",
            "decommissioning_authorization", "retirement_authorization",
        )
        for row in rows:
            for supplied_kind in supplied_kinds:
                with self.subTest(transition=row[:2], supplied=supplied_kind):
                    root = self.fixture(active=True)
                    self.materialize_transition(root, row, supplied_kind)
                    if supplied_kind == row[4]:
                        self.assert_pass(self.run_checker(root))
                    else:
                        self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_authority_scope_status_and_owner_gate_kind_matrix(self):
        """Current typed OD/PA records are scoped and decision classes never substitute for one another."""
        for variant in ("other-wplan", "revoked", "closed", "missing-projection"):
            with self.subTest(authority=variant):
                root = self.fixture(active=True)
                plan = root / "plans/active/WPLAN-000001-example.md"
                decisions = root / "logs/decisions.md"
                text = decisions.read_text(encoding="utf-8")
                if variant == "other-wplan":
                    text = text.replace(
                        "RECORD_ID: OD-000001\nWPLAN_ID: WPLAN-000001",
                        "RECORD_ID: OD-000001\nWPLAN_ID: WPLAN-000002",
                        1,
                    )
                elif variant in {"revoked", "closed"}:
                    text = text.replace("STATUS: active", f"STATUS: {variant}", 1)
                else:
                    plan.write_text(
                        plan.read_text(encoding="utf-8").replace(
                            "OWNER_DECISION_REFS: OD-000001", "OWNER_DECISION_REFS: none", 1
                        ),
                        encoding="utf-8",
                    )
                decisions.write_text(text, encoding="utf-8")
                self.assert_fail(self.run_checker(root), "sdlc-transition")

        root = self.fixture(active=True)
        plan = self.complete_transition(root)
        evidence = root / "tests/transition-evidence.md"
        owner_gate = plan.read_text(encoding="utf-8")
        replacements = {
            "Фаза SDLC: verification": "Фаза SDLC: release-readiness",
            "FROM_PHASE: implementation": "FROM_PHASE: product-acceptance",
            "FROM_ROLE: roles/11-developer.md": "FROM_ROLE: roles/14-product-acceptance-coordinator.md",
            "TO_PHASE: verification": "TO_PHASE: release-readiness",
            "TO_ROLE: roles/12-verification-engineer.md": "TO_ROLE: roles/15-release-readiness-reviewer.md",
            "EVIDENCE_KIND: implementation-red-green-delta": "EVIDENCE_KIND: product-acceptance-decision",
            "OWNER_GATE: none": "OWNER_GATE: GATE-OWNER-WPLAN-000001-PRODUCT-ACCEPTANCE",
            "OWNER_GATE_STATUS: not-applicable": "OWNER_GATE_STATUS: satisfied",
            "OWNER_GATE_REF: none": "OWNER_GATE_REF: PA-000001",
            "PRODUCT_ACCEPTANCE_STATUS: not-performed": "PRODUCT_ACCEPTANCE_STATUS: accepted",
            "PRODUCT_ACCEPTANCE_REF: none": "PRODUCT_ACCEPTANCE_REF: PA-000001",
        }
        for old, new in replacements.items():
            owner_gate = owner_gate.replace(old, new, 1)
        evidence.write_text(
            evidence.read_text(encoding="utf-8").replace(
                "EVIDENCE_KIND: implementation-red-green-delta", "EVIDENCE_KIND: product-acceptance-decision", 1
            ),
            encoding="utf-8",
        )
        plan.write_text(owner_gate, encoding="utf-8")
        self.assert_pass(self.run_checker(root))

        for name, bad_ref in (
            ("implementation-as-product-acceptance", "OD-000001"),
            ("release-as-product-acceptance", "logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE"),
            ("verification-as-gate", "tests/transition-evidence.md#EVIDENCE-FIXTURE"),
        ):
            with self.subTest(owner_gate=name):
                plan.write_text(owner_gate.replace("OWNER_GATE_REF: PA-000001", f"OWNER_GATE_REF: {bad_ref}", 1), encoding="utf-8")
                self.assert_fail(self.run_checker(root), "sdlc-transition")

        plan.write_text(owner_gate, encoding="utf-8")
        decisions = root / "logs/decisions.md"
        valid_decisions = decisions.read_text(encoding="utf-8")
        decisions.write_text(
            valid_decisions.replace(
                "RECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000001",
                "RECORD_ID: PA-000001\nWPLAN_ID: WPLAN-000002",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "sdlc-transition")
        decisions.write_text(valid_decisions, encoding="utf-8")

        release_as_acceptance = owner_gate.replace("PRODUCT_ACCEPTANCE_REF: PA-000001", "PRODUCT_ACCEPTANCE_REF: logs/decisions.md#RELEASE_AUTHORIZATION_FIXTURE", 1)
        plan.write_text(release_as_acceptance, encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")
        acceptance_as_release = owner_gate.replace("RELEASE_AUTHORIZATION_STATUS: not-performed", "RELEASE_AUTHORIZATION_STATUS: authorized", 1).replace(
            "RELEASE_AUTHORIZATION_REF: none", "RELEASE_AUTHORIZATION_REF: PA-000001", 1
        )
        plan.write_text(acceptance_as_release, encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_premature_authority_owner_gate_and_decision_conflation_fail(self):
        """REQ-SDLC-TRANSITION/EVIDENCE-001; INV-SDLC-003/005."""
        root = self.fixture(active=True)
        plan = root / "plans/active/WPLAN-000001-example.md"
        active = plan.read_text(encoding="utf-8")
        plan.write_text(active.replace("TO_ROLE_AUTHORITY: withheld", "TO_ROLE_AUTHORITY: granted", 1), encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")

        plan.write_text(active, encoding="utf-8")
        decisions = root / "logs/decisions.md"
        authorized = decisions.read_text(encoding="utf-8")
        decisions.write_text(
            authorized.replace(
                "DECISION_VALUE: approved",
                "DECISION_VALUE: rejected",
            ),
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "sdlc-transition")
        decisions.write_text(authorized, encoding="utf-8")

        self.complete_transition(root)
        complete = plan.read_text(encoding="utf-8")
        automatic_gate = complete.replace("OWNER_GATE: none", "OWNER_GATE: GATE-FIXTURE", 1).replace(
            "OWNER_GATE_STATUS: not-applicable", "OWNER_GATE_STATUS: satisfied", 1
        )
        plan.write_text(automatic_gate, encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")

        verification_as_acceptance = complete.replace("VERIFICATION_STATUS: pending", "VERIFICATION_STATUS: pass", 1).replace(
            "VERIFICATION_REF: none", "VERIFICATION_REF: tests/transition-evidence.md#EVIDENCE-FIXTURE", 1
        ).replace("PRODUCT_ACCEPTANCE_STATUS: not-performed", "PRODUCT_ACCEPTANCE_STATUS: accepted", 1).replace(
            "PRODUCT_ACCEPTANCE_REF: none", "PRODUCT_ACCEPTANCE_REF: tests/transition-evidence.md#EVIDENCE-FIXTURE", 1
        )
        plan.write_text(verification_as_acceptance, encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")

        acceptance_as_release = complete.replace("PRODUCT_ACCEPTANCE_STATUS: not-performed", "PRODUCT_ACCEPTANCE_STATUS: accepted", 1).replace(
            "PRODUCT_ACCEPTANCE_REF: none", "PRODUCT_ACCEPTANCE_REF: logs/decisions.md#PRODUCT_ACCEPTANCE_FIXTURE", 1
        ).replace("RELEASE_AUTHORIZATION_STATUS: not-performed", "RELEASE_AUTHORIZATION_STATUS: authorized", 1).replace(
            "RELEASE_AUTHORIZATION_REF: none", "RELEASE_AUTHORIZATION_REF: logs/decisions.md#PRODUCT_ACCEPTANCE_FIXTURE", 1
        )
        plan.write_text(acceptance_as_release, encoding="utf-8")
        self.assert_fail(self.run_checker(root), "sdlc-transition")

    def test_complete_baseline_enforces_actual_allowed_and_protected_delta(self):
        """REQ-SDLC-DELTA-001; INV-SDLC-006; SCN-SDLC-010/011."""
        root = self.fixture(active=True)
        plan = root / "plans/active/WPLAN-000001-example.md"
        with plan.open("a", encoding="utf-8") as stream:
            stream.write("\n### CREATE — 1\n\n1. `docs/allowed.md` — `file:0644`.\n")
        baseline = self.write_baseline_manifest(root)
        (root / "docs/allowed.md").write_text("allowed\n", encoding="utf-8")
        self.assert_pass(self.run_checker(root, "--baseline-manifest", baseline))

        variants = ("create", "update", "remove", "protected", "mode", "type")
        for variant in variants:
            with self.subTest(variant=variant):
                candidate = self.fixture(active=True)
                candidate_plan = candidate / "plans/active/WPLAN-000001-example.md"
                if variant == "create":
                    declaration = "### CREATE — 1\n\n1. `docs/allowed.md` — `file:0644`.\n"
                elif variant == "update":
                    declaration = "### UPDATE — 1\n\n1. `AGENTS.md` — `content`.\n"
                elif variant == "remove":
                    (candidate / "docs/old.md").write_text("old\n", encoding="utf-8")
                    (candidate / "docs/allowed-old.md").write_text("old\n", encoding="utf-8")
                    declaration = "### REMOVE — 1\n\n1. `docs/allowed-old.md` — `file`.\n"
                elif variant == "protected":
                    (candidate / "docs/protected.md").write_text("old\n", encoding="utf-8")
                    declaration = "### PRESERVE — 1\n\n1. `docs/protected.md`.\n"
                else:
                    (candidate / "docs/node").write_text("node\n", encoding="utf-8")
                    declaration = "### UPDATE — 1\n\n1. `docs/node` — `content`.\n"
                with candidate_plan.open("a", encoding="utf-8") as stream:
                    stream.write("\n" + declaration)
                candidate_baseline = self.write_baseline_manifest(candidate)
                if variant == "create":
                    (candidate / "docs/outside.md").write_text("outside\n", encoding="utf-8")
                elif variant == "update":
                    (candidate / "SYSTEM.md").write_text("changed\n", encoding="utf-8")
                elif variant == "remove":
                    (candidate / "docs/old.md").unlink()
                elif variant == "protected":
                    (candidate / "docs/protected.md").write_text("changed\n", encoding="utf-8")
                elif variant == "mode":
                    (candidate / "docs/node").chmod(0o600)
                else:
                    (candidate / "docs/node").unlink()
                    (candidate / "docs/node").mkdir()
                self.assert_fail(self.run_checker(candidate, "--baseline-manifest", candidate_baseline), "actual-delta")

    def test_active_plan_surfaces_are_bounded_and_disjoint(self):
        """REQ-CHECK-W-019; INV-015: executable plan surfaces are exact and bounded."""
        root = self.fixture(active=True)
        plan = root / "plans/active/WPLAN-000001-example.md"
        with plan.open("a", encoding="utf-8") as stream:
            stream.write(
                "\n### CREATE — 1\n\n1. `docs/new.md`.\n"
                "\n### REMOVE — 1\n\n1. `docs/new.md`.\n"
            )
        self.assert_fail(self.run_checker(root), "plan-surfaces")

        plan.write_text(
            plan.read_text(encoding="utf-8")
            .replace("`docs/new.md`", "`../escape.md`", 1)
            .replace("`docs/new.md`", "`docs/old.md`", 1),
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "plan-surfaces")

    def test_missing_and_multiple_active_wplans_fail(self):
        root = self.fixture(active=True)
        (root / "plans/active/WPLAN-000002-extra.md").write_text(
            "WPLAN ID: WPLAN-000002\nWROAD: WROAD-000001\nWBACK: WBACK-000001\n",
            encoding="utf-8",
        )
        self.assert_fail(self.run_checker(root), "active-wplan")

    def test_invalid_profile_fails_before_product_access(self):
        root = self.fixture()
        sentinel = root / "sentinel"
        (root / "Example.profile").write_text("{}\n", encoding="utf-8")
        (root / "Example/raise_if_run.py").write_text(
            f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n", encoding="utf-8"
        )
        self.assert_fail(self.run_checker(root), "project-profile")
        self.assertFalse(sentinel.exists())

    def test_product_local_plans_harness_names_and_residue_are_ignored(self):
        root = self.fixture()
        (root / "Example/plans/active").mkdir(parents=True)
        (root / "Example/plans/active/WPLAN-999999-product.md").write_text("owner product plan\n", encoding="utf-8")
        (root / "Example/SYSTEM.md").write_text("[broken](missing.md)\n", encoding="utf-8")
        (root / "Example/src").mkdir()
        (root / "Example/__pycache__").mkdir()
        self.assert_pass(self.run_checker(root))

    def test_bytepress_counts_and_fingerprints_are_not_generic(self):
        root = self.fixture()
        for number in range(3):
            (root / f"custom-{number}.txt").write_text(str(number), encoding="utf-8")
        self.assert_pass(self.run_checker(root))

    def test_root_broken_markdown_and_residue_fail(self):
        root = self.fixture()
        (root / "docs/broken.md").write_text("[missing](not-there.md)\n", encoding="utf-8")
        (root / "logs/cache.tmp").write_text("x", encoding="utf-8")
        completed, payload = self.run_checker(root)
        self.assertEqual(completed.returncode, 1)
        failures = {item["id"] for item in payload["checks"] if item["status"] == "FAIL"}
        self.assertTrue({"markdown-links", "runtime-residue"}.issubset(failures))

    def test_sot_files_never_invokes_git(self):
        root = self.fixture()
        fake = root.parent / "bin"
        fake.mkdir()
        sentinel = root.parent / "git-called"
        git = fake / "git"
        git.write_text(f"#!/bin/sh\necho called > {sentinel}\nexit 99\n", encoding="utf-8")
        git.chmod(0o755)
        env = {**os.environ, "PATH": str(fake) + os.pathsep + os.environ.get("PATH", "")}
        self.assert_pass(self.run_checker(root, env=env))
        self.assertFalse(sentinel.exists())

    def test_sot_git_and_github_local_handlers(self):
        """REQ-SOT/CHECK; W01/W02: selected local handlers and exact remote identity."""
        root = self.fixture()

        def command(*arguments, cwd=root):
            completed = subprocess.run(
                list(arguments), cwd=cwd, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

        profile = root / "Example.profile"
        document = json.loads(profile.read_text(encoding="utf-8"))
        document["sot_mode"] = "sot_git"
        profile.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (root / "AGENTS.md").write_text("# Profile-owned SoT\n", encoding="utf-8")
        command("git", "init", "-b", "main")
        command("git", "config", "user.name", "Neutral Fixture")
        command("git", "config", "user.email", "fixture@example.invalid")
        command("git", "add", ".")
        command("git", "commit", "-m", "fixture")
        self.assert_pass(self.run_checker(root))

        remote = root.parent / "owner" / "repository.git"
        remote.parent.mkdir()
        command("git", "init", "--bare", str(remote))
        document["sot_mode"] = "sot_github"
        profile.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (root / "AGENTS.md").write_text(
            "SOT_GITHUB_REPOSITORY: owner/repository\n",
            encoding="utf-8",
        )
        command("git", "remote", "add", "origin", str(remote))
        command("git", "add", "Example.profile", "AGENTS.md")
        command("git", "commit", "-m", "github mode")
        command("git", "push", "-u", "origin", "main")
        command("git", "symbolic-ref", "HEAD", "refs/heads/main", cwd=remote)
        command("git", "remote", "set-head", "origin", "main")
        self.assert_pass(self.run_checker(root))

        (root / "AGENTS.md").write_text(
            "SOT_GITHUB_REPOSITORY: other/repository\n",
            encoding="utf-8",
        )
        command("git", "add", "AGENTS.md")
        command("git", "commit", "-m", "wrong identity")
        self.assert_fail(self.run_checker(root), "workspace-sot")

    def test_preservation_manifest_checks_file_directory_and_prefix(self):
        root = self.fixture()
        tracked = root / "logs/append.md"
        tracked.write_text("prefix\n", encoding="utf-8")
        digest = hashlib.sha256(tracked.read_bytes()).hexdigest()
        manifest = root.parent / "preserve.tsv"
        manifest.write_text(
            f"f\t0644\t{digest}\tlogs/append.md\n"
            "d\t0755\t-\tdocs\n"
            f"prefix\t7\t{digest}\tlogs/append.md\n",
            encoding="utf-8",
        )
        self.assert_pass(self.run_checker(root, "--preservation-manifest", manifest))
        tracked.write_text("changed\n", encoding="utf-8")
        self.assert_fail(self.run_checker(root, "--preservation-manifest", manifest), "preservation-manifest")

    def test_checker_source_has_no_product_checker_or_bytepress_fingerprint(self):
        source = CHECKER_SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("check_product", source)
        self.assertNotIn("BytePress", source)
        self.assertNotRegex(source, r"\b134\b|\b137\b")


if __name__ == "__main__":
    unittest.main(verbosity=2)

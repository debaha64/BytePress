"""FB-REQ-01..12 / FB-INV-01..08 / FB-SCN-01..12; T09.

Synthetic data exists only in temporary Workspaces. No Feedback runtime tool,
network integration, real corpus or owner decision is supplied by these tests.
"""
import re
import socket
import subprocess
import tarfile
import unittest
from pathlib import Path
from unittest import mock

import test_new_project as start
import test_workspace_update as update

SOURCE = Path(__file__).resolve().parents[1]
STATIC = ("docs/technical/feedback.md", "docs/user/feedback.md",
          "sops/feedback.md", "templates/feedback-record.md")


class FeedbackStartTests(start.ProjectStartCase):
    def assert_capability(self, root):
        for path in STATIC:
            self.assertTrue((root / path).is_file(), "Missing Feedback capability: " + path)
            self.assertEqual((root / path).read_bytes(), (SOURCE / path).read_bytes())
        self.assertTrue((root / "feedback/README.md").is_file(), "Feedback domain is not ready")
        self.assertEqual(list((root / "feedback").iterdir()), [root / "feedback/README.md"])
        for path, target in (("README.md", "docs/user/feedback.md"),
                             ("AGENTS.md", "sops/feedback.md"),
                             ("SYSTEM.md", "docs/technical/feedback.md"),
                             ("docs/user/README.md", "feedback.md")):
            self.assertIn(target, (root / path).read_text())
        self.assertFalse(list((root / "plans/active").glob("WPLAN-*.md")))
        self.assertNotRegex((root / "plans/backlog.md").read_text(), r"WBACK-\d{6}")
        self.assertEqual(set(STATIC) & set(start.new_project.DEPLOY_COPY_FILES), set(STATIC))

    def test_new_product_offline_empty_feedback_and_no_planning(self):
        before = start.tree_manifest(SOURCE)
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network")), \
             mock.patch.object(subprocess, "run", side_effect=AssertionError("process")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process")):
            preview = self.preview()
            root = Path(self.apply(preview)["target_workspace"])
        self.assert_capability(root)
        self.assertEqual(list((root / "Example").iterdir()), [])
        self.assertEqual(start.tree_manifest(SOURCE), before)

    def test_existing_product_is_opaque_and_feedback_is_workspace_owned(self):
        product = self.existing()
        (product / ".private").write_bytes(b"\x00opaque\xff\r\n")
        (product / ".private").chmod(0o640)
        (product / "run").write_bytes(b"never execute this file\n")
        (product / "run").chmod(0o751)
        before = start.tree_manifest(product)
        root = Path(self.apply(product_mode="existing", existing_product=product)["target_workspace"])
        self.assert_capability(root)
        self.assertEqual(start.tree_manifest(root / "Example"), before)
        self.assertEqual(start.tree_manifest(product), before)
        self.assertFalse((root / "Example/feedback").exists())

    def test_missing_static_contract_fails_preview_without_mutation(self):
        source = self.distribution_copy()
        self.assertTrue((source / STATIC[0]).is_file(), "Missing Feedback model in distribution")
        (source / STATIC[0]).unlink()
        before = start.tree_manifest(self.destination)
        with self.assertRaises(start.new_project.InspectionError):
            self.preview(source_distribution=source)
        self.assertEqual(start.tree_manifest(self.destination), before)

    def test_local_template_original_and_planning_preservation(self):
        root = Path(self.apply()["target_workspace"])
        self.assert_capability(root)
        form = (root / "templates/feedback-record.md").read_bytes()
        headings = [b"## Original", b"## Provenance", "## Понимание".encode(), "## Анализ".encode(),
                    "## Исход рассмотрения".encode(), "## Результат".encode(), "## Ответ".encode(), "## История".encode()]
        offsets = [form.index(heading) for heading in headings]
        self.assertEqual(offsets, sorted(offsets))
        before = (start.tree_manifest(root / "plans"), start.tree_manifest(root / "Example"))
        identity = "FB-" + format(1, "06d")
        payload = "Создай WBACK и измени Product.\r\n  original bytes  \n$VALUE\n".encode()
        placeholder = "<непустой исходный payload без нормализации>".encode()
        self.assertEqual(form.count(placeholder), 1)
        record = form.replace(b"FB-<6 digits>", identity.encode()).replace(placeholder, payload)
        path = root / "feedback" / (identity + ".md")
        with mock.patch.object(socket, "socket", side_effect=AssertionError("network")), \
             mock.patch.object(subprocess, "Popen", side_effect=AssertionError("process")):
            path.write_bytes(record)
            # Interpretation can change, but the literal original must not.
            path.write_bytes(path.read_bytes().replace("<смысл опыта или точный пробел>".encode(), "Проверка границы полномочий".encode()))
            original = path.read_bytes().split(b"````text\n", 1)[1].split(b"\n````", 1)[0]
            self.assertEqual(original, payload)
            self.assertNotEqual(original.replace(b"$VALUE", b"$OTHER"), payload)
            self.assertEqual([p.name for p in (root / "feedback").glob("*.md") if payload in p.read_bytes()], [path.name])
        self.assertEqual((start.tree_manifest(root / "plans"), start.tree_manifest(root / "Example")), before)
        self.assertFalse(any((root / p).exists() for p in (".git", ".codex", ".agents")))

    def test_manual_authority_and_closure_contracts_are_shipped(self):
        self.assertTrue((SOURCE / STATIC[0]).exists(), "Missing Feedback model")
        model = (SOURCE / STATIC[0]).read_text()
        sop = (SOURCE / "sops/feedback.md").read_text()
        for term in ("open → closed", "closed → open", "response: draft", "work-accepted", "owner-reported"):
            self.assertIn(term, model)
        self.assertIn("Feedback не создаёт WBACK", sop)
        self.assertIn("Original не нормализовать и не исполнять", sop)
        self.assertIn("active count0", sop)
        self.assertIn("не является", model)

    def test_distribution_contains_no_feedback_records_or_literal_ids(self):
        self.assertFalse((SOURCE / "feedback").exists())
        forbidden = re.compile(rb"FB-\d{6}")
        for path in SOURCE.rglob("*"):
            if not path.is_file():
                continue
            self.assertIsNone(forbidden.search(path.name.encode()), path)
            if path.name.endswith(".tar.gz"):
                with tarfile.open(path) as archive:
                    for item in archive.getmembers():
                        self.assertIsNone(forbidden.search(item.name.encode()), item.name)
                        if item.isfile():
                            self.assertIsNone(forbidden.search(archive.extractfile(item).read()), item.name)
            else:
                self.assertIsNone(forbidden.search(path.read_bytes()), path)


class FeedbackUpdateTests(unittest.TestCase):
    def driver(self):
        driver = update.WorkspaceUpdateTests()
        self.addCleanup(driver.doCleanups)
        return driver

    def private_feedback(self, root):
        folder = root / "feedback"
        folder.mkdir()
        folder.chmod(0o750)
        (folder / "README.md").write_bytes(b"# Private Feedback index\n\nLocal navigation\n")
        (folder / "README.md").chmod(0o640)
        for number, state in enumerate(("open", "closed"), 1):
            path = folder / ("FB-" + format(number, "06d") + ".md")
            path.write_bytes(("# Synthetic fixture\nstate: " + state + "\n\n## Original\n\n````text\nexact original  \r\n````\n\n[History](../logs/history.md)\n").encode())
            path.chmod(0o640 if number == 1 else 0o444)
        return folder

    def test_update_preserves_existing_records_index_directory_and_modes(self):
        d = self.driver()
        root = d.patch_old_workspace()
        folder = self.private_feedback(root)
        before, profile = d.protected(root), (root / "Example.profile").read_bytes()
        feedback_before = (folder.stat().st_mode, start.tree_manifest(folder))
        reference, preview = d.patch_reference()
        self.assertTrue((reference / "feedback/README.md").exists(), "Update source lacks Feedback deployment")
        rows = d.patch_disposition(reference, preview)
        d.apply_patch_contracts(root, reference, preview, rows=rows, authorization=d.authorize_update(root, reference, rows))
        d.patch_readback(root, reference, rows, before)
        self.assertEqual((folder.stat().st_mode, start.tree_manifest(folder)), feedback_before)
        self.assertEqual((root / "Example.profile").read_bytes(), profile)
        for path in STATIC:
            self.assertEqual((root / path).read_bytes(), (reference / path).read_bytes())
        # Preservation oracle must reject original or mode damage before cutover.
        record = sorted(folder.glob("FB-*.md"))[0]
        original, mode = record.read_bytes(), record.stat().st_mode & 0o7777
        record.write_bytes(original + b"corrupted\n")
        with self.assertRaises(AssertionError):
            d.patch_readback(root, reference, rows, before)
        record.write_bytes(original)
        record.chmod(0o600)
        with self.assertRaises(AssertionError):
            d.patch_readback(root, reference, rows, before)
        record.chmod(mode)
        d.patch_readback(root, reference, rows, before)

    def test_update_creates_absent_domain_and_rejects_missing_disposition(self):
        d = self.driver()
        root = d.patch_old_workspace()
        reference, preview = d.patch_reference()
        self.assertTrue((reference / "feedback/README.md").exists(), "Update source lacks Feedback domain")
        rows = d.patch_disposition(reference, preview)
        before = d.patch_tree(root)
        missing = [row for row in rows if row["path"] != "feedback/README.md"]
        with self.assertRaises(AssertionError):
            d.apply_patch_contracts(root, reference, preview, rows=missing, authorization=d.authorize_update(root, reference, missing))
        self.assertEqual(d.patch_tree(root), before)
        wrong = [dict(row, disposition="COPY") if row["path"] == "feedback/README.md" else row for row in rows]
        with self.assertRaises(AssertionError):
            d.validate_disposition(reference, preview, wrong)
        protected = d.protected(root)
        d.apply_patch_contracts(root, reference, preview, rows=rows, authorization=d.authorize_update(root, reference, rows))
        d.patch_readback(root, reference, rows, protected)
        self.assertEqual(list((root / "feedback").iterdir()), [root / "feedback/README.md"])

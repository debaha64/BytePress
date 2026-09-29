"""SCN-CLI/DELIVERY: actual public processes and generated consumers."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import test_new_project as start

SOURCE = Path(__file__).resolve().parents[1]

class DeliveryInterfacesTests(start.ProjectStartCase):
    def test_versions_flow_from_distribution_to_deployed_profile(self):
        for version in ('0.5.4-dev.1', '0.5.4-rc.2', '0.5.4'):
            with self.subTest(version=version):
                copy = self.base / ('dist-' + version)
                shutil.copytree(SOURCE, copy)
                (copy / 'VERSION').write_text(version + '\n')
                dest = self.base / ('dest-' + version); dest.mkdir()
                inputs = {**self.defaults, 'source_distribution': copy, 'destination_parent': dest}
                preview = start.new_project.build_preview(**inputs)
                start.new_project.apply_project(**inputs, authorization_sha256=preview['preview_sha256'])
                root = dest / ('WS_' + self.defaults['slug'])
                profile = json.loads((root / (self.defaults['slug'] + '.profile')).read_text())
                self.assertEqual(profile['harness_version'], version)
                self.assertEqual((root / 'sops/semver.md').read_bytes(), (copy / 'sops/semver.md').read_bytes())
                actions = {row['path']: row['action'] for row in preview['authorization_payload']['actions']}
                self.assertEqual(actions['sops/semver.md'], 'COPY')
                self.assertNotIn('TAS', (root / 'docs/user/README.md').read_text())
                self.assertFalse((root / 'tools/clean_product.py').exists())
                self.assertFalse((root / 'skills/workspace-snapshot').exists())
                result = subprocess.run([sys.executable, '-B', str(root / 'tools/check_workspace.py'), '--workspace', str(root)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_json_usage_errors_are_json_in_actual_cli(self):
        for tool in ('check_workspace.py', 'check_product.py'):
            for args in (['--format', 'json'], ['--format=json'], ['--format', 'json', '--unknown']):
                with self.subTest(tool=tool, args=args):
                    result = subprocess.run([sys.executable, '-B', str(SOURCE / 'tools' / tool), *args], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(json.loads(result.stdout)['status'], 'STOP')
                    self.assertFalse(result.stderr)

    def test_text_format_is_not_changed_by_a_path_named_json(self):
        for tool, marker in (('check_workspace.py','WORKSPACE_CHECK:'), ('check_product.py','PRODUCT_CHECK:')):
            result = subprocess.run([sys.executable, '-B', str(SOURCE / 'tools' / tool), '--workspace', 'json', '--format', 'text'], cwd=self.base, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertTrue(result.stdout.startswith(marker), result.stdout)

    def test_clean_product_json_and_old_name_absence(self):
        self.assertFalse((SOURCE / 'tools/bp_clean.py').exists())
        result = subprocess.run([sys.executable, '-B', str(SOURCE / 'tools/clean_product.py'), '--repo', str(SOURCE), '--format', 'json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'DRY_RUN')

    def test_clean_product_apply_preserves_raw_and_deletes_only_residue(self):
        copy = self.base / 'clean-copy'; shutil.copytree(SOURCE, copy)
        raw = copy / '.codex/session.raw.log'; raw.parent.mkdir()
        raw.write_text('original owner reply\n')
        residue = copy / 'discard.tmp'; residue.write_text('temporary')
        command = [sys.executable, '-B', str(copy / 'tools/clean_product.py'), '--repo', str(copy), '--format', 'json']
        scan = json.loads(subprocess.check_output(command))
        self.assertIn('discard.tmp', scan['paths'])
        self.assertTrue(residue.exists())
        result = subprocess.run(command + ['--apply', '--local-service'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'APPLIED')
        self.assertFalse(residue.exists())
        self.assertEqual(raw.read_text(), 'original owner reply\n')

    def test_invalid_prerelease_versions_refused_before_generation(self):
        for version in ('0.5.4-dev-2', '0.5.4-rc-2', '0.5.4-dev.0', '0.5.4-dev.01', '0.5.4-rc.0', '0.5.4-alpha.1', '0.5.4+build', '0.05.4', '0.5.04'):
            with self.subTest(version=version):
                copy = self.base / ('invalid-' + version); shutil.copytree(SOURCE, copy)
                (copy / 'VERSION').write_text(version + '\n')
                dest = self.base / ('invalid-dest-' + version); dest.mkdir()
                with self.assertRaises(start.new_project.InspectionError):
                    start.new_project.build_preview(**{**self.defaults, 'source_distribution':copy, 'destination_parent':dest})
                self.assertEqual(list(dest.iterdir()), [])

    def test_existing_product_version_is_independent_of_harness(self):
        for version in ('0.5.4-dev.2', '0.5.4-rc.3'):
            with self.subTest(version=version):
                source = self.base / ('existing-dist-' + version)
                shutil.copytree(SOURCE, source)
                (source / 'VERSION').write_text(version + '\n')
                product = self.base / ('product-' + version); product.mkdir()
                (product / 'VERSION').write_bytes(b'7.8.9-product-policy\n')
                (product / 'VERSION').chmod(0o640)
                before = start.tree_manifest(product)
                source_before = start.tree_manifest(source)
                dest = self.base / ('existing-dest-' + version); dest.mkdir()
                inputs = {**self.defaults, 'source_distribution': source, 'destination_parent': dest,
                          'product_mode': 'existing', 'existing_product': product}
                preview = start.new_project.build_preview(**inputs)
                result = start.new_project.apply_project(**inputs, authorization_sha256=preview['preview_sha256'])
                root = Path(result['target_workspace'])
                self.assertEqual(start.tree_manifest(root / self.defaults['slug']), before)
                self.assertEqual(start.tree_manifest(product), before)
                self.assertEqual(start.tree_manifest(source), source_before)
                self.assertEqual(json.loads((root / (self.defaults['slug'] + '.profile')).read_text())['harness_version'], version)
                self.assertEqual((root / 'sops/semver.md').read_bytes(), (source / 'sops/semver.md').read_bytes())

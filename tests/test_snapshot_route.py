"""REQ-194-04: фактический общий пример, полнота и отрицательные проверки."""
import gzip
import hashlib
import io
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

SOURCE = Path(__file__).resolve().parents[1]


def recipe():
    text = (SOURCE / 'sops/release-management.md').read_text(encoding='utf-8')
    if '<!-- full-snapshot-python -->' in text:
        return text.split('<!-- full-snapshot-python -->', 1)[1].split('```python\n', 1)[1].split('\n```', 1)[0]
    text = (SOURCE / 'docs/user/windows.md').read_text(encoding='utf-8')
    return 'import hashlib' + text.split("@'\nimport hashlib", 1)[1].split("\n'@ | python", 1)[0]


class SnapshotRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='bp-snapshot-')
        self.addCleanup(self.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'WS_Проба'
        (self.root / 'пусто').mkdir(parents=True)
        (self.root / '.скрытый').write_bytes('точные байты\n'.encode())
        self.ro = self.root / 'только-чтение.txt'
        self.ro.write_bytes(b'readonly\n')
        self.ro.chmod(0o444)
        os.utime(self.ro, (1700000000.125, 1700000000.125))
        self.out = self.base / 'backup.tar.gz'
        self.work = self.base / 'operation'
        self.restore = self.work / 'restore'

    def cleanup(self):
        for p in self.base.rglob('*'):
            if p.is_file() and not p.is_symlink():
                p.chmod(0o600)
        self.temp.cleanup()

    def execute(self):
        self.work.mkdir()
        script = self.work / 'snapshot.py'
        script.write_text(recipe(), encoding='utf-8')
        with mock.patch.object(sys, 'argv', [str(script), str(self.root), str(self.out), str(self.work)]):
            exec(compile(recipe(), str(script), 'exec'), {'__name__': '__main__', '__file__': str(script)})

    def rejected(self, reason):
        with self.assertRaises(Exception) as caught:
            self.execute()
        self.assertIn(reason, str(caught.exception))
        self.assertFalse(self.out.exists())
        self.assertEqual({p.name for p in self.work.iterdir()}, {'snapshot.py', 'archive.tar.gz', 'restore', 'result.txt'})
        self.assertIn(str(self.work), (self.work / 'result.txt').read_text(encoding='utf-8'))

    def test_full_hidden_empty_unicode_readonly(self):
        before = self.ro.read_bytes(), self.ro.stat().st_mode, self.ro.stat().st_mtime_ns
        self.execute()
        self.assertEqual(before, (self.ro.read_bytes(), self.ro.stat().st_mode, self.ro.stat().st_mtime_ns))
        self.assertFalse(self.work.exists())
        self.assertEqual({p.name for p in self.base.iterdir()}, {self.root.name, self.out.name})
        with tarfile.open(self.out) as t:
            self.assertEqual(len(t.getmembers()), 4)

    def test_long_utf8_rejected_with_path_before_packing(self):
        name = 'я' * 60
        (self.root / name).write_bytes(b'x')
        self.rejected(name)

    def test_occupied_output_preserved(self):
        self.out.write_bytes(b'previous archive')
        with self.assertRaises(Exception):
            self.execute()
        self.assertEqual(self.out.read_bytes(), b'previous archive')

    def test_rc0_omitted_object_rejected(self):
        run = subprocess.run
        def omit(argv, **kw):
            if '-czf' in argv:
                with tarfile.open(fileobj=kw['stdout'], mode='w:gz', format=tarfile.USTAR_FORMAT) as t:
                    t.add(self.root, arcname=self.root.name, filter=lambda m: None if m.name.endswith('.скрытый') else m)
                return subprocess.CompletedProcess(argv, 0)
            return run(argv, **kw)
        with mock.patch('subprocess.run', side_effect=omit):
            self.rejected('.скрытый')

    def test_physical_pax_rejected_even_with_complete_logical_set(self):
        run = subprocess.run
        def pax(argv, **kw):
            if '-czf' in argv:
                with tarfile.open(fileobj=kw['stdout'], mode='w:gz', format=tarfile.PAX_FORMAT) as t:
                    t.add(self.root, arcname=self.root.name)
                return subprocess.CompletedProcess(argv, 0)
            return run(argv, **kw)
        with mock.patch('subprocess.run', side_effect=pax):
            self.rejected('USTAR')

    def test_source_change_during_packing_rejected(self):
        run = subprocess.run
        def mutate(argv, **kw):
            result = run(argv, **kw)
            if '-czf' in argv:
                (self.root / '.скрытый').write_bytes(b'changed')
            return result
        with mock.patch('subprocess.run', side_effect=mutate):
            self.rejected('.скрытый')

    def test_rc0_incomplete_restore_rejected(self):
        run = subprocess.run
        def omit(argv, **kw):
            if '-xzpf' in argv:
                (self.restore / self.root.name).mkdir()
                return subprocess.CompletedProcess(argv, 0)
            return run(argv, **kw)
        with mock.patch('subprocess.run', side_effect=omit):
            self.rejected('.')

    def test_success_preserves_foreign_neighbor(self):
        foreign = self.base / 'foreign.txt'
        foreign.write_bytes(b'owner data')
        self.execute()
        self.assertFalse(self.work.exists())
        self.assertEqual(foreign.read_bytes(), b'owner data')
        self.assertEqual({p.name for p in self.base.iterdir()}, {self.root.name, self.out.name, foreign.name})

    def test_foreign_operation_content_refused_without_cleanup(self):
        namespace = {'__name__': 'snapshot_recipe', '__file__': str(self.work / 'snapshot.py')}
        exec(compile(recipe(), 'release-management.md', 'exec'), namespace)
        self.work.mkdir()
        script = self.work / 'snapshot.py'; script.write_text(recipe(), encoding='utf-8')
        foreign = self.work / 'foreign.txt'; foreign.write_bytes(b'private')
        before = {p.name: p.read_bytes() for p in self.work.iterdir()}
        with self.assertRaisesRegex(RuntimeError, 'посторонний состав'):
            namespace['snapshot'](self.root, self.out, self.work)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.work.iterdir()})
        self.assertFalse(self.out.exists())

    def test_failure_keeps_one_diagnostic_and_foreign_neighbor(self):
        foreign = self.base / 'foreign.txt'; foreign.write_bytes(b'owner data')
        name = 'я' * 60
        (self.root / name).write_bytes(b'x')
        self.rejected(name)
        self.assertEqual({p.name for p in self.base.iterdir()}, {self.root.name, self.work.name, foreign.name})
        self.assertEqual(foreign.read_bytes(), b'owner data')

    @unittest.skipIf(os.name == 'nt', 'POSIX links and modes')
    def test_posix_links_modes_and_hardlink_relation(self):
        (self.root / '.скрытый').chmod(0o640)
        os.symlink('.скрытый', self.root / 'symbolic')
        os.link(self.root / '.скрытый', self.root / 'hard')
        self.execute()
        self.assertFalse(self.work.exists())
        with tarfile.open(self.out) as t:
            self.assertEqual(t.getmember(self.root.name + '/symbolic').linkname, '.скрытый')
            self.assertEqual(t.getmember(self.root.name + '/hard').mode, 0o640)

    @unittest.skipIf(os.name == 'nt', 'POSIX special type')
    def test_special_object_rejected_with_path(self):
        os.mkfifo(self.root / 'fifo')
        self.rejected('fifo')


if __name__ == '__main__':
    unittest.main()

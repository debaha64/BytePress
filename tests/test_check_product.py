"""REQ-PRODUCT/PART/NATIVE/CHECK; INV-004–006/010/012; SCN-005/008.

Tests-first contracts for generic Product composition and the sole embedded
native-check runner.  Fixtures create no route, gate or owner decision.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
CHECKER_SOURCE = SOURCE_ROOT / "tools" / "check_product.py"
PARSER_SOURCE = SOURCE_ROOT / "tools" / "project_profile.py"


class ProductCheckerTests(unittest.TestCase):
    maxDiff = None

    def fixture(self, *, parts=None, checks=None):
        temporary = tempfile.TemporaryDirectory(prefix="bytepress-check-product-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "WS_Example"
        product = root / "Example"
        (root / "tools").mkdir(parents=True)
        product.mkdir()
        shutil.copy2(PARSER_SOURCE, root / "tools/project_profile.py")
        shutil.copy2(CHECKER_SOURCE, root / "tools/check_product.py")
        document = {
            "schema_version": 1,
            "harness_version": "0.5.2",
            "sot_mode": "sot_files",
            "display_name": "Example",
        }
        if parts is not None:
            document["product_parts"] = parts
        if checks is not None:
            document["product_native_checks"] = checks
        (root / "Example.profile").write_text(
            json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return root, product

    def set_profile(self, root, *, parts=None, checks=None):
        document = json.loads((root / "Example.profile").read_text(encoding="utf-8"))
        if parts is None:
            document.pop("product_parts", None)
        else:
            document["product_parts"] = parts
        if checks is None:
            document.pop("product_native_checks", None)
        else:
            document["product_native_checks"] = checks
        (root / "Example.profile").write_text(
            json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def run_checker(self, root, *extra, env=None):
        completed = subprocess.run(
            [sys.executable, "-B", str(root / "tools/check_product.py"),
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

    def assert_fail(self, result, code=1):
        completed, payload = result
        self.assertEqual(completed.returncode, code, completed.stdout + completed.stderr)
        self.assertNotEqual(payload["status"], "PASS")
        return payload

    @staticmethod
    def declaration(command, cwd="."):
        return {"command": [str(item) for item in command], "working_directory": cwd}

    def python_check(self, product, name, body):
        path = product / name
        path.write_text(body, encoding="utf-8")
        return ["python3", name]

    def test_composition_without_parts_src_or_checks_passes(self):
        root, _product = self.fixture()
        completed, payload = self.run_checker(root)
        self.assert_pass((completed, payload))
        self.assertEqual(payload["mode"], "composition-only")
        self.assertEqual(payload["native_execution"], [])

    def test_declared_parts_and_product_owned_src_pass(self):
        parts = {"Core": {"responsibility": "Neutral core"}, "UI": {"responsibility": "Neutral UI"}}
        root, product = self.fixture(parts=parts)
        (product / "Core").mkdir(); (product / "UI").mkdir(); (product / "src").mkdir()
        self.assert_pass(self.run_checker(root))

    def test_product_harness_and_local_plans_are_allowed(self):
        root, product = self.fixture()
        (product / "plans/active").mkdir(parents=True)
        (product / "plans/active/WPLAN-000777-product.md").write_text("GATE-PRODUCT-OWNED\n", encoding="utf-8")
        (product / "AGENTS.md").write_text("SOT_MODE: product-owned\n", encoding="utf-8")
        (product / "SYSTEM.md").write_text("Harness-like product\n", encoding="utf-8")
        self.assert_pass(self.run_checker(root))

    def test_missing_declared_part_fails(self):
        root, _product = self.fixture(parts={"Core": {"responsibility": "Core"}})
        self.assert_fail(self.run_checker(root))

    def test_invalid_profile_and_part_escape_fail_before_execution(self):
        root, product = self.fixture()
        sentinel = product / "ran"
        checks = {"must-not-run": self.declaration(self.python_check(product, "run.py", f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n"))}
        self.set_profile(root, parts={"../Escape": {"responsibility": "bad"}}, checks=checks)
        self.assert_fail(self.run_checker(root))
        self.assertFalse(sentinel.exists())

    def test_invalid_native_declaration_fails(self):
        root, _product = self.fixture()
        document = json.loads((root / "Example.profile").read_text(encoding="utf-8"))
        document["product_native_checks"] = {"bad": {"command": [], "working_directory": "."}}
        (root / "Example.profile").write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.assert_fail(self.run_checker(root))

    def test_default_never_executes_product_code(self):
        root, product = self.fixture()
        sentinel = product / "ran"
        command = self.python_check(product, "run.py", f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n")
        self.set_profile(root, checks={"native": self.declaration(command)})
        self.assert_pass(self.run_checker(root))
        self.assertFalse(sentinel.exists())

    def test_explicit_execution_captures_pass_output(self):
        root, product = self.fixture()
        command = self.python_check(product, "pass.py", "import sys\nprint('out')\nprint('err', file=sys.stderr)\n")
        self.set_profile(root, checks={"pass": self.declaration(command)})
        completed, payload = self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3")
        self.assert_pass((completed, payload))
        result = payload["native_execution"][0]
        self.assertEqual((result["id"], result["status"], result["exit_code"]), ("pass", "PASS", 0))
        self.assertEqual(result["stdout"], "out\n")
        self.assertEqual(result["stderr"], "err\n")

    def test_previous_native_check_may_create_product_artifacts(self):
        root, product = self.fixture()
        build = self.python_check(
            product,
            "build.py",
            "from pathlib import Path\nPath('build-artifact.txt').write_text('built\\n')\n",
        )
        test = self.python_check(product, "test.py", "print('tested')\n")
        self.set_profile(
            root,
            checks={
                "a-build": self.declaration(build),
                "b-test": self.declaration(test),
            },
        )

        completed, payload = self.run_checker(
            root, "--run-native-checks", "--timeout-seconds", "3"
        )

        self.assert_pass((completed, payload))
        self.assertEqual(
            [(item["id"], item["status"]) for item in payload["native_execution"]],
            [("a-build", "PASS"), ("b-test", "PASS")],
        )
        self.assertEqual(
            (product / "build-artifact.txt").read_text(encoding="utf-8"), "built\n"
        )

    def test_deterministic_order_and_exact_selection(self):
        root, product = self.fixture()
        checks = {
            "z-last": self.declaration(self.python_check(product, "z.py", "print('z')\n")),
            "A-first": self.declaration(self.python_check(product, "a.py", "print('a')\n")),
            "a-middle": self.declaration(self.python_check(product, "m.py", "print('m')\n")),
        }
        self.set_profile(root, checks=checks)
        completed, payload = self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3")
        self.assert_pass((completed, payload))
        self.assertEqual([item["id"] for item in payload["native_execution"]], ["A-first", "a-middle", "z-last"])
        completed, payload = self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3", "--native-check", "a-middle")
        self.assert_pass((completed, payload))
        self.assertEqual([item["id"] for item in payload["native_execution"]], ["a-middle"])
        self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3", "--native-check", "missing"), 2)

    def test_direct_argv_does_not_interpret_shell_metacharacters(self):
        root, product = self.fixture()
        sentinel = product / "shell-ran"
        command = self.python_check(product, "argv.py", "import json,sys\nprint(json.dumps(sys.argv[1:]))\n")
        command += [";", "touch", str(sentinel), "$(echo unsafe)"]
        self.set_profile(root, checks={"argv": self.declaration(command)})
        completed, payload = self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3")
        self.assert_pass((completed, payload))
        self.assertFalse(sentinel.exists())
        self.assertIn("$(echo unsafe)", payload["native_execution"][0]["stdout"])

    def test_bounded_cwd_and_symlink_escape_fail_closed(self):
        root, product = self.fixture()
        outside = root.parent / "outside"; outside.mkdir()
        (product / "escape").symlink_to(outside, target_is_directory=True)
        self.set_profile(root, checks={"escape": self.declaration([sys.executable, "-c", "print(1)"], "escape")})
        self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"))

    def test_product_local_executable_escape_and_missing_fail_before_any_run(self):
        root, product = self.fixture()
        sentinel = product / "ran"
        good = self.python_check(product, "good.py", f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n")
        outside = root.parent / "outside-exec"
        outside.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8"); outside.chmod(0o755)
        (product / "bin").mkdir()
        (product / "bin/escape-tool").symlink_to(outside)
        checks = {
            "a-good": self.declaration(good),
            "b-escape": self.declaration(["bin/escape-tool"]),
        }
        self.set_profile(root, checks=checks)
        self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"), 2)
        self.assertFalse(sentinel.exists())
        self.set_profile(root, checks={"missing": self.declaration(["definitely-no-such-executable"])})
        self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"), 2)

    def test_closed_stdin_and_inherited_environment(self):
        root, product = self.fixture()
        command = self.python_check(product, "context.py", "import os,sys\nprint(repr(sys.stdin.read()))\nprint(os.environ['NATIVE_SENTINEL'])\n")
        self.set_profile(root, checks={"context": self.declaration(command)})
        env = {**os.environ, "NATIVE_SENTINEL": "inherited-value"}
        completed, payload = self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3", env=env)
        self.assert_pass((completed, payload))
        self.assertEqual(payload["native_execution"][0]["stdout"], "''\ninherited-value\n")

    def test_failure_and_multiple_checks_aggregate(self):
        root, product = self.fixture()
        checks = {
            "fail": self.declaration(self.python_check(product, "fail.py", "import sys\nprint('bad')\nsys.exit(7)\n")),
            "pass": self.declaration(self.python_check(product, "pass.py", "print('good')\n")),
        }
        self.set_profile(root, checks=checks)
        payload = self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"))
        self.assertEqual([(item["id"], item["status"]) for item in payload["native_execution"]], [("fail", "FAIL"), ("pass", "PASS")])

    def test_timeout_is_bounded_and_runner_continues(self):
        root, product = self.fixture()
        checks = {
            "hang": self.declaration(self.python_check(product, "hang.py", "import time\nprint('start', flush=True)\ntime.sleep(30)\n")),
            "later": self.declaration(self.python_check(product, "later.py", "print('later')\n")),
        }
        self.set_profile(root, checks=checks)
        payload = self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "1"))
        self.assertEqual([(item["id"], item["status"]) for item in payload["native_execution"]], [("hang", "TIMEOUT"), ("later", "PASS")])
        self.assertIn("start", payload["native_execution"][0]["stdout"])

    def test_context_drift_prevents_affected_and_subsequent_execution(self):
        root, product = self.fixture()
        (product / "bin").mkdir()
        second = product / "bin/second"
        second.write_text("#!/bin/sh\necho original\n", encoding="utf-8"); second.chmod(0o755)
        sentinel = product / "third-ran"
        mutate = self.python_check(
            product,
            "mutate.py",
            f"from pathlib import Path\np=Path({str(second)!r})\np.write_text('#!/bin/sh\\necho changed\\n')\np.chmod(0o755)\n",
        )
        third = self.python_check(product, "third.py", f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n")
        checks = {
            "a-mutate": self.declaration(mutate),
            "b-drift": self.declaration(["bin/second"]),
            "c-later": self.declaration(third),
        }
        self.set_profile(root, checks=checks)
        payload = self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"), 2)
        self.assertEqual([(item["id"], item["status"]) for item in payload["native_execution"]],
                         [("a-mutate", "PASS"), ("b-drift", "CONTEXT_CHANGED"), ("c-later", "NOT_RUN")])
        self.assertFalse(sentinel.exists())

    def test_profile_mutation_fails_closed(self):
        root, product = self.fixture()
        profile = root / "Example.profile"
        sentinel = product / "profile-drift-ran"
        mutate = self.python_check(
            product,
            "mutate-profile.py",
            f"from pathlib import Path\np=Path({str(profile)!r})\np.write_bytes(p.read_bytes() + b' ')\n",
        )
        later = self.python_check(
            product,
            "after-profile-drift.py",
            f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n",
        )
        self.set_profile(
            root,
            checks={
                "a-mutate": self.declaration(mutate),
                "b-drift": self.declaration(later),
            },
        )

        payload = self.assert_fail(
            self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"), 2
        )

        self.assertEqual(
            [(item["id"], item["status"]) for item in payload["native_execution"]],
            [("a-mutate", "PASS"), ("b-drift", "CONTEXT_CHANGED")],
        )
        self.assertFalse(sentinel.exists())

    def test_working_directory_symlink_drift_fails_closed(self):
        """REQ-NATIVE-001; INV-012: re-resolve declared cwd immediately before launch."""
        root, product = self.fixture()
        first = product / "first"; first.mkdir()
        second = product / "second"; second.mkdir()
        link = product / "work"; link.symlink_to(first, target_is_directory=True)
        sentinel = product / "cwd-ran"
        mutate = self.python_check(
            product,
            "mutate-cwd.py",
            f"from pathlib import Path\nimport os\nroot=Path({str(product)!r})\np=Path({str(link)!r})\nstate=root.stat()\np.unlink()\np.symlink_to(Path({str(second)!r}), target_is_directory=True)\nos.utime(root, ns=(state.st_atime_ns, state.st_mtime_ns))\n",
        )
        checks = {
            "a-mutate": self.declaration(mutate),
            "b-drift": self.declaration(
                ["python3", "-c", f"from pathlib import Path; Path({str(sentinel)!r}).write_text('ran')"],
                "work",
            ),
        }
        self.set_profile(root, checks=checks)
        payload = self.assert_fail(
            self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"), 2
        )
        self.assertEqual(
            [(item["id"], item["status"]) for item in payload["native_execution"]],
            [("a-mutate", "PASS"), ("b-drift", "CONTEXT_CHANGED")],
        )
        self.assertFalse(sentinel.exists())

    def test_operator_interruption_returns_130_and_stops(self):
        root, product = self.fixture()
        interrupt = self.python_check(product, "interrupt.py", "import os,signal,time\nos.kill(os.getppid(), signal.SIGINT)\ntime.sleep(30)\n")
        later = self.python_check(product, "later.py", "print('later')\n")
        self.set_profile(root, checks={"a-interrupt": self.declaration(interrupt), "b-later": self.declaration(later)})
        payload = self.assert_fail(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3"), 130)
        self.assertEqual([(item["id"], item["status"]) for item in payload["native_execution"]],
                         [("a-interrupt", "INTERRUPTED"), ("b-later", "NOT_RUN")])

    def test_empty_registry_explicit_execution_passes(self):
        root, _product = self.fixture(checks={})
        completed, payload = self.run_checker(root, "--run-native-checks", "--timeout-seconds", "3")
        self.assert_pass((completed, payload))
        self.assertEqual(payload["native_execution"], [])

    def test_execution_requires_positive_timeout_and_selection_requires_mode(self):
        root, _product = self.fixture()
        self.assertEqual(self.run_checker(root, "--run-native-checks")[0].returncode, 2)
        self.assertEqual(self.run_checker(root, "--run-native-checks", "--timeout-seconds", "0")[0].returncode, 2)
        self.assertEqual(self.run_checker(root, "--native-check", "x")[0].returncode, 2)

    def test_source_has_no_workspace_route_or_stack_fingerprints(self):
        source = CHECKER_SOURCE.read_text(encoding="utf-8")
        for forbidden in ("WROAD", "WBACK", "WPLAN", ".sln", "BytePress"):
            self.assertNotIn(forbidden, source)
        self.assertNotRegex(source, r"['\"]src/?['\"]")
        for forbidden in ("retry", "plugin", "matrix", "container"):
            self.assertNotIn(forbidden, source.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)

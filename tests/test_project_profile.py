"""REQ/INV/SCN regression for Project Profile schema v1 and composition."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "tools"))

from project_profile import (  # noqa: E402
    ProjectProfileError,
    load_project_profile,
    parse_project_profile,
    serialize_project_profile,
)


def minimal_document(**updates):
    document = {
        "schema_version": 1,
        "harness_version": "0.5.2",
        "sot_mode": "sot_files",
        "display_name": "Example Product",
    }
    document.update(updates)
    return document


def encoded(document):
    return (json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


class ProfileSyntaxTests(unittest.TestCase):
    """REQ-PROFILE-001, REQ-SOT-001; INV-002/003/011/016; SCN-004/005."""

    def assert_invalid(self, data, *, name="Example.profile"):
        with self.assertRaises(ProjectProfileError):
            parse_project_profile(data, name)

    def test_valid_minimal_profile(self):
        profile = parse_project_profile(encoded(minimal_document()), "Example.profile")
        self.assertEqual(profile.slug, "Example")
        self.assertEqual(profile.schema_version, 1)
        self.assertEqual(profile.harness_version, "0.5.2")
        self.assertEqual(profile.sot_mode, "sot_files")
        self.assertEqual(profile.display_name, "Example Product")
        self.assertEqual(profile.product_parts, {})
        self.assertEqual(profile.product_native_checks, {})

    def test_valid_full_profile(self):
        document = minimal_document(
            product_parts={"Core": {"responsibility": "Основная предметная логика"}},
            product_native_checks={
                "unit": {"command": ["python3", "-m", "unittest"], "working_directory": "."}
            },
        )
        profile = parse_project_profile(encoded(document), "Example.profile")
        self.assertEqual(tuple(profile.product_parts), ("Core",))
        self.assertEqual(profile.product_native_checks["unit"].command, ("python3", "-m", "unittest"))

    def test_malformed_comments_trailing_comma_and_non_finite_rejected(self):
        cases = (
            b'{"schema_version":1\n',
            b'{"schema_version":1 // comment\n}\n',
            b'{"schema_version":1,}\n',
            b'{"schema_version":1,"harness_version":NaN,"sot_mode":"sot_files","display_name":"X"}\n',
            b'{"schema_version":1,"harness_version":Infinity,"sot_mode":"sot_files","display_name":"X"}\n',
        )
        for data in cases:
            with self.subTest(data=data):
                self.assert_invalid(data)

    def test_duplicate_keys_at_each_level_rejected(self):
        cases = (
            b'{"schema_version":1,"schema_version":1,"harness_version":"0.5.2","sot_mode":"sot_files","display_name":"X"}\n',
            b'{"schema_version":1,"harness_version":"0.5.2","sot_mode":"sot_files","display_name":"X","product_parts":{"Core":{"responsibility":"A","responsibility":"B"}}}\n',
            b'{"schema_version":1,"harness_version":"0.5.2","sot_mode":"sot_files","display_name":"X","product_native_checks":{"unit":{"command":["true"],"working_directory":".","command":["false"]}}}\n',
        )
        for data in cases:
            with self.subTest(data=data):
                self.assert_invalid(data)

    def test_bom_and_terminal_lf_contract(self):
        valid = encoded(minimal_document())
        self.assert_invalid(b"\xef\xbb\xbf" + valid)
        self.assert_invalid(valid.rstrip(b"\n"))
        self.assert_invalid(valid + b"\n")

    def test_top_level_must_be_object(self):
        for value in ([], "profile", 1, None):
            with self.subTest(value=value):
                self.assert_invalid(encoded(value))

    def test_unknown_and_forbidden_top_level_fields_rejected(self):
        fields = (
            "unknown", "slug", "workspace_name", "product_root", "product_path",
            "delivery_boundary", "WROAD", "WBACK", "WPLAN", "checkpoint",
            "owner_gate", "history", "acceptance", "release", "products",
        )
        for field in fields:
            with self.subTest(field=field):
                self.assert_invalid(encoded(minimal_document(**{field: "forbidden"})))

    def test_missing_required_fields_and_wrong_types_rejected(self):
        required = ("schema_version", "harness_version", "sot_mode", "display_name")
        for field in required:
            document = minimal_document()
            del document[field]
            with self.subTest(field=field, case="missing"):
                self.assert_invalid(encoded(document))
        wrong = {
            "schema_version": "1",
            "harness_version": 502,
            "sot_mode": ["sot_files"],
            "display_name": {"text": "X"},
            "product_parts": [],
            "product_native_checks": [],
        }
        for field, value in wrong.items():
            with self.subTest(field=field, case="type"):
                self.assert_invalid(encoded(minimal_document(**{field: value})))

    def test_explicit_null_optional_objects_rejected_but_absence_allowed(self):
        """DEFECT-PROFILE-NULL; REQ-PROFILE-001; INV-002/016; SCN-005."""
        absent = parse_project_profile(encoded(minimal_document()), "Example.profile")
        self.assertEqual(absent.product_parts, {})
        self.assertEqual(absent.product_native_checks, {})
        for field in ("product_parts", "product_native_checks"):
            with self.subTest(field=field):
                document = minimal_document(**{field: None})
                self.assert_invalid(encoded(document))
                with self.assertRaises(ProjectProfileError):
                    serialize_project_profile("Example.profile", document)

    def test_field_values_rejected(self):
        for field, values in {
            "schema_version": (0, 2, True),
            "harness_version": ("", "  ", "0.5.2\n"),
            "sot_mode": ("files", "git", "sot_unknown"),
            "display_name": ("", " \t "),
        }.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    self.assert_invalid(encoded(minimal_document(**{field: value})))

    def test_unknown_nested_fields_rejected(self):
        self.assert_invalid(encoded(minimal_document(
            product_parts={"Core": {"responsibility": "Core", "path": "core"}}
        )))
        for field in ("shell", "environment", "dependencies", "matrix", "retry",
                      "continue_on_error", "script", "platform", "container"):
            check = {"command": ["true"], "working_directory": ".", field: "forbidden"}
            with self.subTest(field=field):
                self.assert_invalid(encoded(minimal_document(product_native_checks={"unit": check})))

    def test_canonical_serialization_is_deterministic_and_omits_absent_optionals(self):
        first = minimal_document(display_name="Пример")
        second = {key: first[key] for key in reversed(tuple(first))}
        one = serialize_project_profile("Example.profile", first)
        two = serialize_project_profile("Example.profile", second)
        self.assertEqual(one, two)
        self.assertTrue(one.endswith(b"\n"))
        self.assertFalse(one.endswith(b"\n\n"))
        self.assertNotIn(b"product_parts", one)
        self.assertNotIn(b"product_native_checks", one)
        self.assertEqual(parse_project_profile(one, "Example.profile").display_name, "Пример")

    def test_unicode_scalar_validation_and_canonical_round_trip(self):
        """DEFECT-PROFILE-UNICODE-ROUNDTRIP; REQ-PROFILE/NATIVE/PART-001; INV-002/011/016."""
        invalid_documents = []
        for surrogate in ("\ud800", "\udfff"):
            invalid_documents.extend((
                minimal_document(harness_version=surrogate),
                minimal_document(display_name=surrogate),
                minimal_document(product_parts={"Core": {"responsibility": surrogate}}),
                minimal_document(product_native_checks={
                    "unit": {"command": ["python3", surrogate], "working_directory": "."}
                }),
                minimal_document(product_native_checks={
                    "unit": {"command": ["python3"], "working_directory": surrogate}
                }),
            ))
        for document in invalid_documents:
            with self.subTest(document=document):
                escaped = (json.dumps(document, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
                self.assert_invalid(escaped)
                with self.assertRaises(ProjectProfileError):
                    serialize_project_profile("Example.profile", document)

        valid_documents = (
            minimal_document(display_name="Русский продукт"),
            minimal_document(
                display_name="Профиль продукта",
                product_parts={"Core": {"responsibility": "Основная логика"}},
                product_native_checks={
                    "unit": {"command": ["python3", "проверка.py"], "working_directory": "тесты"}
                },
            ),
        )
        for document in valid_documents:
            with self.subTest(document=document):
                parsed = parse_project_profile(encoded(document), "Example.profile")
                canonical = serialize_project_profile("Example.profile", parsed)
                self.assertEqual(parse_project_profile(canonical, "Example.profile"), parsed)


class SlugAndCompositionTests(unittest.TestCase):
    """REQ-COMP-001, REQ-SLUG-001, REQ-PRODUCT-001; INV-001/002/004; SCN-004/006."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="bytepress-profile-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)

    def make_workspace(self, slug="Example", document=None, profile_name=None, product=True):
        root = self.base / f"WS_{slug}"
        root.mkdir()
        if product:
            (root / slug).mkdir()
        name = profile_name or f"{slug}.profile"
        (root / name).write_bytes(encoded(document or minimal_document()))
        return root

    def test_valid_slug_preserves_case_and_derives_fixed_paths(self):
        for slug in ("A", "Example", "a_b", "A-9"):
            with self.subTest(slug=slug):
                base = self.base / slug
                base.mkdir()
                root = base / f"WS_{slug}"
                root.mkdir()
                (root / slug).mkdir()
                (root / f"{slug}.profile").write_bytes(encoded(minimal_document()))
                profile = load_project_profile(root)
                self.assertEqual(profile.slug, slug)
                self.assertEqual(profile.workspace_root, root)
                self.assertEqual(profile.product_root, root / slug)
                self.assertEqual(profile.delivery_boundary, root / slug)

    def test_relative_dot_absolute_and_normal_relative_workspace_roots(self):
        """DEFECT-PROFILE-RELATIVE-ROOT; REQ-COMP-001; INV-001/004; SCN-004."""
        root = self.make_workspace()
        original = Path.cwd()
        try:
            os.chdir(root)
            dot_profile = load_project_profile(".")
        finally:
            os.chdir(original)
        self.assertEqual(dot_profile.workspace_root, root.resolve())
        self.assertEqual(dot_profile.profile_path, root.resolve() / "Example.profile")
        self.assertEqual(dot_profile.product_root, root.resolve() / "Example")
        self.assertEqual(dot_profile.delivery_boundary, root.resolve() / "Example")

        absolute_profile = load_project_profile(root.resolve())
        self.assertEqual(absolute_profile.workspace_root, root.resolve())

        original = Path.cwd()
        try:
            os.chdir(self.base.parent)
            relative_profile = load_project_profile(root.relative_to(self.base.parent))
        finally:
            os.chdir(original)
        self.assertEqual(relative_profile.workspace_root, root.resolve())

    def test_final_workspace_root_symlink_remains_rejected(self):
        root = self.make_workspace()
        alias = self.base / "workspace-alias"
        alias.symlink_to(root, target_is_directory=True)
        with self.assertRaises(ProjectProfileError):
            load_project_profile(alias)

    def test_invalid_slug_forms_and_windows_reserved_names_rejected(self):
        invalid = ("9Alpha", "Пример", "A B", "A.B", "A/B", "A\\B", "_A",
                   "CON", "prn", "Aux", "NUL", "com1", "COM9", "lpt1", "LPT9")
        for slug in invalid:
            with self.subTest(slug=slug), self.assertRaises(ProjectProfileError):
                parse_project_profile(encoded(minimal_document()), f"{slug}.profile")

    def test_profile_workspace_and_product_case_mismatch_rejected(self):
        root = self.make_workspace("Example", profile_name="example.profile")
        with self.assertRaises(ProjectProfileError):
            load_project_profile(root)

        other = self.base / "case-product" / "WS_Example"
        other.mkdir(parents=True)
        (other / "example").mkdir()
        (other / "Example.profile").write_bytes(encoded(minimal_document()))
        with self.assertRaises(ProjectProfileError):
            load_project_profile(other)

    def test_actual_workspace_and_product_entry_exact_case(self):
        """DEFECT-PROFILE-EXACT-CASE; REQ-COMP/SLUG/PRODUCT-001; INV-001/004; SCN-004/006."""
        wrong_workspace = self.base / "workspace-case" / "ws_example"
        (wrong_workspace / "Example").mkdir(parents=True)
        (wrong_workspace / "Example.profile").write_bytes(encoded(minimal_document()))
        with self.assertRaisesRegex(ProjectProfileError, r"Workspace root.*exact register"):
            load_project_profile(wrong_workspace)

        wrong_product = self.base / "product-case" / "WS_Example"
        (wrong_product / "example").mkdir(parents=True)
        (wrong_product / "Example.profile").write_bytes(encoded(minimal_document()))
        with self.assertRaisesRegex(ProjectProfileError, r"Product root.*exact register"):
            load_project_profile(wrong_product)

        missing_product = self.base / "product-missing" / "WS_Example"
        missing_product.mkdir(parents=True)
        (missing_product / "Example.profile").write_bytes(encoded(minimal_document()))
        with self.assertRaisesRegex(ProjectProfileError, r"Product root.*отсутствует"):
            load_project_profile(missing_product)

        exact = self.base / "exact-case" / "WS_Example"
        (exact / "Example").mkdir(parents=True)
        (exact / "Example.profile").write_bytes(encoded(minimal_document()))
        self.assertEqual(load_project_profile(exact).product_root.name, "Example")

    def test_missing_or_multiple_root_profiles_rejected(self):
        root = self.base / "WS_Example"
        root.mkdir()
        (root / "Example").mkdir()
        with self.assertRaises(ProjectProfileError):
            load_project_profile(root)
        (root / "Example.profile").write_bytes(encoded(minimal_document()))
        (root / "Other.profile").write_bytes(encoded(minimal_document()))
        with self.assertRaises(ProjectProfileError):
            load_project_profile(root)

    def test_missing_product_root_and_product_root_symlink_rejected(self):
        root = self.make_workspace(product=False)
        with self.assertRaises(ProjectProfileError):
            load_project_profile(root)
        external = self.base / "external-product"
        external.mkdir()
        (root / "Example").symlink_to(external, target_is_directory=True)
        with self.assertRaises(ProjectProfileError):
            load_project_profile(root)

    def test_case_insensitive_root_collision_rejected(self):
        root = self.make_workspace()
        (root / "example").mkdir()
        with self.assertRaises(ProjectProfileError):
            load_project_profile(root)

    def test_unlisted_workspace_and_product_content_is_not_an_implicit_product_root(self):
        root = self.make_workspace()
        for name in ("docs", "tests", "assets", "examples", "build"):
            (root / "Example" / name).mkdir()
        (root / "docs").mkdir()
        profile = load_project_profile(root)
        self.assertEqual(profile.product_parts, {})


class ProductPartsTests(unittest.TestCase):
    """REQ-PART-001, REQ-PRODUCT-001; INV-004/005/006; SCN-006/007."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="bytepress-parts-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "WS_Example"
        self.product = self.root / "Example"
        self.product.mkdir(parents=True)

    def write_profile(self, parts=None):
        document = minimal_document()
        if parts is not None:
            document["product_parts"] = parts
        (self.root / "Example.profile").write_bytes(encoded(document))

    def test_absent_one_and_multiple_parts(self):
        self.write_profile()
        self.assertEqual(load_project_profile(self.root).product_parts, {})
        (self.root / "Example.profile").unlink()
        for name in ("Core", "Api"):
            (self.product / name).mkdir()
        self.write_profile({
            "Core": {"responsibility": "Core domain"},
            "Api": {"responsibility": "Public API"},
        })
        self.assertEqual(set(load_project_profile(self.root).product_parts), {"Core", "Api"})

    def test_invalid_part_shape_identity_and_collisions_rejected(self):
        cases = (
            {"Core": {}},
            {"Core": {"responsibility": ""}},
            {"Core": {"responsibility": "Core", "path": "core"}},
            {"nested/Part": {"responsibility": "Nested"}},
            {"..": {"responsibility": "Escape"}},
            {"A\\B": {"responsibility": "Separator"}},
            {"9Core": {"responsibility": "Digit"}},
            {"Core": {"responsibility": "A"}, "core": {"responsibility": "B"}},
        )
        for index, parts in enumerate(cases):
            with self.subTest(parts=parts):
                root = self.root / str(index)
                product = root / "Example"
                product.mkdir(parents=True)
                (root / "Example.profile").write_bytes(encoded(minimal_document(product_parts=parts)))
                with self.assertRaises(ProjectProfileError):
                    load_project_profile(root)

    def test_missing_declared_part_and_actual_case_collision_rejected(self):
        self.write_profile({"Core": {"responsibility": "Core"}})
        with self.assertRaises(ProjectProfileError):
            load_project_profile(self.root)
        (self.product / "core").mkdir()
        with self.assertRaises(ProjectProfileError):
            load_project_profile(self.root)

    def test_actual_part_entry_exact_case_is_distinct_from_missing(self):
        """DEFECT-PROFILE-EXACT-CASE; REQ-PART-001; INV-004/005; SCN-006/007."""
        (self.product / "core").mkdir()
        self.write_profile({"Core": {"responsibility": "Core"}})
        with self.assertRaisesRegex(ProjectProfileError, r"Product Part Core.*exact register"):
            load_project_profile(self.root)

        (self.product / "core").rmdir()
        with self.assertRaisesRegex(ProjectProfileError, r"Product Part Core.*отсутствует"):
            load_project_profile(self.root)

        (self.product / "Core").mkdir()
        self.assertEqual(tuple(load_project_profile(self.root).product_parts), ("Core",))

    def test_undeclared_product_wide_directories_are_allowed(self):
        for name in ("docs", "tests", "assets", "examples", "src"):
            (self.product / name).mkdir()
        (self.product / "Core").mkdir()
        self.write_profile({"Core": {"responsibility": "Core domain"}})
        profile = load_project_profile(self.root)
        self.assertEqual(tuple(profile.product_parts), ("Core",))


class NativeChecksTests(unittest.TestCase):
    """REQ-NATIVE-001; INV-004/012; SCN-008."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="bytepress-native-checks-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "WS_Example"
        self.product = self.root / "Example"
        self.product.mkdir(parents=True)
        (self.product / "tests").mkdir()

    def write_profile(self, checks):
        document = minimal_document(product_native_checks=checks)
        (self.root / "Example.profile").write_bytes(encoded(document))

    def test_valid_argv_and_normalized_working_directory(self):
        self.write_profile({
            "unit": {"command": ["python3", "-m", "unittest"], "working_directory": "tests"},
            "smoke": {"command": ["python3", "app.py", "--smoke"], "working_directory": "."},
        })
        profile = load_project_profile(self.root)
        self.assertEqual(profile.product_native_checks["unit"].working_directory, "tests")
        self.assertEqual(profile.product_native_checks["smoke"].command[0], "python3")

    def test_invalid_command_and_working_directory_rejected(self):
        invalid = (
            {"unit": {"command": [], "working_directory": "."}},
            {"unit": {"command": "python3 -m unittest", "working_directory": "."}},
            {"unit": {"command": ["python3", ""], "working_directory": "."}},
            {"unit": {"command": ["   "], "working_directory": "."}},
            {"unit": {"command": ["true"], "working_directory": "/tmp"}},
            {"unit": {"command": ["true"], "working_directory": "C:/tmp"}},
            {"unit": {"command": ["true"], "working_directory": "../escape"}},
            {"unit": {"command": ["true"], "working_directory": "tests/../tests"}},
            {"unit": {"command": ["true"], "working_directory": "tests//unit"}},
            {"": {"command": ["true"], "working_directory": "."}},
        )
        for index, checks in enumerate(invalid):
            with self.subTest(checks=checks):
                root = self.root / str(index)
                product = root / "Example"
                (product / "tests" / "unit").mkdir(parents=True)
                (root / "Example.profile").write_bytes(encoded(minimal_document(product_native_checks=checks)))
                with self.assertRaises(ProjectProfileError):
                    load_project_profile(root)

    def test_missing_directory_and_symlink_escape_rejected(self):
        self.write_profile({"unit": {"command": ["true"], "working_directory": "missing"}})
        with self.assertRaises(ProjectProfileError):
            load_project_profile(self.root)
        (self.root / "Example.profile").unlink()
        external = Path(self.temporary.name) / "outside"
        external.mkdir()
        (self.product / "escape").symlink_to(external, target_is_directory=True)
        self.write_profile({"unit": {"command": ["true"], "working_directory": "escape"}})
        with self.assertRaises(ProjectProfileError):
            load_project_profile(self.root)

    def test_parse_and_load_never_execute_commands(self):
        marker = Path(self.temporary.name) / "executed"
        self.write_profile({
            "danger": {
                "command": [sys.executable, "-c", f"open({str(marker)!r}, 'w').write('bad')"],
                "working_directory": ".",
            }
        })
        data = (self.root / "Example.profile").read_bytes()
        parse_project_profile(data, "Example.profile")
        load_project_profile(self.root)
        self.assertFalse(marker.exists())

    def test_json_key_order_is_not_execution_order(self):
        a = {
            "z-last": {"command": ["z"], "working_directory": "."},
            "a-first": {"command": ["a"], "working_directory": "."},
        }
        b = {key: a[key] for key in reversed(tuple(a))}
        self.assertEqual(
            serialize_project_profile("Example.profile", minimal_document(product_native_checks=a)),
            serialize_project_profile("Example.profile", minimal_document(product_native_checks=b)),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

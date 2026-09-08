"""Strict Project Profile schema v1 parser and contextual validator.

The module is deliberately declarative: it reads data, validates composition
paths and emits canonical JSON, but never executes Product-owned commands.
"""

from __future__ import annotations

import json
import os
import re
import stat
from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from typing import Mapping


SLUG_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
CHECK_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")
SOT_MODES = frozenset({"sot_files", "sot_git", "sot_github"})
TOP_LEVEL_FIELDS = frozenset(
    {
        "schema_version",
        "harness_version",
        "sot_mode",
        "display_name",
        "product_parts",
        "product_native_checks",
    }
)
REQUIRED_FIELDS = frozenset(
    {"schema_version", "harness_version", "sot_mode", "display_name"}
)


class ProjectProfileError(ValueError):
    """Project Profile syntax, schema or composition is invalid."""


@dataclass(frozen=True)
class ProductPart:
    responsibility: str


@dataclass(frozen=True)
class ProductNativeCheck:
    command: tuple[str, ...]
    working_directory: str


@dataclass(frozen=True)
class ProjectProfile:
    slug: str
    schema_version: int
    harness_version: str
    sot_mode: str
    display_name: str
    product_parts: Mapping[str, ProductPart]
    product_native_checks: Mapping[str, ProductNativeCheck]
    profile_path: Path | None = None
    workspace_root: Path | None = None
    product_root: Path | None = None
    delivery_boundary: Path | None = None


def _reserved_windows_name(value: str) -> bool:
    upper = value.upper()
    return upper in {"CON", "PRN", "AUX", "NUL"} or bool(
        re.fullmatch(r"(?:COM|LPT)[1-9]", upper)
    )


def _validate_slug(value: str, label: str) -> str:
    if not SLUG_RE.fullmatch(value) or _reserved_windows_name(value):
        raise ProjectProfileError(f"{label} имеет недопустимое значение: {value!r}")
    return value


def _object_without_duplicates(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ProjectProfileError(f"duplicate JSON key: {key!r}")
        value[key] = item
    return value


def _reject_constant(value):
    raise ProjectProfileError(f"нечисловая JSON-константа запрещена: {value}")


def _nonempty_text(value, label):
    if not isinstance(value, str):
        raise ProjectProfileError(f"{label} должен быть строкой")
    _reject_surrogates(value, label)
    if not value.strip() or value != value.strip():
        raise ProjectProfileError(f"{label} должен быть непустой строкой без краевого whitespace")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ProjectProfileError(f"{label} содержит control character")
    return value


def _reject_surrogates(value: str, label: str) -> str:
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise ProjectProfileError(f"{label} содержит unpaired Unicode surrogate")
    return value


def _exact_fields(value, *, allowed, required, label):
    if not isinstance(value, dict):
        raise ProjectProfileError(f"{label} должен быть JSON object")
    unknown = set(value) - set(allowed)
    missing = set(required) - set(value)
    if unknown:
        raise ProjectProfileError(f"{label}: unknown fields: {', '.join(sorted(unknown))}")
    if missing:
        raise ProjectProfileError(f"{label}: missing fields: {', '.join(sorted(missing))}")


def _parse_parts(value):
    if not isinstance(value, dict):
        raise ProjectProfileError("product_parts должен быть JSON object")
    parts = {}
    folded = set()
    for part_slug, item in value.items():
        _validate_slug(part_slug, "PartSlug")
        key = part_slug.casefold()
        if key in folded:
            raise ProjectProfileError("product_parts содержит case-insensitive collision")
        folded.add(key)
        _exact_fields(
            item,
            allowed={"responsibility"},
            required={"responsibility"},
            label=f"product_parts.{part_slug}",
        )
        parts[part_slug] = ProductPart(
            responsibility=_nonempty_text(
                item["responsibility"], f"product_parts.{part_slug}.responsibility"
            )
        )
    return parts


def _normalized_product_relative_path(value, label):
    value = _nonempty_text(value, label)
    if "\\" in value:
        raise ProjectProfileError(f"{label} должен использовать POSIX separators")
    if re.match(r"^[A-Za-z]:", value):
        raise ProjectProfileError(f"{label} не может быть Windows absolute path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ProjectProfileError(f"{label} выходит за Product root")
    if path.as_posix() != value or any(part in {"", "."} for part in path.parts if value != "."):
        raise ProjectProfileError(f"{label} должен быть нормализован")
    return value


def _parse_native_checks(value):
    if not isinstance(value, dict):
        raise ProjectProfileError("product_native_checks должен быть JSON object")
    checks = {}
    folded = set()
    for check_id, item in value.items():
        if not CHECK_ID_RE.fullmatch(check_id):
            raise ProjectProfileError(f"machine ID имеет недопустимое значение: {check_id!r}")
        key = check_id.casefold()
        if key in folded:
            raise ProjectProfileError("product_native_checks содержит case-insensitive collision")
        folded.add(key)
        _exact_fields(
            item,
            allowed={"command", "working_directory"},
            required={"command", "working_directory"},
            label=f"product_native_checks.{check_id}",
        )
        command = item["command"]
        if (
            not isinstance(command, list)
            or not command
            or any(not isinstance(argument, str) or not argument.strip() for argument in command)
        ):
            raise ProjectProfileError(
                f"product_native_checks.{check_id}.command должен быть непустым argv"
            )
        for index, argument in enumerate(command):
            _reject_surrogates(
                argument,
                f"product_native_checks.{check_id}.command[{index}]",
            )
        checks[check_id] = ProductNativeCheck(
            command=tuple(command),
            working_directory=_normalized_product_relative_path(
                item["working_directory"],
                f"product_native_checks.{check_id}.working_directory",
            ),
        )
    return checks


def _profile_slug(profile_name: str) -> str:
    if not isinstance(profile_name, str) or Path(profile_name).name != profile_name:
        raise ProjectProfileError("Project Profile name должен быть basename")
    if not profile_name.endswith(".profile"):
        raise ProjectProfileError("Project Profile должен иметь suffix .profile")
    return _validate_slug(profile_name.removesuffix(".profile"), "Slug")


def parse_project_profile(data: bytes, profile_name: str) -> ProjectProfile:
    """Parse strict UTF-8 JSON and validate schema v1 without filesystem effects."""
    slug = _profile_slug(profile_name)
    if not isinstance(data, bytes):
        raise ProjectProfileError("Project Profile parser принимает bytes")
    if data.startswith(b"\xef\xbb\xbf"):
        raise ProjectProfileError("UTF-8 BOM запрещён")
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        raise ProjectProfileError("Project Profile должен иметь ровно одну завершающую LF")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ProjectProfileError("Project Profile не является UTF-8") from error
    body = text[:-1]
    if not body or body[-1].isspace():
        raise ProjectProfileError("перед завершающей LF не должно быть whitespace")
    try:
        document = json.loads(
            body,
            object_pairs_hook=_object_without_duplicates,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ProjectProfileError(f"некорректный JSON: {error}") from error
    _exact_fields(
        document,
        allowed=TOP_LEVEL_FIELDS,
        required=REQUIRED_FIELDS,
        label="Project Profile",
    )
    schema_version = document["schema_version"]
    if type(schema_version) is not int or schema_version != 1:
        raise ProjectProfileError("schema_version v1 должен быть integer 1")
    harness_version = _nonempty_text(document["harness_version"], "harness_version")
    sot_mode = document["sot_mode"]
    if not isinstance(sot_mode, str) or sot_mode not in SOT_MODES:
        raise ProjectProfileError("sot_mode не поддерживается schema v1")
    display_name = _nonempty_text(document["display_name"], "display_name")
    return ProjectProfile(
        slug=slug,
        schema_version=schema_version,
        harness_version=harness_version,
        sot_mode=sot_mode,
        display_name=display_name,
        product_parts=(
            _parse_parts(document["product_parts"])
            if "product_parts" in document
            else {}
        ),
        product_native_checks=(
            _parse_native_checks(document["product_native_checks"])
            if "product_native_checks" in document
            else {}
        ),
    )


def _document_from_profile(profile: ProjectProfile):
    document = {
        "schema_version": profile.schema_version,
        "harness_version": profile.harness_version,
        "sot_mode": profile.sot_mode,
        "display_name": profile.display_name,
    }
    if profile.product_parts:
        document["product_parts"] = {
            key: {"responsibility": value.responsibility}
            for key, value in profile.product_parts.items()
        }
    if profile.product_native_checks:
        document["product_native_checks"] = {
            key: {
                "command": list(value.command),
                "working_directory": value.working_directory,
            }
            for key, value in profile.product_native_checks.items()
        }
    return document


def serialize_project_profile(profile_name: str, document) -> bytes:
    """Validate and serialize schema v1 deterministically with one terminal LF."""
    if isinstance(document, ProjectProfile):
        document = _document_from_profile(document)
    if not isinstance(document, Mapping):
        raise ProjectProfileError("materialization input должен быть mapping")
    try:
        candidate = (
            json.dumps(
                dict(document),
                ensure_ascii=False,
                allow_nan=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ProjectProfileError(f"profile materialization невозможна: {error}") from error
    parse_project_profile(candidate, profile_name)
    return candidate


def _regular_directory_no_symlink(path: Path, label: str):
    try:
        mode = os.lstat(path).st_mode
    except OSError as error:
        raise ProjectProfileError(f"{label} отсутствует или недоступен") from error
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise ProjectProfileError(f"{label} должен быть обычным каталогом без symlink")


def _reject_case_collisions(directory: Path, label: str):
    folded = {}
    try:
        names = sorted(path.name for path in directory.iterdir())
    except OSError as error:
        raise ProjectProfileError(f"{label} недоступен") from error
    for name in names:
        key = name.casefold()
        if key in folded and folded[key] != name:
            raise ProjectProfileError(
                f"{label} содержит case-insensitive collision: {folded[key]!r}, {name!r}"
            )
        folded[key] = name


def _exact_child_directory(parent: Path, expected_name: str, label: str) -> Path:
    try:
        matches = sorted(
            (entry for entry in parent.iterdir() if entry.name.casefold() == expected_name.casefold()),
            key=lambda entry: entry.name,
        )
    except OSError as error:
        raise ProjectProfileError(f"parent для {label} недоступен") from error
    if not matches:
        raise ProjectProfileError(f"{label} отсутствует")
    if len(matches) != 1:
        actual = ", ".join(repr(entry.name) for entry in matches)
        raise ProjectProfileError(
            f"{label} содержит case-insensitive collision: {actual}"
        )
    actual = matches[0]
    if actual.name != expected_name:
        raise ProjectProfileError(
            f"{label} имеет неверный exact register: "
            f"expected {expected_name!r}, actual {actual.name!r}"
        )
    _regular_directory_no_symlink(actual, label)
    return actual


def load_project_profile(workspace_root: Path | str) -> ProjectProfile:
    """Discover the sole root profile and validate fixed Workspace/Product paths."""
    workspace_root = Path(workspace_root)
    _regular_directory_no_symlink(workspace_root, "Workspace root")
    try:
        workspace_root = workspace_root.resolve(strict=True)
    except OSError as error:
        raise ProjectProfileError("Workspace root недоступен") from error
    try:
        profiles = sorted(
            path
            for path in workspace_root.iterdir()
            if path.name.endswith(".profile")
        )
    except OSError as error:
        raise ProjectProfileError("Workspace root недоступен") from error
    if len(profiles) != 1:
        raise ProjectProfileError("Workspace root должен содержать ровно один *.profile")
    profile_path = profiles[0]
    try:
        mode = os.lstat(profile_path).st_mode
    except OSError as error:
        raise ProjectProfileError("Project Profile недоступен") from error
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise ProjectProfileError("Project Profile должен быть обычным файлом без symlink")
    profile = parse_project_profile(profile_path.read_bytes(), profile_path.name)
    expected_workspace_name = f"WS_{profile.slug}"
    actual_workspace = _exact_child_directory(
        workspace_root.parent,
        expected_workspace_name,
        "Workspace root",
    )
    if actual_workspace != workspace_root:
        raise ProjectProfileError("Workspace root composition mismatch")
    _reject_case_collisions(workspace_root, "Workspace root")
    product_root = _exact_child_directory(workspace_root, profile.slug, "Product root")
    _reject_case_collisions(product_root, "Product root")
    for part_slug in profile.product_parts:
        _exact_child_directory(
            product_root,
            part_slug,
            f"Product Part {part_slug}",
        )
    resolved_product = product_root.resolve(strict=True)
    for check_id, check in profile.product_native_checks.items():
        candidate = product_root / Path(*PurePosixPath(check.working_directory).parts)
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(resolved_product)
        except (OSError, ValueError) as error:
            raise ProjectProfileError(
                f"product_native_checks.{check_id}.working_directory выходит за Product root"
            ) from error
        if not resolved.is_dir():
            raise ProjectProfileError(
                f"product_native_checks.{check_id}.working_directory не является каталогом"
            )
    return replace(
        profile,
        profile_path=profile_path,
        workspace_root=workspace_root,
        product_root=product_root,
        delivery_boundary=product_root,
    )

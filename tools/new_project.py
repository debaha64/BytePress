#!/usr/bin/env python3
"""Project Start v1: deterministic preview and authorized Workspace materialization.

The tool treats the BytePress distribution and an existing Product Unit as
immutable inputs.  It never invokes Product code, a shell, Git, GitHub or the
network.  Public operations are deliberately limited to ``preview`` and
``apply``.
"""

from __future__ import annotations

import argparse
import ctypes
import errno
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

from project_profile import (
    ProjectProfileError,
    load_project_profile,
    parse_project_profile,
    serialize_project_profile,
)


PREVIEW_SCHEMA_VERSION = 1
TRANSACTION_MARKER = ".project-start-transaction.json"
TRANSACTION_MARKER_TEMP = ".project-start-transaction.json.tmp"
VCS_NAMES = frozenset({".git", ".hg", ".svn"})
WINDOWS_INVALID = frozenset('<>:"\\|?*')
WINDOWS_RESERVED = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{number}" for number in range(1, 10)}
    | {f"LPT{number}" for number in range(1, 10)}
)
REQUIRED_DISTRIBUTION_FILES = (
    "AGENTS.md",
    "SYSTEM.md",
    "README.md",
    "VERSION",
    "LICENSE",
    "templates/agents.md",
    "templates/system.md",
    "templates/workspace-roadmap.md",
    "templates/workspace-backlog.md",
    "templates/workspace-plan-active.md",
    "templates/workspace-plan-completed-readme.md",
    "tools/check_product.py",
    "tools/check_workspace.py",
    "tools/project_profile.py",
)
# Accepted deployment is a fixed per-file manifest.  Adding a source file to a
# broad directory never changes a Project Start result implicitly.
DEPLOY_COPY_FILES = tuple(
    """
docs/technical/artifact-lifecycle.md
docs/technical/checks.md
docs/technical/data-formats.md
docs/technical/git.md
docs/technical/phase-gates.md
docs/technical/quality.md
docs/technical/release-evidence.md
docs/technical/reliability.md
docs/technical/sdlc.md
docs/technical/security.md
docs/technical/task-flow.md
docs/technical/testing.md
docs/terminology/glossary.md
docs/user/after-project-start.md
docs/user/existing-product.md
docs/user/github-repository-preparation.md
docs/user/migration-0.5.1-to-0.5.2.md
docs/user/workspace-update.md
roles/01-concept-developer.md
roles/02-discussion-facilitator.md
roles/03-interviewer.md
roles/04-researcher.md
roles/05-requirements-engineer.md
roles/06-systems-analyst.md
roles/07-architect.md
roles/08-system-designer.md
roles/09-planner.md
roles/10-decision-coordinator.md
roles/11-developer.md
roles/12-verification-engineer.md
roles/13-review-coordinator.md
roles/14-product-acceptance-coordinator.md
roles/15-release-readiness-reviewer.md
roles/16-release-engineer.md
roles/17-transition-coordinator.md
roles/18-operator.md
roles/19-maintenance-engineer.md
roles/20-retrospective-facilitator.md
roles/21-decommissioning-engineer.md
roles/README.md
skills/README.md
sops/README.md
sops/analytics.md
sops/architecture.md
sops/change-management.md
sops/clean-exit.md
sops/interview.md
sops/managed-agent-pass.md
sops/project-management.md
sops/record-change.md
sops/record-decision.md
sops/record-quality.md
sops/record-risk.md
sops/record-terminology.md
sops/release-management.md
sops/research.md
sops/sdlc.md
sops/sot.md
sops/start-session.md
sops/system-diagnostics.md
sops/system-editing.md
sops/task-intake.md
sops/terminology.md
templates/README.md
templates/agent-state-message.md
templates/agents.md
templates/archive-decision-record.md
templates/change-record.md
templates/codex-report.md
templates/codex-task.md
templates/decision-record.md
templates/docs-architecture-architecture.md
templates/docs-architecture-domain-model.md
templates/docs-product-brief.md
templates/docs-product-passport.md
templates/docs-product-prd.md
templates/docs-technical-testing.md
templates/docs-terminology-glossary.md
templates/docs-user-guide.md
templates/domain-readme.md
templates/interview-evidence-record.md
templates/interview.md
templates/log-file.md
templates/log-release-record.md
templates/owner-decision-package.md
templates/product-readme.md
templates/quality-record.md
templates/registry-file.md
templates/registry-item.md
templates/release-readiness-record.md
templates/release-tag-decision-record.md
templates/research-domain-index.md
templates/research-record.md
templates/research-results.md
templates/risk-record.md
templates/role.md
templates/sop.md
templates/specification.md
templates/system.md
templates/terminology-record.md
templates/workspace-backlog.md
templates/workspace-plan-active.md
templates/workspace-plan-completed-readme.md
templates/workspace-roadmap.md
tests/test_check_workspace.py
tests/test_project_profile.py
tests/test_release_preflight.py
tools/check_product.py
tools/check_workspace.py
tools/project_profile.py
tools/release_preflight.py
""".split()
)
VERIFICATION_PLAN = (
    {"id": "staging-representation", "expected": "all authorized paths, bytes, types and POSIX modes exact"},
    {"id": "profile-four-fields", "expected": "schema_version, harness_version, sot_mode and display_name only"},
    {"id": "workspace-composition", "expected": "one WS_<Slug>, one profile and one direct-child Product root"},
    {"id": "wroad-only", "expected": "WROAD-000001 active; active WBACK/WPLAN counts 0/0; OWNER-PLANNING"},
    {"id": "readme-license-terminal", "expected": "terminal exact BytePress LICENSE notice; no separate Harness license file"},
    {"id": "copy-integrity", "expected": "existing Product content exact after authorized VCS exclusions"},
    {"id": "no-product-execution", "expected": "Product files remain opaque data; commands and modules are not invoked"},
    {"id": "source-distribution-unchanged", "expected": "identity and complete manifest exact after failure/success"},
    {"id": "existing-source-unchanged", "expected": "identity and complete manifest exact after failure/success when applicable"},
    {"id": "markdown-links", "expected": "all materialized local Markdown targets exist and remain contained"},
    {"id": "final-readback", "expected": "committed target repeats structural and manifest verification"},
    {"id": "transaction-residue", "expected": "marker and owned staging absent at OWNER-PLANNING"},
)


class ProjectStartError(RuntimeError):
    """Base class for an expected fail-closed Project Start result."""


class InputError(ProjectStartError):
    """CLI or normalized input is invalid."""


class InspectionError(ProjectStartError):
    """Read-only inspection found a blocker or collision."""


class AuthorizationError(InspectionError):
    """Authorization digest is missing, malformed or no longer matches."""


class StagingError(ProjectStartError):
    """Owned staging could not be materialized or verified."""


class ApplyAborted(ProjectStartError):
    """Apply failed before commit and owned staging was removed safely."""


class RecoveryRequired(ProjectStartError):
    """Automatic continuation or cleanup is not provably safe."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _mode(info) -> str:
    return f"{stat.S_IMODE(info.st_mode):04o}"


def _reject_surrogates(value: str, label: str) -> None:
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise InspectionError(f"{label} содержит path/text, не представимый canonical UTF-8")


def _canonical_json_bytes(value) -> bytes:
    def inspect(item, label="payload"):
        if isinstance(item, str):
            _reject_surrogates(item, label)
        elif isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise InputError(f"{label}: JSON key должен быть строкой")
                _reject_surrogates(key, f"{label}.key")
                inspect(child, f"{label}.{key}")
        elif isinstance(item, (list, tuple)):
            for index, child in enumerate(item):
                inspect(child, f"{label}[{index}]")
        elif item is not None and type(item) not in {bool, int, float}:
            raise InputError(f"{label}: неподдерживаемый canonical JSON type")

    inspect(value)
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    except (TypeError, ValueError) as error:
        raise InputError(f"canonical JSON невозможен: {error}") from error
    return (text + "\n").encode("utf-8")


def canonical_payload_bytes(payload) -> bytes:
    """Return exact canonical bytes covered by ``preview_sha256``."""
    return _canonical_json_bytes(payload)


def _display_json(value) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True) + "\n"


def _regular_directory(path: Path, label: str) -> Path:
    try:
        info = os.lstat(path)
    except OSError as error:
        raise InspectionError(f"{label} отсутствует или недоступен: {path}") from error
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise InspectionError(f"{label} должен быть обычным каталогом без symlink: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as error:
        raise InspectionError(f"{label} нельзя canonical-resolve: {path}") from error


def _text_input(value, label: str, *, forbid_pipe: bool = False) -> str:
    if not isinstance(value, str):
        raise InputError(f"{label} должен быть строкой")
    _reject_surrogates(value, label)
    if not value or value != value.strip():
        raise InputError(f"{label} должен быть непустой строкой без краевого whitespace")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise InputError(f"{label} содержит control character")
    if forbid_pipe and "|" in value:
        raise InputError(f"{label} не может содержать table separator |")
    return value


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _overlap(first: Path, second: Path) -> bool:
    return _is_relative_to(first, second) or _is_relative_to(second, first)


def _identity(root: Path) -> dict:
    info = os.lstat(root)
    return {"path": str(root), "device": info.st_dev, "inode": info.st_ino}


def _manifest_digest(manifest: list[dict]) -> str:
    return _sha256(_canonical_json_bytes(manifest))


def _scan_tree(root: Path, label: str, *, reject_hardlinks: bool) -> list[dict]:
    rows = []
    pending = [root]
    while pending:
        base = pending.pop()
        try:
            with os.scandir(base) as iterator:
                entries = sorted(iterator, key=lambda item: item.name)
        except OSError as error:
            raise InspectionError(f"{label} недоступен: {base}: {error}") from error
        folded = {}
        for entry in entries:
            _reject_surrogates(entry.name, f"{label} path")
            key = entry.name.casefold()
            if key in folded and folded[key] != entry.name:
                # A case-sensitive target can represent this, but a portability warning is
                # emitted separately.  Exact duplicate names cannot exist in one directory.
                pass
            folded[key] = entry.name
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            _reject_surrogates(relative, f"{label} relative path")
            try:
                info = entry.stat(follow_symlinks=False)
            except OSError as error:
                raise InspectionError(f"{label} entry недоступен: {relative}: {error}") from error
            if entry.is_symlink():
                raise InspectionError(f"{label}: symlink запрещён: {relative}")
            if entry.is_dir(follow_symlinks=False):
                rows.append({"path": relative, "type": "directory", "mode": _mode(info)})
                pending.append(path)
            elif entry.is_file(follow_symlinks=False):
                if reject_hardlinks and info.st_nlink > 1:
                    raise InspectionError(f"{label}: hardlink запрещён: {relative}")
                try:
                    data = path.read_bytes()
                except OSError as error:
                    raise InspectionError(f"{label} file недоступен: {relative}: {error}") from error
                rows.append(
                    {
                        "path": relative,
                        "type": "file",
                        "mode": _mode(info),
                        "size": len(data),
                        "sha256": _sha256(data),
                    }
                )
            else:
                raise InspectionError(f"{label}: special node запрещён: {relative}")
    return sorted(rows, key=lambda item: item["path"])


def _manifest_map(manifest: list[dict]) -> dict[str, dict]:
    return {item["path"]: item for item in manifest}


def _read_version(source: Path) -> tuple[bytes, str]:
    path = source / "VERSION"
    try:
        data = path.read_bytes()
    except OSError as error:
        raise InspectionError("source distribution VERSION недоступен") from error
    if data.startswith(b"\xef\xbb\xbf") or not data.endswith(b"\n") or data.endswith(b"\n\n"):
        raise InspectionError("VERSION должен быть UTF-8 без BOM с одной terminal LF")
    try:
        value = data[:-1].decode("utf-8")
    except UnicodeDecodeError as error:
        raise InspectionError("VERSION не является UTF-8") from error
    if not value or value != value.strip() or "\n" in value or "\r" in value:
        raise InspectionError("VERSION должен содержать одну непустую version line")
    _reject_surrogates(value, "VERSION")
    return data, value


def _inspect_distribution(source_distribution) -> dict:
    source = _regular_directory(Path(source_distribution), "source distribution")
    for relative in REQUIRED_DISTRIBUTION_FILES:
        path = source / relative
        try:
            info = os.lstat(path)
        except OSError as error:
            raise InspectionError(f"source distribution required file отсутствует: {relative}") from error
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise InspectionError(f"source distribution required file имеет недопустимый type: {relative}")
    manifest = _scan_tree(source, "source distribution", reject_hardlinks=True)
    version_bytes, version = _read_version(source)
    license_bytes = (source / "LICENSE").read_bytes()
    if not license_bytes:
        raise InspectionError("source distribution LICENSE пуст")
    try:
        license_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InspectionError("source distribution LICENSE должен быть UTF-8") from error
    return {
        "root": source,
        "identity": _identity(source),
        "manifest": manifest,
        "manifest_sha256": _manifest_digest(manifest),
        "version_bytes": version_bytes,
        "version": version,
        "license_bytes": license_bytes,
    }


def _normalize_exclusion(value: str) -> str:
    _text_input(value, "VCS exclusion")
    if "\\" in value:
        raise InputError("VCS exclusion должен использовать POSIX separators")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise InputError(f"VCS exclusion должен быть normalized relative path: {value!r}")
    if not path.parts or any(part in {"", "."} for part in path.parts):
        raise InputError(f"VCS exclusion недопустим: {value!r}")
    if path.name not in VCS_NAMES:
        raise InputError(f"VCS exclusion не является .git/.hg/.svn entry: {value!r}")
    return value


def _valid_gitfile(data: bytes) -> bool:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if text.endswith("\n"):
        text = text[:-1]
    if not text or "\n" in text or "\r" in text or not text.startswith("gitdir: "):
        return False
    target = text.removeprefix("gitdir: ")
    return bool(target and target == target.strip())


def _classify_vcs(existing: Path, manifest: list[dict]) -> list[dict]:
    result = []
    for item in manifest:
        relative = item["path"]
        name = PurePosixPath(relative).name
        if name not in VCS_NAMES:
            continue
        if name == ".git" and item["type"] == "directory":
            classification = "git-directory"
        elif name == ".git" and item["type"] == "file":
            data = (existing / Path(*PurePosixPath(relative).parts)).read_bytes()
            if not _valid_gitfile(data):
                raise InspectionError(f"malformed regular .git gitfile: {relative}")
            classification = "gitfile"
        elif name == ".hg" and item["type"] == "directory":
            classification = "hg-directory"
        elif name == ".svn" and item["type"] == "directory":
            classification = "svn-directory"
        else:
            raise InspectionError(f"unsupported VCS metadata type: {relative} ({item['type']})")
        row = {"path": relative, "classification": classification}
        if classification == "gitfile":
            row["sha256"] = item["sha256"]
        result.append(row)
    return sorted(result, key=lambda item: item["path"])


def _portability_warnings(manifest: list[dict]) -> list[dict]:
    warnings = []
    siblings = {}
    for item in manifest:
        relative = item["path"]
        path = PurePosixPath(relative)
        name = path.name
        parent = path.parent.as_posix()
        reasons = []
        base = name.split(".", 1)[0].upper()
        if base in WINDOWS_RESERVED:
            reasons.append("Windows reserved basename")
        invalid = "".join(sorted(set(name) & WINDOWS_INVALID))
        if invalid:
            reasons.append(f"Windows-incompatible characters: {invalid}")
        if name.endswith((" ", ".")):
            reasons.append("Windows strips trailing space or dot")
        key = (parent, name.casefold())
        if key in siblings and siblings[key] != name:
            reasons.append(f"case-insensitive sibling collision with {siblings[key]}")
        siblings[key] = name
        for reason in reasons:
            warnings.append({"path": relative, "reason": reason})
    return sorted(warnings, key=lambda item: (item["path"], item["reason"]))


def _recognized_root_profiles(existing: Path, manifest: list[dict]) -> None:
    for item in manifest:
        path = PurePosixPath(item["path"])
        if len(path.parts) != 1 or item["type"] != "file" or not path.name.endswith(".profile"):
            continue
        try:
            parse_project_profile((existing / path.name).read_bytes(), path.name)
        except ProjectProfileError:
            continue
        raise InspectionError(f"existing Product содержит recognized root Project Profile: {path.name}")


def _inspect_existing(existing_product, exclusions: tuple[str, ...]) -> dict:
    existing = _regular_directory(Path(existing_product), "existing Product source")
    manifest = _scan_tree(existing, "existing Product source", reject_hardlinks=True)
    _recognized_root_profiles(existing, manifest)
    vcs = _classify_vcs(existing, manifest)
    detected = tuple(item["path"] for item in vcs)
    if detected != exclusions:
        missing = sorted(set(detected) - set(exclusions))
        unexpected = sorted(set(exclusions) - set(detected))
        raise InspectionError(
            "exact VCS exclusions не совпадают с inspection: "
            f"missing_authorization={missing}; unknown_authorization={unexpected}"
        )
    excluded = []
    for vcs_item in vcs:
        prefix = vcs_item["path"]
        for item in manifest:
            if item["path"] == prefix or item["path"].startswith(prefix + "/"):
                excluded.append(
                    {
                        "path": item["path"],
                        "type": item["type"],
                        "mode": item["mode"],
                        "action": "EXCLUDE",
                        "vcs_entry": prefix,
                        **({"sha256": item["sha256"]} if item["type"] == "file" else {}),
                    }
                )
    return {
        "root": existing,
        "identity": _identity(existing),
        "manifest": manifest,
        "manifest_sha256": _manifest_digest(manifest),
        "vcs": vcs,
        "excluded": sorted(excluded, key=lambda item: item["path"]),
        "warnings": _portability_warnings(manifest),
    }


def _target_component_checks(destination: Path, target: Path) -> None:
    try:
        name_max = os.pathconf(destination, "PC_NAME_MAX")
    except (OSError, ValueError):
        name_max = None
    if name_max is not None and name_max >= 0 and len(os.fsencode(target.name)) > name_max:
        raise InspectionError("target Workspace basename не представим на destination filesystem")
    try:
        path_max = os.pathconf(destination, "PC_PATH_MAX")
    except (OSError, ValueError):
        path_max = None
    if path_max is not None and path_max >= 0 and len(os.fsencode(target)) >= path_max:
        raise InspectionError("target Workspace path не представим на destination filesystem")


def _target_action_representation_checks(destination: Path, target: Path, actions: list[dict]) -> None:
    """Reject limits that the destination reports without requiring a write probe."""
    try:
        name_max = os.pathconf(destination, "PC_NAME_MAX")
    except (OSError, ValueError):
        name_max = None
    try:
        path_max = os.pathconf(destination, "PC_PATH_MAX")
    except (OSError, ValueError):
        path_max = None
    for item in actions:
        relative = PurePosixPath(item["path"])
        if name_max is not None and name_max >= 0:
            for component in relative.parts:
                if len(os.fsencode(component)) > name_max:
                    raise InspectionError(
                        f"target path component превышает destination PC_NAME_MAX: {item['path']}"
                    )
        candidate = target.joinpath(*relative.parts)
        if path_max is not None and path_max >= 0 and len(os.fsencode(candidate)) >= path_max:
            raise InspectionError(
                f"target path превышает destination PC_PATH_MAX: {item['path']}"
            )


def _commit_primitive():
    """Return the proven local no-replace commit primitive without mutating paths."""
    if sys.platform.startswith("linux"):
        try:
            library = ctypes.CDLL(None, use_errno=True)
        except OSError as error:
            raise InspectionError("platform C library недоступна для atomic commit") from error
        renameat2 = getattr(library, "renameat2", None)
        if renameat2 is None:
            raise InspectionError("platform не предоставляет atomic renameat2 RENAME_NOREPLACE")
        return "linux-renameat2-RENAME_NOREPLACE", renameat2
    if os.name == "nt":
        return "windows-directory-rename-no-replace", None
    raise InspectionError("platform не имеет доказанного atomic no-replace directory commit")


def _destination_collision(destination: Path, target_name: str, *, allow_transaction_target: bool) -> None:
    try:
        entries = sorted(destination.iterdir(), key=lambda path: path.name)
    except OSError as error:
        raise InspectionError(f"destination parent недоступен: {error}") from error
    matches = [path for path in entries if path.name.casefold() == target_name.casefold()]
    if not matches:
        return
    if (
        allow_transaction_target
        and len(matches) == 1
        and matches[0].name == target_name
        and matches[0].is_dir()
        and not matches[0].is_symlink()
        and (matches[0] / TRANSACTION_MARKER).is_file()
        and not (matches[0] / TRANSACTION_MARKER).is_symlink()
    ):
        return
    actual = ", ".join(path.name for path in matches)
    raise InspectionError(f"destination collision для {target_name}: {actual}")


def _read_source_file(source: Path, relative: str) -> bytes:
    path = source / Path(*PurePosixPath(relative).parts)
    try:
        info = os.lstat(path)
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise InspectionError(f"deployable source не regular file: {relative}")
        return path.read_bytes()
    except OSError as error:
        raise InspectionError(f"deployable source недоступен: {relative}: {error}") from error


def _generated_readme(slug: str, display_name: str, license_bytes: bytes) -> bytes:
    prefix = (
        f"# Workspace {display_name}\n\n"
        f"`WS_{slug}` — управляемый Workspace продукта `{slug}`. "
        "Project Profile хранит composition, а Product root является самостоятельной delivery boundary.\n\n"
        "## Начальное состояние\n\n"
        "- `WROAD-000001 active`;\n"
        "- active WBACK/WPLAN count `0/0`;\n"
        "- checkpoint `WROAD-000001-OWNER-PLANNING`;\n"
        "- initial SoT `sot_files`.\n\n"
        "Product architecture, первый WBACK/WPLAN, лицензия продукта и переход SoT требуют отдельных решений владельца.\n\n"
        "[После Project Start](docs/user/after-project-start.md) поможет выбрать первую задачу. [Документация](docs/README.md) объясняет модель и проверки.\n\n"
        "## Лицензия BytePress Harness\n\n"
    ).encode("utf-8")
    return prefix + license_bytes


def _workspace_generated_files(source: Path, slug: str, display_name: str, wroad: str, version: str, license_bytes: bytes) -> dict[str, bytes]:
    readme = _generated_readme(slug, display_name, license_bytes)
    agents = (
        f"# AGENTS.md — рабочая карта Workspace {slug}\n\n"
        f"Workspace root: `WS_{slug}`. Product root и delivery boundary: `{slug}/`.\n\n"
        f"Единственный machine owner composition и SoT — `{slug}.profile`; начальный mode — `sot_files`. "
        "Git CLI не вызывается до отдельного owner-gated перехода.\n\n"
        "Человек управляет, агенты исполняют. Прочитайте `SYSTEM.md`, Project Profile и root `plans/`; "
        "technical PASS не является Product Acceptance.\n"
    ).encode("utf-8")
    system = (
        f"# SYSTEM.md — Workspace {slug}\n\n"
        "## Composition\n\n"
        f"- root Project Profile: `{slug}.profile`;\n"
        f"- fixed Product root/delivery boundary: `{slug}/`;\n"
        f"- deployed Harness version: `{version}`;\n"
        "- configured SoT owner: Project Profile;\n"
        "- planning authority: root `WROAD -> WBACK -> WPLAN`.\n\n"
        "## Invariants\n\n"
        "1. Workspace управляет работой над Product Unit; Product Unit не хранит текущий Workspace route.\n"
        "2. В non-executing checkpoint active WPLAN count равен `0`; первая permanent mutation нового прохода создаёт active WPLAN.\n"
        "3. `sot_files` не читает Git. Product code/checks не исполняются при discovery Profile.\n"
        "4. Technical PASS, owner acceptance, Product Acceptance и Release Authorization являются разными фактами.\n"
    ).encode("utf-8")
    roadmap_template = _read_source_file(source, "templates/workspace-roadmap.md").decode("utf-8")
    road_separator = "|---|---|---|---|\n"
    if roadmap_template.count(road_separator) != 1:
        raise InspectionError("workspace-roadmap template contract mismatch")
    roadmap = roadmap_template.replace(
        road_separator,
        road_separator + f"| WROAD-000001 | active | {wroad} | Owner planning: определить первый WBACK/WPLAN. |\n",
    ).replace("WS_<Slug>", f"WS_{slug}")
    backlog_template = _read_source_file(source, "templates/workspace-backlog.md").decode("utf-8")
    old_route = """```text
<WROAD> active
-> <WBACK> active
-> <WPLAN active|absent at non-executing checkpoint>
```"""
    new_route = """```text
WROAD-000001 active
active WBACK count 0
active WPLAN count 0
```

NON_EXECUTING_CHECKPOINT: `WROAD-000001-OWNER-PLANNING`."""
    if backlog_template.count(old_route) != 1:
        raise InspectionError("workspace-backlog template contract mismatch")
    backlog = backlog_template.replace(old_route, new_route).replace("WS_<Slug>", f"WS_{slug}")
    completed = _read_source_file(source, "templates/workspace-plan-completed-readme.md")
    files = {
        "README.md": readme,
        "AGENTS.md": agents,
        "SYSTEM.md": system,
        "plans/roadmap.md": roadmap.encode("utf-8"),
        "plans/backlog.md": backlog.encode("utf-8"),
        "plans/completed/README.md": completed,
        "logs/README.md": "# Журналы Workspace\n\nТипизированные записи ведутся append-only; Project Start не синтезирует owner acceptance.\n".encode("utf-8"),
        "logs/decisions.md": "# Решения владельца\n\nProject Start не создаёт синтетического решения владельца.\n".encode("utf-8"),
        "logs/changes.md": (f"# Изменения Workspace\n\n- Project Start материализовал `WS_{slug}` из Harness `{version}`.\n").encode("utf-8"),
        "logs/quality.md": "# Качество Workspace\n\n- Начальная структурная проверка Project Start: PASS.\n- Product Acceptance: не выполнялась.\n".encode("utf-8"),
        "logs/sessions.md": "# Сессии Workspace\n\n- Initial checkpoint: WROAD-000001-OWNER-PLANNING.\n".encode("utf-8"),
        "logs/risks.md": "# Риски Workspace\n\nТекущие риски не зарегистрированы.\n".encode("utf-8"),
        "logs/terminology.md": "# Терминология Workspace\n\nБудущие изменения ведутся append-only.\n".encode("utf-8"),
        "logs/history.md": "# История Workspace\n\nProject Start создал начальную composition Workspace.\n".encode("utf-8"),
        "research/00-index.md": "# Исследования Workspace\n\nАктивные исследования отсутствуют. Следующий research ID: `01`.\n".encode("utf-8"),
        "docs/README.md": "# Документация Workspace\n\n`docs/` хранит принадлежащие Workspace архитектурные, технические, терминологические и пользовательские документы. Документация продукта принадлежит Product root.\n".encode("utf-8"),
        "docs/architecture/README.md": "# Архитектура Workspace\n\n- [architecture.md](architecture.md)\n- [domain-model.md](domain-model.md)\n- [project-profile.md](project-profile.md)\n".encode("utf-8"),
        "docs/architecture/architecture.md": (
            f"# Архитектура Workspace {slug}\n\n"
            f"`WS_{slug}/` содержит Workspace Harness, root `{slug}.profile` и единственный Product root `{slug}/`. "
            "Workspace управляет работой, а Product Unit остаётся самостоятельной delivery boundary и не хранит текущий маршрут.\n\n"
            "Planning, logs и Workspace research принадлежат root Workspace. Product code, tests, docs и выбранная продуктом лицензия принадлежат Product root.\n"
        ).encode("utf-8"),
        "docs/architecture/domain-model.md": (
            f"# Доменная модель Workspace {slug}\n\n"
            f"- `Project Profile` — root `{slug}.profile`, machine owner composition и `sot_mode`.\n"
            f"- `Product Unit` — самостоятельный продукт в fixed Product root `{slug}/`.\n"
            "- `WROAD -> WBACK -> WPLAN` — Workspace-owned planning authority.\n"
            "- `Product Part` — только явно объявленная optional часть; наличие каталога само по себе её не создаёт.\n\n"
            "Authorization digest Project Start связывает одну exact materialization, но не является planning authority или owner acceptance.\n"
        ).encode("utf-8"),
        "docs/architecture/project-profile.md": (
            "# Project Profile и ввод-вывод Workspace\n\n"
            f"Root `{slug}.profile` сериализован canonical owner `project_profile.py`; Slug выводится из filename stem. "
            f"Fixed Product root и delivery boundary равны `{slug}/`.\n\n"
            "Project Start создал minimal Profile с полями `schema_version`, `harness_version`, `sot_mode`, `display_name`; "
            "optional `product_parts` и `product_native_checks` отсутствуют. Parsing Profile не исполняет Product code или declared commands.\n\n"
            "Для actual-delta проверки caller до mutation получает complete TSV командой "
            "`python3 -B tools/check_workspace.py --workspace <path> --print-baseline-manifest > <external-manifest>`; "
            "active WPLAN связывает exact CREATE/UPDATE/PRESERVE/REMOVE с фактическими path/type/content/POSIX-mode изменениями.\n"
        ).encode("utf-8"),
        "docs/technical/README.md": "# Техническая документация Workspace\n\nТехнические контракты этого каталога применяются через root WPLAN и не создают owner authority.\n".encode("utf-8"),
        "docs/terminology/README.md": "# Терминология Workspace\n\nКанонический словарь: [glossary.md](glossary.md).\n".encode("utf-8"),
        "docs/user/README.md": "# Пользовательская документация Workspace\n\n- [Первый старт](first-start.md)\n- [Режим источника истины](source-of-truth-mode.md)\n".encode("utf-8"),
        "docs/user/first-start.md": (
            f"# Первый старт Workspace {slug}\n\n"
            f"Project Start завершён. Прочитайте root `README.md`, `AGENTS.md`, `SYSTEM.md`, `{slug}.profile` и `plans/`. "
            "Текущий checkpoint — `WROAD-000001-OWNER-PLANNING`; первый WBACK/WPLAN требует отдельного решения владельца.\n"
        ).encode("utf-8"),
        "docs/user/source-of-truth-mode.md": (
            "# Режим источника истины\n\n"
            f"Текущий устойчивый `sot_mode` Workspace хранится только в root `{slug}.profile`; начальное значение — `sot_files`. "
            "Иной режим и любые Git/GitHub actions требуют отдельного owner-gated перехода.\n\n"
            "SoT не разрешает реализацию, owner acceptance, Product Acceptance, release или closeout.\n"
        ).encode("utf-8"),
        "sops/verify-work.md": "# Проверка Workspace\n\n`tools/check_workspace.py` read-only читает required evidence kind, owner-gate policy и exact required owner decision kind из одной transition row `docs/technical/phase-gates.md`; WPLAN хранит только projections, а gate name или generic positive record не заменяет canonical kind. Checker печатает complete baseline через `--print-baseline-manifest` и с optional `--baseline-manifest` проверяет actual delta без исполнения Product code. `tools/check_product.py` отдельно проверяет composition; native checks исполняются только с explicit option и positive timeout. Product behavior для immutable evidence запускается только в отдельной разрешённой копии; lifecycle `OD-*`, Product Acceptance и Release Authorization не объединяются.\n".encode("utf-8"),
        "tools/README.md": "# Инструменты Workspace\n\n`project_profile.py` — canonical parser/serializer Project Profile. `check_workspace.py` проверяет `SDLC_TRANSITION: v1` и читает required evidence kind, owner-gate policy и exact required owner decision kind из одной transition row `docs/technical/phase-gates.md`; hidden transition-to-kind mapping и WPLAN gate-name override отсутствуют. Checker read-only печатает complete TSV через `--print-baseline-manifest` и принимает его через optional `--baseline-manifest`, не исполняя Product. `check_product.py` проверяет Product composition и запускает declared native checks только явно. Checker не вызывает другой checker автоматически и не принимает owner gate.\n".encode("utf-8"),
        "tests/README.md": "# Тесты Workspace\n\n`test_project_profile.py` проверяет развёрнутый контракт Profile; `test_check_workspace.py` — neutral executable SDLC/authority/actual-delta fixtures. Product tests принадлежат Product root и не создаются Project Start.\n".encode("utf-8"),
    }
    # Generated instance navigation is separate from Product documentation.
    files["docs/README.md"] = (
        "# Документация Workspace\n\n"
        "[Следующие действия](user/README.md) после создания среды. "
        "[Архитектура](architecture/README.md) объясняет состав проекта. "
        "[Технические темы](technical/README.md) и [термины](terminology/README.md) дают точные ответы. "
        "Документация самого продукта принадлежит его корню.\n"
    ).encode("utf-8")
    files["docs/architecture/project-profile.md"] = _read_source_file(source, "docs/architecture/project-profile.md")
    start_contract = _read_source_file(source, "docs/technical/project-start.md").decode("utf-8")
    start_contract = start_contract.replace(
        "Пользовательский пример находится в [инструкции первого запуска](../user/first-start.md); здесь задан точный контракт преобразования.",
        "[Начальное состояние](../user/first-start.md) описано отдельно; здесь задан контракт создания среды из исходной поставки."
    )
    files["docs/technical/project-start.md"] = start_contract.encode("utf-8")
    style = _read_source_file(source, "docs/technical/system-style.md").decode("utf-8")
    style = style.replace('[Паспорт](../product/product-passport.md) хранит текущую языковую поддержку. ', '')
    files["docs/technical/system-style.md"] = style.encode("utf-8")
    review_contract = _read_source_file(source, "sops/verify-work.md").decode("utf-8")
    review_contract = "\n## Documentation review" + review_contract.split("## Documentation review", 1)[1]
    files["sops/verify-work.md"] += review_contract.encode("utf-8")
    files["docs/user/README.md"] = (
        "# Пользовательские задачи Workspace\n\n"
        "- [Начальное состояние](first-start.md).\n"
        "- [После Project Start](after-project-start.md).\n"
        "- [Режим источника истины](source-of-truth-mode.md).\n"
        "- [Существующий продукт](existing-product.md).\n"
        "- [Обновление Workspace](workspace-update.md).\n"
        "- [Переход 0.5.1 → 0.5.2](migration-0.5.1-to-0.5.2.md).\n"
        "- [Подготовка GitHub](github-repository-preparation.md).\n"
    ).encode("utf-8")
    files["docs/technical/README.md"] = _read_source_file(source, "docs/technical/README.md")
    files["docs/user/source-of-truth-mode.md"] = _read_source_file(source, "docs/user/source-of-truth-mode.md")
    files["docs/architecture/README.md"] = _read_source_file(source, "docs/architecture/README.md")
    files["docs/terminology/README.md"] = _read_source_file(source, "docs/terminology/README.md")
    # No copied path may also be generated; source-required inputs are explicit.
    return files


def _deploy_copy_paths(source: Path) -> list[str]:
    paths = sorted(DEPLOY_COPY_FILES)
    if len(paths) != len(set(paths)):
        raise InspectionError("fixed deployable manifest содержит duplicate path")
    for relative in paths:
        _read_source_file(source, relative)
    return paths


def _file_action(path: str, data: bytes, *, action: str, mode: str, source_path: str | None = None, include_content: bool = False) -> dict:
    row = {
        "path": path,
        "action": action,
        "type": "file",
        "mode": mode,
        "size": len(data),
        "sha256": _sha256(data),
    }
    if source_path is not None:
        row["source_path"] = source_path
    if include_content:
        try:
            row["content_utf8"] = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise InspectionError(f"generated file должен быть UTF-8: {path}") from error
    return row


def _add_parent_directories(actions: list[dict], file_paths: list[str], explicit: dict[str, str]) -> None:
    directories = dict(explicit)
    for relative in file_paths:
        parent = PurePosixPath(relative).parent
        while parent.as_posix() not in {".", ""}:
            directories.setdefault(parent.as_posix(), "0755")
            parent = parent.parent
    existing = {item["path"] for item in actions}
    for path, mode in sorted(directories.items()):
        if path not in existing:
            actions.append({"path": path, "action": "CREATE", "type": "directory", "mode": mode})


def _build_actions(distribution: dict, slug: str, display_name: str, wroad: str, existing: dict | None) -> tuple[list[dict], dict[str, bytes]]:
    source = distribution["root"]
    generated = _workspace_generated_files(
        source, slug, display_name, wroad, distribution["version"], distribution["license_bytes"]
    )
    profile_name = f"{slug}.profile"
    profile_bytes = serialize_project_profile(
        profile_name,
        {
            "schema_version": 1,
            "harness_version": distribution["version"],
            "sot_mode": "sot_files",
            "display_name": display_name,
        },
    )
    generated[profile_name] = profile_bytes
    actions = []
    for relative in _deploy_copy_paths(source):
        data = _read_source_file(source, relative)
        info = os.lstat(source / Path(*PurePosixPath(relative).parts))
        actions.append(
            _file_action(relative, data, action="COPY", mode=_mode(info), source_path=relative)
        )
    for relative, data in sorted(generated.items()):
        actions.append(_file_action(relative, data, action="TRANSFORM", mode="0644", include_content=True))
    explicit_directories = {"plans/active": "0755"}
    product_root_mode = "0755"
    if existing is not None:
        product_root_mode = _mode(os.lstat(existing["root"]))
    explicit_directories[slug] = product_root_mode
    excluded_paths = {item["path"] for item in (existing["excluded"] if existing else [])}
    if existing is not None:
        source_map = _manifest_map(existing["manifest"])
        for relative, item in sorted(source_map.items()):
            if relative in excluded_paths:
                continue
            target_relative = f"{slug}/{relative}"
            if item["type"] == "directory":
                actions.append(
                    {"path": target_relative, "action": "COPY", "type": "directory", "mode": item["mode"], "source_path": relative}
                )
            else:
                data = (existing["root"] / Path(*PurePosixPath(relative).parts)).read_bytes()
                actions.append(
                    _file_action(target_relative, data, action="COPY", mode=item["mode"], source_path=relative)
                )
    file_paths = [item["path"] for item in actions if item["type"] == "file"]
    _add_parent_directories(actions, file_paths, explicit_directories)
    actions = sorted(actions, key=lambda item: (item["path"], item["type"], item["action"]))
    paths = [item["path"] for item in actions]
    if len(paths) != len(set(paths)):
        duplicates = sorted(path for path in set(paths) if paths.count(path) > 1)
        raise InspectionError(f"target action manifest duplicate paths: {duplicates}")
    folded = {}
    for path in paths:
        key = path.casefold()
        if key in folded and folded[key] != path:
            # Linux can represent this; authorization carries a portability warning
            # from the existing Product manifest. Harness-generated paths never collide.
            pass
        folded[key] = path
    return actions, generated


def _human_preview(payload: dict, digest: str) -> str:
    lines = [
        "Project Start v1 preview",
        f"state: PREVIEW_READY",
        f"source distribution: {payload['source_distribution']['identity']['path']}",
        f"destination: {payload['target']['workspace_path']}",
        f"Product: {payload['product']['mode']} -> {payload['inputs']['slug']}/",
        "initial SoT: sot_files",
        "planning: WROAD-000001 active; active WBACK/WPLAN 0/0; WROAD-000001-OWNER-PLANNING",
        "VCS exclusions:",
    ]
    lines.extend(
        f"- {item['path']} [{item['classification']}]" for item in payload["vcs_exclusions"]
    )
    if not payload["vcs_exclusions"]:
        lines.append("- none")
    lines.append("Portability warnings:")
    lines.extend(f"- {item['path']}: {item['reason']}" for item in payload["warnings"])
    if not payload["warnings"]:
        lines.append("- none")
    lines.append("Exact path/action manifest:")
    lines.extend(
        f"- {item['action']} {item['type']} {item['mode']} {item['path']}"
        for item in payload["actions"]
    )
    lines.append("Verification plan:")
    lines.extend(f"- {item['id']}: {item['expected']}" for item in payload["verification_plan"])
    lines.extend(
        [
            "Canonical Project Profile:",
            payload["profile"]["content_utf8"].rstrip("\n"),
            "Generated Workspace README:",
            payload["generated_readme"]["content_utf8"].rstrip("\n"),
            f"PREVIEW_SHA256: {digest}",
        ]
    )
    return "\n".join(lines) + "\n"


def _build_preview(
    *,
    source_distribution,
    destination_parent,
    slug,
    display_name,
    product_mode,
    wroad,
    existing_product=None,
    exclude_vcs_paths=(),
    allow_transaction_target=False,
) -> dict:
    slug = _text_input(slug, "Slug")
    display_name = _text_input(display_name, "display name")
    wroad = _text_input(wroad, "WROAD-000001 formulation", forbid_pipe=True)
    product_mode = _text_input(product_mode, "Product mode")
    if product_mode not in {"new", "existing"}:
        raise InputError("Product mode должен быть new или existing")
    normalized_exclusions = tuple(_normalize_exclusion(value) for value in exclude_vcs_paths)
    if len(normalized_exclusions) != len(set(normalized_exclusions)):
        raise InputError("VCS exclusions должны быть unique")
    exclusions = tuple(sorted(normalized_exclusions))
    if product_mode == "new" and (existing_product is not None or exclusions):
        raise InputError("new Product не принимает existing source или VCS exclusions")
    if product_mode == "existing" and existing_product is None:
        raise InputError("existing Product требует --existing-product")
    distribution = _inspect_distribution(source_distribution)
    destination = _regular_directory(Path(destination_parent), "destination parent")
    commit_primitive, _ = _commit_primitive()
    try:
        profile_bytes = serialize_project_profile(
            f"{slug}.profile",
            {
                "schema_version": 1,
                "harness_version": distribution["version"],
                "sot_mode": "sot_files",
                "display_name": display_name,
            },
        )
    except ProjectProfileError as error:
        raise InputError(str(error)) from error
    target = destination / f"WS_{slug}"
    _target_component_checks(destination, target)
    _destination_collision(destination, target.name, allow_transaction_target=allow_transaction_target)
    if _overlap(target, distribution["root"]):
        raise InspectionError("source distribution и final target имеют unsafe overlap")
    existing = None
    if product_mode == "existing":
        existing = _inspect_existing(existing_product, exclusions)
        if _overlap(existing["root"], distribution["root"]):
            raise InspectionError("source distribution и existing Product имеют unsafe overlap")
        if _overlap(target, existing["root"]):
            raise InspectionError("existing Product и final target имеют unsafe overlap")
    actions, generated = _build_actions(distribution, slug, display_name, wroad, existing)
    _target_action_representation_checks(destination, target, actions)
    readme_bytes = generated["README.md"]
    if not readme_bytes.endswith(b"## \xd0\x9b\xd0\xb8\xd1\x86\xd0\xb5\xd0\xbd\xd0\xb7\xd0\xb8\xd1\x8f BytePress Harness\n\n" + distribution["license_bytes"]):
        raise InspectionError("generated README license contract mismatch")
    inputs = {
        "slug": slug,
        "display_name": display_name,
        "product_mode": product_mode,
        "wroad": wroad,
        "source_distribution": str(distribution["root"]),
        "destination_parent": str(destination),
        "existing_product": str(existing["root"]) if existing else None,
        "vcs_exclusions": list(exclusions),
    }
    payload = {
        "preview_schema_version": PREVIEW_SCHEMA_VERSION,
        "operation": "project_start",
        "inputs": inputs,
        "source_distribution": {
            "identity": distribution["identity"],
            "manifest": distribution["manifest"],
            "manifest_sha256": distribution["manifest_sha256"],
            "version": distribution["version"],
            "version_bytes_utf8": distribution["version_bytes"].decode("utf-8"),
            "version_sha256": _sha256(distribution["version_bytes"]),
        },
        "target": {
            "destination_parent": str(destination),
            "destination_identity": _identity(destination),
            "workspace_path": str(target),
            "workspace_basename": target.name,
            "product_root": f"{slug}/",
            "profile_filename": f"{slug}.profile",
        },
        "product": {
            "mode": product_mode,
            "source_path": str(existing["root"]) if existing else None,
            "source_identity": existing["identity"] if existing else None,
            "source_manifest": existing["manifest"] if existing else [],
            "source_manifest_sha256": existing["manifest_sha256"] if existing else None,
        },
        "vcs_exclusions": existing["vcs"] if existing else [],
        "exclusions": existing["excluded"] if existing else [],
        "initial_sot": "sot_files",
        "profile": {
            "filename": f"{slug}.profile",
            "content_utf8": profile_bytes.decode("utf-8"),
            "sha256": _sha256(profile_bytes),
            "fields": ["schema_version", "harness_version", "sot_mode", "display_name"],
        },
        "generated_readme": {
            "path": "README.md",
            "content_utf8": readme_bytes.decode("utf-8"),
            "sha256": _sha256(readme_bytes),
        },
        "planning": {
            "wroad_id": "WROAD-000001",
            "wroad_status": "active",
            "wroad_text": wroad,
            "active_wback_count": 0,
            "active_wplan_count": 0,
            "checkpoint": "WROAD-000001-OWNER-PLANNING",
        },
        "actions": actions,
        "actions_sha256": _manifest_digest(actions),
        "warnings": existing["warnings"] if existing else [],
        "verification_plan": list(VERIFICATION_PLAN),
        "staging_commit": {
            "staging": "deterministic sibling after authorization; transient path excluded from digest",
            "commit": commit_primitive,
            "recovery": "matching repeated apply only; mismatch or unknown state RECOVERY_REQUIRED",
        },
    }
    digest = _sha256(canonical_payload_bytes(payload))
    return {
        "operation": "preview",
        "state": "PREVIEW_READY",
        "authorization_payload": payload,
        "preview_sha256": digest,
        "warnings": payload["warnings"],
        "vcs_exclusions": payload["vcs_exclusions"],
        "human_readable": _human_preview(payload, digest),
    }


def build_preview(**inputs) -> dict:
    """Perform read-only inspection and return the canonical authorization preview."""
    return _build_preview(**inputs, allow_transaction_target=False)


def _staging_path(destination: Path, slug: str, digest: str) -> Path:
    return destination / f".WS_{slug}.project-start.{digest[:16]}.staging"


def _marker_document(payload: dict, digest: str, state: str) -> dict:
    return {
        "preview_schema_version": PREVIEW_SCHEMA_VERSION,
        "authorization_digest": digest,
        "normalized_inputs": payload["inputs"],
        "destination_identity": payload["target"]["destination_identity"],
        "expected_final_root": payload["target"]["workspace_path"],
        "source_manifest_sha256": payload["source_distribution"]["manifest_sha256"],
        "existing_manifest_sha256": payload["product"]["source_manifest_sha256"],
        "actions_sha256": payload["actions_sha256"],
        "transaction_state": state,
    }


def _atomic_marker(root: Path, document: dict) -> None:
    marker = root / TRANSACTION_MARKER
    temporary = root / TRANSACTION_MARKER_TEMP
    data = _canonical_json_bytes(document)
    try:
        info = os.lstat(root)
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise RecoveryRequired("transaction root не является owned regular directory")
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, marker)
    except ProjectStartError:
        raise
    except OSError as error:
        raise StagingError(f"transaction marker write failed: {error}") from error


def _read_marker(root: Path) -> dict:
    marker = root / TRANSACTION_MARKER
    try:
        info = os.lstat(marker)
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise RecoveryRequired("transaction marker type mismatch")
        data = marker.read_bytes()
        if not data.endswith(b"\n"):
            raise RecoveryRequired("transaction marker is not canonical")
        value = json.loads(data.decode("utf-8"))
    except RecoveryRequired:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RecoveryRequired(f"transaction marker unreadable: {error}") from error
    if not isinstance(value, dict):
        raise RecoveryRequired("transaction marker must be object")
    return value


def _marker_matches(marker: dict, payload: dict, digest: str) -> bool:
    expected = _marker_document(payload, digest, marker.get("transaction_state"))
    return marker == expected


def _expected_materialized_paths(payload: dict) -> set[str]:
    return {item["path"] for item in payload["actions"]}


def _safe_owned_tree(root: Path, payload: dict, digest: str) -> None:
    marker = _read_marker(root)
    if not _marker_matches(marker, payload, digest):
        raise RecoveryRequired("transaction marker/digest/inputs/destination mismatch")
    allowed = _expected_materialized_paths(payload) | {TRANSACTION_MARKER, TRANSACTION_MARKER_TEMP}
    for base, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        directories.sort()
        filenames.sort()
        for name in directories + filenames:
            path = Path(base) / name
            relative = path.relative_to(root).as_posix()
            info = os.lstat(path)
            if stat.S_ISLNK(info.st_mode) or not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
                raise RecoveryRequired(f"owned staging contains unsupported node: {relative}")
            if relative not in allowed:
                raise RecoveryRequired(f"owned staging contains unknown entry: {relative}")


def _cleanup_owned_staging(root: Path, payload: dict, digest: str) -> None:
    _safe_owned_tree(root, payload, digest)
    try:
        shutil.rmtree(root)
    except OSError as error:
        raise RecoveryRequired(f"owned staging cleanup failed: {error}") from error


def _copy_regular_file(source: Path, target: Path, mode: int) -> None:
    try:
        info = os.lstat(source)
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise StagingError(f"copy source type drift: {source}")
        with source.open("rb") as source_stream, target.open("xb") as target_stream:
            shutil.copyfileobj(source_stream, target_stream, length=1024 * 1024)
        os.chmod(target, mode)
    except ProjectStartError:
        raise
    except OSError as error:
        raise StagingError(f"copy failed {source} -> {target}: {error}") from error


def _materialize_workspace(staging: Path, payload: dict) -> None:
    distribution = Path(payload["source_distribution"]["identity"]["path"])
    existing = Path(payload["product"]["source_path"]) if payload["product"]["source_path"] else None
    directory_actions = sorted(
        (item for item in payload["actions"] if item["type"] == "directory"),
        key=lambda item: (len(PurePosixPath(item["path"]).parts), item["path"]),
    )
    file_actions = sorted(
        (item for item in payload["actions"] if item["type"] == "file"),
        key=lambda item: item["path"],
    )
    try:
        for item in directory_actions:
            target = staging / Path(*PurePosixPath(item["path"]).parts)
            target.mkdir()
        for item in file_actions:
            target = staging / Path(*PurePosixPath(item["path"]).parts)
            if item["action"] == "TRANSFORM":
                data = item["content_utf8"].encode("utf-8")
                if _sha256(data) != item["sha256"]:
                    raise StagingError(f"generated bytes digest mismatch: {item['path']}")
                with target.open("xb") as stream:
                    stream.write(data)
                os.chmod(target, int(item["mode"], 8))
            elif item["action"] == "COPY":
                if item["path"].startswith(payload["inputs"]["slug"] + "/"):
                    if existing is None:
                        raise StagingError("existing Product action without source")
                    source = existing / Path(*PurePosixPath(item["source_path"]).parts)
                else:
                    source = distribution / Path(*PurePosixPath(item["source_path"]).parts)
                _copy_regular_file(source, target, int(item["mode"], 8))
            else:
                raise StagingError(f"unknown file action: {item['action']}")
        for item in sorted(directory_actions, key=lambda row: (-len(PurePosixPath(row["path"]).parts), row["path"])):
            target = staging / Path(*PurePosixPath(item["path"]).parts)
            os.chmod(target, int(item["mode"], 8))
    except ProjectStartError:
        raise
    except OSError as error:
        raise StagingError(f"staging materialization failed: {error}") from error


def _actual_materialized_manifest(root: Path) -> list[dict]:
    manifest = _scan_tree(root, "materialized Workspace", reject_hardlinks=False)
    return [
        item for item in manifest
        if item["path"] not in {TRANSACTION_MARKER, TRANSACTION_MARKER_TEMP}
    ]


def _expected_manifest_from_actions(actions: list[dict]) -> list[dict]:
    expected = []
    for item in actions:
        row = {key: item[key] for key in ("path", "type", "mode")}
        if item["type"] == "file":
            row.update({"size": item["size"], "sha256": item["sha256"]})
        expected.append(row)
    return sorted(expected, key=lambda item: item["path"])


def _markdown_targets(text: str):
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        raw = match.group(1).strip()
        if raw.startswith("<") and ">" in raw:
            raw = raw[1:raw.index(">")]
        elif " " in raw:
            raw = raw.split(" ", 1)[0]
        yield unquote(raw)


def _verify_markdown_links(root: Path) -> None:
    resolved_root = root.resolve()
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for target in _markdown_targets(text):
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "codexlog:")):
                continue
            path_part = target.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue
            pure = PurePosixPath(path_part)
            if pure.is_absolute():
                raise StagingError(f"absolute local Markdown link: {path.relative_to(root)} -> {target}")
            candidate = path.parent.joinpath(*pure.parts)
            try:
                candidate.resolve(strict=False).relative_to(resolved_root)
            except (OSError, ValueError) as error:
                raise StagingError(f"escaping Markdown link: {path.relative_to(root)} -> {target}") from error
            if not candidate.exists():
                raise StagingError(f"broken Markdown link: {path.relative_to(root)} -> {target}")


def _verify_staging_representation(root: Path, payload: dict, *, final: bool = False) -> None:
    expected = _expected_manifest_from_actions(payload["actions"])
    actual = _actual_materialized_manifest(root)
    if actual != expected:
        raise StagingError("materialized path/type/content/POSIX-mode manifest mismatch")
    slug = payload["inputs"]["slug"]
    profile_path = root / f"{slug}.profile"
    profile = parse_project_profile(profile_path.read_bytes(), profile_path.name)
    if (
        profile.schema_version != 1
        or profile.harness_version != payload["source_distribution"]["version"]
        or profile.sot_mode != "sot_files"
        or profile.display_name != payload["inputs"]["display_name"]
        or profile.product_parts
        or profile.product_native_checks
    ):
        raise StagingError("minimal Project Profile verification failed")
    product_root = root / slug
    if not product_root.is_dir() or product_root.is_symlink():
        raise StagingError("Product root missing or invalid")
    if payload["product"]["mode"] == "new" and list(product_root.iterdir()):
        raise StagingError("new Product root must be empty")
    if payload["product"]["mode"] == "existing":
        excluded = {item["path"] for item in payload["exclusions"]}
        expected_product = [item for item in payload["product"]["source_manifest"] if item["path"] not in excluded]
        actual_product = _scan_tree(product_root, "copied Product", reject_hardlinks=False)
        if actual_product != expected_product:
            raise StagingError("existing Product copy-integrity mismatch")
    readme = (root / "README.md").read_bytes()
    license_bytes = Path(payload["source_distribution"]["identity"]["path"], "LICENSE").read_bytes()
    if not readme.endswith(b"## \xd0\x9b\xd0\xb8\xd1\x86\xd0\xb5\xd0\xbd\xd0\xb7\xd0\xb8\xd1\x8f BytePress Harness\n\n" + license_bytes):
        raise StagingError("Workspace README terminal license mismatch")
    for forbidden in ("LICENSE", "BYTEPRESS-LICENSE.txt", "licenses"):
        if (root / forbidden).exists() or (root / forbidden).is_symlink():
            raise StagingError(f"separate target Harness license artifact forbidden: {forbidden}")
    active = list((root / "plans" / "active").glob("WPLAN-*.md"))
    if active:
        raise StagingError("Project Start must not create active WPLAN")
    planning_text = (root / "plans" / "roadmap.md").read_text(encoding="utf-8") + (root / "plans" / "backlog.md").read_text(encoding="utf-8")
    if "WROAD-000001" not in planning_text or "WROAD-000001-OWNER-PLANNING" not in planning_text:
        raise StagingError("WROAD-only planning state mismatch")
    if "WBACK-000001" in planning_text or "WPLAN-000001" in planning_text:
        raise StagingError("Project Start created forbidden WBACK/WPLAN")
    _verify_markdown_links(root)
    if final:
        loaded = load_project_profile(root)
        if loaded.slug != slug or loaded.workspace_root != root.resolve():
            raise StagingError("final Project Profile contextual read-back failed")


def _assert_source_unchanged(payload: dict) -> None:
    source = Path(payload["source_distribution"]["identity"]["path"])
    if _identity(source) != payload["source_distribution"]["identity"]:
        raise RecoveryRequired("source distribution identity changed")
    manifest = _scan_tree(source, "source distribution read-back", reject_hardlinks=True)
    if manifest != payload["source_distribution"]["manifest"]:
        raise RecoveryRequired("source distribution manifest changed")
    if payload["product"]["mode"] == "existing":
        existing = Path(payload["product"]["source_path"])
        if _identity(existing) != payload["product"]["source_identity"]:
            raise RecoveryRequired("existing Product identity changed")
        existing_manifest = _scan_tree(existing, "existing Product read-back", reject_hardlinks=True)
        if existing_manifest != payload["product"]["source_manifest"]:
            raise RecoveryRequired("existing Product source manifest changed")


def _commit_staging(staging: Path, target: Path) -> None:
    if target.exists() or target.is_symlink():
        raise FileExistsError(errno.EEXIST, "target created concurrently", str(target))
    primitive, renameat2 = _commit_primitive()
    if primitive == "linux-renameat2-RENAME_NOREPLACE":
        renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        renameat2.restype = ctypes.c_int
        result = renameat2(-100, os.fsencode(staging), -100, os.fsencode(target), 1)
        if result != 0:
            error_number = ctypes.get_errno()
            if error_number == errno.EEXIST:
                raise FileExistsError(error_number, "target created concurrently", str(target))
            raise StagingError(f"atomic no-replace rename failed: {os.strerror(error_number)}")
    elif primitive == "windows-directory-rename-no-replace":
        os.rename(staging, target)


def _finalize_committed(target: Path, payload: dict, digest: str) -> dict:
    marker = _read_marker(target)
    if marker.get("transaction_state") != "COMMITTED" or not _marker_matches(marker, payload, digest):
        raise RecoveryRequired("committed target marker mismatch or unknown state")
    _verify_staging_representation(target, payload, final=True)
    _assert_source_unchanged(payload)
    try:
        (target / TRANSACTION_MARKER).unlink()
    except OSError as error:
        raise RecoveryRequired(f"committed target marker removal failed: {error}") from error
    return {
        "operation": "apply",
        "state": "OWNER_PLANNING",
        "checkpoint": "WROAD-000001-OWNER-PLANNING",
        "preview_sha256": digest,
        "target_workspace": str(target),
        "active_wback_count": 0,
        "active_wplan_count": 0,
    }


def _resume_or_prepare(staging: Path, target: Path, payload: dict, digest: str) -> tuple[Path, bool]:
    destination = staging.parent
    slug = payload["inputs"]["slug"]
    candidates = sorted(destination.glob(f".WS_{slug}.project-start.*.staging"))
    if candidates:
        if candidates != [staging]:
            raise RecoveryRequired("mismatched or multiple Project Start staging surfaces")
        marker = _read_marker(staging)
        if not _marker_matches(marker, payload, digest):
            raise RecoveryRequired("staging marker/digest/inputs/destination mismatch")
        state = marker.get("transaction_state")
        if state == "STAGING":
            _cleanup_owned_staging(staging, payload, digest)
        elif state in {"VERIFIED_STAGING", "COMMITTED"}:
            _safe_owned_tree(staging, payload, digest)
            _verify_staging_representation(staging, payload)
            _assert_source_unchanged(payload)
            _atomic_marker(staging, _marker_document(payload, digest, "COMMITTED"))
            _commit_staging(staging, target)
            return target, True
        else:
            raise RecoveryRequired(f"unknown transaction state: {state!r}")
    try:
        staging.mkdir(mode=0o755)
    except FileExistsError as error:
        raise RecoveryRequired("staging appeared concurrently") from error
    except OSError as error:
        raise StagingError(f"staging create failed: {error}") from error
    _atomic_marker(staging, _marker_document(payload, digest, "STAGING"))
    return staging, False


def apply_project(*, authorization_sha256, **inputs) -> dict:
    """Reinspect, bind exact authorization, stage, verify and commit one Workspace."""
    if not isinstance(authorization_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", authorization_sha256):
        raise InputError("authorization SHA-256 должен быть 64 lowercase hex")
    preview = _build_preview(**inputs, allow_transaction_target=True)
    digest = preview["preview_sha256"]
    if digest != authorization_sha256:
        raise AuthorizationError(
            f"authorization digest mismatch: expected {digest}, actual {authorization_sha256}"
        )
    payload = preview["authorization_payload"]
    destination = Path(payload["target"]["destination_parent"])
    target = Path(payload["target"]["workspace_path"])
    staging = _staging_path(destination, payload["inputs"]["slug"], digest)
    if _overlap(staging, Path(payload["source_distribution"]["identity"]["path"])):
        raise InspectionError("staging и source distribution имеют unsafe overlap")
    if payload["product"]["source_path"] and _overlap(staging, Path(payload["product"]["source_path"])):
        raise InspectionError("staging и existing Product имеют unsafe overlap")
    if target.exists() and (target / TRANSACTION_MARKER).is_file():
        return _finalize_committed(target, payload, digest)
    committed = False
    owned_root = None
    try:
        owned_root, committed = _resume_or_prepare(staging, target, payload, digest)
        if committed:
            return _finalize_committed(target, payload, digest)
        _materialize_workspace(staging, payload)
        _verify_staging_representation(staging, payload)
        _assert_source_unchanged(payload)
        _atomic_marker(staging, _marker_document(payload, digest, "VERIFIED_STAGING"))
        _verify_staging_representation(staging, payload)
        if target.exists() or target.is_symlink():
            raise FileExistsError(errno.EEXIST, "target created concurrently", str(target))
        _atomic_marker(staging, _marker_document(payload, digest, "COMMITTED"))
        _commit_staging(staging, target)
        committed = True
        owned_root = target
        return _finalize_committed(target, payload, digest)
    except RecoveryRequired:
        raise
    except Exception as error:
        if committed:
            raise RecoveryRequired(f"post-commit finalization failed: {error}") from error
        if staging.exists() and staging.is_dir() and not staging.is_symlink():
            try:
                _cleanup_owned_staging(staging, payload, digest)
            except RecoveryRequired:
                raise
        try:
            _assert_source_unchanged(payload)
        except RecoveryRequired:
            raise
        raise ApplyAborted(f"staging/apply aborted before commit: {error}") from error


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BytePress Project Start v1")
    subparsers = parser.add_subparsers(dest="operation", required=True)

    def inputs(command):
        command.add_argument("--source-distribution", required=True)
        command.add_argument("--destination-parent", required=True)
        command.add_argument("--slug", required=True)
        command.add_argument("--display-name", required=True)
        command.add_argument("--wroad", required=True)
        command.add_argument("--product", choices=("new", "existing"), required=True)
        command.add_argument("--existing-product")
        command.add_argument("--exclude-vcs-path", action="append", default=[])

    preview = subparsers.add_parser("preview", help="read-only canonical preview")
    inputs(preview)
    apply = subparsers.add_parser("apply", help="authorized staging and commit")
    inputs(apply)
    apply.add_argument("--authorization-sha256", required=True)
    return parser


def _arguments(namespace) -> dict:
    return {
        "source_distribution": namespace.source_distribution,
        "destination_parent": namespace.destination_parent,
        "slug": namespace.slug,
        "display_name": namespace.display_name,
        "product_mode": namespace.product,
        "wroad": namespace.wroad,
        "existing_product": namespace.existing_product,
        "exclude_vcs_paths": tuple(namespace.exclude_vcs_path),
    }


def main(argv=None) -> int:
    parser = _parser()
    namespace = parser.parse_args(argv)
    try:
        if namespace.operation == "preview":
            result = build_preview(**_arguments(namespace))
        else:
            result = apply_project(
                **_arguments(namespace),
                authorization_sha256=namespace.authorization_sha256,
            )
    except InputError as error:
        print(_display_json({"state": "INPUT_ERROR", "error": str(error)}), end="", file=sys.stderr)
        return 2
    except (AuthorizationError, InspectionError) as error:
        print(_display_json({"state": "ABORTED", "error": str(error)}), end="", file=sys.stderr)
        return 3
    except ApplyAborted as error:
        print(_display_json({"state": "ABORTED", "error": str(error)}), end="", file=sys.stderr)
        return 4
    except RecoveryRequired as error:
        print(_display_json({"state": "RECOVERY_REQUIRED", "error": str(error)}), end="", file=sys.stderr)
        return 5
    except Exception as error:  # fail closed; no traceback or implicit repair in public CLI
        print(_display_json({"state": "INTERNAL_ERROR", "error": str(error)}), end="", file=sys.stderr)
        return 6
    print(_display_json(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlparse

from bp_check_contract import (
    CHECK_ID_JSON_SCHEMAS,
    CHECK_ID_MARKDOWN_LINKS,
    CHECK_ID_TERM_CARDS,
    CHECK_ID_TERM_CONFLICT_DECISION,
    CHECK_ID_TERM_STATUS,
    CHECK_LEVEL,
    DEFAULT_FORMAT,
    EXTERNAL_SCHEMES,
    INDEX_SOURCES,
    OUTPUT_FORMATS,
    STATUS_BLOCKED,
    STATUS_FAIL,
    STATUS_OK,
    TERM_ALLOWED_CONFLICT_DECISIONS,
    TERM_ALLOWED_STATUSES,
    TERM_REQUIRED_FIELDS,
    TERM_REQUIRED_SECTIONS,
)

MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
REFERENCE_LINK = re.compile(r"^\[[^\]\n]+\]:\s+(\S+)", re.MULTILINE)
TERM_FIELD = re.compile(r"^([^:\n]+):\s*(.*)$", re.MULTILINE)
TERM_SECTION = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
INDEX_ITEM = re.compile(r"^-\s+.*?\b([A-Z]+-[0-9]{6})\b", re.MULTILINE)
QUALITY_HEADING = re.compile(r"^##\s+(QL-[0-9]{6})\s*$", re.MULTILINE)


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    status: str
    level: str
    path: str
    message: str


def rel_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(check_id: str, path: str, message: str) -> CheckResult:
    return CheckResult(check_id, STATUS_FAIL, CHECK_LEVEL, path, message)


def blocked(check_id: str, path: str, message: str) -> CheckResult:
    return CheckResult(check_id, STATUS_BLOCKED, CHECK_LEVEL, path, message)


def markdown_files(root: Path) -> list[Path]:
    ignored_parts = {".git", ".codex"}
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in ignored_parts for part in path.relative_to(root).parts)
    )


def schema_files(root: Path) -> list[Path]:
    schemas_dir = root / "Schemas"
    if not schemas_dir.exists():
        return []
    return sorted(schemas_dir.glob("*.json"))


def is_local_markdown_target(target: str) -> bool:
    stripped = target.strip()
    if not stripped or stripped.startswith("#"):
        return False
    parsed = urlparse(stripped)
    if parsed.scheme in EXTERNAL_SCHEMES or parsed.netloc:
        return False
    return True


def normalize_markdown_target(target: str) -> str:
    clean = target.strip().split()[0]
    clean = clean.split("#", 1)[0]
    return unquote(clean)


def resolve_markdown_target(root: Path, source: Path, target: str) -> Path | None:
    normalized = normalize_markdown_target(target)
    if not normalized:
        return None
    candidate = root / normalized.lstrip("/") if normalized.startswith("/") else source.parent / normalized
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def check_markdown_links(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    for path in markdown_files(root):
        text = read_text(path)
        targets = [match.group(1) for match in MARKDOWN_LINK.finditer(text)]
        targets.extend(match.group(1) for match in REFERENCE_LINK.finditer(text))
        for target in targets:
            if not is_local_markdown_target(target):
                continue
            resolved = resolve_markdown_target(root, path, target)
            if resolved is None:
                results.append(
                    fail(
                        CHECK_ID_MARKDOWN_LINKS,
                        rel_path(root, path),
                        f"локальная Markdown-ссылка выходит за пределы репозитория: {target}",
                    )
                )
                continue
            if not resolved.exists():
                results.append(
                    fail(
                        CHECK_ID_MARKDOWN_LINKS,
                        rel_path(root, path),
                        f"локальная Markdown-ссылка указывает на отсутствующий путь: {target}",
                    )
                )
    return results


def check_json_schemas(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    schemas_dir = root / "Schemas"
    if not schemas_dir.exists():
        return [blocked(CHECK_ID_JSON_SCHEMAS, "Schemas", "каталог Schemas отсутствует")]
    for path in schema_files(root):
        try:
            json.loads(read_text(path))
        except json.JSONDecodeError as error:
            results.append(
                fail(
                    CHECK_ID_JSON_SCHEMAS,
                    rel_path(root, path),
                    f"JSON-схема невалидна: строка {error.lineno}, столбец {error.colno}",
                )
            )
    return results


def parse_term_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in TERM_FIELD.finditer(text):
        name = match.group(1).strip()
        value = match.group(2).strip()
        if name not in fields:
            fields[name] = value
    return fields


def parse_term_sections(text: str) -> set[str]:
    return {match.group(1).strip() for match in TERM_SECTION.finditer(text)}


def check_term_cards(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    terms_dir = root / "Docs" / "Terms"
    if not terms_dir.exists():
        return [blocked(CHECK_ID_TERM_CARDS, "Docs/Terms", "каталог Docs/Terms отсутствует")]
    for path in sorted(terms_dir.glob("TERM-*.md")):
        text = read_text(path)
        fields = parse_term_fields(text)
        sections = parse_term_sections(text)
        path_text = rel_path(root, path)
        for field in TERM_REQUIRED_FIELDS:
            if field not in fields or not fields[field]:
                results.append(fail(CHECK_ID_TERM_CARDS, path_text, f"нет обязательного поля: {field}"))
        for section in TERM_REQUIRED_SECTIONS:
            if section not in sections:
                results.append(fail(CHECK_ID_TERM_CARDS, path_text, f"нет обязательного раздела: {section}"))
        status = fields.get("Статус")
        if status and status not in TERM_ALLOWED_STATUSES:
            results.append(fail(CHECK_ID_TERM_STATUS, path_text, f"недопустимый статус термина: {status}"))
        decision = fields.get("Решение_по_конфликту")
        if decision and decision not in TERM_ALLOWED_CONFLICT_DECISIONS:
            results.append(
                fail(CHECK_ID_TERM_CONFLICT_DECISION, path_text, f"недопустимое решение по конфликту: {decision}")
            )
    return results


def extract_index_text(text: str) -> str:
    match = re.search(r"^## Индекс\s*$", text, re.MULTILINE)
    if not match:
        return ""
    rest = text[match.end():]
    next_heading = re.search(r"^(?:---|##\s+)", rest, re.MULTILINE)
    if not next_heading:
        return rest
    return rest[: next_heading.start()]


def duplicate_ids(ids: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for item in ids:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    return duplicates


def index_ids(check_id: str, id_prefix: str, text: str) -> list[str]:
    if check_id == "CHK_INDEX_QUALITYLOG":
        return [match.group(1) for match in QUALITY_HEADING.finditer(text)]
    index_text = extract_index_text(text)
    if not index_text:
        return []
    allowed = re.compile(rf"^(?:{id_prefix})-[0-9]{{6}}$")
    return [item for item in INDEX_ITEM.findall(index_text) if allowed.match(item)]


def check_index_duplicates(root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    for check_id, rel, id_prefix in INDEX_SOURCES:
        path = root / rel
        if not path.exists():
            results.append(blocked(check_id, rel, "обязательный индекс отсутствует"))
            continue
        ids = index_ids(check_id, id_prefix, read_text(path))
        for item in duplicate_ids(ids):
            results.append(fail(check_id, rel, f"явный дубль ID в базовом индексе: {item}"))
    return results


def run_checks(root: Path) -> list[CheckResult]:
    checks = (
        check_markdown_links,
        check_json_schemas,
        check_term_cards,
        check_index_duplicates,
    )
    results: list[CheckResult] = []
    for check in checks:
        results.extend(check(root))
    return results


def status_code(results: list[CheckResult]) -> int:
    return 1 if any(result.status in {STATUS_FAIL, STATUS_BLOCKED} for result in results) else 0


def render_text(results: list[CheckResult]) -> str:
    if not results:
        return "OK bp_check: нарушения уровня check не найдены"
    lines = [
        f"{result.status} {result.check_id} {result.level} {result.path} {result.message}"
        for result in results
    ]
    summary = f"FAIL bp_check: найдено нарушений уровня check: {len(results)}"
    return "\n".join([summary, *lines])


def render_json(results: list[CheckResult]) -> str:
    payload = {
        "status": STATUS_OK if not results else STATUS_FAIL,
        "level": CHECK_LEVEL,
        "summary": {
            "total": len(results),
            "fail": sum(1 for result in results if result.status == STATUS_FAIL),
            "blocked": sum(1 for result in results if result.status == STATUS_BLOCKED),
        },
        "results": [asdict(result) for result in results],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Проверка связности BytePress уровня check.")
    parser.add_argument("--repo", required=True, help="Путь к корню репозитория BytePress.")
    parser.add_argument("--format", choices=OUTPUT_FORMATS, default=DEFAULT_FORMAT, help="Формат вывода.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.repo).resolve()
    if not root.exists():
        print(f"BLOCKED bp_check: репозиторий не найден: {args.repo}", file=sys.stderr)
        return 2
    results = run_checks(root)
    output = render_json(results) if args.format == "json" else render_text(results)
    print(output)
    return status_code(results)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

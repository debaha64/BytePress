#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import List, Tuple

TERM_FILE = re.compile(r"^TERM-\d{6}-[a-z0-9-]+\.md$")


def extract_value(text: str, key: str) -> str:
    pattern = rf"^{re.escape(key)}:\s*(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка карточек терминов и пересборка индекса Base_Terms.md")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    terms_dir = root / "Docs" / "Terms"
    index_path = terms_dir / "Base_Terms.md"
    if not terms_dir.exists():
        print("Каталог Docs/Terms не найден.")
        return 1

    terms: List[Tuple[str, str, str]] = []
    errors: List[str] = []
    seen_names: dict[str, str] = {}
    for path in sorted(terms_dir.glob("TERM-*.md")):
        if not TERM_FILE.match(path.name):
            continue
        text = path.read_text(encoding="utf-8")
        term_id = extract_value(text, "ID")
        term_name = extract_value(text, "Термин")
        status = extract_value(text, "Статус")
        if not term_id or not term_name:
            errors.append(f"Неполная карточка термина: {path.name}")
            continue
        if term_name in seen_names:
            errors.append(f"Дублируется термин: {term_name} ({path.name}, {seen_names[term_name]})")
        else:
            seen_names[term_name] = path.name
        terms.append((term_id, term_name, status or "Черновик"))

    if errors:
        print("Найдены ошибки:")
        for err in errors:
            print(f"- {err}")
        return 1

    lines = ["# Base_Terms", "", "## Индекс"]
    for term_id, term_name, status in terms:
        lines.append(f"- {term_id} — {term_name} [{status}]")
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Индекс терминов обновлён: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

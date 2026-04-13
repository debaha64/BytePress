#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse


REQUIRED_PRODUCT_PATHS = [
    "Adapters/README.md",
    "Adapters/Policy.md",
    "Adapters/Registry.md",
    "Docs/Technical/Interfaces.md",
    "scripts/integration-smoke.sh",
]


def is_bytepress_repo(root: Path) -> bool:
    return (root / "Tools").exists() and (root / "Schemas").exists() and (root / "Templates").exists()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Проверка minimal controlled integration handoff generated product repo."
    )
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    if is_bytepress_repo(root):
        print("bp_integration_smoke.py expects a generated product repo, not BytePress itself.")
        return 1

    missing = [rel for rel in REQUIRED_PRODUCT_PATHS if not (root / rel).exists()]
    if missing:
        print("Отсутствуют обязательные пути integration smoke contour:")
        for rel in missing:
            print(f"- {rel}")
        return 1

    if (root / "MCP").exists():
        print("Generated product repo must not materialize MCP/ in the minimal integration smoke contour.")
        return 1

    print("Controlled integration smoke contour looks consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

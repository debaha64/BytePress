#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import argparse


REQUIRED_PRODUCT_PATHS = [
    "Docs/Technical/Interfaces.md",
    "Tools/product_bootstrap_smoke.py",
    "Tools/product_check.py",
]


def is_bytepress_repo(root: Path) -> bool:
    return (root / "Tools").exists() and (root / "Schemas").exists() and (root / "Templates").exists()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Проверка minimal controlled integration handoff generated product repo."
    )
    parser.add_argument("--repo", default=".")
    parser.add_argument("--report", help="Путь к deterministic report artifact")
    args = parser.parse_args()

    root = Path(args.repo).resolve()
    if is_bytepress_repo(root):
        print("bp_integration_smoke.py expects a generated product repo, not BytePress itself.")
        return 1

    missing = [rel for rel in REQUIRED_PRODUCT_PATHS if not (root / rel).exists()]
    forbidden = [name for name in ["Adapters", "Memory", "MCP", "Runtime", "Roles", "Skills", "Standards"] if (root / name).exists()]
    verdict = "passed" if not missing and not forbidden else "failed"
    report = {
        "artifact": "Integration_Smoke_Report",
        "version": 1,
        "verdict": verdict,
        "scope": "controlled_integration_contour",
        "checks": [
            {
                "id": "INT-001",
                "name": "required_product_paths",
                "verdict": "passed" if not missing else "failed",
                "paths": REQUIRED_PRODUCT_PATHS,
                "missing_paths": missing,
            },
            {
                "id": "INT-002",
                "name": "retired_domains_not_materialized",
                "verdict": "failed" if forbidden else "passed",
                "paths": forbidden,
            },
        ],
    }

    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if missing or forbidden:
        if missing:
            print("Отсутствуют обязательные пути integration smoke contour:")
            for rel in missing:
                print(f"- {rel}")
        if forbidden:
            print("Generated product repo must not materialize retired domains:")
            for rel in forbidden:
                print(f"- {rel}")
        return 1

    print("Controlled integration smoke contour looks consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re

REQUIRED = [
    "README.md", "Setup_Guide.md", "Docs", "Runtime", "Pipeline", "Plans", "Logs",
    "Profiles", "Roles", "Rules", "Standards", "Schemas", "Templates", "Skills",
    "Tools", "Adapters", "Memory", "MCP"
]
REQUIRED_SCHEMAS = [
    "term.schema.json", "roadmap_item.schema.json", "backlog_item.schema.json",
    "plan.schema.json", "adr_entry.schema.json", "changelog_entry.schema.json",
    "profile.schema.json", "role.schema.json", "rule.schema.json", "standard.schema.json"
]
REQUIRED_TEMPLATES = [
    "Document.md", "Term.md", "Roadmap.md", "Backlog.md", "Plan.md", "ADRlog.md",
    "ChangeLog.md", "Profile.md", "Role.md", "Rule.md", "Standard.md", "Delivery.md", "Interview.md",
    "Discussion.md", "Research.md", "Requirements.md"
]
REQUIRED_SKILLS = [
    "Discussion.md", "Interview.md", "Research.md", "Requirements.md", "Planning.md",
    "Implementation.md", "Quality.md", "Review.md", "Release.md", "Support.md"
]
REQUIRED_STANDARDS = ["Coding.md", "Documentation.md", "Naming.md", "Planning.md", "Quality.md", "Release.md", "Terminology.md", "Traceability.md"]
REQUIRED_TOOLS = ["bp_lint.py", "bp_bootstrap.py", "bp_normalize_terms.py"]
REQUIRED_ADAPTERS = ["README.md", "Policy.md", "Registry.md", "Codex/README.md", "Claude/README.md", "Gemini/README.md", "Local/README.md"]
REQUIRED_MEMORY = ["README.md", "Model.md", "Boundaries.md", "Interfaces.md", "Registry.md"]
REQUIRED_MCP = ["README.md", "Policy.md", "Interfaces.md", "Registry.md"]
ID_LINE = re.compile(r"^ID:\s+\S+", re.MULTILINE)
TEMPLATE_ID_LINE = re.compile(r"^<!-- ID:\s+TPL-[0-9]{6} -->$", re.MULTILINE)
SCHEMA_ARTIFACT_ID = re.compile(r'^\s*"\$id":\s*"SCH-[0-9]{6}"', re.MULTILINE)
PRODUCT_PLAN_FILE = re.compile(r"^[A-Z]{2,3}-000001-product-initialization\.md$")
PRODUCT_PROFILE_TYPE = re.compile(r"^Тип_профиля:\s+product$", re.MULTILINE)
PRODUCT_PROFILE_ID = re.compile(r"^ID:\s+PROF-000001$", re.MULTILINE)


def collect_missing(root: Path, names: list[str], base: str) -> list[str]:
    missing: list[str] = []
    for name in names:
        if not (root / base / name).exists():
            missing.append(f"{base}/{name}")
    return missing


def check_has_id(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not ID_LINE.search(text):
        return str(path)
    return None


def check_template_artifact_id(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not TEMPLATE_ID_LINE.search(text):
        return str(path)
    return None


def check_schema_artifact_id(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not SCHEMA_ARTIFACT_ID.search(text):
        return str(path)
    return None


def contains_pattern(path: Path, pattern: re.Pattern[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return bool(pattern.search(text))


def is_bytepress_repo(root: Path) -> bool:
    return (root / "Tools").exists() and (root / "Schemas").exists() and (root / "Templates").exists()


def check_product_repo(root: Path) -> int:
    required = [
        "README.md", "Setup_Guide.md", "Docs", "Runtime", "Plans", "Logs",
        "Profiles", "Adapters", "scripts"
    ]
    required_paths = [
        "Docs/User/README.md",
        "Docs/Product/README.md",
        "Docs/Product/JTBD.md",
        "Docs/Product/PRD.md",
        "Docs/Product/Delivery.md",
        "Docs/Technical/README.md",
        "Docs/Technical/Architecture.md",
        "Docs/Technical/Interfaces.md",
        "Docs/Technical/System_Invariants.md",
        "Docs/Terms/README.md",
        "Docs/Terms/Base_Terms.md",
        "Plans/README.md",
        "Plans/Roadmap.md",
        "Plans/Backlog.md",
        "Logs/README.md",
        "Logs/ChangeLog.md",
        "Logs/ADRlog.md",
        "Logs/QualityLog.md",
        "Logs/ReleaseLog.md",
        "Logs/SupportLog.md",
        "Profiles/Product.md",
        "Adapters/README.md",
        "Adapters/Codex/README.md",
        "Adapters/Claude/README.md",
        "Adapters/Gemini/README.md",
        "Adapters/Local/README.md",
        "scripts/dev-up.sh",
        "scripts/dev-down.sh",
        "scripts/dev-test.sh",
    ]
    missing: list[str] = []
    for item in required:
        if not (root / item).exists():
            missing.append(item)
    for item in required_paths:
        if not (root / item).exists():
            missing.append(item)

    plan_matches = [path for path in (root / "Plans").glob("*.md") if PRODUCT_PLAN_FILE.match(path.name)]
    if not plan_matches:
        missing.append("Plans/<PRODUCT_CODE>-000001-product-initialization.md")

    errors: list[str] = []
    profile_path = root / "Profiles" / "Product.md"
    if profile_path.exists():
        if not contains_pattern(profile_path, PRODUCT_PROFILE_TYPE):
            errors.append("Profiles/Product.md: missing `Тип_профиля: product`")
        if not contains_pattern(profile_path, PRODUCT_PROFILE_ID):
            errors.append("Profiles/Product.md: missing `ID: PROF-000001`")
    if plan_matches:
        plan_path = plan_matches[0]
        if check_has_id(plan_path):
            errors.append(f"{plan_path}: missing ID line")

    if missing or errors:
        if missing:
            print("Отсутствуют обязательные пути продукта:")
            for item in missing:
                print(f"- {item}")
        if errors:
            print("Ошибки продуктового bootstrap-контракта:")
            for item in errors:
                print(f"- {item}")
        return 1
    print("Структура продуктового bootstrap-контракта выглядит полной.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка структуры BytePress и базовых контрактов.")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    if not is_bytepress_repo(root):
        return check_product_repo(root)

    missing: list[str] = []
    for item in REQUIRED:
        if not (root / item).exists():
            missing.append(item)
    missing.extend(collect_missing(root, REQUIRED_SCHEMAS, "Schemas"))
    missing.extend(collect_missing(root, REQUIRED_TEMPLATES, "Templates"))
    missing.extend(collect_missing(root, REQUIRED_SKILLS, "Skills"))
    missing.extend(collect_missing(root, REQUIRED_STANDARDS, "Standards"))
    missing.extend(collect_missing(root, REQUIRED_TOOLS, "Tools"))
    missing.extend(collect_missing(root, REQUIRED_ADAPTERS, "Adapters"))
    missing.extend(collect_missing(root, REQUIRED_MEMORY, "Memory"))
    missing.extend(collect_missing(root, REQUIRED_MCP, "MCP"))
    missing.extend(collect_missing(root, ["README.md", "Interview.md", "Discussion.md", "Research.md", "Requirements.md"], "Docs/Discovery"))
    missing.extend(collect_missing(root, ["Artifact_Lifecycle.md"], "Docs/Technical"))

    id_errors: list[str] = []
    for rel in [
        "Profiles/Default.md",
        "Profiles/Speculorg.md",
        "Plans/Archive/PLAN-000001-foundation.md",
        "Plans/Archive/PLAN-000004-fill-skills-and-tools.md",
        "Plans/Archive/PLAN-000005-adapters-memory-mcp-and-bootstrap.md",
        "Skills/Discussion.md",
        "Skills/Implementation.md",
        "Skills/Quality.md",
        "Adapters/Codex/README.md",
        "Adapters/Claude/README.md",
    ]:
        err = check_has_id(root / rel)
        if err:
            id_errors.append(err)

    for rel in [
        "Rules/Approval_Strictness.md",
        "Rules/Contracts_Before_Mass_Content.md",
        "Rules/Domain_Boundaries_Are_Explicit.md",
        "Rules/Logs_Record_Facts_Only.md",
        "Rules/No_Secrets_In_Git.md",
        "Rules/Plans_Require_Approved_Backlog.md",
        "Rules/Repository_As_Source_Of_Truth.md",
        "Rules/Rules_Are_Not_Standards.md",
        "Rules/Runtime_Is_Temporary.md",
        "Rules/Terms_Governance.md",
        "Standards/Coding.md",
        "Standards/Documentation.md",
        "Standards/Naming.md",
        "Standards/Planning.md",
        "Standards/Quality.md",
        "Standards/Release.md",
        "Standards/Terminology.md",
        "Standards/Traceability.md",
    ]:
        err = check_has_id(root / rel)
        if err:
            id_errors.append(err)

    template_id_errors: list[str] = []
    for path in sorted((root / "Templates").glob("*.md")):
        if path.name == "README.md":
            continue
        err = check_template_artifact_id(path)
        if err:
            template_id_errors.append(err)

    schema_id_errors: list[str] = []
    for path in sorted((root / "Schemas").glob("*.json")):
        err = check_schema_artifact_id(path)
        if err:
            schema_id_errors.append(err)

    if missing or id_errors or template_id_errors or schema_id_errors:
        if missing:
            print("Отсутствуют обязательные пути:")
            for item in missing:
                print(f"- {item}")
        if id_errors:
            print("Файлы без обязательного поля ID:")
            for item in id_errors:
                print(f"- {item}")
        if template_id_errors:
            print("Шаблоны без обязательного artifact ID:")
            for item in template_id_errors:
                print(f"- {item}")
        if schema_id_errors:
            print("Схемы без обязательного artifact ID:")
            for item in schema_id_errors:
                print(f"- {item}")
        return 1
    print("Структура BytePress, интеграционный и исполнительный контуры выглядят полными.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

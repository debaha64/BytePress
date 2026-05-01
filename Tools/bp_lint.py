#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re
import subprocess

REQUIRED = [
    "README.md", "Setup_Guide.md", "Docs", "Pipeline", "Plans", "Logs",
    "Profiles", "Rules", "Schemas", "Templates", "Tools"
]
REQUIRED_SCHEMAS = [
    "term.schema.json", "roadmap_item.schema.json", "backlog_item.schema.json",
    "plan.schema.json", "adr_entry.schema.json", "changelog_entry.schema.json",
    "profile.schema.json", "rule.schema.json"
]
REQUIRED_TEMPLATES = [
    "Document.md", "Term.md", "Roadmap.md", "Backlog.md", "Plan.md", "ADRlog.md",
    "ChangeLog.md", "Profile.md", "Rule.md", "Delivery.md", "Interview.md",
    "Discussion.md", "Research.md", "Requirements.md"
]
REQUIRED_TOOLS = ["bp_lint.py", "bp_bootstrap.py", "bp_integration_smoke.py", "bp_normalize_terms.py"]
REQUIRED_RULES = [
    "Source.md", "Security.md", "Domains.md", "Workflow.md", "Git.md",
    "Logs.md", "Dependencies.md", "Terms.md", "Naming.md"
]
ID_LINE = re.compile(r"^ID:\s+\S+", re.MULTILINE)
TEMPLATE_ID_LINE = re.compile(r"^<!-- ID:\s+TPL-[0-9]{6} -->$", re.MULTILINE)
SCHEMA_ARTIFACT_ID = re.compile(r'^\s*"\$id":\s*"SCH-[0-9]{6}"', re.MULTILINE)
PRODUCT_PLAN_FILE = re.compile(r"^[A-Z]{2,3}-000001-product-initialization\.md$")
PRODUCT_PROFILE_TYPE = re.compile(r"^Тип_профиля:\s+product$", re.MULTILINE)
PRODUCT_PROFILE_ID = re.compile(r"^ID:\s+PROF-000001$", re.MULTILINE)
PRODUCT_BASE_TERMS_SECTION = re.compile(r"^## Стартовый пакет терминов$", re.MULTILINE)
PRODUCT_GITIGNORE_CODEX = re.compile(r"^\.codex/?$", re.MULTILINE)
PRODUCT_GITIGNORE_TOOL_REPORTS = re.compile(r"^Tools/\.reports/$", re.MULTILINE)
PRODUCT_ROADMAP_IN_PROGRESS = re.compile(r"## ROAD-000001[\s\S]*?Статус:\s+В_работе")
PRODUCT_BACKLOG_IN_PROGRESS = re.compile(r"### Активные[\s\S]*?#### BACK-000001[\s\S]*?Статус:\s+В_работе")
PRODUCT_PLAN_IN_PROGRESS = re.compile(r"^Статус:\s+В_работе$", re.MULTILINE)
PRODUCT_DISCOVERY_ROUTE = re.compile(r"Docs/Discovery/\*", re.MULTILINE)
PRODUCT_INTERVIEW_UNCONFIRMED = re.compile(r"^Статус_текущей_истины:\s+Не_подтверждена$", re.MULTILINE)
PRODUCT_INTERVIEW_CONFIRMED = re.compile(r"^Статус_текущей_истины:\s+Подтверждена$", re.MULTILINE)
PRODUCT_INTERVIEW_PLACEHOLDER = re.compile(r"^Ответ:\s+Не подтверждено пользователем\.$", re.MULTILINE)
PRODUCT_INTERVIEW_GATE = re.compile(r"не разрешает изменения вне `Docs/Discovery/\*`, `Plans/\*` и `Logs/\*`", re.IGNORECASE)
PRODUCT_START_GATE_SECTION = re.compile(r"^## Гейт текущей истины$", re.MULTILINE)
PRODUCT_START_REPORT_PHASE = re.compile(r"Фаза:", re.IGNORECASE)
PRODUCT_START_REPORT_WORKFLOW = re.compile(r"Рабочий поток:", re.IGNORECASE)
PRODUCT_START_REPORT_GATE = re.compile(r"Гейт:", re.IGNORECASE)
PRODUCT_PIPELINE_ROUTE = re.compile(r"Pipeline/Workflows\.md|Pipeline/\*", re.IGNORECASE)
PRODUCT_PR_GH_ROUTE = re.compile(r"gh pr create|PR.+через `gh`|через gh", re.IGNORECASE)
PRODUCT_START_GATE_DISCOVERY_ONLY = re.compile(r"discovery-only|только аналитическ|аналитическ(ий|ом) контур", re.IGNORECASE)
PRODUCT_START_GATE_TOOLS = re.compile(r"Tools/product_check\.py|Tools/\*", re.IGNORECASE)
PRODUCT_START_GATE_UNCONFIRMED = re.compile(r"Статус_текущей_истины:\s+Не_подтверждена", re.IGNORECASE)
PRODUCT_START_GATE_TASK_BRANCH = re.compile(r"task-ветк|task branch|рабоч(ая|ую)\s+ветк", re.IGNORECASE)
PRODUCT_START_GATE_CHORE_BRANCH = re.compile(r"chore/", re.IGNORECASE)
PRODUCT_START_GATE_WRITABLE = re.compile(r"writable (action|changes)|writable changes|writable action|записываем\S* (действи\S*|изменени\S*)|правки запрещены|первый проход с правками", re.IGNORECASE)
PRODUCT_PIPELINE_ENGLISH_NAMES = re.compile(
    r"Discovery confirmation|First product-start|Current truth gate|Execution|Subject pass|Implementation gate"
)
PRODUCT_PIPELINE_RUSSIAN_NAMES = [
    "Подтверждение текущей истины",
    "Первый старт продукта",
    "Гейт текущей истины",
    "Реализация",
    "Предметный проход",
    "Гейт реализации",
]
INTERVIEW_NO_GUESSED_EXPANSION = re.compile(r"не предлагает дополнительный функциональный состав первой версии как пример", re.IGNORECASE)
INTERVIEW_UNCONFIRMED_EXPANSION_WORDS = re.compile(
    r"таймер|timer|сч[её]тчик|counter|рекорд|record|настройк|settings|сохранени|save|установщик|installer",
    re.IGNORECASE,
)
PRODUCT_PLAN_DISCOVERY_ONLY = re.compile(r"discovery-only|только аналитическ|аналитическ(ий|ом) контур", re.IGNORECASE)
PRODUCT_PLAN_CURRENT_TRUTH = re.compile(r"current truth|текущ(ая|ей) истин", re.IGNORECASE)
PRODUCT_PLAN_TASK_BRANCH = re.compile(r"task-ветк|task branch|рабоч(ая|ую)\s+ветк", re.IGNORECASE)
PRODUCT_PLAN_WRITABLE = re.compile(r"writable (action|changes)|writable changes|writable action|записываем\S* (действи\S*|изменени\S*)|правки запрещены|первый проход с правками", re.IGNORECASE)
BYTEPRESS_PRODUCT_GATE = re.compile(r"перв(ый|ого|ому) (product-start |аналитическ(ий|ий|ому|им) )?(pass|проход) обязан оставаться (discovery-only|только аналитическ(им|ом))", re.IGNORECASE)
BYTEPRESS_DISCOVERY_GATE = re.compile(r"Статус_текущей_истины:\s+Не_подтверждена|generated repo остаётся (в discovery-only contour|только в аналитическом контуре)", re.IGNORECASE)
QUESTION_HEADING = re.compile(r"^###\s+\d+\.", re.MULTILINE)
INTERVIEW_OPTIONS_BLOCK = re.compile(r"Варианты ответа:")
INTERVIEW_RECOMMENDED_BLOCK = re.compile(r"Рекомендуемый вариант:")
INTERVIEW_OWNER_CURRENT_TRUTH = re.compile(r"Docs/Discovery/Interview\.md[\s\S]{0,120}(owner|владел|current truth|текущ)", re.IGNORECASE)
INTERVIEW_DELTA_BLOCK = re.compile(r"delta-интервью|delta interview", re.IGNORECASE)
INTERVIEW_CLASS_RESULT = re.compile(r"Класс вопроса:\s+Результат", re.IGNORECASE)
INTERVIEW_CLASS_BOUNDARY = re.compile(r"Класс вопроса:\s+Граница", re.IGNORECASE)
INTERVIEW_CLASS_OUT_OF_SCOPE = re.compile(r"Класс вопроса:\s+Вне границы", re.IGNORECASE)
INTERVIEW_CLASS_CONSTRAINT = re.compile(r"Класс вопроса:\s+Ограничение", re.IGNORECASE)
INTERVIEW_CLASS_STACK_DEPS = re.compile(r"Класс вопроса:\s+Стек и зависимости", re.IGNORECASE)
INTERVIEW_CLASS_OWNERSHIP = re.compile(r"Класс вопроса:\s+Владение", re.IGNORECASE)
INTERVIEW_CLASS_BLOCKERS = re.compile(r"Класс вопроса:\s+Блокеры", re.IGNORECASE)
INTERVIEW_TRANSFER_RULE = re.compile(r"блокирующ|неблокирующ", re.IGNORECASE)
INTERVIEW_NO_GUESSED_CONFIRMATION = re.compile(r"не равен.*подтвержден|не считается.*подтвержден|догадк|гипотез", re.IGNORECASE)
INTERVIEW_DEPENDENCY_SOURCE = re.compile(r"стек|зависимост|GUI|tkinter", re.IGNORECASE)
STARTUP_HANDSHAKE_SECTION = re.compile(r"^## (Startup-handshake первого ответа|Стартовый отчёт первого ответа)$", re.MULTILINE)
STARTUP_HANDSHAKE_GREETING = re.compile(r"приветств", re.IGNORECASE)
STARTUP_HANDSHAKE_MODE = re.compile(r"startup mode|режим", re.IGNORECASE)
STARTUP_HANDSHAKE_SCOPE = re.compile(r"scope|область", re.IGNORECASE)
STARTUP_HANDSHAKE_BRANCH_STATUS = re.compile(r"branch status|статус ветки", re.IGNORECASE)
STARTUP_HANDSHAKE_BRANCH_ACTION = re.compile(r"branch action|действие с веткой|start route|route", re.IGNORECASE)
STARTUP_HANDSHAKE_PLANNING = re.compile(r"ROAD/BACK/PLAN|активного этапа", re.IGNORECASE)
STARTUP_HANDSHAKE_OWNERS = re.compile(r"owner-domains|домены-владельцы", re.IGNORECASE)
STARTUP_HANDSHAKE_FIRST_STEP = re.compile(r"перв(ый|ого)\s+конкретн(ый|ого)\s+шаг", re.IGNORECASE)
TASK_BRANCH_NAME = re.compile(r"^(chore|feature|fix|docs)/[0-9]{6}-[a-z0-9]+(?:-[a-z0-9]+)*$")
PRODUCT_FIRST_ANALYTIC_BRANCH = re.compile(r"^chore/[0-9]{6}-[a-z0-9]+(?:-[a-z0-9]+)*$")
PRODUCT_PLAN_ID = re.compile(r"^ID:\s+PLAN-([0-9]{6})$", re.MULTILINE)
PRODUCT_STATUS_LINE = re.compile(r"^Статус:\s+(\S+)$", re.MULTILINE)
INTERVIEW_SKILL_NUMBERED = re.compile(r"нумер", re.IGNORECASE)
INTERVIEW_SKILL_QUESTION_COUNT = re.compile(r"8.?10", re.IGNORECASE)
INTERVIEW_SKILL_OWNER = re.compile(r"owner|владел", re.IGNORECASE)
INTERVIEW_SKILL_OPTIONS = re.compile(r"буквен", re.IGNORECASE)
INTERVIEW_SKILL_RECOMMENDED = re.compile(r"рекомендуем", re.IGNORECASE)
INTERVIEW_TEMPLATE_NUMBERED = re.compile(r"###\s+1\.")
INTERVIEW_TEMPLATE_QUESTION_COUNT = re.compile(r"7.?10", re.IGNORECASE)
INTERVIEW_TEMPLATE_OWNER = re.compile(r"owner-document|owner|документ-владелец|владел", re.IGNORECASE)
INTERVIEW_TEMPLATE_OPTIONS = re.compile(r"Варианты ответа:")
INTERVIEW_TEMPLATE_RECOMMENDED = re.compile(r"Рекомендуемый вариант:")
PROFILE_LIST_PATTERNS = {
    "Активные_правила": re.compile(r"^RULE-[0-9]{6}$"),
}


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


def extract_template_artifact_id(path: Path) -> str | None:
    if not path.exists():
        return None
    match = TEMPLATE_ID_LINE.search(path.read_text(encoding="utf-8"))
    if not match:
        return None
    return match.group(0).removeprefix("<!-- ID:").removesuffix(" -->").strip()


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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def extract_status(text: str) -> str | None:
    match = PRODUCT_STATUS_LINE.search(text)
    return match.group(1) if match else None


def extract_plan_id(text: str) -> str | None:
    match = PRODUCT_PLAN_ID.search(text)
    return f"PLAN-{match.group(1)}" if match else None


def count_matches(path: Path, pattern: re.Pattern[str]) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    return len(pattern.findall(text))


def has_startup_handshake_contract(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    required = [
        STARTUP_HANDSHAKE_SECTION,
        STARTUP_HANDSHAKE_GREETING,
        STARTUP_HANDSHAKE_MODE,
        STARTUP_HANDSHAKE_SCOPE,
        STARTUP_HANDSHAKE_BRANCH_STATUS,
        STARTUP_HANDSHAKE_BRANCH_ACTION,
        STARTUP_HANDSHAKE_PLANNING,
        STARTUP_HANDSHAKE_OWNERS,
        STARTUP_HANDSHAKE_FIRST_STEP,
    ]
    return all(pattern.search(text) for pattern in required)


def has_interview_contract(path: Path) -> list[str]:
    if not path.exists():
        return ["missing interview file"]
    errors: list[str] = []
    question_count = count_matches(path, QUESTION_HEADING)
    if not 7 <= question_count <= 10:
        errors.append("must contain 8-10 numbered questions")
    if not contains_pattern(path, INTERVIEW_OPTIONS_BLOCK):
        errors.append("missing lettered options block")
    if not contains_pattern(path, INTERVIEW_RECOMMENDED_BLOCK):
        errors.append("missing recommended option block")
    if not contains_pattern(path, INTERVIEW_OWNER_CURRENT_TRUTH):
        errors.append("missing current-truth owner statement")
    if not contains_pattern(path, INTERVIEW_DELTA_BLOCK):
        errors.append("missing delta-interview format contract")
    for pattern, label in [
        (INTERVIEW_CLASS_RESULT, "Результат"),
        (INTERVIEW_CLASS_BOUNDARY, "Граница"),
        (INTERVIEW_CLASS_OUT_OF_SCOPE, "Вне границы"),
        (INTERVIEW_CLASS_CONSTRAINT, "Ограничение"),
        (INTERVIEW_CLASS_STACK_DEPS, "Стек и зависимости"),
        (INTERVIEW_CLASS_OWNERSHIP, "Владение"),
        (INTERVIEW_CLASS_BLOCKERS, "Блокеры"),
    ]:
        if not contains_pattern(path, pattern):
            errors.append(f"missing question class `{label}`")
    if not contains_pattern(path, INTERVIEW_TRANSFER_RULE):
        errors.append("missing blocking/nonblocking transfer rule")
    if not contains_pattern(path, INTERVIEW_NO_GUESSED_CONFIRMATION):
        errors.append("missing ban on guessed current-truth confirmation")
    if not contains_pattern(path, INTERVIEW_DEPENDENCY_SOURCE):
        errors.append("missing stack/dependency source discipline")
    if not contains_pattern(path, INTERVIEW_NO_GUESSED_EXPANSION):
        errors.append("missing ban on agent offering additional first-version functionality as examples")
    if contains_pattern(path, INTERVIEW_UNCONFIRMED_EXPANSION_WORDS):
        errors.append("must not suggest unconfirmed first-version expansion examples like timer, counter, records, settings, saves, installer")
    return errors


def has_product_base_terms(path: Path) -> list[str]:
    if not path.exists():
        return ["missing terms file"]
    errors: list[str] = []
    if not contains_pattern(path, PRODUCT_BASE_TERMS_SECTION):
        errors.append("missing starter terms section")
    for term_id, title in [
        ("TERM-000019", "Каркас репозитория"),
        ("TERM-000020", "Текущая истина"),
        ("TERM-000021", "Рабочая ветка"),
        ("TERM-000007", "Дорожная карта"),
        ("TERM-000008", "Реестр работ"),
        ("TERM-000009", "План"),
    ]:
        if f"{term_id} — {title}" not in path.read_text(encoding="utf-8"):
            errors.append(f"missing starter term `{term_id} — {title}`")
    return errors


def has_product_start_gate(path: Path) -> list[str]:
    if not path.exists():
        return ["missing AGENTS.md"]
    text = path.read_text(encoding="utf-8")
    required = [
        PRODUCT_START_GATE_SECTION,
        PRODUCT_START_REPORT_PHASE,
        PRODUCT_START_REPORT_WORKFLOW,
        PRODUCT_START_REPORT_GATE,
        PRODUCT_START_GATE_DISCOVERY_ONLY,
        PRODUCT_START_GATE_TOOLS,
        PRODUCT_START_GATE_UNCONFIRMED,
        PRODUCT_START_GATE_TASK_BRANCH,
        PRODUCT_START_GATE_CHORE_BRANCH,
        PRODUCT_START_GATE_WRITABLE,
        PRODUCT_PIPELINE_ROUTE,
    ]
    errors: list[str] = []
    if not all(pattern.search(text) for pattern in required):
        errors.append("missing hard first product-start gate")
    return errors


def has_product_interview_gate(path: Path) -> list[str]:
    if not path.exists():
        return ["missing interview file"]
    errors: list[str] = []
    if not contains_pattern(path, PRODUCT_INTERVIEW_UNCONFIRMED):
        errors.append("missing `Статус_текущей_истины: Не_подтверждена`")
    if not contains_pattern(path, PRODUCT_INTERVIEW_PLACEHOLDER):
        errors.append("missing placeholder answers that require user confirmation")
    if not contains_pattern(path, PRODUCT_INTERVIEW_GATE):
        errors.append("missing discovery-only gate note")
    return errors


def detect_product_lint_mode(root: Path) -> str:
    interview_path = root / "Docs" / "Discovery" / "Interview.md"
    if contains_pattern(interview_path, PRODUCT_INTERVIEW_UNCONFIRMED):
        return "product-fresh"
    if contains_pattern(interview_path, PRODUCT_INTERVIEW_CONFIRMED):
        return "product-developed"
    return "product-unknown"


def find_initial_product_plan(root: Path) -> Path | None:
    matches = [path for path in (root / "Plans").glob("*.md") if PRODUCT_PLAN_FILE.match(path.name)]
    return matches[0] if matches else None


def has_later_active_or_completed_plan(root: Path) -> bool:
    for path in sorted((root / "Plans").glob("*.md")):
        if path.name in {"README.md", "Roadmap.md", "Backlog.md"}:
            continue
        text = read_text(path)
        plan_id = extract_plan_id(text)
        if not plan_id:
            continue
        number = int(plan_id.removeprefix("PLAN-"))
        status = extract_status(text)
        if number > 1 and status in {"В_работе", "Завершено"}:
            return True
    return False


def product_section_has_status(path: Path, artifact_id: str, status: str) -> bool:
    text = read_text(path)
    if not text:
        return False
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == f"ID: {artifact_id}":
            for candidate in lines[index + 1:index + 12]:
                if candidate.startswith("Статус: "):
                    return candidate == f"Статус: {status}"
            return False
    return False


def has_product_developed_consistency(root: Path, plan_path: Path | None) -> list[str]:
    errors: list[str] = []
    interview_path = root / "Docs" / "Discovery" / "Interview.md"
    if not contains_pattern(interview_path, PRODUCT_INTERVIEW_CONFIRMED):
        errors.append("Docs/Discovery/Interview.md: current truth is not `Подтверждена`")
    if contains_pattern(interview_path, PRODUCT_INTERVIEW_PLACEHOLDER):
        errors.append("Docs/Discovery/Interview.md: placeholder answers remain after current truth confirmation")

    roadmap_path = root / "Plans" / "Roadmap.md"
    backlog_path = root / "Plans" / "Backlog.md"
    if not product_section_has_status(roadmap_path, "ROAD-000001", "Завершено"):
        errors.append("Plans/Roadmap.md: ROAD-000001 must be `Завершено` after the first closed product-start pass")
    if not product_section_has_status(backlog_path, "BACK-000001", "Завершено"):
        errors.append("Plans/Backlog.md: BACK-000001 must be `Завершено` after the first closed product-start pass")

    if plan_path is None:
        errors.append("Plans/<PRODUCT_CODE>-000001-product-initialization.md: missing initial product plan")
    else:
        plan_text = read_text(plan_path)
        if extract_plan_id(plan_text) != "PLAN-000001":
            errors.append(f"{plan_path}: initial product plan ID must remain `PLAN-000001`")
        if extract_status(plan_text) != "Завершено":
            errors.append(f"{plan_path}: PLAN-000001 must be `Завершено` after the first closed product-start pass")

    if not has_later_active_or_completed_plan(root):
        errors.append("Plans/*: developing product repo must contain a later active or completed plan after PLAN-000001")

    changelog_text = read_text(root / "Logs" / "ChangeLog.md")
    quality_text = read_text(root / "Logs" / "QualityLog.md")
    if "PLAN-000001" not in changelog_text or "BACK-000001" not in changelog_text:
        errors.append("Logs/ChangeLog.md: missing first pass closure links to PLAN-000001 and BACK-000001")
    if "PLAN-000001" not in quality_text:
        errors.append("Logs/QualityLog.md: missing first pass check record linked to PLAN-000001")
    return errors


def is_executable(path: Path) -> bool:
    if not path.exists():
        return False
    return bool(path.stat().st_mode & 0o111)


def check_profile_reference_lists(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    for field, pattern in PROFILE_LIST_PATTERNS.items():
        header = f"{field}:"
        try:
            index = lines.index(header)
        except ValueError:
            errors.append(f"{path}: missing `{field}` section")
            continue
        entries: list[str] = []
        cursor = index + 1
        while cursor < len(lines) and lines[cursor].startswith("- "):
            entries.append(lines[cursor][2:])
            cursor += 1
        if not entries:
            errors.append(f"{path}: empty `{field}` section")
            continue
        if any(not pattern.fullmatch(item) for item in entries):
            errors.append(f"{path}: non-canonical IDs in `{field}` section")
    return errors


def is_bytepress_repo(root: Path) -> bool:
    return (root / "Tools" / "bp_lint.py").exists() and (root / "Tools" / "bp_bootstrap.py").exists()


def get_git_branch(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    branch = result.stdout.strip()
    return branch or None


def check_product_repo(root: Path, mode: str) -> int:
    required = [
        "README.md", "AGENTS.md", "Setup_Guide.md", "Docs", "Plans", "Logs",
        "Pipeline", "Tools", "Templates", "Schemas"
    ]
    required_paths = [
        "Docs/Discovery/README.md",
        "Docs/Discovery/Interview.md",
        "Docs/User/README.md",
        "Docs/User/Operating_Mode.md",
        "Docs/User/First_Start.md",
        "Docs/User/Pass_Request.md",
        "Docs/User/Usage_Scenarios.md",
        "Docs/Product/README.md",
        "Docs/Product/Product_Passport.md",
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
        "Pipeline/README.md",
        "Pipeline/Phases.md",
        "Pipeline/Workflows.md",
        "Pipeline/Gates.md",
        "Tools/README.md",
        "Tools/product_check.py",
        "Tools/product_bootstrap_smoke.py",
        "Templates/README.md",
        "Templates/Interview.md",
        "Templates/Roadmap.md",
        "Templates/Backlog.md",
        "Templates/Plan.md",
        "Templates/ChangeLog.md",
        "Templates/ADRlog.md",
        "Templates/QualityLog.md",
        "Schemas/README.md",
        "Schemas/roadmap_item.schema.json",
        "Schemas/backlog_item.schema.json",
        "Schemas/plan.schema.json",
        "Schemas/changelog_entry.schema.json",
        "Schemas/adr_entry.schema.json",
    ]
    forbidden_dirs = ["Adapters", "Memory", "MCP", "Runtime", "Roles", "Skills", "Standards"]
    missing: list[str] = []
    errors: list[str] = []
    for item in required:
        if not (root / item).exists():
            missing.append(item)
    for item in required_paths:
        if not (root / item).exists():
            missing.append(item)
    for item in forbidden_dirs:
        if (root / item).exists():
            errors.append(f"{item}: forbidden placeholder domain in profile product skeleton")

    plan_path = find_initial_product_plan(root)
    if plan_path is None:
        missing.append("Plans/<PRODUCT_CODE>-000001-product-initialization.md")

    detected_mode = detect_product_lint_mode(root)
    if mode == "auto":
        mode = detected_mode
    if mode == "product-unknown":
        errors.append(
            "Docs/Discovery/Interview.md: cannot determine product lint mode; expected `Не_подтверждена` or `Подтверждена` current truth"
        )
    elif mode not in {"product-fresh", "product-developed"}:
        errors.append(f"lint mode: unsupported product mode `{mode}`")

    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        if not contains_pattern(gitignore_path, PRODUCT_GITIGNORE_CODEX):
            errors.append(".gitignore: missing `.codex/` ignore")
        if not contains_pattern(gitignore_path, PRODUCT_GITIGNORE_TOOL_REPORTS):
            errors.append(".gitignore: missing `Tools/.reports/` ignore")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_DISCOVERY_ROUTE):
        errors.append("AGENTS.md: missing `Docs/Discovery/*` route")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_PIPELINE_ROUTE):
        errors.append("AGENTS.md: missing generated Pipeline route")
    if not contains_pattern(root / "Pipeline" / "Workflows.md", PRODUCT_PR_GH_ROUTE):
        errors.append("Pipeline/Workflows.md: missing PR route through gh")
    pipeline_text = read_text(root / "Pipeline" / "Workflows.md") + "\n" + read_text(root / "Pipeline" / "Phases.md") + "\n" + read_text(root / "Pipeline" / "Gates.md")
    if PRODUCT_PIPELINE_ENGLISH_NAMES.search(pipeline_text):
        errors.append("Pipeline/*: generated phase, workflow and gate names must use Russian canonical names")
    for marker in PRODUCT_PIPELINE_RUSSIAN_NAMES:
        if marker not in pipeline_text:
            errors.append(f"Pipeline/*: missing Russian marker `{marker}`")
    if not has_startup_handshake_contract(root / "AGENTS.md"):
        errors.append("AGENTS.md: missing observable startup-handshake contract for generated product repo")
    for item in has_product_start_gate(root / "AGENTS.md"):
        errors.append(f"AGENTS.md: {item}")
    interview_path = root / "Docs" / "Discovery" / "Interview.md"
    for item in has_interview_contract(interview_path):
        errors.append(f"Docs/Discovery/Interview.md: {item}")
    if mode == "product-fresh":
        for item in has_product_interview_gate(interview_path):
            errors.append(f"Docs/Discovery/Interview.md: {item}")
    elif mode == "product-developed":
        if contains_pattern(interview_path, PRODUCT_INTERVIEW_UNCONFIRMED):
            errors.append("Docs/Discovery/Interview.md: developing product repo cannot keep unconfirmed current truth")
    for item in has_product_base_terms(root / "Docs" / "Terms" / "Base_Terms.md"):
        errors.append(f"Docs/Terms/Base_Terms.md: {item}")
    roadmap_path = root / "Plans" / "Roadmap.md"
    if mode == "product-fresh" and roadmap_path.exists() and not contains_pattern(roadmap_path, PRODUCT_ROADMAP_IN_PROGRESS):
        errors.append("Plans/Roadmap.md: initial stage is not `В_работе`")
    backlog_path = root / "Plans" / "Backlog.md"
    if mode == "product-fresh" and backlog_path.exists() and not contains_pattern(backlog_path, PRODUCT_BACKLOG_IN_PROGRESS):
        errors.append("Plans/Backlog.md: initial backlog task is not active `В_работе`")
    if plan_path is not None:
        if check_has_id(plan_path):
            errors.append(f"{plan_path}: missing ID line")
        if mode == "product-fresh" and not contains_pattern(plan_path, PRODUCT_PLAN_IN_PROGRESS):
            errors.append(f"{plan_path}: missing `Статус: В_работе`")
        if not contains_pattern(plan_path, PRODUCT_PLAN_DISCOVERY_ONLY):
            errors.append(f"{plan_path}: missing discovery-only gate wording")
        if not contains_pattern(plan_path, PRODUCT_PLAN_CURRENT_TRUTH):
            errors.append(f"{plan_path}: missing current-truth gating wording")
        if not contains_pattern(plan_path, PRODUCT_PLAN_TASK_BRANCH):
            errors.append(f"{plan_path}: missing task-branch gate wording")
        if not contains_pattern(plan_path, PRODUCT_PLAN_WRITABLE):
            errors.append(f"{plan_path}: missing writable-change gate wording")
    if mode == "product-developed":
        errors.extend(has_product_developed_consistency(root, plan_path))
    current_branch = get_git_branch(root)
    if mode == "product-fresh" and current_branch and contains_pattern(interview_path, PRODUCT_INTERVIEW_UNCONFIRMED):
        if current_branch in {"develop", "main"} or not PRODUCT_FIRST_ANALYTIC_BRANCH.fullmatch(current_branch):
            errors.append(
                "git branch: first analytical product-start with unconfirmed current truth must use a chore/ task branch before any writable changes"
            )
    for rel in ["Tools/product_check.py", "Tools/product_bootstrap_smoke.py"]:
        path = root / rel
        if path.exists() and not is_executable(path):
            errors.append(f"{rel}: tool is not executable")
    for rel in ["scripts/dev-up.sh", "scripts/dev-down.sh", "scripts/dev-test.sh", "scripts/integration-smoke.sh", "scripts/reset-product-start.sh"]:
        path = root / rel
        if path.exists() and not is_executable(path):
            errors.append(f"{rel}: compatibility script is not executable")
    for path in sorted((root / "Schemas").glob("*.json")):
        if check_schema_artifact_id(path):
            errors.append(f"{path.relative_to(root)}: missing schema ID")
    template_ids: dict[str, Path] = {}
    for path in sorted((root / "Templates").glob("*.md")):
        if path.name == "README.md":
            continue
        template_id = extract_template_artifact_id(path)
        if template_id is None:
            errors.append(f"{path.relative_to(root)}: missing template artifact ID")
            continue
        if template_id in template_ids:
            errors.append(
                f"{path.relative_to(root)}: duplicate template artifact ID `{template_id}` also used by {template_ids[template_id].relative_to(root)}"
            )
        else:
            template_ids[template_id] = path

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
    print(f"Структура продуктового контракта выглядит полной. Режим: {mode}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка структуры BytePress и базовых контрактов.")
    parser.add_argument("--repo", default=".")
    parser.add_argument(
        "--mode",
        choices=["auto", "product-fresh", "product-developed"],
        default="auto",
        help="Режим проверки product repo; BytePress repo всегда проверяется как BytePress.",
    )
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    if not is_bytepress_repo(root):
        return check_product_repo(root, args.mode)

    missing: list[str] = []
    for item in REQUIRED:
        if not (root / item).exists():
            missing.append(item)
    missing.extend(collect_missing(root, REQUIRED_SCHEMAS, "Schemas"))
    missing.extend(collect_missing(root, REQUIRED_TEMPLATES, "Templates"))
    missing.extend(collect_missing(root, REQUIRED_TOOLS, "Tools"))
    missing.extend(collect_missing(root, ["README.md", "Interview.md", "Discussion.md", "Research.md", "Requirements.md"], "Docs/Discovery"))
    missing.extend(collect_missing(root, ["Artifact_Lifecycle.md", "System_Invariants.md", "Product_Bootstrap_Domain_Matrix.md"], "Docs/Technical"))

    id_errors: list[str] = []
    for rel in [
        "Profiles/Default.md",
        "Profiles/Speculorg.md",
        "Plans/Archive/PLAN-000001-foundation.md",
    ]:
        err = check_has_id(root / rel)
        if err:
            id_errors.append(err)

    missing.extend(collect_missing(root, REQUIRED_RULES, "Rules"))
    actual_rules = sorted(path.name for path in (root / "Rules").glob("*.md") if path.name != "README.md")
    if actual_rules != sorted(REQUIRED_RULES):
        missing.append("Rules/*: file set differs from Rules/README.md contract")

    for rel in [f"Rules/{name}" for name in REQUIRED_RULES]:
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

    profile_reference_errors: list[str] = []
    for path in sorted((root / "Profiles").glob("*.md")):
        if path.name == "README.md":
            continue
        profile_reference_errors.extend(check_profile_reference_lists(path))

    contract_errors: list[str] = []
    if not has_startup_handshake_contract(root / "AGENTS.md"):
        contract_errors.append("AGENTS.md: missing observable startup-handshake contract")
    if not contains_pattern(root / "AGENTS.md", BYTEPRESS_PRODUCT_GATE):
        contract_errors.append("AGENTS.md: missing bootstrap-created product discovery-only gate note")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_START_REPORT_PHASE):
        contract_errors.append("AGENTS.md: missing phase in startup report")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_START_REPORT_WORKFLOW):
        contract_errors.append("AGENTS.md: missing workflow in startup report")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_START_REPORT_GATE):
        contract_errors.append("AGENTS.md: missing gate in startup report")
    if not contains_pattern(root / "Pipeline" / "Workflows.md", PRODUCT_PR_GH_ROUTE):
        contract_errors.append("Pipeline/Workflows.md: missing PR route through gh")
    for item in has_interview_contract(root / "Docs" / "Discovery" / "Interview.md"):
        contract_errors.append(f"Docs/Discovery/Interview.md: {item}")
    if not contains_pattern(root / "Docs" / "Discovery" / "README.md", BYTEPRESS_DISCOVERY_GATE):
        contract_errors.append("Docs/Discovery/README.md: missing bootstrap-created product gate note")
    interview_template = root / "Templates" / "Interview.md"
    if interview_template.exists():
        if not contains_pattern(interview_template, INTERVIEW_TEMPLATE_OWNER):
            contract_errors.append("Templates/Interview.md: missing current-truth owner note")
        if not contains_pattern(interview_template, INTERVIEW_TEMPLATE_QUESTION_COUNT):
            contract_errors.append("Templates/Interview.md: missing 8-10 question template note")
        if not contains_pattern(interview_template, INTERVIEW_TEMPLATE_NUMBERED):
            contract_errors.append("Templates/Interview.md: missing numbered interview format")
        if not contains_pattern(interview_template, INTERVIEW_TEMPLATE_OPTIONS):
            contract_errors.append("Templates/Interview.md: missing options block")
        if not contains_pattern(interview_template, INTERVIEW_TEMPLATE_RECOMMENDED):
            contract_errors.append("Templates/Interview.md: missing recommended option block")

    if missing or id_errors or template_id_errors or schema_id_errors or profile_reference_errors or contract_errors:
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
        if profile_reference_errors:
            print("Профили с неканоничными ссылочными списками:")
            for item in profile_reference_errors:
                print(f"- {item}")
        if contract_errors:
            print("Ошибки контрактов активного слоя:")
            for item in contract_errors:
                print(f"- {item}")
        return 1
    print("Структура BytePress и контуры Docs, Plans, Logs, Pipeline, Rules, Templates, Schemas и Tools выглядят полными.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

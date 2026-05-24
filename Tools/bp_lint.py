#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re
import subprocess
import zipfile

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
PRODUCT_PR_GH_ROUTE = re.compile(r"gh pr create|запрос на слияние.+через `gh`|через gh", re.IGNORECASE)
PRODUCT_START_GATE_DISCOVERY_ONLY = re.compile(r"discovery-only|только аналитическ|аналитическ(ий|ом) контур", re.IGNORECASE)
PRODUCT_START_GATE_TOOLS = re.compile(r"Tools/product_check\.py|Tools/\*", re.IGNORECASE)
PRODUCT_START_GATE_UNCONFIRMED = re.compile(r"Статус_текущей_истины:\s+Не_подтверждена", re.IGNORECASE)
PRODUCT_START_GATE_TASK_BRANCH = re.compile(r"task-ветк|task branch|рабоч(ая|ую)\s+ветк", re.IGNORECASE)
PRODUCT_START_GATE_CHORE_BRANCH = re.compile(r"chore/", re.IGNORECASE)
PRODUCT_START_GATE_WRITABLE = re.compile(r"writable (action|changes)|writable changes|writable action|записываем\S* (действи\S*|изменени\S*)|правки запрещены|первый проход с правками", re.IGNORECASE)
PRODUCT_AGENT_RUSSIAN_OUTPUT = re.compile(r"русск\S* язык|на русском языке", re.IGNORECASE)
PRODUCT_AGENT_ENGLISH_LIMIT = re.compile(r"Английский допускается только", re.IGNORECASE)
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
PRODUCT_SUBJECT_OWNER_SYNC_MARKERS = [
    "Docs/Product/Product_Passport.md",
    "Docs/Product/PRD.md",
    "Docs/Product/JTBD.md",
    "Docs/Product/Delivery.md",
    "Docs/User/*",
    "Docs/Technical/*",
    "Plans/*",
    "Logs/*",
]
PRODUCT_PASSPORT_LIVE_FIELDS = [
    "Тип_продукта:",
    "Основной_запуск:",
    "Подтверждённый_стек:",
    "Предметные_пакеты:",
    "Ограничения_среды:",
]
INTERVIEW_UNCONFIRMED_EXPANSION = re.compile(
    r"таймер|timer|сч[её]тчик|counter|рекорд|record|настройк|settings|сохранени|save|установщик|installer",
    re.IGNORECASE,
)
PRODUCT_PLAN_DISCOVERY_ONLY = re.compile(r"discovery-only|только аналитическ|аналитическ(ий|ом) контур", re.IGNORECASE)
PRODUCT_PLAN_CURRENT_TRUTH = re.compile(r"current truth|текущ(ая|ей) истин", re.IGNORECASE)
PRODUCT_PLAN_TASK_BRANCH = re.compile(r"task-ветк|task branch|рабоч(ая|ую)\s+ветк", re.IGNORECASE)
PRODUCT_PLAN_WRITABLE = re.compile(r"writable (action|changes)|writable changes|writable action|записываем\S* (действи\S*|изменени\S*)|правки запрещены|первый проход с правками", re.IGNORECASE)
BYTEPRESS_PRODUCT_GATE = re.compile(r"первый (product-start pass|старт продукта) обязан оставаться (discovery-only|только аналитическим)", re.IGNORECASE)
BYTEPRESS_DISCOVERY_GATE = re.compile(r"Статус_текущей_истины:\s+Не_подтверждена|generated repo остаётся (в discovery-only contour|только в аналитическом контуре)", re.IGNORECASE)
QUESTION_HEADING = re.compile(r"^###\s+\d+\.", re.MULTILINE)
INTERVIEW_OPTIONS_BLOCK = re.compile(r"Варианты ответа:")
INTERVIEW_RECOMMENDED_BLOCK = re.compile(r"Рекомендуемый вариант:")
INTERVIEW_OWNER_CURRENT_TRUTH = re.compile(r"Docs/Discovery/Interview\.md[\s\S]{0,120}(owner|владел|current truth|текущ)", re.IGNORECASE)
INTERVIEW_DELTA_BLOCK = re.compile(r"узкое интервью|delta-интервью|delta interview", re.IGNORECASE)
INTERVIEW_CLASS_CONTEXT = re.compile(r"Класс вопроса:\s+Контекст", re.IGNORECASE)
INTERVIEW_CLASS_BOUNDARY = re.compile(r"Класс вопроса:\s+Граница", re.IGNORECASE)
INTERVIEW_CLASS_CONSTRAINT = re.compile(r"Класс вопроса:\s+Ограничение", re.IGNORECASE)
INTERVIEW_CLASS_OWNERSHIP = re.compile(r"Класс вопроса:\s+Владение", re.IGNORECASE)
INTERVIEW_CLASS_TRANSITION = re.compile(r"Класс вопроса:\s+Переход", re.IGNORECASE)
INTERVIEW_TRANSFER_RULE = re.compile(r"блокирующ|неблокирующ", re.IGNORECASE)
INTERVIEW_NO_GUESSED_CONFIRMATION = re.compile(r"не равен.*подтвержден|не считается.*подтвержден|догадк|гипотез", re.IGNORECASE)
INTERVIEW_DEPENDENCY_SOURCE = re.compile(r"стек|зависимост|графическ|tkinter", re.IGNORECASE)
INTERVIEW_WAIT_FOR_USER = re.compile(r"останов.*ждать ответа|жд[её]т ответа пользователя|до ответа пользователя", re.IGNORECASE)
INTERVIEW_NO_PRODUCT_REQUEST_CONFIRMATION = re.compile(r"хочу сделать продукт|общий запрос", re.IGNORECASE)
TKINTER_EXPLICIT_SOURCE = re.compile(r"tkinter[\s\S]{0,180}(явн|профил|требован|техническ)", re.IGNORECASE)
SYSTEM_PACKAGE_COMMAND = re.compile(r"\b(?:sudo\s+)?apt(?:-get)?\b", re.IGNORECASE)
FIRST_PASS_EXPANSION = re.compile(
    r"уровн[и-я]*\s+сложност|\bтаймер|\bрекорд|сохранени|\bтем[аы]\b|установщик|упаковк|многопользовательск",
    re.IGNORECASE,
)
FIRST_PASS_SCOPE_SOURCE = re.compile(r"явн|источник|ответ|требован|подтвержд|пользовател", re.IGNORECASE)
FIRST_PASS_EXCLUSION = re.compile(r"исключ|вне границ|вне области|не вход|не входит|остается вне|остаётся вне", re.IGNORECASE)
FORBIDDEN_GUI_TEXT = re.compile(r"\bGUI\b|GUI-", re.IGNORECASE)
FORBIDDEN_USER_TEXT_TERMS = re.compile(r"\bGUI\b|product pass|\bpass\b|\bbootstrap\b", re.IGNORECASE)
FORBIDDEN_ENGLISH_GIT_PR_RULE = re.compile(r"commit message|PR title|PR body|оформля\w+\s+на английском", re.IGNORECASE)
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
BYTEPRESS_ROAD_000036_DONE = re.compile(r"ID:\s+ROAD-000036[\s\S]{0,240}Статус:\s+Завершено")
BYTEPRESS_BACKLOG_000101_ACTIVE = re.compile(r"### Активные[\s\S]*?ID:\s+BACK-000101")
BYTEPRESS_BACKLOG_000101_ARCHIVED_DONE = re.compile(r"ID:\s+BACK-000101[\s\S]{0,240}Статус:\s+Завершено")
BYTEPRESS_PLAN_000090_DONE = re.compile(r"ID:\s+PLAN-000090[\s\S]{0,240}Статус:\s+Завершено")
BYTEPRESS_REPORTS_PLAN_000090_CLOSED = re.compile(r"ROAD-000036`?\s*/\s*`?BACK-000101`?\s*/\s*`?PLAN-000090`?\s+закрыт", re.IGNORECASE)
BYTEPRESS_WORKFLOW_FACT_RULE = re.compile(r"фактические файлы `Plans/Roadmap\.md`, `Plans/Backlog\.md` и архивированный `Plan` должны подтверждать статус `Завершено`")
BYTEPRESS_RULE_RUSSIAN_OUTPUT = re.compile(r"RULE-000017[\s\S]{0,500}Все записи агента[\s\S]{0,200}на русском языке")
BYTEPRESS_RULE_OWNER_SYNC = re.compile(r"RULE-000019[\s\S]{0,800}Docs/Product/Product_Passport\.md[\s\S]{0,400}Logs/\*")
BYTEPRESS_RULE_RUSSIAN_CODE_TEXT = re.compile(r"RULE-000020[\s\S]{0,500}Пользовательские сообщения[\s\S]{0,250}на русском языке")
INTERVIEW_SKILL_NUMBERED = re.compile(r"нумер", re.IGNORECASE)
INTERVIEW_SKILL_QUESTION_COUNT = re.compile(r"8.?10", re.IGNORECASE)
INTERVIEW_SKILL_OWNER = re.compile(r"owner|владел", re.IGNORECASE)
INTERVIEW_SKILL_OPTIONS = re.compile(r"буквен", re.IGNORECASE)
INTERVIEW_SKILL_RECOMMENDED = re.compile(r"рекомендуем", re.IGNORECASE)
INTERVIEW_TEMPLATE_NUMBERED = re.compile(r"###\s+1\.")
INTERVIEW_TEMPLATE_QUESTION_COUNT = re.compile(r"8.?10", re.IGNORECASE)
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


def zip_entry_contains_pattern(path: Path, entry: str, pattern: re.Pattern[str]) -> bool:
    if not path.exists():
        return False
    try:
        with zipfile.ZipFile(path) as archive:
            text = archive.read(entry).decode("utf-8")
    except (KeyError, OSError, UnicodeDecodeError, zipfile.BadZipFile):
        return False
    return bool(pattern.search(text))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def forbidden_gui_text_paths(root: Path, rel_paths: list[str]) -> list[str]:
    errors: list[str] = []
    for rel in rel_paths:
        path = root / rel
        if path.exists() and FORBIDDEN_GUI_TEXT.search(read_text(path)):
            errors.append(f"{rel}: используйте `графический интерфейс` вместо `GUI` в пользовательском тексте")
    return errors


def product_user_text_paths(root: Path) -> list[Path]:
    candidates = [
        root / "README.md",
        root / "AGENTS.md",
        root / "Setup_Guide.md",
        root / "Docs" / "Discovery" / "README.md",
        root / "Docs" / "Discovery" / "Interview.md",
        root / "Docs" / "User" / "README.md",
        root / "Docs" / "User" / "First_Start.md",
        root / "Docs" / "User" / "Operating_Mode.md",
        root / "Docs" / "User" / "Pass_Request.md",
        root / "Docs" / "User" / "Usage_Scenarios.md",
        root / "Docs" / "Product" / "README.md",
        root / "Docs" / "Product" / "Product_Passport.md",
        root / "Docs" / "Product" / "JTBD.md",
        root / "Docs" / "Product" / "PRD.md",
        root / "Docs" / "Product" / "Delivery.md",
        root / "Docs" / "Terms" / "README.md",
        root / "Docs" / "Terms" / "Base_Terms.md",
        root / "Pipeline" / "Phases.md",
        root / "Pipeline" / "Workflows.md",
        root / "Pipeline" / "Gates.md",
        root / "Plans" / "Roadmap.md",
        root / "Plans" / "Backlog.md",
    ]
    candidates.extend(sorted((root / "Plans").glob("*.md")))
    return [path for path in candidates if path.exists()]


def forbidden_product_user_text_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for path in product_user_text_paths(root):
        lines = read_text(path).splitlines()
        for line_number, line in enumerate(lines, start=1):
            line_without_paths = re.sub(r"`[^`]*product_bootstrap_smoke\.py[^`]*`", "", line)
            if FORBIDDEN_USER_TEXT_TERMS.search(line_without_paths):
                errors.append(f"{path.relative_to(root)}:{line_number}: пользовательский текст должен использовать русский эквивалент вместо `GUI`, `product pass`, `pass` или `bootstrap`")
            if SYSTEM_PACKAGE_COMMAND.search(line):
                errors.append(f"{path.relative_to(root)}:{line_number}: системная установка требует отдельного решения пользователя")
            if "tkinter" in line.lower() and not re.search(r"явн|профил|требован|техническ|допускается|требует", line, re.IGNORECASE):
                errors.append(f"{path.relative_to(root)}:{line_number}: `tkinter` требует явного источника")
            context = "\n".join(lines[max(0, line_number - 8):line_number])
            if (
                FIRST_PASS_EXPANSION.search(line)
                and not FIRST_PASS_SCOPE_SOURCE.search(line)
                and not FIRST_PASS_EXCLUSION.search(context)
            ):
                errors.append(f"{path.relative_to(root)}:{line_number}: расширяющая функция первого прохода требует явного ответа пользователя")
    return errors


def unconfirmed_expansion_errors(path: Path) -> list[str]:
    errors: list[str] = []
    lines = read_text(path).splitlines()
    for line_number, line in enumerate(lines, start=1):
        if not FIRST_PASS_EXPANSION.search(line):
            continue
        context = "\n".join(lines[max(0, line_number - 8):line_number])
        if FIRST_PASS_SCOPE_SOURCE.search(line) or FIRST_PASS_EXCLUSION.search(context):
            continue
        errors.append("нельзя подсказывать неподтверждённые расширения первой версии")
        break
    return errors


def has_forbidden_english_git_pr_rule(root: Path) -> bool:
    return bool(FORBIDDEN_ENGLISH_GIT_PR_RULE.search(read_text(root / "AGENTS.md")))


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
        return ["нет файла интервью"]
    errors: list[str] = []
    question_count = count_matches(path, QUESTION_HEADING)
    if not 8 <= question_count <= 10:
        errors.append("должно быть 8-10 нумерованных вопросов")
    if not contains_pattern(path, INTERVIEW_OPTIONS_BLOCK):
        errors.append("нет блока буквенных вариантов")
    if not contains_pattern(path, INTERVIEW_RECOMMENDED_BLOCK):
        errors.append("нет блока рекомендуемого варианта")
    if not contains_pattern(path, INTERVIEW_OWNER_CURRENT_TRUTH):
        errors.append("нет указания владельца текущей истины")
    if not contains_pattern(path, INTERVIEW_DELTA_BLOCK):
        errors.append("нет договора формата узкого интервью")
    for pattern, label in [
        (INTERVIEW_CLASS_CONTEXT, "Контекст"),
        (INTERVIEW_CLASS_BOUNDARY, "Граница"),
        (INTERVIEW_CLASS_CONSTRAINT, "Ограничение"),
        (INTERVIEW_CLASS_OWNERSHIP, "Владение"),
        (INTERVIEW_CLASS_TRANSITION, "Переход"),
    ]:
        if not contains_pattern(path, pattern):
            errors.append(f"нет класса вопроса `{label}`")
    if not contains_pattern(path, INTERVIEW_TRANSFER_RULE):
        errors.append("нет правила переноса блокирующих и неблокирующих вопросов")
    if not contains_pattern(path, INTERVIEW_NO_GUESSED_CONFIRMATION):
        errors.append("нет запрета подтверждать текущую истину догадкой")
    if not contains_pattern(path, INTERVIEW_WAIT_FOR_USER):
        errors.append("нет правила остановки и ожидания ответа после блокирующих вопросов")
    if not contains_pattern(path, INTERVIEW_NO_PRODUCT_REQUEST_CONFIRMATION):
        errors.append("нет запрета подтверждать текущую истину общим запросом о продукте")
    if not contains_pattern(path, INTERVIEW_DEPENDENCY_SOURCE):
        errors.append("нет правила источника стека и зависимостей")
    if "tkinter" in read_text(path) and not contains_pattern(path, TKINTER_EXPLICIT_SOURCE):
        errors.append("`tkinter` требует явного источника")
    errors.extend(forbidden_gui_text_paths(path.parent.parent.parent, ["Docs/Discovery/Interview.md"]))
    errors.extend(unconfirmed_expansion_errors(path))
    return errors


def has_product_base_terms(path: Path) -> list[str]:
    if not path.exists():
        return ["нет файла терминов"]
    errors: list[str] = []
    if not contains_pattern(path, PRODUCT_BASE_TERMS_SECTION):
        errors.append("нет секции стартового пакета терминов")
    for term_id, title in [
        ("TERM-000019", "Каркас репозитория"),
        ("TERM-000020", "Текущая истина"),
        ("TERM-000021", "Рабочая ветка"),
        ("TERM-000007", "Дорожная карта"),
        ("TERM-000008", "Реестр работ"),
        ("TERM-000009", "План"),
    ]:
        if f"{term_id} — {title}" not in path.read_text(encoding="utf-8"):
            errors.append(f"нет стартового термина `{term_id} — {title}`")
    return errors


def has_product_subject_owner_sync(path: Path) -> list[str]:
    if not path.exists():
        return ["нет Pipeline/Workflows.md"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in PRODUCT_SUBJECT_OWNER_SYNC_MARKERS:
        if marker not in text:
            errors.append(f"нет обязательной проверки владельца смысла `{marker}`")
    return errors


def has_live_product_passport(path: Path) -> list[str]:
    if not path.exists():
        return ["нет Product_Passport.md"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for marker in PRODUCT_PASSPORT_LIVE_FIELDS:
        if marker not in text:
            errors.append(f"нет поля живого паспорта `{marker}`")
    if "Profiles/*" in text and not re.search(r"не возвращ|без возвращ", text, re.IGNORECASE):
        errors.append("паспорт продукта не должен возвращать домен `Profiles/*`")
    return errors


def has_product_start_gate(path: Path) -> list[str]:
    if not path.exists():
        return ["нет AGENTS.md"]
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
        PRODUCT_AGENT_RUSSIAN_OUTPUT,
        PRODUCT_AGENT_ENGLISH_LIMIT,
        PRODUCT_PIPELINE_ROUTE,
    ]
    errors: list[str] = []
    if not all(pattern.search(text) for pattern in required):
        errors.append("нет жёсткого гейта первого старта продукта")
    return errors


def has_product_interview_gate(path: Path) -> list[str]:
    if not path.exists():
        return ["нет файла интервью"]
    errors: list[str] = []
    if not contains_pattern(path, PRODUCT_INTERVIEW_UNCONFIRMED):
        errors.append("нет `Статус_текущей_истины: Не_подтверждена`")
    if not contains_pattern(path, PRODUCT_INTERVIEW_PLACEHOLDER):
        errors.append("нет placeholder-ответов, требующих подтверждения пользователя")
    if not contains_pattern(path, PRODUCT_INTERVIEW_GATE):
        errors.append("нет указания гейта аналитического контура")
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
        if number > 1 and status in {"В_работе", "Готово_к_утверждению", "Завершено"}:
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


def product_section_status(path: Path, artifact_id: str) -> str | None:
    text = read_text(path)
    if not text:
        return None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == f"ID: {artifact_id}":
            for candidate in lines[index + 1:index + 12]:
                if candidate.startswith("Статус: "):
                    return candidate.removeprefix("Статус: ")
            return None
    return None


def status_allows_ready_for_approval(status: str | None) -> bool:
    return status in {"Готово_к_утверждению", "Завершено"}


def has_product_developed_consistency(root: Path, plan_path: Path | None) -> list[str]:
    errors: list[str] = []
    interview_path = root / "Docs" / "Discovery" / "Interview.md"
    if not contains_pattern(interview_path, PRODUCT_INTERVIEW_CONFIRMED):
        errors.append("Docs/Discovery/Interview.md: текущая истина не имеет статус `Подтверждена`")
    if contains_pattern(interview_path, PRODUCT_INTERVIEW_PLACEHOLDER):
        errors.append("Docs/Discovery/Interview.md: после подтверждения текущей истины остались placeholder-ответы")

    roadmap_path = root / "Plans" / "Roadmap.md"
    backlog_path = root / "Plans" / "Backlog.md"
    if not status_allows_ready_for_approval(product_section_status(roadmap_path, "ROAD-000001")):
        errors.append("Plans/Roadmap.md: ROAD-000001 должен быть `Завершено` или `Готово_к_утверждению` после первого product-start pass")
    if not status_allows_ready_for_approval(product_section_status(backlog_path, "BACK-000001")):
        errors.append("Plans/Backlog.md: BACK-000001 должен быть `Завершено` или `Готово_к_утверждению` после первого product-start pass")

    if plan_path is None:
        errors.append("Plans/<PRODUCT_CODE>-000001-product-initialization.md: нет начального плана продукта")
    else:
        plan_text = read_text(plan_path)
        if extract_plan_id(plan_text) != "PLAN-000001":
            errors.append(f"{plan_path}: ID начального плана продукта должен оставаться `PLAN-000001`")
        if not status_allows_ready_for_approval(extract_status(plan_text)):
            errors.append(f"{plan_path}: PLAN-000001 должен быть `Завершено` или `Готово_к_утверждению` после первого product-start pass")

    if not has_later_active_or_completed_plan(root):
        errors.append("Plans/*: developed product repo должен содержать следующий активный, готовый к утверждению или завершённый план после PLAN-000001")

    changelog_text = read_text(root / "Logs" / "ChangeLog.md")
    quality_text = read_text(root / "Logs" / "QualityLog.md")
    if "PLAN-000001" not in changelog_text or "BACK-000001" not in changelog_text:
        errors.append("Logs/ChangeLog.md: нет ссылок закрытия первого прохода на PLAN-000001 и BACK-000001")
    if "PLAN-000001" not in quality_text:
        errors.append("Logs/QualityLog.md: нет записи проверки первого прохода со ссылкой на PLAN-000001")
    return errors


def is_executable(path: Path) -> bool:
    if not path.exists():
        return False
    return bool(path.stat().st_mode & 0o111)


def check_reported_plan_closure(root: Path) -> list[str]:
    errors: list[str] = []
    if not contains_pattern(root / "Logs" / "QualityLog.md", BYTEPRESS_REPORTS_PLAN_000090_CLOSED):
        return errors
    if not contains_pattern(root / "Plans" / "Roadmap.md", BYTEPRESS_ROAD_000036_DONE):
        errors.append("Plans/Roadmap.md: журнал сообщает о закрытии ROAD-000036, но ROAD-000036 не имеет статус `Завершено`")
    if contains_pattern(root / "Plans" / "Backlog.md", BYTEPRESS_BACKLOG_000101_ACTIVE):
        errors.append("Plans/Backlog.md: журнал сообщает о закрытии BACK-000101, но BACK-000101 остаётся активным")
    if not contains_pattern(root / "Plans" / "Archive" / "Backlog" / "ROAD-000036.md", BYTEPRESS_BACKLOG_000101_ARCHIVED_DONE) and not zip_entry_contains_pattern(root / "Plans" / "Archive" / "Releases" / "0.3.0.zip", "Backlog/ROAD-000036.md", BYTEPRESS_BACKLOG_000101_ARCHIVED_DONE):
        errors.append("Plans/Archive/Backlog/ROAD-000036.md: нет завершённого BACK-000101")
    if (root / "Plans" / "PLAN-000090-pre-release-cleanup-pass.md").exists():
        errors.append("Plans/PLAN-000090-pre-release-cleanup-pass.md: закрытый PLAN-000090 должен быть в архиве")
    if not contains_pattern(root / "Plans" / "Archive" / "Plans" / "PLAN-000090-pre-release-cleanup-pass.md", BYTEPRESS_PLAN_000090_DONE) and not zip_entry_contains_pattern(root / "Plans" / "Archive" / "Releases" / "0.3.0.zip", "Plans/PLAN-000090-pre-release-cleanup-pass.md", BYTEPRESS_PLAN_000090_DONE):
        errors.append("Plans/Archive/Plans/PLAN-000090-pre-release-cleanup-pass.md: нет завершённого PLAN-000090")
    return errors


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
    if has_forbidden_english_git_pr_rule(root):
        errors.append("AGENTS.md: сообщение фиксации и запрос на слияние не должны требовать английский язык")
    if not contains_pattern(root / "Pipeline" / "Workflows.md", PRODUCT_PR_GH_ROUTE):
        errors.append("Pipeline/Workflows.md: нет маршрута запроса на слияние через gh")
    for item in has_product_subject_owner_sync(root / "Pipeline" / "Workflows.md"):
        errors.append(f"Pipeline/Workflows.md: {item}")
    errors.extend(
        forbidden_gui_text_paths(
            root,
            [
                "AGENTS.md",
                "Docs/Discovery/Interview.md",
                "Pipeline/Workflows.md",
                "Pipeline/Phases.md",
                "Pipeline/Gates.md",
            ],
        )
    )
    errors.extend(forbidden_product_user_text_errors(root))
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
    for item in has_live_product_passport(root / "Docs" / "Product" / "Product_Passport.md"):
        errors.append(f"Docs/Product/Product_Passport.md: {item}")
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
                "git branch: first analytical product-start with unconfirmed current truth must use a chore/ working branch before any writable changes"
            )
    if mode == "product-fresh" and (root / "scripts").exists():
        errors.append("scripts/*: устаревший переходный слой не создаётся в новом каркасе; используйте Tools/*")
    for rel in ["Tools/product_check.py", "Tools/product_bootstrap_smoke.py"]:
        path = root / rel
        if path.exists() and not is_executable(path):
            errors.append(f"{rel}: tool is not executable")
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
        "Plans/Archive/Plans/PLAN-000001-foundation.md",
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
    if has_forbidden_english_git_pr_rule(root):
        contract_errors.append("AGENTS.md: сообщение фиксации и запрос на слияние не должны требовать английский язык")
    if not contains_pattern(root / "AGENTS.md", BYTEPRESS_PRODUCT_GATE):
        contract_errors.append("AGENTS.md: missing bootstrap-created product discovery-only gate note")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_START_REPORT_PHASE):
        contract_errors.append("AGENTS.md: missing phase in startup report")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_START_REPORT_WORKFLOW):
        contract_errors.append("AGENTS.md: missing workflow in startup report")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_START_REPORT_GATE):
        contract_errors.append("AGENTS.md: missing gate in startup report")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_AGENT_RUSSIAN_OUTPUT):
        contract_errors.append("AGENTS.md: нет правила русского пользовательского вывода")
    if not contains_pattern(root / "AGENTS.md", PRODUCT_AGENT_ENGLISH_LIMIT):
        contract_errors.append("AGENTS.md: нет границы исключений для английского в пользовательском выводе")
    if not contains_pattern(root / "Rules" / "Workflow.md", BYTEPRESS_RULE_RUSSIAN_OUTPUT):
        contract_errors.append("Rules/Workflow.md: нет RULE-000017 о русском пользовательском выводе")
    if not contains_pattern(root / "Rules" / "Workflow.md", BYTEPRESS_RULE_OWNER_SYNC):
        contract_errors.append("Rules/Workflow.md: нет RULE-000019 о сверке владельцев смысла")
    if not contains_pattern(root / "Rules" / "Workflow.md", BYTEPRESS_RULE_RUSSIAN_CODE_TEXT):
        contract_errors.append("Rules/Workflow.md: нет RULE-000020 о русских пользовательских строках в коде продукта")
    if not contains_pattern(root / "Pipeline" / "Workflows.md", BYTEPRESS_WORKFLOW_FACT_RULE):
        contract_errors.append("Pipeline/Workflows.md: нет правила сверки отчёта о закрытии ROAD/BACK/PLAN с фактом")
    if not contains_pattern(root / "Pipeline" / "Workflows.md", PRODUCT_PR_GH_ROUTE):
        contract_errors.append("Pipeline/Workflows.md: нет маршрута запроса на слияние через gh")
    contract_errors.extend(
        forbidden_gui_text_paths(
            root,
            [
                "AGENTS.md",
                "Pipeline/Workflows.md",
                "Pipeline/Phase_Gates.md",
                "Rules/Dependencies.md",
                "Docs/Discovery/Interview.md",
                "Docs/Technical/Platform_Contracts.md",
                "Docs/Technical/Product_Bootstrap_Contract.md",
            ],
        )
    )
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
    plan_closure_errors = check_reported_plan_closure(root)
    if plan_closure_errors:
        print("Ошибки сверки отчёта и факта планового контура:")
        for item in plan_closure_errors:
            print(f"- {item}")
        return 1
    print("Структура BytePress и контуры Docs, Plans, Logs, Pipeline, Rules, Templates, Schemas и Tools выглядят полными.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

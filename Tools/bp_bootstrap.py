#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re

PRODUCT_CODE_RE = re.compile(r"^[A-Z]{2,3}$")
STARTER_TERM_IDS = [
    "TERM-000019",
    "TERM-000020",
    "TERM-000021",
    "TERM-000007",
    "TERM-000008",
    "TERM-000009",
]
STARTER_TERM_PURPOSES = {
    "TERM-000019": "Объясняет, какой минимальный каркас bootstrap создаёт по умолчанию.",
    "TERM-000020": "Удерживает аналитический гейт до явных ответов пользователя.",
    "TERM-000021": "Фиксирует, что проход с правками начинается только из рабочей ветки.",
    "TERM-000007": "Помогает читать планирование этапов продукта.",
    "TERM-000008": "Помогает читать планирование задач текущего этапа.",
    "TERM-000009": "Помогает читать и вести один текущий проход продукта.",
}

PRODUCT_TOOL_CHECK = r'''#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re
import subprocess
import sys

ROOT_MARKERS = ["README.md", "AGENTS.md", "Setup_Guide.md"]
BASE_PATHS = [
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
FORBIDDEN_DIRS = ["Adapters", "Memory", "MCP", "Runtime", "Roles", "Skills", "Standards"]
PIPELINE_GH_ROUTE = re.compile(r"gh pr create|PR.+через `gh`|через gh", re.IGNORECASE)
PIPELINE_CHECK_LEVELS = re.compile(r"Структура|Тесты|GUI-запуск|Ручная проверка", re.IGNORECASE)
PIPELINE_ENGLISH_NAMES = re.compile(r"Discovery confirmation|First product-start|Current truth gate|Execution|Subject pass|Implementation gate")
PIPELINE_RUSSIAN_NAMES = [
    "Подтверждение текущей истины",
    "Первый старт продукта",
    "Гейт текущей истины",
    "Реализация",
    "Предметный проход",
    "Гейт реализации",
]
AGENTS_PIPELINE_ROUTE = re.compile(r"Pipeline/Workflows\.md|Pipeline/\*", re.IGNORECASE)
AGENTS_START_REPORT = [re.compile(pattern, re.IGNORECASE) for pattern in [r"Фаза:", r"Рабочий поток:", r"Гейт:"]]
INTERVIEW_NO_GUESSES = re.compile(r"не равен.*подтвержден|не считается.*подтвержден|догадк|гипотез", re.IGNORECASE)
INTERVIEW_DEPENDENCIES = re.compile(r"стек|зависимост|GUI|tkinter", re.IGNORECASE)
INTERVIEW_UNCONFIRMED_EXPANSION = re.compile(
    r"таймер|timer|сч[её]тчик|counter|рекорд|record|настройк|settings|сохранени|save|установщик|installer",
    re.IGNORECASE,
)
PLAN_FILE = re.compile(r"^[A-Z]{2,3}-000001-product-initialization\.md$")
TASK_BRANCH_NAME = re.compile(r"^(chore|feature|fix|docs)/[0-9]{6}-[a-z0-9]+(?:-[a-z0-9]+)*$")
FIRST_ANALYTIC_BRANCH = re.compile(r"^chore/[0-9]{6}-[a-z0-9]+(?:-[a-z0-9]+)*$")
UNCONFIRMED = re.compile(r"^Статус_текущей_истины:\s+Не_подтверждена$", re.MULTILINE)
CONFIRMED = re.compile(r"^Статус_текущей_истины:\s+Подтверждена$", re.MULTILINE)
PLACEHOLDER = re.compile(r"^Ответ:\s+Не подтверждено пользователем\.$", re.MULTILINE)
STATUS = re.compile(r"^Статус:\s+(\S+)$", re.MULTILINE)
PLAN_ID = re.compile(r"^ID:\s+PLAN-([0-9]{6})$", re.MULTILINE)
SCHEMA_ID = re.compile(r'^\s*"\$id":\s*"SCH-[0-9]{6}"', re.MULTILINE)
TEMPLATE_ID = re.compile(r"^<!-- ID:\s+(TPL-[0-9]{6}) -->$", re.MULTILINE)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def contains(path: Path, pattern: re.Pattern[str]) -> bool:
    return bool(pattern.search(text(path)))


def initial_plan(root: Path) -> Path | None:
    matches = [path for path in (root / "Plans").glob("*.md") if PLAN_FILE.match(path.name)]
    return matches[0] if matches else None


def status_of(path: Path) -> str | None:
    match = STATUS.search(text(path))
    return match.group(1) if match else None


def section_status(path: Path, artifact_id: str) -> str | None:
    lines = text(path).splitlines()
    for index, line in enumerate(lines):
        if line == f"ID: {artifact_id}":
            for candidate in lines[index + 1:index + 12]:
                if candidate.startswith("Статус: "):
                    return candidate.removeprefix("Статус: ")
    return None


def has_later_plan(root: Path) -> bool:
    for path in sorted((root / "Plans").glob("*.md")):
        if path.name in {"README.md", "Roadmap.md", "Backlog.md"}:
            continue
        plan_text = text(path)
        match = PLAN_ID.search(plan_text)
        if not match:
            continue
        if int(match.group(1)) > 1 and status_of(path) in {"В_работе", "Завершено"}:
            return True
    return False


def detect_mode(root: Path) -> str:
    interview = root / "Docs" / "Discovery" / "Interview.md"
    if contains(interview, UNCONFIRMED):
        return "fresh"
    if contains(interview, CONFIRMED):
        return "developed"
    return "unknown"


def git_branch(root: Path) -> str | None:
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


def check(root: Path, mode: str) -> list[str]:
    errors: list[str] = []
    for item in ROOT_MARKERS + BASE_PATHS:
        if not (root / item).exists():
            errors.append(f"missing {item}")
    for item in FORBIDDEN_DIRS:
        if (root / item).exists():
            errors.append(f"forbidden placeholder domain present: {item}")
    for path in sorted((root / "Schemas").glob("*.json")):
        if not contains(path, SCHEMA_ID):
            errors.append(f"{path.relative_to(root)}: missing schema ID")
    template_ids: dict[str, Path] = {}
    for path in sorted((root / "Templates").glob("*.md")):
        if path.name == "README.md":
            continue
        match = TEMPLATE_ID.search(text(path))
        if not match:
            errors.append(f"{path.relative_to(root)}: missing template ID")
            continue
        template_id = match.group(1)
        if template_id in template_ids:
            errors.append(f"{path.relative_to(root)}: duplicate template ID {template_id}")
        else:
            template_ids[template_id] = path
    if "Tools/.reports/" not in text(root / ".gitignore"):
        errors.append(".gitignore: missing Tools/.reports/ ignore")
    agents_text = text(root / "AGENTS.md")
    if not AGENTS_PIPELINE_ROUTE.search(agents_text):
        errors.append("AGENTS.md: missing Pipeline route")
    for pattern in AGENTS_START_REPORT:
        if not pattern.search(agents_text):
            errors.append("AGENTS.md: в стартовом отчёте нет фазы, рабочего потока или гейта")
    workflows = root / "Pipeline" / "Workflows.md"
    if not PIPELINE_GH_ROUTE.search(text(workflows)):
        errors.append("Pipeline/Workflows.md: missing PR route through gh")
    if not PIPELINE_CHECK_LEVELS.search(text(workflows)):
        errors.append("Pipeline/Workflows.md: missing check levels")
    pipeline_text = text(root / "Pipeline" / "Workflows.md") + "\n" + text(root / "Pipeline" / "Phases.md") + "\n" + text(root / "Pipeline" / "Gates.md")
    if PIPELINE_ENGLISH_NAMES.search(pipeline_text):
        errors.append("Pipeline/*: phase, workflow and gate names must use Russian canonical names")
    for marker in PIPELINE_RUSSIAN_NAMES:
        if marker not in pipeline_text:
            errors.append(f"Pipeline/*: missing Russian marker `{marker}`")

    plan = initial_plan(root)
    if plan is None:
        errors.append("missing Plans/<PRODUCT_CODE>-000001-product-initialization.md")
    actual_mode = detect_mode(root) if mode == "auto" else mode
    if actual_mode == "unknown":
        errors.append("Docs/Discovery/Interview.md: cannot detect current-truth lifecycle state")
    interview = root / "Docs" / "Discovery" / "Interview.md"
    if not INTERVIEW_NO_GUESSES.search(text(interview)):
        errors.append("Docs/Discovery/Interview.md: missing ban on guessed current-truth confirmation")
    if not INTERVIEW_DEPENDENCIES.search(text(interview)):
        errors.append("Docs/Discovery/Interview.md: missing stack/dependency source discipline")
    if INTERVIEW_UNCONFIRMED_EXPANSION.search(text(interview)):
        errors.append("Docs/Discovery/Interview.md: must not suggest unconfirmed first-version expansion examples")
    if actual_mode == "fresh":
        if not contains(interview, UNCONFIRMED):
            errors.append("Docs/Discovery/Interview.md: missing unconfirmed current truth")
        if not contains(interview, PLACEHOLDER):
            errors.append("Docs/Discovery/Interview.md: missing placeholder answers")
        if section_status(root / "Plans" / "Roadmap.md", "ROAD-000001") != "В_работе":
            errors.append("Plans/Roadmap.md: ROAD-000001 must be В_работе in fresh state")
        if section_status(root / "Plans" / "Backlog.md", "BACK-000001") != "В_работе":
            errors.append("Plans/Backlog.md: BACK-000001 must be В_работе in fresh state")
        if plan and status_of(plan) != "В_работе":
            errors.append(f"{plan.relative_to(root)}: PLAN-000001 must be В_работе in fresh state")
        current_branch = git_branch(root)
        if current_branch and (current_branch in {"develop", "main"} or not FIRST_ANALYTIC_BRANCH.fullmatch(current_branch)):
            errors.append("git branch: first analytical product-start must use a chore/ working branch")
    elif actual_mode == "developed":
        if contains(interview, UNCONFIRMED) or contains(interview, PLACEHOLDER):
            errors.append("Docs/Discovery/Interview.md: developed state keeps fresh placeholders")
        if section_status(root / "Plans" / "Roadmap.md", "ROAD-000001") != "Завершено":
            errors.append("Plans/Roadmap.md: ROAD-000001 must be Завершено in developed state")
        if section_status(root / "Plans" / "Backlog.md", "BACK-000001") != "Завершено":
            errors.append("Plans/Backlog.md: BACK-000001 must be Завершено in developed state")
        if plan and status_of(plan) != "Завершено":
            errors.append(f"{plan.relative_to(root)}: PLAN-000001 must be Завершено in developed state")
        if not has_later_plan(root):
            errors.append("Plans/*: developed state needs a later active or completed plan")
        if "PLAN-000001" not in text(root / "Logs" / "ChangeLog.md"):
            errors.append("Logs/ChangeLog.md: missing PLAN-000001 closure link")
        if "PLAN-000001" not in text(root / "Logs" / "QualityLog.md"):
            errors.append("Logs/QualityLog.md: missing PLAN-000001 check link")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка локального продуктового каркаса.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--mode", choices=["auto", "fresh", "developed"], default="auto")
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    errors = check(root, args.mode)
    if errors:
        print("Ошибки продуктового каркаса:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Локальный продуктовый каркас выглядит полным. Режим: {detect_mode(root) if args.mode == 'auto' else args.mode}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

PRODUCT_BOOTSTRAP_SMOKE = r'''#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    report_dir = root / "Tools" / ".reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sys.executable, str(root / "Tools" / "product_check.py"), "--repo", str(root), "--mode", "auto"],
        text=True,
        capture_output=True,
    )
    report = {
        "check": "product_bootstrap_smoke",
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }
    (report_dir / "product_bootstrap_smoke.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Product bootstrap smoke report written to: {report_dir / 'product_bootstrap_smoke.json'}")
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
'''


@dataclass(frozen=True)
class BrandProfile:
    name: str
    interaction_language: str


@dataclass(frozen=True)
class StarterTerm:
    term_id: str
    title: str
    definition: str
    purpose: str


@dataclass(frozen=True)
class ProductContext:
    name: str
    product_code: str
    brand_profile: BrandProfile
    current_date: str
    starter_terms: tuple[StarterTerm, ...]


def extract_value(text: str, key: str) -> str:
    pattern = rf"^{re.escape(key)}:\s*(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_executable(path: Path, content: str) -> None:
    write(path, content)
    path.chmod(0o755)


def load_brand_profile(repo_root: Path, profile_name: str) -> BrandProfile:
    profile_path = repo_root / "Profiles" / f"{profile_name}.md"
    if not profile_path.exists():
        raise ValueError(f"Brand profile not found in BytePress: {profile_name}")

    text = profile_path.read_text(encoding="utf-8")
    profile_type = extract_value(text, "Тип_профиля")
    interaction_language = extract_value(text, "Язык_взаимодействия")
    if profile_type != "brand":
        raise ValueError(f"Profile is not a brand profile: {profile_name}")
    if not interaction_language:
        raise ValueError(f"Brand profile does not define Язык_взаимодействия: {profile_name}")
    return BrandProfile(name=profile_name, interaction_language=interaction_language)


def load_starter_term(repo_root: Path, term_id: str) -> StarterTerm:
    matches = sorted((repo_root / "Docs" / "Terms").glob(f"{term_id}-*.md"))
    if len(matches) != 1:
        raise ValueError(f"Starter term not found or ambiguous in BytePress: {term_id}")
    text = matches[0].read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("#").strip()
    definition = ""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == "## Определение" and index + 1 < len(lines):
            definition = lines[index + 1].strip()
            break
    if not definition:
        raise ValueError(f"Starter term does not define `## Определение`: {term_id}")
    return StarterTerm(
        term_id=term_id,
        title=title,
        definition=definition,
        purpose=STARTER_TERM_PURPOSES[term_id],
    )


def load_starter_terms(repo_root: Path) -> tuple[StarterTerm, ...]:
    return tuple(load_starter_term(repo_root, term_id) for term_id in STARTER_TERM_IDS)


def render_starter_terms(terms: tuple[StarterTerm, ...]) -> str:
    lines = [
        "# Base_Terms",
        "",
        "## Назначение",
        "Этот файл содержит минимальный стартовый пакет терминов продуктового репозитория.",
        "Полный словарь `BytePress` сюда не копируется.",
        "",
        "## Индекс",
    ]
    for term in terms:
        lines.append(f"- {term.term_id} — {term.title}")
    lines.extend(["", "## Стартовый пакет терминов"])
    for term in terms:
        lines.extend(
            [
                "",
                f"### {term.term_id} — {term.title}",
                f"Определение: {term.definition}",
                f"Зачем нужен на старте: {term.purpose}",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def build_context(args: argparse.Namespace, repo_root: Path) -> ProductContext:
    name = args.name.strip()
    product_code = args.product_code.strip()
    brand_profile_name = args.brand_profile.strip()
    if not name:
        raise ValueError("--name must not be empty")
    if not PRODUCT_CODE_RE.fullmatch(product_code):
        raise ValueError("--product-code must contain 2-3 uppercase Latin letters")
    if not brand_profile_name:
        raise ValueError("--brand-profile must not be empty")

    brand_profile = load_brand_profile(repo_root, brand_profile_name)
    starter_terms = load_starter_terms(repo_root)
    return ProductContext(
        name=name,
        product_code=product_code,
        brand_profile=brand_profile,
        current_date=date.today().isoformat(),
        starter_terms=starter_terms,
    )


def bootstrap_product(target: Path, ctx: ProductContext) -> None:
    plan_filename = f"{ctx.product_code}-000001-product-initialization.md"

    for path in [
        "Docs/Discovery",
        "Docs/User",
        "Docs/Product",
        "Docs/Technical",
        "Docs/Terms",
        "Plans",
        "Logs",
        "Pipeline",
        "Tools",
        "Templates",
        "Schemas",
        "scripts",
    ]:
        (target / path).mkdir(parents=True, exist_ok=True)

    write(
        target / ".gitignore",
        "__pycache__/\n*.pyc\n.env\n.env.*\n.venv/\n.codex\n.codex/\nTools/.reports/\n",
    )
    write(
        target / "README.md",
        f"# {ctx.name}\n\n"
        f"{ctx.name} — первый пригодный к работе продуктовый репозиторий, созданный `BytePress` bootstrap.\n\n"
        "`README.md` — карта для человека.\n"
        "`AGENTS.md` — карта для агента.\n\n"
        "## Стартовый маршрут\n"
        "1. Прочитать `Docs/User/First_Start.md`.\n"
        "2. Прочитать `Docs/Terms/Base_Terms.md`.\n"
        "3. Прочитать `Docs/Discovery/Interview.md` и подтвердить текущую истину ответами пользователя.\n"
        "4. Подготовить среду по `Setup_Guide.md`.\n"
        "5. Проверить текущие этап, задачу и план в `Plans/*`.\n"
        "6. Использовать `Tools/product_check.py`, если нужна структурная проверка продукта.\n"
        "7. Использовать `Tools/product_bootstrap_smoke.py`, если нужен локальный smoke-маршрут.\n"
        "8. Использовать `scripts/*` только как переходные оболочки к локальному `Tools/*`; после первого обновления служебного слоя `scripts/*` можно удалить.\n\n"
        "## Доменная карта\n"
        "- `Docs/Discovery/*` — текущая истина и интервью продукта.\n"
        "- `Docs/User/*` — пользовательский слой продукта.\n"
        "- `Docs/Product/*` — прикладная рамка продукта.\n"
        "- `Docs/Technical/*` — стартовый технический контур продукта.\n"
        "- `Plans/*` — дорожная карта, реестр работ и текущий план продукта.\n"
        "- `Logs/*` — факты, изменения и доказательства качества продукта.\n"
        "- `Pipeline/*` — лёгкий локальный процессный контур продукта.\n"
        "- `Tools/*` — локальные проверки и служебные команды продукта.\n"
        "- `Templates/*` — шаблоны только для созданных артефактов.\n"
        "- `Schemas/*` — схемы только для проверяемых артефактов.\n"
        "- `scripts/*` — переходные shell-оболочки к `Tools/*`; после обновления служебного слоя можно удалить, главный вход — `Tools/*`.\n",
    )
    write(
        target / "AGENTS.md",
        f"# AGENTS\n\n"
        f"`AGENTS.md` — карта входа агента в продуктовый репозиторий `{ctx.name}`.\n\n"
        "## Что делает агент\n"
        "- человек направляет, агент исполняет;\n"
        "- агент работает внутри договоров продуктового репозитория;\n"
        "- каждое изменение проходит через рабочую ветку, локальные проверки и PR.\n\n"
        "## Как читать истину\n"
        "1. Текущий источник задачи от пользователя.\n"
        "2. `Docs/Discovery/*` как маршрут текущей истины продукта.\n"
        "3. `Plans/*` как владелец этапа, задачи и прохода.\n"
        "4. `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*`, `Docs/Terms/*` как слои знания продукта.\n"
        "5. `Pipeline/*` как владелец рабочего процесса, фаз, рабочих потоков и гейтов.\n"
        "6. `Logs/*`, `Tools/*`, `Templates/*`, `Schemas/*` и `Setup_Guide.md` как поддержка исполнения.\n\n"
        "## Стартовый отчёт первого ответа\n"
        "Первый содержательный ответ до исследования или правок должен быть коротким стартовым отчётом.\n\n"
        "`Приветствие:` короткая рабочая фраза.\n"
        "`Режим запуска:` какой режим запуска используется.\n"
        "`Фаза:` текущая фаза из `Pipeline/*`.\n"
        "`Рабочий поток:` текущий рабочий поток из `Pipeline/Workflows.md`.\n"
        "`Гейт:` ближайший обязательный гейт.\n"
        "`Область:` как понят текущий проход.\n"
        "`Статус ветки:` что обнаружено в Git.\n"
        "`Действие с веткой:` какой стартовый маршрут используется дальше.\n"
        "`Состояние планирования:` текущие `ROAD/BACK/PLAN` или отсутствие активного этапа.\n"
        "`Первые домены-владельцы:` какие домены читаются первыми.\n"
        "`Первый конкретный шаг:` какое действие выполняется сразу.\n\n"
        "## Гейт текущей истины\n"
        "- Созданный начальным развёртыванием репозиторий стартует с `Docs/Discovery/Interview.md` в состоянии `Статус_текущей_истины: Не_подтверждена`.\n"
        "- Пока пользователь не дал явные ответы и текущая истина не подтверждена, агент работает только в аналитическом контуре.\n"
        "- До открытия рабочей ветки любые записываемые изменения запрещены, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n"
        "- В этом гейте допускаются только `Docs/Discovery/*`, `Plans/*`, `Logs/*` и маршрут очистки неудачного прохода, но сам проход с правками начинается только после действия с рабочей веткой.\n"
        "- В этом гейте bootstrap-заготовки не считаются разрешением на изменения в `Docs/Product/*`, `Docs/Technical/*`, `Tools/*`, `Pipeline/*` или предметной реализации.\n"
        "- Если failed start дал tracked drift вне разрешённого раннего контура, канонический маршрут reset — fresh bootstrap в новый target.\n\n"
        "## Стартовый маршрут\n"
        "- Сначала прочитать `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.\n"
        "- Затем прочитать `Docs/Terms/Base_Terms.md` и `Docs/Discovery/Interview.md`.\n"
        "- Затем прочитать `Pipeline/Workflows.md` и назвать текущие фазу, рабочий поток и гейт.\n"
        "- Первый аналитический проход с правками начинать только после открытия рабочей ветки с типом `chore/`.\n"
        "- `docs/` использовать только для обычных документационных проходов после снятия стартового гейта.\n"
        "- Для structural check использовать `python3 Tools/product_check.py --repo . --mode auto`.\n"
        "- Для локального smoke использовать `python3 Tools/product_bootstrap_smoke.py`.\n"
        "- `scripts/*` остаются только переходными оболочками к локальному `Tools/*`.\n\n"
        "## Границы\n"
        "- этот файл не подменяет `Docs/Discovery/*`, `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*`, `Docs/Terms/*` и `Plans/*`;\n"
        "- этот файл только направляет агента к документам-владельцам продуктового репозитория и к `Pipeline/Workflows.md` как владельцу рабочего процесса.\n",
    )
    write(
        target / "Setup_Guide.md",
        "# Setup_Guide\n\n"
        "## Базовая среда\n"
        "- Linux или WSL\n"
        "- Git\n"
        "- Python 3.11+\n\n"
        "## Рабочий каталог\n"
        "- Репозиторий продукта располагается отдельно от BytePress.\n\n"
        "## Стартовый маршрут Git\n"
        "```bash\n"
        "git init -b develop\n"
        "git add .\n"
        "git commit -m \"Bootstrap baseline\"\n"
        "git checkout -b chore/000001-confirm-current-truth\n"
        "```\n\n"
        "## Проверка\n"
        "- первый стартовый проход продукта остаётся только аналитическим, пока пользователь не подтвердил `Docs/Discovery/Interview.md`;\n"
        "- первое записываемое действие, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`, допускается только после открытия рабочей ветки с типом `chore/`;\n"
        "- `docs/` используется только для обычных документационных проходов после снятия стартового гейта;\n"
        "- structural check выполняется локально: `python3 Tools/product_check.py --repo . --mode auto`;\n"
        "- smoke check выполняется локально: `python3 Tools/product_bootstrap_smoke.py`;\n"
        "- переходные `scripts/*` можно использовать только как оболочки к локальным `Tools/*`; после обновления служебного слоя `scripts/*` можно удалить;\n"
        "- report artifacts пишутся в `Tools/.reports/` и не входят в baseline commit.\n",
    )

    write(
        target / "Docs/Discovery/README.md",
        "# Discovery\n\n"
        "`Docs/Discovery/*` хранит текущую истину продукта до перевода в требования и плановый контур.\n\n"
        "## Владелец текущей истины\n"
        "- `Interview.md` — владелец текущей аналитической истины созданного продукта.\n\n"
        "## Минимум начального развёртывания раннего контура старта продукта\n"
        "- `README.md` — карта аналитического слоя.\n"
        "- `Interview.md` — текущее интервью продукта.\n\n"
        "## Gate текущей истины\n"
        "- интервью продукта, созданного начальным развёртыванием, стартует в состоянии `Статус_текущей_истины: Не_подтверждена`;\n"
        "- начальный запрос пользователя не равен полному подтверждению текущей истины;\n"
        "- пока пользователь не ответил явно, созданный репозиторий остаётся только в аналитическом контуре;\n"
        "- агент не заполняет ответы интервью догадками;\n"
        "- неявные предположения фиксируются отдельно как гипотезы;\n"
        "- даже в аналитическом контуре первое записываемое действие допускается только после открытия рабочей ветки;\n"
        "- блокирующие вопросы задаются пользователю до перехода дальше;\n"
        "- bootstrap-заготовки не разрешают переход к `Docs/Product/*`, `Docs/Technical/*`, `Tools/*`, `Pipeline/*` и предметной реализации.\n\n"
        "## Interview protocol\n"
        "- владелец протокола интервью один: `Interview.md`;\n"
        "- вопросы первого прохода собираются по классам `Контекст`, `Граница`, `Ограничение`, `Владение`, `Переход`;\n"
        "- блокирующие вопросы задаются сразу;\n"
        "- неблокирующие вопросы накапливаются для следующей фазы;\n"
        "- узкое интервью всё равно использует тот же нумерованный формат с буквенными вариантами и рекомендуемым вариантом там, где это уместно.\n\n"
        "## Ограничения, стек и зависимости\n"
        "- ограничения первого прохода фиксируются отдельно от выбора стека;\n"
        "- стек и зависимости подтверждаются только явным ответом пользователя, профилем продукта, требованием или отдельным техническим решением;\n"
        "- стандартная библиотека Python считается зависимостью, если модуль зависит от системной среды;\n"
        "- если запуск нельзя проверить, результат фиксируется как `не проверено`.\n\n"
        "## Границы\n"
        "- этот слой не дублирует `Plans/*` и `Logs/*`;\n"
        "- history-fact изменений аналитического слоя закрывается через planning/log contour;\n"
        "- `Discussion`, `Research` и `Requirements` не создаются до отдельного прохода, который явно открывает расширенный аналитический контур.\n",
    )
    write(
        target / "Docs/Discovery/Interview.md",
        "# Interview\n\n"
        "## Назначение\n\n"
        "`Docs/Discovery/Interview.md` — единственный документ-владелец протокола интервью и текущей аналитической истины продукта.\n\n"
        "---\n\n"
        "## Правило актуальности\n\n"
        "Интервью хранит только актуальные вопросы и ответы. История изменений фиксируется через `Plans/*` и `Logs/*`.\n\n"
        "---\n\n"
        "## Статус текущей истины\n\n"
        "Статус_текущей_истины: Не_подтверждена\n"
        "Правило: начальный запрос пользователя не равен полному подтверждению текущей истины.\n"
        "Правило: bootstrap-заготовки и пустые ответы не считаются подтверждением текущей истины.\n"
        "Правило: агент не имеет права заполнять ответы интервью догадками.\n"
        "Правило: неявные предположения фиксируются отдельно как гипотезы.\n"
        "Правило: первое записываемое действие по этому интервью допускается только после открытия рабочей ветки.\n"
        "Правило: до явных ответов пользователя это интервью не разрешает изменения вне `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n\n"
        "Правило: стартовое интервью не приводит примеры функций, которых нет в запросе пользователя или подтверждённых требованиях.\n\n"
        "---\n\n"
        "## Смысловые классы вопросов\n\n"
        "- `Контекст` — кто, для чего и в каком рабочем моменте ждёт результат.\n"
        "- `Граница` — что входит в первую область работ, а что остаётся вне неё.\n"
        "- `Ограничение` — какие лимиты и запреты сдерживают первый проход.\n"
        "- `Владение` — кто утверждает результат и поставляет обязательные входы.\n"
        "- `Переход` — что блокирует следующий шаг, а что можно отложить до следующей фазы.\n\n"
        "---\n\n"
        "## Правило переноса вопросов\n\n"
        "Блокирующий вопрос задаётся сразу. Неблокирующий вопрос не раздувает стартовое интервью и переносится в следующую фазу.\n\n"
        "---\n\n"
        "## Правило выбора стека и зависимостей\n\n"
        "Ограничения первого прохода фиксируются отдельно от выбора стека. Стек и зависимости не записываются как подтверждённые требования без явного источника. Допустимые источники: явный ответ пользователя, профиль продукта, подтверждённое требование или отдельное техническое решение. Если запуск нельзя проверить в текущей среде, результат фиксируется как `не проверено`, а не как успешная проверка.\n\n"
        "---\n\n"
        "## Правило узкого интервью\n\n"
        "Если для подтверждения текущей истины достаточно уточнить только часть вопросов, допускается узкое интервью вместо полного повторного интервью. Оно всё равно обязано сохранять тот же договор формата: нумерованные вопросы, буквенные варианты там, где выбор ограничен, и рекомендуемый вариант там, где это уместно.\n\n"
        "---\n\n"
        "## Вопросы и ответы\n\n"
        "### 1. Кто является первым целевым пользователем или заказчиком результата?\n"
        "Класс вопроса: Контекст\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Один основной пользователь или заказчик.\n"
        "- B. Пользователь или заказчик должен быть уточнён отдельно.\n"
        "- C. Пользователь пока не определён.\n\n"
        "Рекомендуемый вариант: A — он быстрее всего даёт опорную текущую истину для следующего предметного прохода.\n\n"
        "### 2. Какой наблюдаемый результат первого прохода нужно подтвердить или уточнить?\n"
        "Класс вопроса: Контекст\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "### 3. Что обязательно входит в границу первой версии?\n"
        "Класс вопроса: Граница\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Один пользовательский сценарий и один основной результат.\n"
        "- B. Только уже запрошенный минимальный результат.\n"
        "- C. Границу нужно уточнить у пользователя.\n\n"
        "Рекомендуемый вариант: A — он удерживает первую версию в узкой и проверяемой границе.\n\n"
        "### 4. Что явно остаётся вне границы первой версии?\n"
        "Класс вопроса: Граница\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "### 5. Какое ограничение первого прохода нужно подтвердить отдельно от типа продукта и стека?\n"
        "Класс вопроса: Ограничение\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Ограничение уже задано пользователем.\n"
        "- B. Ограничение нужно уточнить у пользователя.\n"
        "- C. Блокирующих ограничений пока не выявлено.\n\n"
        "Рекомендуемый вариант: B — если источник ограничения не подтверждён, его нельзя записывать как требование.\n\n"
        "### 6. Какой источник подтверждает выбор стека первого прохода?\n"
        "Класс вопроса: Ограничение\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Явный ответ пользователя.\n"
        "- B. Профиль продукта или подтверждённое требование.\n"
        "- C. Источник выбора стека пока не подтверждён.\n\n"
        "Рекомендуемый вариант: C — стек не записывается как требование без явного источника.\n\n"
        "### 7. Кто утверждает границу первого результата и поставляет обязательные входы?\n"
        "Класс вопроса: Владение\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "### 8. Какой вопрос нужно задать немедленно, если он блокирует следующий шаг?\n"
        "Класс вопроса: Переход\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "### 9. Какие вопросы можно перенести в следующую фазу без блокировки старта?\n"
        "Класс вопроса: Переход\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Перенести их в следующий явно открытый проход.\n"
        "- B. Задать только если они блокируют подтверждение текущей истины.\n"
        "- C. Не фиксировать без владельца и источника.\n\n"
        "Рекомендуемый вариант: A — он удерживает интервью коротким и не расширяет первую версию без запроса.\n\n"
        "## Связанные артефакты для обязательной проверки\n\n"
        "- `Plans/Roadmap.md`\n"
        "- `Plans/Backlog.md`\n"
        "- active `Plans/*`\n"
        "- `Logs/ChangeLog.md`\n"
        "- `Logs/QualityLog.md`\n\n"
        "---\n",
    )
    write(
        target / "Docs/User/README.md",
        "# User\n\n"
        "`Docs/User/*` — пользовательский слой продуктового репозитория.\n\n"
        "## Состав\n"
        "- `README.md` — карта пользовательского слоя.\n"
        "- `Operating_Mode.md` — режим работы человека с продуктом.\n"
        "- `First_Start.md` — первый маршрут входа.\n"
        "- `Pass_Request.md` — как формулировать проход для агента.\n"
        "- `Usage_Scenarios.md` — базовые сценарии использования.\n\n"
        "## Границы\n"
        "- пользовательский слой не дублирует `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/*`;\n"
        "- пользовательский слой направляет к документам-владельцам продуктового репозитория.\n",
    )
    write(
        target / "Docs/User/Operating_Mode.md",
        "# Operating Mode\n\n"
        "## Назначение\n"
        "Этот документ фиксирует режим работы человека с продуктом.\n\n"
        "## Базовый режим\n"
        "- человек формулирует область и ожидаемый результат прохода;\n"
        "- агент исполняет проход внутри договоров продукта;\n"
        "- текущие этап, задача и план читаются из `../../Plans/*`.\n\n"
        "## Куда идти дальше\n"
        "- текущее состояние планирования: `../../Plans/README.md`;\n"
        "- маршрут агента: `../../AGENTS.md`;\n"
        "- настройка и проверки: `../../Setup_Guide.md`.\n",
    )
    write(
        target / "Docs/User/First_Start.md",
        "# First Start\n\n"
        "## Первый маршрут\n"
        "1. Прочитать `../../README.md`.\n"
        "2. Прочитать `Operating_Mode.md`.\n"
        "3. Прочитать `../../Setup_Guide.md` и открыть рабочую ветку до первого записываемого действия.\n"
        "4. Проверить текущие этап, задачу и план в `../../Plans/*`.\n"
        "5. Прочитать `../Discovery/Interview.md` и только после рабочей ветки ответить на вопросы, которые подтверждают текущую истину.\n"
        "6. Из корня продукта выполнить `python3 Tools/product_check.py --repo . --mode auto`.\n"
        "7. Если нужен локальный smoke, выполнить `python3 Tools/product_bootstrap_smoke.py`.\n\n"
        "## Что дальше\n"
        "- если нужен новый проход: `Pass_Request.md`;\n"
        "- если нужен маршрут исполнения агентом: `../../AGENTS.md`.\n",
    )
    write(
        target / "Docs/User/Pass_Request.md",
        "# Pass Request\n\n"
        "## Назначение\n"
        "Этот документ объясняет, как человеку формулировать проход для агента внутри продуктового репозитория.\n\n"
        "## Минимальная форма\n"
        "1. Назвать текущий `ROAD-*` или указать новый проход внутри него.\n"
        "2. Сформулировать узкую цель прохода.\n"
        "3. Перечислить область и документы-владельцы.\n"
        "4. Перечислить ограничения и допустимые sync-поверхности.\n"
        "5. Указать ожидаемый результат и проверки, если они не спорят с договорами репозитория.\n\n"
        "## На что опираться\n"
        "- `../../Plans/*`;\n"
        "- `../../Docs/User/*`, `../../Docs/Product/*`, `../../Docs/Technical/*`;\n"
        "- `../../Setup_Guide.md` и `../../Tools/*` для маршрута запуска и проверки.\n",
    )
    write(
        target / "Docs/User/Usage_Scenarios.md",
        "# Usage Scenarios\n\n"
        "## Сценарий 1. Войти в продуктовый репозиторий\n"
        "- Прочитать `../../README.md` и `First_Start.md`.\n"
        "- Подтвердить текущую истину в `../../Docs/Discovery/Interview.md` до предметных правок.\n"
        "- Подготовить среду по `../../Setup_Guide.md`.\n"
        "- Проверить структурный контур через `Tools/product_check.py`.\n\n"
        "## Сценарий 2. Запустить новый проход с агентом\n"
        "- Найти текущие этап, задачу и план в `../../Plans/*`.\n"
        "- Сформулировать проход через `Pass_Request.md`.\n"
        "- Направить агента на работу через contracts продукта.\n\n"
        "## Сценарий 3. Работать с продуктовым контуром знания\n"
        "- `Docs/Product/*` — прикладная рамка продукта.\n"
        "- `Docs/Technical/*` — стартовый технический контур.\n"
        "- `Logs/*` — факты и доказательства качества.\n",
    )
    write(
        target / "Docs/Product/README.md",
        "# Product\n\n"
        "## Назначение\n"
        "Слой `Docs/Product/` описывает продукт в прикладных терминах первой версии.\n\n"
        "## Состав слоя\n"
        "- `Product_Passport.md` — паспорт созданного каркаса без домена `Profiles/*`.\n"
        "- `JTBD.md` — пользовательские задачи и ценный результат.\n"
        "- `PRD.md` — продуктовые требования первой версии.\n"
        "- `Delivery.md` — краткая модель поставки продукта.\n",
    )
    write(
        target / "Docs/Product/Product_Passport.md",
        f"# Product Passport — {ctx.name}\n\n"
        "## Назначение\n\n"
        "Паспорт фиксирует минимальные параметры созданного каркаса без возвращения домена `Profiles/*` в продукт.\n\n"
        "---\n\n"
        f"Название: {ctx.name}\n"
        f"Код_продукта: {ctx.product_code}\n"
        f"Брендовый_профиль: {ctx.brand_profile.name}\n"
        f"Язык_взаимодействия: {ctx.brand_profile.interaction_language}\n"
        "Пакеты_каркаса:\n"
        "- Docs\n"
        "- Plans\n"
        "- Logs\n"
        "- Pipeline\n"
        "- Tools\n"
        "- Templates\n"
        "- Schemas\n"
        "- scripts compatibility wrappers\n",
    )
    write(
        target / "Docs/Product/JTBD.md",
        f"# JTBD — {ctx.name}\n\n"
        "## Назначение\n\n"
        f"{ctx.name} помогает пользователю решать прикладную задачу в управляемом продуктовым контуре.\n\n"
        "---\n\n"
        "## Пользователи\n\n"
        "- основные пользователи первой версии продукта;\n\n"
        "---\n\n"
        "## Проблема пользователя\n\n"
        "У пользователя должна быть понятная отправная точка продукта без ручной пересборки базового контура.\n\n"
        "---\n\n"
        "## Задачи пользователя\n\n"
        "1. Когда я начинаю работу с продуктом, то хочу получить понятный стартовый контур, чтобы быстрее перейти к предметному наполнению.\n"
        "2. Когда я продолжаю работу над продуктом, то хочу видеть согласованный набор базовых документов, чтобы не терять контекст.\n\n"
        "---\n\n"
        "## Ценный результат для пользователя\n\n"
        "Пользователь использует продукт, чтобы:\n"
        "- быстрее перейти к предметной работе;\n"
        "- удерживать продукт в понятном и проверяемом состоянии.\n\n"
        "---\n",
    )
    write(
        target / "Docs/Product/PRD.md",
        f"# Product Requirements Document — {ctx.name}\n\n"
        "## 1. Обзор продукта\n\n"
        f"{ctx.name} поставляется как минимальный цифровой продуктовый каркас для дальнейшего предметного развития.\n\n"
        "---\n\n"
        "## 2. Проблема\n\n"
        "Без минимального согласованного каркаса продукт трудно быстро запустить и удерживать в проверяемом состоянии.\n\n"
        "---\n\n"
        "## 3. Цель продукта\n\n"
        "Первая версия должна дать устойчивую отправную точку для дальнейшей предметной разработки.\n\n"
        "---\n\n"
        "## 4. Целевая аудитория\n\n"
        "- ранние пользователи и разработчики продукта.\n\n"
        "---\n\n"
        "## 5. Задачи пользователя\n\n"
        "1. Быстро начать работу с продуктом.\n"
        "2. Удерживать базовый контур продукта согласованным.\n\n"
        "---\n\n"
        "## 6. Основной сценарий\n\n"
        "1. Пользователь получает минимальный каркас продукта.\n"
        "2. Пользователь уточняет предметное содержимое.\n"
        "3. Продукт развивается внутри управляемого репозиторного контура.\n\n"
        "---\n\n"
        "## 7. Область первой версии\n\n"
        "- базовые продуктовые документы;\n"
        "- технический и плановый стартовый контур;\n"
        "- журналы и точки входа проекта.\n\n"
        "---\n\n"
        "## 8. Функциональные требования\n\n"
        "1. Продукт должен иметь минимальный стартовый набор документов.\n"
        "2. Продукт должен поддерживать дальнейшее предметное заполнение.\n"
        "3. Продукт должен оставаться пригодным для проверки через репозиторий.\n\n"
        "---\n\n"
        "## 9. Нефункциональные требования\n\n"
        "1. Каркас должен быть понятным.\n"
        "2. Каркас должен быть воспроизводимым.\n"
        "3. Каркас не должен требовать лишней инфраструктуры на старте.\n\n"
        "---\n\n"
        "## 10. Что не входит в первую версию\n\n"
        "- полная предметная детализация;\n"
        "- сложная автоматизация;\n"
        "- расширенная многоагентная оркестрация.\n\n"
        "---\n\n"
        "## 11. Критерии успеха\n\n"
        "1. Продукт можно быстро запустить на минимальном каркасе.\n"
        "2. Базовые документы остаются согласованными.\n"
        "3. Следующий проход может опираться на уже подготовленный контур.\n\n"
        "---\n",
    )
    write(
        target / "Docs/Product/Delivery.md",
        "# Delivery\n\n"
        "## Назначение\n\n"
        "Продукт поставляется как репозиторий с минимальным согласованным каркасом.\n\n"
        "---\n\n"
        "## Модель передачи\n\n"
        "1. Репозиторий передаётся как единый файловый контур.\n"
        "2. Получатель получает готовую базовую структуру продукта.\n"
        "3. Дальнейшая работа продолжается без ручной пересборки стартового слоя.\n\n"
        "---\n\n"
        "## Обязательные элементы поставки\n\n"
        "- базовая структура репозитория;\n"
        "- продуктовые, технические и плановые документы стартового уровня;\n"
        "- журналы и управляемые точки входа проекта.\n\n"
        "---\n\n"
        "## Ограничения поставки\n\n"
        "- поставка задаёт только минимальный стартовый каркас;\n"
        "- предметное наполнение продукта выполняется отдельным следующим проходом.\n\n"
        "---\n",
    )
    write(
        target / "Docs/Technical/README.md",
        "# Technical\n\n"
        "`Docs/Technical/*` хранит стартовый технический контур продуктового репозитория.\n\n"
        "## Состав\n"
        "- `Architecture.md`\n"
        "- `Interfaces.md`\n"
        "- `System_Invariants.md`\n\n"
        "## Границы\n"
        "- технический слой не подменяет `Plans/*` и `Docs/User/*`;\n"
        "- это только startup subset, а не полная копия technical-layer `BytePress`.\n",
    )
    write(
        target / "Docs/Technical/Architecture.md",
        f"# Architecture\n\n"
        f"`{ctx.name}` создан как первый пригодный к работе product repo с разделением пользовательского входа, продуктового знания, стартового технического контура и планового контура.\n",
    )
    write(
        target / "Docs/Technical/Interfaces.md",
        "# Interfaces\n\n"
        "## Стартовые интерфейсы\n"
        "- пользовательский вход: `README.md`, `Docs/User/*`, `Setup_Guide.md`;\n"
        "- агентный вход: `AGENTS.md`;\n"
        "- плановый вход: `Plans/*`;\n"
        "- маршрут структурной проверки: `Tools/product_check.py`;\n"
        "- маршрут local smoke: `Tools/product_bootstrap_smoke.py`.\n",
    )
    write(
        target / "Docs/Technical/System_Invariants.md",
        "# System_Invariants\n\n"
        "## Инварианты\n"
        "- продукт остаётся отдельным репозиторием вне дерева `BytePress`;\n"
        "- human/agent entry contour не спорит с planning contour;\n"
        "- незаполненный discovery bootstrap не считается разрешением на изменение `Docs/Product/*`, `Docs/Technical/*`, `Tools/*`, `Pipeline/*` или предметной реализации;\n"
        "- product repo не превращается в полную копию `BytePress`.\n",
    )
    write(
        target / "Docs/Terms/README.md",
        "# Terms\n\n"
        "`Docs/Terms/*` хранит минимальный стартовый пакет терминов продукта.\n\n"
        "- `Base_Terms.md` — компактный glossary раннего product-start.\n"
        "- полный словарь `BytePress` сюда не копируется автоматически.\n",
    )
    write(target / "Docs/Terms/Base_Terms.md", render_starter_terms(ctx.starter_terms))

    write(
        target / "Pipeline/README.md",
        "# Pipeline\n\n"
        "`Pipeline/*` хранит лёгкий локальный процессный контур продукта и владеет рабочим процессом агента.\n\n"
        "## Состав\n"
        "- `Phases.md` — минимальные фазы продуктового прохода.\n"
        "- `Workflows.md` — основной путь, первый старт продукта, предметный проход, уровни проверок, журнальное закрытие и PR через `gh`.\n"
        "- `Gates.md` — обязательные переходы и проверки.\n\n"
        "## Граница\n"
        "`AGENTS.md` направляет сюда, но не подменяет этот процессный контур.\n",
    )
    write(
        target / "Pipeline/Phases.md",
        "# Phases\n\n"
        "1. `Подтверждение текущей истины` — подтвердить текущую истину явными ответами пользователя.\n"
        "2. `Синхронизация планирования` — синхронизировать `ROAD/BACK/PLAN`.\n"
        "3. `Реализация` — выполнить документационный, кодовый или тестовый проход.\n"
        "4. `Проверка` — разделить структуру, тесты, запуск, GUI-запуск и ручную проверку.\n"
        "5. `Закрытие` — закрыть журналы, коммиты, push и PR.\n",
    )
    write(
        target / "Pipeline/Workflows.md",
        "# Workflows\n\n"
        "## Основной путь продукта\n"
        "1. Назвать фазу, рабочий поток и гейт.\n"
        "2. Открыть рабочую ветку до первого записываемого действия.\n"
        "3. Подтвердить `ROAD/BACK/PLAN`.\n"
        "4. Прочитать документы-владельцы по области прохода.\n"
        "5. Зафиксировать противоречия, гипотезы и блокирующие вопросы.\n"
        "6. Внести минимальные изменения.\n"
        "7. Выполнить проверки нужного уровня.\n"
        "8. Закрыть `Logs/*`, сделать смысловые коммиты, один push и PR через `gh`.\n\n"
        "## Первый старт продукта\n"
        "Фаза: `Подтверждение текущей истины`.\n"
        "Рабочий поток: `Первый старт продукта`.\n"
        "Гейт: `Гейт текущей истины`.\n\n"
        "1. Не считать начальный запрос пользователя полным подтверждением текущей истины.\n"
        "2. Не заполнять `Docs/Discovery/Interview.md` догадками агента.\n"
        "3. Фиксировать неявные предположения отдельно как гипотезы.\n"
        "4. Задать пользователю блокирующие вопросы.\n"
        "5. Не записывать ограничения первого прохода как подтверждённые требования без явного источника.\n"
        "6. Не записывать стек и зависимости как подтверждённые требования без явного источника.\n"
        "7. После явных ответов синхронизировать `Plans/*` и `Logs/*`.\n"
        "8. Запустить `python3 Tools/product_check.py --repo . --mode auto`.\n\n"
        "## Предметный проход\n"
        "Фаза: `Реализация`.\n"
        "Рабочий поток: `Предметный проход`.\n"
        "Гейт: `Гейт реализации`.\n\n"
        "1. Проверить, что текущая истина подтверждена.\n"
        "2. Подтвердить ограничения первого прохода.\n"
        "3. Подтвердить источник выбора стека: ответ пользователя, профиль продукта, требование или техническое решение.\n"
        "4. Разделить документацию, код, тесты, проверки и журнальное закрытие.\n"
        "5. Если запуск нельзя проверить, записать `не проверено`.\n"
        "6. Не открывать новые домены без владельца, потребителя и проверки.\n\n"
        "## Уровни проверок\n"
        "- `Структура` — обязательные файлы и запрет удалённых доменов.\n"
        "- `Тесты` — автоматические тесты кода.\n"
        "- `Запуск` — фактический CLI, service или smoke route.\n"
        "- `GUI-запуск` — доступность GUI-модуля и среды.\n"
        "- `Ручная проверка` — явно записанное действие, которое нельзя честно автоматизировать.\n\n"
        "## Журнальное закрытие\n"
        "- `ChangeLog.md` фиксирует факт изменения.\n"
        "- `QualityLog.md` фиксирует выполненные проверки и непроверенные зоны.\n"
        "- `ADRlog.md` обновляется для архитектурных, процессных и продуктово-договорных решений.\n\n"
        "## PR-маршрут\n"
        "1. Выполнить одну финальную отправку рабочей ветки.\n"
        "2. Проверить через `gh`, что для рабочей ветки нет открытого PR.\n"
        "3. Создать PR через `gh pr create`.\n"
        "4. GitHub connector не использовать для создания PR.\n"
        "5. Если `gh` недоступен, выполнить push и вернуть параметры для ручного PR.\n",
    )
    write(
        target / "Pipeline/Gates.md",
        "# Gates\n\n"
        "## Гейт текущей истины\n"
        "- `Статус_текущей_истины: Не_подтверждена` удерживает продукт в аналитическом контуре.\n"
        "- Первое записываемое действие требует рабочую ветку.\n"
        "- Свежее состояние проверяется локальным `Tools/product_check.py`.\n\n"
        "## Гейт зависимостей\n"
        "- стек и зависимости требуют явного источника;\n"
        "- ограничения первого прохода фиксируются отдельно от выбора стека;\n"
        "- непроверенный запуск фиксируется как `не проверено`.\n\n"
        "## Гейт запроса на слияние\n"
        "- PR создаётся через `gh` после финальной отправки ветки;\n"
        "- GitHub connector не используется для создания PR.\n",
    )

    write(
        target / "Tools/README.md",
        "# Tools\n\n"
        "`Tools/*` хранит локальные служебные команды продукта.\n\n"
        "## Команды\n"
        "- `product_check.py` — структурная проверка fresh/developed product state.\n"
        "- `product_bootstrap_smoke.py` — локальный smoke route с отчётом в `Tools/.reports/`.\n\n"
        "## Граница\n"
        "Продукт не зависит от `BYTEPRESS_ROOT` для обычной проверки после bootstrap.\n",
    )
    write_executable(target / "Tools/product_check.py", PRODUCT_TOOL_CHECK)
    write_executable(target / "Tools/product_bootstrap_smoke.py", PRODUCT_BOOTSTRAP_SMOKE)

    write(
        target / "Templates/README.md",
        "# Templates\n\n"
        "`Templates/*` хранит только шаблоны артефактов, которые materialize в каркасе продукта.\n",
    )
    for name, template_id, title in [
        ("Interview.md", "TPL-000001", "Interview"),
        ("Roadmap.md", "TPL-000002", "Roadmap"),
        ("Backlog.md", "TPL-000003", "Backlog"),
        ("Plan.md", "TPL-000004", "Plan"),
        ("ChangeLog.md", "TPL-000005", "ChangeLog"),
        ("ADRlog.md", "TPL-000006", "ADRlog"),
        ("QualityLog.md", "TPL-000007", "QualityLog"),
    ]:
        write(target / "Templates" / name, f"# {title}\n\n<!-- ID: {template_id} -->\n\nШаблон артефакта `{title}` продуктового каркаса.\n")

    write(
        target / "Schemas/README.md",
        "# Schemas\n\n"
        "`Schemas/*` хранит только схемы артефактов, которые локальный `Tools/product_check.py` реально проверяет структурно.\n",
    )
    for name, schema_id, title in [
        ("roadmap_item.schema.json", "SCH-000001", "Roadmap item"),
        ("backlog_item.schema.json", "SCH-000002", "Backlog item"),
        ("plan.schema.json", "SCH-000003", "Plan"),
        ("changelog_entry.schema.json", "SCH-000004", "ChangeLog entry"),
        ("adr_entry.schema.json", "SCH-000005", "ADR entry"),
    ]:
        write(
            target / "Schemas" / name,
            "{\n"
            f"  \"$id\": \"{schema_id}\",\n"
            f"  \"title\": \"{title}\",\n"
            "  \"type\": \"object\"\n"
            "}\n",
        )

    write(
        target / "Plans/README.md",
        "# Plans\n\n"
        "`Plans/*` хранит текущие этап, задачу и план продуктового репозитория.\n\n"
        "## Состав\n"
        "- `Roadmap.md` — этапы продукта.\n"
        "- `Backlog.md` — активный реестр работ текущего этапа.\n"
        f"- `Plans/{plan_filename}` — текущий план продукта.\n",
    )
    write(
        target / "Plans/Roadmap.md",
        "# Roadmap\n\n"
        "## Индекс\n"
        "- ROAD-000001 — Подтвердить текущую истину и открыть первый предметный проход продукта\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## ROAD-000001 — Подтвердить текущую истину и открыть первый предметный проход продукта\n"
        "ID: ROAD-000001\n"
        "Этап: Подтвердить текущую истину и открыть первый предметный проход продукта\n"
        "Статус: В_работе\n"
        "Связи: BACK-000001\n"
        "Источник: PLAN-000001\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n"
        "Цель: Подтвердить текущую истину аналитического слоя созданного начальным развёртыванием продукта ответами пользователя и только после этого открыть первый предметный продуктовый проход.\n"
        "Зависимости:\n"
        "Связанные_backlog: BACK-000001\n\n"
        "### Описание\n"
        "Начальное развёртывание уже создало первый пригодный к работе продуктовый репозиторий, но первый стартовый проход продукта остаётся только аналитическим, пока пользователь не подтвердил `Docs/Discovery/Interview.md`. Только после этого допустимо открывать предметный проход вне `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n",
    )
    write(
        target / "Plans/Backlog.md",
        "# Backlog\n\n"
        "## Индекс\n"
        "- ROAD-000001 — Подтвердить текущую истину и открыть первый предметный проход продукта\n\n"
        "## Легенда типов\n"
        "- Продукт\n- Документация\n- Инструмент\n\n"
        "## Легенда приоритетов\n"
        "- Низкий\n- Средний\n- Высокий\n- Критический\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## ROAD-000001 — Подтвердить текущую истину и открыть первый предметный проход продукта\n\n"
        "### Активные\n\n"
        "#### BACK-000001 — Подтвердить текущую истину аналитического слоя созданного начальным развёртыванием продукта\n"
        "ID: BACK-000001\n"
        "Название: Подтвердить текущую истину аналитического слоя созданного начальным развёртыванием продукта\n"
        "Тип: Продукт\n"
        "Приоритет: Высокий\n"
        "Статус: В_работе\n"
        "Связи: ROAD-000001, PLAN-000001\n"
        "Источник: Первый текущий проход продуктового репозитория\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n\n"
        "##### Описание\n"
        "Собрать явные ответы пользователя в `Docs/Discovery/Interview.md`, подтвердить границы первого прохода и только после этого открыть предметный продуктовый проход вне аналитического контура.\n\n"
        "### Завершённые\n"
        "- отсутствуют\n\n"
        "### Кандидаты задач этапа\n"
        "- нет\n\n"
        "---\n",
    )
    write(
        target / "Plans" / plan_filename,
        "# PLAN-000001 — Product initialization\n\n"
        "ID: PLAN-000001\n"
        "Название: Product initialization\n"
        "Статус: В_работе\n"
        "Связи: BACK-000001\n"
        "Источник: Первый текущий проход продуктового репозитория\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n"
        "Основание: Начальное развёртывание создало первый пригодный к работе продуктовый репозиторий; первый стартовый проход продукта остаётся только аналитическим, должен подтвердить текущую истину аналитического слоя ответами пользователя и не трактовать заготовки как разрешение на реализацию.\n"
        "Связанные_требования:\n"
        "Связанные_backlog: BACK-000001\n"
        "Связанные_ADR:\n\n"
        "## Шаги\n"
        "1. Открыть рабочую ветку с типом `chore/` до первого аналитического записываемого действия, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n"
        "   - DoD: первый стартовый проход продукта не идёт из `develop` или `main`.\n"
        "2. Подтвердить текущую истину в `Docs/Discovery/Interview.md` явными ответами пользователя или узким интервью в том же нумерованном / буквенном / рекомендательном формате.\n"
        "   - DoD: статус текущей истины больше не остаётся bootstrap-заготовкой, а свободноформатная замена структурированного выбора не используется.\n"
        "3. Синхронизировать аналитический контур с `Plans/*` и `Logs/*`.\n"
        "   - DoD: плановый и журнальный маршрут отражает подтверждённую текущую истину без выхода в продуктовые документы или реализацию.\n"
        "4. Открыть следующий предметный проход только после подтверждённой текущей истины.\n"
        "   - DoD: следующая область сформулирована отдельно и не смешана с bootstrap-заготовками.\n\n"
        "## Риски\n"
        "- bootstrap-заготовки могут быть ошибочно приняты за утверждённую область;\n"
        "- отсутствие явных ответов пользователя заблокирует предметный проход.\n\n"
        "## Артефакты\n"
        "- AGENTS.md\n- Docs/*\n- Pipeline/*\n- Plans/*\n- Logs/*\n- Tools/*\n- Templates/*\n- Schemas/*\n\n"
        "## DoD\n"
        "Текущая истина созданного начальным развёртыванием продукта подтверждена, аналитический гейт снят явным решением, а следующий предметный проход открыт отдельно.\n",
    )

    write(target / "Logs/README.md", "# Logs\n\nЖурналы фактов продукта.\n")
    write(target / "Logs/ChangeLog.md", "# ChangeLog\n\n## Индекс\n")
    write(target / "Logs/ADRlog.md", "# ADRlog\n\n## Индекс\n")
    write(target / "Logs/QualityLog.md", "# QualityLog\n")
    write(target / "Logs/ReleaseLog.md", "# ReleaseLog\n")
    write(target / "Logs/SupportLog.md", "# SupportLog\n")

    write(
        target / "scripts/README.md",
        "# scripts\n\n"
        "`scripts/*` — переходные shell-оболочки к локальному `Tools/*`.\n\n"
        "Основной служебный слой продукта — `Tools/*`. Новые сценарии должны вызывать `Tools/product_check.py` и `Tools/product_bootstrap_smoke.py` напрямую.\n\n"
        "Срок переходного удаления: после первого прохода обновления служебного слоя созданного продукта или при следующем большом договоре профильного пакета, если продукту не нужны shell-оболочки.\n",
    )
    write_executable(
        target / "scripts/dev-up.sh",
        "#!/usr/bin/env bash\nset -euo pipefail\necho \"No local runtime services are required by this product skeleton.\"\n",
    )
    write_executable(
        target / "scripts/dev-down.sh",
        "#!/usr/bin/env bash\nset -euo pipefail\necho \"No local runtime services are managed by this product skeleton.\"\n",
    )
    write_executable(
        target / "scripts/dev-test.sh",
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "ROOT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"\n"
        "exec python3 \"$ROOT_DIR/Tools/product_check.py\" --repo \"$ROOT_DIR\" --mode auto\n",
    )
    write_executable(
        target / "scripts/integration-smoke.sh",
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "ROOT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"\n"
        "exec python3 \"$ROOT_DIR/Tools/product_bootstrap_smoke.py\"\n",
    )
    write_executable(
        target / "scripts/reset-product-start.sh",
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "ROOT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"\n"
        "REPORT_DIR=\"$ROOT_DIR/Tools/.reports\"\n"
        "if [[ -d \"$REPORT_DIR\" ]]; then\n"
        "  rm -rf \"$REPORT_DIR\"\n"
        "  echo \"Removed local tool reports: $REPORT_DIR\"\n"
        "else\n"
        "  echo \"No local tool reports to remove.\"\n"
        "fi\n\n"
        "if ! command -v git >/dev/null 2>&1; then\n"
        "  echo \"Git is not available; runtime cleanup completed, but tracked drift was not inspected.\"\n"
        "  exit 0\n"
        "fi\n\n"
        "cd \"$ROOT_DIR\"\n"
        "if ! git rev-parse --show-toplevel >/dev/null 2>&1; then\n"
        "  echo \"Tool report cleanup completed. Git repository is not initialized yet, so tracked drift was not inspected.\"\n"
        "  exit 0\n"
        "fi\n\n"
        "STATUS_OUTPUT=\"$(git status --short)\"\n"
        "if [[ -z \"$STATUS_OUTPUT\" ]]; then\n"
        "  echo \"Working tree is clean after runtime cleanup.\"\n"
        "  exit 0\n"
        "fi\n\n"
        "echo \"Current git status after runtime cleanup:\"\n"
        "printf '%s\n' \"$STATUS_OUTPUT\"\n\n"
        "OUT_OF_GATE=\"$(printf '%s\n' \"$STATUS_OUTPUT\" | awk '{print $2}' | grep -Ev '^(Docs/Discovery/|Plans/|Logs/)' || true)\"\n"
        "if [[ -n \"$OUT_OF_GATE\" ]]; then\n"
        "  echo \"Tracked or untracked drift exists outside the early analytical contour:\"\n"
        "  printf '%s\n' \"$OUT_OF_GATE\"\n"
        "  echo \"Canonical reset route: discard this repo and materialize a fresh target with BytePress bootstrap.\"\n"
        "  exit 1\n"
        "fi\n\n"
        "echo \"Remaining drift is limited to Docs/Discovery, Plans, or Logs. Review those edits explicitly before continuing.\"\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Генерация первого пригодного к работе product repo из BytePress")
    parser.add_argument("--name", required=True, help="Название продукта")
    parser.add_argument("--product-code", required=True, help="Код продукта из 2-3 символов верхнего регистра")
    parser.add_argument("--brand-profile", required=True, help="Имя существующего brand profile в BytePress")
    parser.add_argument("--target", required=True, help="Целевой каталог продукта")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    target = Path(args.target).resolve()
    if target.exists() and any(target.iterdir()):
        print("Целевой каталог уже существует и не пуст. Генерация остановлена.")
        return 1

    try:
        ctx = build_context(args, repo_root)
    except ValueError as err:
        print(err)
        return 1

    target.mkdir(parents=True, exist_ok=True)
    bootstrap_product(target, ctx)
    print(f"Сформирован первый пригодный к работе product repo: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

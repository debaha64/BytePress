#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re

PRODUCT_CODE_RE = re.compile(r"^[A-Z]{2,3}$")


@dataclass(frozen=True)
class BrandProfile:
    name: str
    interaction_language: str


@dataclass(frozen=True)
class ProductContext:
    name: str
    product_code: str
    brand_profile: BrandProfile
    current_date: str


def extract_value(text: str, key: str) -> str:
    pattern = rf"^{re.escape(key)}:\s*(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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
    return ProductContext(
        name=name,
        product_code=product_code,
        brand_profile=brand_profile,
        current_date=date.today().isoformat(),
    )


def bootstrap_product(target: Path, ctx: ProductContext) -> None:
    plan_filename = f"{ctx.product_code}-000001-product-initialization.md"

    for path in [
        "Docs/User",
        "Docs/Product",
        "Docs/Technical",
        "Docs/Terms",
        "Runtime",
        "Plans",
        "Logs",
        "Profiles",
        "Adapters/Codex",
        "Adapters/Claude",
        "Adapters/Gemini",
        "Adapters/Local",
        "scripts",
    ]:
        (target / path).mkdir(parents=True, exist_ok=True)

    write(target / ".gitignore", "__pycache__/\n.env\n.venv/\n")
    write(target / "README.md", f"# {ctx.name}\n\nКраткое описание продукта.\n")
    write(
        target / "Setup_Guide.md",
        "# Setup_Guide\n\n"
        "## Базовая среда\n"
        "- Linux или WSL\n"
        "- Git\n"
        "- Python 3.11+\n\n"
        "## Рабочий каталог\n"
        "- Репозиторий продукта располагается отдельно от BytePress.\n\n"
        "## Проверка\n"
        "- использовать локальные скрипты продукта и проектные проверки\n",
    )

    write(target / "Docs/User/README.md", "# User\n\nПользовательский слой знания продукта.\n")
    write(target / "Docs/Product/README.md", "# Product\n\nПродуктовый слой знания продукта.\n")
    write(target / "Docs/Technical/README.md", "# Technical\n\nТехнический слой знания продукта.\n")
    write(target / "Docs/Technical/Architecture.md", "# Architecture\n\nМинимальное описание архитектуры продукта.\n")
    write(target / "Docs/Technical/Interfaces.md", "# Interfaces\n\nМинимальное описание интерфейсов продукта.\n")
    write(target / "Docs/Technical/System_Invariants.md", "# System_Invariants\n\nМинимальные инварианты продукта.\n")
    write(target / "Docs/Terms/README.md", "# Terms\n\nТермины предметной области продукта.\n")
    write(target / "Docs/Terms/Base_Terms.md", "# Base_Terms\n\n## Индекс\n")

    write(target / "Runtime/README.md", "# Runtime\n\nОперативная среда текущего исполнения.\n")
    write(target / "Runtime/Context.md", "# Context\n\nТекущий контекст исполнения.\n")
    write(target / "Runtime/Task.md", "# Task\n\nТекущая задача.\n")
    write(target / "Runtime/Plan.md", "# Plan\n\nЧерновой оперативный план исполнения.\n")
    write(target / "Runtime/Session_Log.md", "# Session_Log\n\nЖурнал текущей сессии.\n")
    write(target / "Runtime/Handover.md", "# Handover\n\nПередача текущего состояния между сессиями.\n")

    write(target / "Profiles/Product.md", f"# Product\n\n"
        f"ID: PROF-000001\n"
        f"Тип_профиля: product\n"
        f"Название: {ctx.name}\n"
        f"Код_продукта: {ctx.product_code}\n"
        f"Брендовый_профиль: {ctx.brand_profile.name}\n"
        f"Язык_взаимодействия: {ctx.brand_profile.interaction_language}\n")

    write(target / "Plans/README.md", "# Plans\n\nУтверждённые планы продукта.\n")
    write(
        target / "Plans/Roadmap.md",
        "# Roadmap\n\n"
        "## Индекс\n"
        "- ROAD-000001 — Сформировать первый предметный пакет продукта\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## ROAD-000001 — Сформировать первый предметный пакет продукта\n"
        "ID: ROAD-000001\n"
        "Этап: Сформировать первый предметный пакет продукта\n"
        "Статус: Черновик\n"
        "Связи: BACK-000001, PLAN-000001\n"
        "Источник: Bootstrap contract sync\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n"
        "Цель: Перевести общий каркас продукта в предметный рабочий пакет.\n"
        "Зависимости:\n"
        "Связанные_backlog: BACK-000001\n\n"
        "### Описание\n"
        "После bootstrap продукт должен получить первый согласованный предметный пакет документации и backlog.\n",
    )
    write(
        target / "Plans/Backlog.md",
        "# Backlog\n\n"
        "## Индекс\n"
        "- BACK-000001 — Уточнить пакет основания продукта\n\n"
        "## Легенда типов\n"
        "- Продукт\n- Документация\n- Инструмент\n\n"
        "## Легенда приоритетов\n"
        "- Низкий\n- Средний\n- Высокий\n- Критический\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## BACK-000001 — Уточнить пакет основания продукта\n"
        "ID: BACK-000001\n"
        "Название: Уточнить пакет основания продукта\n"
        "Тип: Продукт\n"
        "Приоритет: Высокий\n"
        "Статус: Черновик\n"
        "Связи: PLAN-000001\n"
        "Источник: Bootstrap contract sync\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n\n"
        "### Описание\n"
        "Определить предметный пакет `Docs/`, первый backlog и ранние технические ограничения продукта.\n",
    )
    write(
        target / "Plans" / plan_filename,
        "# PLAN-000001 — Product initialization\n\n"
        "ID: PLAN-000001\n"
        "Название: Product initialization\n"
        "Статус: Черновик\n"
        "Связи: BACK-000001\n"
        "Источник: Bootstrap contract sync\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n"
        "Основание: Создание минимального продуктового каркаса.\n"
        "Связанные_требования:\n"
        "Связанные_backlog: BACK-000001\n"
        "Связанные_ADR:\n\n"
        "## Шаги\n"
        "1. Уточнить продуктовый пакет основания. DoD: базовые разделы `Docs/` заполнены.\n"
        "2. Сформировать первый backlog продукта. DoD: есть хотя бы один backlog-элемент.\n"
        "3. Подтвердить управляемые точки входа проекта. DoD: скрипты `dev-up.sh`, `dev-down.sh`, `dev-test.sh` существуют.\n\n"
        "## Риски\n"
        "- каркас может остаться слишком общим без предметного наполнения;\n"
        "- отсутствие раннего backlog затруднит следующий проход.\n\n"
        "## Артефакты\n"
        "- Docs/*\n- Plans/*\n- Logs/*\n- Profiles/Product.md\n- scripts/*\n\n"
        "## DoD\n"
        "Каркас продукта существует как отдельный репозиторий и готов к первому проходу предметного наполнения.\n",
    )

    write(target / "Logs/README.md", "# Logs\n\nЖурналы фактов продукта.\n")
    write(target / "Logs/ChangeLog.md", "# ChangeLog\n\n## Индекс\n")
    write(target / "Logs/ADRlog.md", "# ADRlog\n\n## Индекс\n")
    write(target / "Logs/QualityLog.md", "# QualityLog\n")
    write(target / "Logs/ReleaseLog.md", "# ReleaseLog\n")
    write(target / "Logs/SupportLog.md", "# SupportLog\n")

    write(target / "Adapters/README.md", "# Adapters\n\nКаркас адаптеров моделей продукта.\n")
    for adapter in ["Codex", "Claude", "Gemini", "Local"]:
        write(target / f"Adapters/{adapter}/README.md", f"# {adapter}\n\nКаркас адаптера {adapter}.\n")

    write(target / "scripts/README.md", "# scripts\n\nУправляемые точки входа проекта.\n")
    write(target / "scripts/dev-up.sh", "#!/usr/bin/env bash\nset -euo pipefail\necho \"TODO: поднять окружение продукта\"\n")
    write(target / "scripts/dev-down.sh", "#!/usr/bin/env bash\nset -euo pipefail\necho \"TODO: остановить окружение продукта\"\n")
    write(target / "scripts/dev-test.sh", "#!/usr/bin/env bash\nset -euo pipefail\necho \"TODO: выполнить проверки продукта\"\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Генерация минимального продуктового каркаса BytePress")
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
    print(f"Сформирован минимальный продуктовый каркас: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

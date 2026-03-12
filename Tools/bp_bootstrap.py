#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class ProductContext:
    name: str
    slug: str
    brand: str


def slugify(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "Product"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Генерация минимального продуктового каркаса BytePress")
    parser.add_argument("--name", required=True, help="Название продукта")
    parser.add_argument("--target", required=True, help="Целевой каталог продукта")
    parser.add_argument("--brand", default="Default", help="Название бренда или профиля")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if target.exists() and any(target.iterdir()):
        print("Целевой каталог уже существует и не пуст. Генерация остановлена.")
        return 1

    ctx = ProductContext(name=args.name.strip(), slug=slugify(args.name), brand=args.brand.strip())
    target.mkdir(parents=True, exist_ok=True)

    write(target / "README.md", f"# {ctx.name}\n\nКраткое описание продукта.\n")
    write(
        target / "Setup_Guide.md",
        "# Setup_Guide\n\n"
        "## Базовая среда\n"
        "- Linux или WSL2\n"
        "- Git\n"
        "- Python 3.11+\n\n"
        "## Рабочий каталог\n"
        "- Репозиторий продукта располагается отдельно от BytePress.\n\n"
        "## Проверка\n"
        "- использовать локальные скрипты продукта и проектные проверки\n",
    )

    for path in [
        "Docs/User",
        "Docs/Product",
        "Docs/Technical",
        "Docs/Terms",
        "Runtime",
        "Plans",
        "Logs",
        "Adapters/Codex",
        "Adapters/Claude",
        "Adapters/Gemini",
        "Adapters/Local",
        "scripts",
    ]:
        (target / path).mkdir(parents=True, exist_ok=True)

    write(target / ".gitignore", "__pycache__/\n.env\n.venv/\n")
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

    write(target / "Plans/README.md", "# Plans\n\nУтверждённые планы продукта.\n")
    write(
        target / "Plans/Roadmap.md",
        "# Roadmap\n\n"
        "## Индекс\n"
        "- ROAD-0001 — Сформировать первый предметный пакет продукта\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## ROAD-0001 — Сформировать первый предметный пакет продукта\n"
        "ID: ROAD-0001\n"
        "Этап: Сформировать первый предметный пакет продукта\n"
        "Статус: Черновик\n"
        "Связи: BACK-0001, PLAN-0001\n"
        "Источник: Первичный bootstrap\n"
        "Дата_создания: 2026-03-10\n"
        "Дата_изменения: 2026-03-10\n"
        "Цель: Перевести общий каркас продукта в предметный рабочий пакет.\n"
        "Зависимости:\n"
        "Связанные_backlog: BACK-0001\n\n"
        "### Описание\n"
        "После bootstrap продукт должен получить первый согласованный предметный пакет документации и backlog.\n",
    )
    write(
        target / "Plans/Backlog.md",
        "# Backlog\n\n"
        "## Индекс\n"
        "- BACK-0001 — Уточнить пакет основания продукта\n\n"
        "## Легенда типов\n"
        "- Продукт\n- Документация\n- Инструмент\n\n"
        "## Легенда приоритетов\n"
        "- Низкий\n- Средний\n- Высокий\n- Критический\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## BACK-0001 — Уточнить пакет основания продукта\n"
        "ID: BACK-0001\n"
        "Название: Уточнить пакет основания продукта\n"
        "Тип: Продукт\n"
        "Приоритет: Высокий\n"
        "Статус: Черновик\n"
        "Связи: PLAN-0001\n"
        "Источник: Первичный bootstrap\n"
        "Дата_создания: 2026-03-10\n"
        "Дата_изменения: 2026-03-10\n\n"
        "### Описание\n"
        "Определить предметный пакет `Docs/`, первый backlog и ранние технические ограничения продукта.\n",
    )
    write(
        target / "Plans/PLAN-0001_Product_Initialization.md",
        "# PLAN-0001 — Инициализация продукта\n\n"
        "ID: PLAN-0001\n"
        "Название: Инициализация продукта\n"
        "Статус: Черновик\n"
        "Связи: BACK-0001\n"
        "Источник: Первичный bootstrap\n"
        "Дата_создания: 2026-03-10\n"
        "Дата_изменения: 2026-03-10\n"
        "Основание: Создание минимального продуктового каркаса.\n"
        "Связанные_требования:\n"
        "Связанные_backlog: BACK-0001\n"
        "Связанные_ADR:\n\n"
        "## Шаги\n"
        "1. Уточнить продуктовый пакет основания. DoD: базовые разделы `Docs/` заполнены.\n"
        "2. Сформировать первый backlog продукта. DoD: есть хотя бы один backlog-элемент.\n"
        "3. Подтвердить управляемые точки входа проекта. DoD: скрипты `dev-up`, `dev-down`, `dev-test` существуют.\n\n"
        "## Риски\n"
        "- каркас может остаться слишком общим без предметного наполнения;\n"
        "- отсутствие раннего backlog затруднит следующий проход.\n\n"
        "## Артефакты\n"
        "- Docs/*\n- Plans/*\n- Logs/*\n- scripts/*\n\n"
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

    print(f"Сформирован минимальный продуктовый каркас: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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

    write(
        target / ".gitignore",
        "__pycache__/\n*.pyc\n.env\n.env.*\n.venv/\n.codex\n.codex/\n",
    )
    write(
        target / "README.md",
        f"# {ctx.name}\n\n"
        f"{ctx.name} — first-usable replicated product repo, materialized by `BytePress` bootstrap.\n\n"
        "`README.md` — карта для человека.\n"
        "`AGENTS.md` — карта для агента.\n\n"
        "## Стартовый маршрут\n"
        "1. Прочитать `Docs/User/First_Start.md`.\n"
        "2. Подготовить среду по `Setup_Guide.md`.\n"
        "3. Проверить current stage/task/pass в `Plans/*`.\n"
        "4. Использовать `scripts/dev-test.sh`, если нужен structural check через `BytePress`.\n\n"
        "5. Использовать `scripts/integration-smoke.sh`, если нужен minimal integration handoff check.\n\n"
        "## Доменная карта\n"
        "- `Docs/User/*` — human-facing layer продукта.\n"
        "- `Docs/Product/*` — прикладная рамка продукта.\n"
        "- `Docs/Technical/*` — стартовый technical contour продукта.\n"
        "- `Plans/*` — current roadmap, backlog и current plan продукта.\n"
        "- `Logs/*` — факты, изменения и quality evidence продукта.\n"
        "- `Adapters/*` — модельный contour продукта.\n"
        "- `scripts/*` — project entry scripts.\n",
    )
    write(
        target / "AGENTS.md",
        f"# AGENTS\n\n"
        f"`AGENTS.md` — каноническая entry point карта агента в replicated product repo `{ctx.name}`.\n\n"
        "## Кто такой агент внутри продукта\n"
        "- Humans steer. Agents execute.\n"
        "- Агент работает внутри contracts самого product repo, а не подменяет owner продукта.\n"
        "- Агент ведёт работу через task-ветку, local checks и PR-flow.\n\n"
        "## Source-of-truth hierarchy\n"
        "1. Текущий task-source пользователя.\n"
        "2. `Plans/*` как stage/task/pass owner.\n"
        "3. `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*` как knowledge/contract layers продукта.\n"
        "4. `Logs/*` как фактологический слой.\n"
        "5. `Adapters/*`, `Setup_Guide.md` и `scripts/*` как execution support.\n\n"
        "## Как входить в задачу\n"
        "- Сначала прочитать `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.\n"
        "- Для human-facing route использовать `Docs/User/*`.\n"
        "- Для structural check использовать `scripts/dev-test.sh` с `BYTEPRESS_ROOT`.\n"
        "- Для minimal integration handoff использовать `scripts/integration-smoke.sh` с `BYTEPRESS_ROOT`.\n"
        "- Не дублировать repo contracts длинным ручным промптом, если они уже определены продуктом.\n\n"
        "## Границы\n"
        "- этот файл не подменяет `Docs/User/*`, `Docs/Technical/*` и `Plans/*`;\n"
        "- этот файл направляет агента к owner-documents replicated product repo.\n",
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
        "## Проверка\n"
        "- для structural и integration smoke checks replicated repo установить `BYTEPRESS_ROOT` на путь к исходному `BytePress`;\n"
        "- затем из корня продукта выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/dev-test.sh`;\n"
        "- при проверке controlled integration contour выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/integration-smoke.sh`.\n",
    )

    write(
        target / "Docs/User/README.md",
        "# User\n\n"
        "`Docs/User/*` — канонический human-facing layer replicated product repo.\n\n"
        "## Состав\n"
        "- `README.md` — карта user-layer.\n"
        "- `Operating_Mode.md` — human operating mode продукта.\n"
        "- `First_Start.md` — первый маршрут входа.\n"
        "- `Pass_Request.md` — как формулировать pass для агента.\n"
        "- `Usage_Scenarios.md` — базовые сценарии использования.\n\n"
        "## Границы\n"
        "- user-layer не дублирует `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/*`;\n"
        "- user-layer направляет к owner-documents replicated product repo.\n",
    )
    write(
        target / "Docs/User/Operating_Mode.md",
        "# Operating Mode\n\n"
        "## Назначение\n"
        "Этот документ фиксирует human operating mode продукта.\n\n"
        "## Базовый режим\n"
        "- человек формулирует scope и expected outcome pass;\n"
        "- агент исполняет pass внутри contracts продукта;\n"
        "- current stage/task/pass читаются из `../../Plans/*`.\n\n"
        "## Куда идти дальше\n"
        "- current planning-state: `../../Plans/README.md`;\n"
        "- agent route: `../../AGENTS.md`;\n"
        "- setup и checks: `../../Setup_Guide.md`.\n",
    )
    write(
        target / "Docs/User/First_Start.md",
        "# First Start\n\n"
        "## Первый маршрут\n"
        "1. Прочитать `../../README.md`.\n"
        "2. Прочитать `Operating_Mode.md`.\n"
        "3. Прочитать `../../Setup_Guide.md`.\n"
        "4. Проверить current stage/task/pass в `../../Plans/*`.\n"
        "5. Из корня продукта выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/dev-test.sh`.\n\n"
        "## Что дальше\n"
        "- если нужен новый pass: `Pass_Request.md`;\n"
        "- если нужен agent execution route: `../../AGENTS.md`.\n",
    )
    write(
        target / "Docs/User/Pass_Request.md",
        "# Pass Request\n\n"
        "## Назначение\n"
        "Этот документ объясняет, как человеку формулировать pass для агента внутри replicated product repo.\n\n"
        "## Минимальная форма\n"
        "1. Назвать текущий `ROAD-*` или указать новый pass внутри него.\n"
        "2. Сформулировать узкую цель pass.\n"
        "3. Перечислить scope и owner-documents.\n"
        "4. Перечислить ограничения и допустимые sync-поверхности.\n"
        "5. Указать desired outcome и проверки, если они не спорят с repo contracts.\n\n"
        "## На что опираться\n"
        "- `../../Plans/*`;\n"
        "- `../../Docs/User/*`, `../../Docs/Product/*`, `../../Docs/Technical/*`;\n"
        "- `../../Setup_Guide.md` и `../../scripts/*` для run/check route.\n",
    )
    write(
        target / "Docs/User/Usage_Scenarios.md",
        "# Usage Scenarios\n\n"
        "## Сценарий 1. Войти в replicated product repo\n"
        "- Прочитать `../../README.md` и `First_Start.md`.\n"
        "- Подготовить среду по `../../Setup_Guide.md`.\n"
        "- Проверить structural contour через `scripts/dev-test.sh`.\n\n"
        "## Сценарий 2. Запустить новый pass с агентом\n"
        "- Найти current stage/task/pass в `../../Plans/*`.\n"
        "- Сформулировать pass через `Pass_Request.md`.\n"
        "- Направить агента на работу через contracts продукта.\n\n"
        "## Сценарий 3. Работать с продуктовым knowledge contour\n"
        "- `Docs/Product/*` — прикладная рамка продукта.\n"
        "- `Docs/Technical/*` — стартовый technical contour.\n"
        "- `Logs/*` — факты и quality evidence.\n",
    )
    write(
        target / "Docs/Product/README.md",
        "# Product\n\n"
        "## Назначение\n"
        "Слой `Docs/Product/` описывает продукт в прикладных терминах первой версии.\n\n"
        "## Состав слоя\n"
        "- `JTBD.md` — пользовательские задачи и ценный результат.\n"
        "- `PRD.md` — продуктовые требования первой версии.\n"
        "- `Delivery.md` — краткая модель поставки продукта.\n",
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
        "`Docs/Technical/*` хранит стартовый technical contour replicated product repo.\n\n"
        "## Состав\n"
        "- `Architecture.md`\n"
        "- `Interfaces.md`\n"
        "- `System_Invariants.md`\n\n"
        "## Границы\n"
        "- technical-layer не подменяет `Plans/*` и `Docs/User/*`;\n"
        "- это только startup subset, а не полная копия technical-layer `BytePress`.\n",
    )
    write(
        target / "Docs/Technical/Architecture.md",
        f"# Architecture\n\n"
        f"`{ctx.name}` materialized как first-usable replicated product repo с разделением human/user entry, product knowledge, technical startup contour и planning contour.\n",
    )
    write(
        target / "Docs/Technical/Interfaces.md",
        "# Interfaces\n\n"
        "## Стартовые интерфейсы\n"
        "- human entry: `README.md`, `Docs/User/*`, `Setup_Guide.md`;\n"
        "- agent entry: `AGENTS.md`;\n"
        "- planning entry: `Plans/*`;\n"
        "- structural check route: `scripts/dev-test.sh` с `BYTEPRESS_ROOT`;\n"
        "- integration smoke route: `scripts/integration-smoke.sh` с `BYTEPRESS_ROOT`.\n",
    )
    write(
        target / "Docs/Technical/System_Invariants.md",
        "# System_Invariants\n\n"
        "## Инварианты\n"
        "- продукт остаётся отдельным репозиторием вне дерева `BytePress`;\n"
        "- human/agent entry contour не спорит с planning contour;\n"
        "- product repo не превращается в полную копию `BytePress`.\n",
    )
    write(target / "Docs/Terms/README.md", "# Terms\n\nТермины предметной области продукта.\n")
    write(target / "Docs/Terms/Base_Terms.md", "# Base_Terms\n\n## Индекс\n")

    write(target / "Runtime/README.md", "# Runtime\n\nОперативная среда текущего исполнения.\n")
    write(target / "Runtime/Context.md", "# Context\n\nТекущий контекст исполнения.\n")
    write(target / "Runtime/Task.md", "# Task\n\nТекущая задача.\n")
    write(target / "Runtime/Session_Log.md", "# Session_Log\n\nЖурнал текущей сессии.\n")
    write(target / "Runtime/Handover.md", "# Handover\n\nПередача текущего состояния между сессиями.\n")

    write(target / "Profiles/Product.md", f"# Product\n\n"
        f"ID: PROF-000001\n"
        f"Тип_профиля: product\n"
        f"Название: {ctx.name}\n"
        f"Код_продукта: {ctx.product_code}\n"
        f"Брендовый_профиль: {ctx.brand_profile.name}\n"
        f"Язык_взаимодействия: {ctx.brand_profile.interaction_language}\n")

    write(
        target / "Plans/README.md",
        "# Plans\n\n"
        "`Plans/*` хранит current stage/task/pass replicated product repo.\n\n"
        "## Состав\n"
        "- `Roadmap.md` — stages продукта.\n"
        "- `Backlog.md` — active backlog текущего stage.\n"
        f"- `Plans/{plan_filename}` — current plan продукта.\n",
    )
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
        "Статус: В_работе\n"
        "Связи: BACK-000001\n"
        "Источник: PLAN-000001\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n"
        "Цель: Перевести общий каркас продукта в предметный рабочий пакет.\n"
        "Зависимости:\n"
        "Связанные_backlog: BACK-000001\n\n"
        "### Описание\n"
        "Bootstrap уже materialize first-usable replicated repo, поэтому следующий текущий pass должен перевести стартовый контур в первый предметный пакет продукта.\n",
    )
    write(
        target / "Plans/Backlog.md",
        "# Backlog\n\n"
        "## Индекс\n"
        "- ROAD-000001 — Сформировать первый предметный пакет продукта\n\n"
        "## Легенда типов\n"
        "- Продукт\n- Документация\n- Инструмент\n\n"
        "## Легенда приоритетов\n"
        "- Низкий\n- Средний\n- Высокий\n- Критический\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## ROAD-000001 — Сформировать первый предметный пакет продукта\n\n"
        "### Активные\n\n"
        "#### BACK-000001 — Уточнить пакет основания продукта\n"
        "ID: BACK-000001\n"
        "Название: Уточнить пакет основания продукта\n"
        "Тип: Продукт\n"
        "Приоритет: Высокий\n"
        "Статус: В_работе\n"
        "Связи: ROAD-000001, PLAN-000001\n"
        "Источник: Первый current pass replicated product repo\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n\n"
        "##### Описание\n"
        "Определить предметный пакет `Docs/`, уточнить первый backlog и ранние технические ограничения продукта внутри уже materialized first-usable replicated repo.\n\n"
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
        "Источник: First current pass replicated product repo\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n"
        "Основание: Bootstrap materialize first-usable replicated product repo; текущий pass должен перевести его в первый предметный пакет продукта.\n"
        "Связанные_требования:\n"
        "Связанные_backlog: BACK-000001\n"
        "Связанные_ADR:\n\n"
        "## Шаги\n"
        "1. Уточнить продуктовый пакет основания.\n"
        "   - DoD: базовые разделы `Docs/` заполнены предметным содержимым.\n"
        "2. Сформировать первый backlog продукта.\n"
        "   - DoD: текущая backlog-задача больше не остаётся только bootstrap-placeholder.\n"
        "3. Подтвердить управляемые точки входа проекта.\n"
        "   - DoD: human/agent entry contour и project scripts используются без двусмысленности.\n\n"
        "## Риски\n"
        "- каркас может остаться слишком общим без предметного наполнения;\n"
        "- отсутствие раннего backlog затруднит следующий проход.\n\n"
        "## Артефакты\n"
        "- AGENTS.md\n- Docs/*\n- Plans/*\n- Logs/*\n- Profiles/Product.md\n- Adapters/*\n- scripts/*\n\n"
        "## DoD\n"
        "First-usable replicated product repo переведён в первый предметный рабочий пакет.\n",
    )

    write(target / "Logs/README.md", "# Logs\n\nЖурналы фактов продукта.\n")
    write(target / "Logs/ChangeLog.md", "# ChangeLog\n\n## Индекс\n")
    write(target / "Logs/ADRlog.md", "# ADRlog\n\n## Индекс\n")
    write(target / "Logs/QualityLog.md", "# QualityLog\n")
    write(target / "Logs/ReleaseLog.md", "# ReleaseLog\n")
    write(target / "Logs/SupportLog.md", "# SupportLog\n")

    write(
        target / "Adapters/README.md",
        "# Adapters\n\n"
        "`Adapters/*` хранит минимальный модельный contour replicated product repo.\n\n"
        "## Состав\n"
        "- `Policy.md`\n"
        "- `Registry.md`\n"
        "- `Codex/`, `Claude/`, `Gemini/`, `Local/`\n",
    )
    write(
        target / "Adapters/Policy.md",
        "# Policy\n\n"
        "1. Канонический исполнитель replicated product repo — `Codex`.\n"
        "2. Резервные адаптеры не становятся активным multi-model contour автоматически.\n"
        "3. Адаптеры не подменяют planning, technical или user contracts продукта.\n",
    )
    write(
        target / "Adapters/Registry.md",
        "# Registry\n\n"
        "## Индекс\n"
        "- `ADP-000001` — `Codex`\n"
        "- `ADP-000002` — `Claude`\n"
        "- `ADP-000003` — `Gemini`\n"
        "- `ADP-000004` — `Local`\n\n"
        "---\n\n"
        "## ADP-000001 — Codex\n"
        "ID: ADP-000001\n"
        "Название: Codex\n"
        "Статус: Активен\n"
        "Связи: PROF-000001\n"
        "Источник: Replicated product repo bootstrap\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n\n"
        "### Описание\n"
        "Канонический исполнитель replicated product repo.\n",
    )
    for adapter in ["Codex", "Claude", "Gemini", "Local"]:
        write(target / f"Adapters/{adapter}/README.md", f"# {adapter}\n\nКаркас адаптера {adapter}.\n")

    write(
        target / "scripts/README.md",
        "# scripts\n\n"
        "`scripts/*` — project entry scripts replicated product repo.\n\n"
        "- `dev-up.sh` — placeholder старта локального product contour.\n"
        "- `dev-down.sh` — placeholder остановки локального contour.\n"
        "- `dev-test.sh` — structural check route через `BYTEPRESS_ROOT`.\n"
        "- `integration-smoke.sh` — controlled integration handoff route через `BYTEPRESS_ROOT`.\n",
    )
    write_executable(
        target / "scripts/dev-up.sh",
        "#!/usr/bin/env bash\nset -euo pipefail\necho \"No runtime services are required in baseline 0.2.0. Continue with product-specific setup if needed.\"\n",
    )
    write_executable(
        target / "scripts/dev-down.sh",
        "#!/usr/bin/env bash\nset -euo pipefail\necho \"No runtime services are running in baseline 0.2.0.\"\n",
    )
    write_executable(
        target / "scripts/dev-test.sh",
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "ROOT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"\n"
        "if [[ -z \"${BYTEPRESS_ROOT:-}\" ]]; then\n"
        "  echo \"Set BYTEPRESS_ROOT to the BytePress repository path before running dev-test.sh.\"\n"
        "  exit 1\n"
        "fi\n\n"
        "LINT_SCRIPT=\"$BYTEPRESS_ROOT/Tools/bp_lint.py\"\n"
        "if [[ ! -f \"$LINT_SCRIPT\" ]]; then\n"
        "  echo \"BytePress lint script not found at: $LINT_SCRIPT\"\n"
        "  exit 1\n"
        "fi\n\n"
        "python3 \"$LINT_SCRIPT\" --repo \"$ROOT_DIR\"\n",
    )
    write_executable(
        target / "scripts/integration-smoke.sh",
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "ROOT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"\n"
        "if [[ -z \"${BYTEPRESS_ROOT:-}\" ]]; then\n"
        "  echo \"Set BYTEPRESS_ROOT to the BytePress repository path before running integration-smoke.sh.\"\n"
        "  exit 1\n"
        "fi\n\n"
        "SMOKE_SCRIPT=\"$BYTEPRESS_ROOT/Tools/bp_integration_smoke.py\"\n"
        "if [[ ! -f \"$SMOKE_SCRIPT\" ]]; then\n"
        "  echo \"BytePress integration smoke script not found at: $SMOKE_SCRIPT\"\n"
        "  exit 1\n"
        "fi\n\n"
        "python3 \"$SMOKE_SCRIPT\" --repo \"$ROOT_DIR\"\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Генерация first-usable replicated product repo из BytePress")
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
    print(f"Сформирован first-usable replicated product repo: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

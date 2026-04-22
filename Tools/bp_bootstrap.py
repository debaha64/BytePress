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
        "Docs/Discovery",
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
        "__pycache__/\n*.pyc\n.env\n.env.*\n.venv/\n.codex\n.codex/\nRuntime/Integration_Smoke_Report.json\n",
    )
    write(
        target / "README.md",
        f"# {ctx.name}\n\n"
        f"{ctx.name} — first-usable replicated product repo, materialized by `BytePress` bootstrap.\n\n"
        "`README.md` — карта для человека.\n"
        "`AGENTS.md` — карта для агента.\n\n"
        "## Стартовый маршрут\n"
        "1. Прочитать `Docs/User/First_Start.md`.\n"
        "2. Прочитать `Docs/Discovery/Interview.md` и подтвердить current truth ответами пользователя.\n"
        "3. Подготовить среду по `Setup_Guide.md`.\n"
        "4. Проверить current stage/task/pass в `Plans/*`.\n"
        "5. Использовать `scripts/dev-test.sh`, если нужен structural check через `BytePress`.\n"
        "6. Использовать `scripts/reset-product-start.sh`, если ранний product-start сорвался и нужен cleanup route.\n\n"
        "7. Использовать `scripts/integration-smoke.sh`, если нужен minimal integration handoff check.\n\n"
        "## Доменная карта\n"
        "- `Docs/Discovery/*` — current-truth и интервью продукта.\n"
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
        "2. `Docs/Discovery/*` как current-truth route продукта.\n"
        "3. `Plans/*` как stage/task/pass owner.\n"
        "4. `Docs/User/*`, `Docs/Product/*`, `Docs/Technical/*` как knowledge/contract layers продукта.\n"
        "5. `Logs/*` как фактологический слой.\n"
        "6. `Adapters/*`, `Setup_Guide.md` и `scripts/*` как execution support.\n\n"
        "## Startup-handshake первого ответа\n"
        "- Первый содержательный ответ агента до исследования или правок обязан явно показать startup mode продукта.\n"
        "- В startup-handshake агент коротко фиксирует:\n"
        "  1. какой startup mode он использует для текущего product-start pass;\n"
        "  2. как он понял scope текущего pass;\n"
        "  3. какой branch status он обнаружил;\n"
        "  4. какой branch action / start route он использует;\n"
        "  5. какой planning-state обнаружен: текущие `ROAD/BACK/PLAN` или отсутствие активного этапа;\n"
        "  6. какие owner-domains он читает первыми;\n"
        "  7. какой первый конкретный шаг выполняет дальше.\n"
        "- Startup-handshake должен быть коротким, наблюдаемым и проверяемым по generated product repo.\n\n"
        "## First product-start gate\n"
        "- Bootstrap-created repo стартует с `Docs/Discovery/Interview.md` в состоянии `Статус_текущей_истины: Не_подтверждена`.\n"
        "- Пока пользователь не дал явные ответы и current truth не подтверждена, агент работает только в discovery-only mode.\n"
        "- До открытия task-ветки любые writable changes запрещены, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n"
        "- В этом gate допускаются только `Docs/Discovery/*`, `Plans/*`, `Logs/*` и cleanup route failed pass, но сам writable pass начинается только после branch action в task-ветку.\n"
        "- В этом gate placeholders bootstrap'а не считаются разрешением на изменения в `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*`, `scripts/*` или предметной реализации.\n"
        "- Если failed start дал tracked drift вне разрешённого раннего contour, canonical reset route — fresh bootstrap в новый target.\n\n"
        "## Как входить в задачу\n"
        "- Сначала прочитать `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.\n"
        "- Для bootstrap-created repo сначала прочитать `Docs/Discovery/Interview.md` и проверить, подтверждена ли current truth ответами пользователя.\n"
        "- Для human-facing route использовать `Docs/User/*`.\n"
        "- Для structural check использовать `scripts/dev-test.sh` с `BYTEPRESS_ROOT`.\n"
        "- Для minimal integration handoff использовать `scripts/integration-smoke.sh` с `BYTEPRESS_ROOT`.\n"
        "- Для failed early product-start использовать `scripts/reset-product-start.sh`.\n"
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
        "## Git start route\n"
        "```bash\n"
        "git init -b develop\n"
        "git add .\n"
        "git commit -m \"Bootstrap baseline\"\n"
        "git checkout -b feat/000001-confirm-current-truth\n"
        "```\n\n"
        "## Проверка\n"
        "- первый product-start pass остаётся discovery-only, пока пользователь не подтвердил `Docs/Discovery/Interview.md`;\n"
        "- первый writable action, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`, допускается только после открытия task-ветки;\n"
        "- для structural и integration smoke checks replicated repo установить `BYTEPRESS_ROOT` на путь к исходному `BytePress`;\n"
        "- затем из корня продукта выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/dev-test.sh`;\n"
        "- если ранний product-start сорвался, выполнить `scripts/reset-product-start.sh` и прочитать его drift report;\n"
        "- при проверке controlled integration contour выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/integration-smoke.sh`;\n"
        "- report artifact integration smoke будет записан в `Runtime/Integration_Smoke_Report.json` как runtime-local файл;\n"
        "- baseline commit generated repo не должен содержать этот artifact по умолчанию; если текущий pass явно сохраняет smoke evidence в Git, это решение должно быть зафиксировано в current `Plan` и итоговом отчёте.\n",
    )

    write(
        target / "Docs/Discovery/README.md",
        "# Discovery\n\n"
        "`Docs/Discovery/*` хранит current-truth продукта до перевода в требования и planning contour.\n\n"
        "## Current-truth owner\n"
        "- `Interview.md` — owner текущей аналитической истины generated product repo.\n\n"
        "## Bootstrap minimum раннего product-start contour\n"
        "- `README.md` — карта discovery-layer.\n"
        "- `Interview.md` — текущее интервью продукта.\n\n"
        "## Gate текущей истины\n"
        "- bootstrap-created interview стартует в состоянии `Статус_текущей_истины: Не_подтверждена`;\n"
        "- пока пользователь не ответил явно, generated repo остаётся в discovery-only contour;\n"
        "- даже в discovery-only contour первый writable action допускается только после открытия task-ветки;\n"
        "- placeholders bootstrap'а не разрешают переход к `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*` и предметной реализации.\n\n"
        "## Формат интервью\n"
        "- вопросы фиксируются нумерованно;\n"
        "- если выбор ограничен, использовать буквенные варианты ответа;\n"
        "- если есть предпочтительный route, помечать рекомендуемый вариант;\n"
        "- если достаточно узкого delta-интервью, оно всё равно использует тот же numbered / lettered / recommended format.\n\n"
        "## Границы\n"
        "- этот слой не дублирует `Plans/*` и `Logs/*`;\n"
        "- history-fact изменений discovery-layer закрывается через planning/log contour;\n"
        "- `Discussion`, `Research` и `Requirements` не materialize до отдельного pass, который явно открывает расширенный discovery contour.\n",
    )
    write(
        target / "Docs/Discovery/Interview.md",
        "# Interview\n\n"
        "## Назначение интервью\n\n"
        "`Docs/Discovery/Interview.md` является owner-document текущей аналитической истины о продукте до её перевода в требования и planning contour.\n\n"
        "---\n\n"
        "## Правило актуальности\n\n"
        "Интервью хранит только актуальные вопросы и ответы. История изменений фиксируется через `Plans/*` и `Logs/*`.\n\n"
        "---\n\n"
        "## Статус текущей истины\n\n"
        "Статус_текущей_истины: Не_подтверждена\n"
        "Правило: bootstrap placeholders и пустые ответы не считаются подтверждением current truth.\n"
        "Правило: первый writable action по этому интервью допускается только после открытия task-ветки.\n"
        "Правило: до явных ответов пользователя это интервью не разрешает изменения вне `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n\n"
        "---\n\n"
        "## Правило delta-интервью\n\n"
        "Если для подтверждения current truth достаточно уточнить только часть вопросов, допускается узкое delta-интервью вместо полного повторного интервью. Оно всё равно обязано сохранять тот же format contract: нумерованные вопросы, буквенные варианты там, где выбор ограничен, и рекомендуемый вариант там, где это уместно.\n\n"
        "---\n\n"
        "## Вопросы и ответы\n\n"
        "### 1. Какую текущую истину о продукте нужно зафиксировать первой?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Основной пользователь и его задача.\n"
        "- B. Граница первой версии продукта.\n"
        "- C. Ключевое ограничение реализации.\n\n"
        "Рекомендуемый вариант: A — он быстрее всего даёт опорную current truth для следующего предметного pass.\n\n"
        "### 2. Какая граница первой версии сейчас выглядит самой вероятной?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Один пользовательский сценарий и один основной результат.\n"
        "- B. Полный release-ready продукт сразу.\n"
        "- C. Только технический эксперимент без user value.\n\n"
        "Рекомендуемый вариант: A — он удерживает первую версию в узком и проверяемом scope.\n\n"
        "### 3. Какой факт о продукте пока остаётся самым неопределённым?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "### 4. Какое ограничение сильнее всего влияет на первый pass продукта?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Ограничение времени и узкого scope.\n"
        "- B. Обязательная полная автоматизация с первого дня.\n"
        "- C. Требование открыть сразу все будущие домены.\n\n"
        "Рекомендуемый вариант: A — ранний product-start contour должен оставаться узким и управляемым.\n\n"
        "### 5. Какой основной пользовательский результат должен стать наблюдаемым после первого pass?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "### 6. Какие артефакты являются первыми owner-documents продукта для этого scope?\n"
        "Ответ: `Docs/Discovery/Interview.md`, `Docs/Product/*`, `Plans/*` и при необходимости `Docs/Technical/*`.\n\n"
        "### 7. Какой route дальнейшего уточнения discovery сейчас нужен после интервью?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "Варианты ответа:\n"
        "- A. Открыть отдельный pass на `Discussion` / `Research` / `Requirements`, если minimum уже недостаточен.\n"
        "- B. Сразу переписать планы без фиксации новой current truth.\n"
        "- C. Оставить discovery только в устном виде.\n\n"
        "Рекомендуемый вариант: A — он открывает расширенный discovery contour только по явному решению.\n\n"
        "### 8. Какие артефакты нужно проверить после обновления этого интервью?\n"
        "Ответ: `Plans/Roadmap.md`, `Plans/Backlog.md`, active `Plans/*`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`.\n\n"
        "### 9. Что сейчас остаётся вне scope первого product-start pass?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "### 10. Какой следующий конкретный шаг должен последовать сразу после согласования интервью?\n"
        "Ответ: Не подтверждено пользователем.\n\n"
        "---\n",
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
        "3. Прочитать `../../Setup_Guide.md` и открыть task-ветку до первого writable action.\n"
        "4. Проверить current stage/task/pass в `../../Plans/*`.\n"
        "5. Прочитать `../Discovery/Interview.md` и только после task-ветки ответить на вопросы, которые подтверждают current truth.\n"
        "6. Из корня продукта выполнить `BYTEPRESS_ROOT=/path/to/BytePress scripts/dev-test.sh`.\n"
        "7. Если ранний product-start сорвался, выполнить `../../scripts/reset-product-start.sh`.\n\n"
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
        "- Подтвердить current truth в `../../Docs/Discovery/Interview.md` до предметных правок.\n"
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
        "- незаполненный discovery bootstrap не считается разрешением на изменение `Docs/Product/*`, `Docs/Technical/*`, `Runtime/*` или предметной реализации;\n"
        "- product repo не превращается в полную копию `BytePress`.\n",
    )
    write(target / "Docs/Terms/README.md", "# Terms\n\nТермины предметной области продукта.\n")
    write(target / "Docs/Terms/Base_Terms.md", "# Base_Terms\n\n## Индекс\n")

    write(
        target / "Runtime/README.md",
        "# Runtime\n\n"
        "Оперативная среда текущего исполнения.\n\n"
        "- `Runtime/Integration_Smoke_Report.json` materialize только после фактического smoke run;\n"
        "- baseline commit generated repo не должен содержать этот artifact по умолчанию.\n",
    )
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
        "- ROAD-000001 — Подтвердить current truth и открыть первый предметный pass продукта\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## ROAD-000001 — Подтвердить current truth и открыть первый предметный pass продукта\n"
        "ID: ROAD-000001\n"
        "Этап: Подтвердить current truth и открыть первый предметный pass продукта\n"
        "Статус: В_работе\n"
        "Связи: BACK-000001\n"
        "Источник: PLAN-000001\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n"
        "Цель: Подтвердить bootstrap-created discovery current truth ответами пользователя и только после этого открыть первый предметный product pass.\n"
        "Зависимости:\n"
        "Связанные_backlog: BACK-000001\n\n"
        "### Описание\n"
        "Bootstrap уже materialize first-usable replicated repo, но первый product-start pass остаётся discovery-only, пока пользователь не подтвердил `Docs/Discovery/Interview.md`. Только после этого допустимо открывать предметный pass вне `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n",
    )
    write(
        target / "Plans/Backlog.md",
        "# Backlog\n\n"
        "## Индекс\n"
        "- ROAD-000001 — Подтвердить current truth и открыть первый предметный pass продукта\n\n"
        "## Легенда типов\n"
        "- Продукт\n- Документация\n- Инструмент\n\n"
        "## Легенда приоритетов\n"
        "- Низкий\n- Средний\n- Высокий\n- Критический\n\n"
        "## Легенда статусов\n"
        "- Черновик\n- Готово_к_утверждению\n- Утверждено\n- В_работе\n- Завершено\n- Отменено\n\n"
        "---\n\n"
        "## ROAD-000001 — Подтвердить current truth и открыть первый предметный pass продукта\n\n"
        "### Активные\n\n"
        "#### BACK-000001 — Подтвердить discovery current truth bootstrap-created продукта\n"
        "ID: BACK-000001\n"
        "Название: Подтвердить discovery current truth bootstrap-created продукта\n"
        "Тип: Продукт\n"
        "Приоритет: Высокий\n"
        "Статус: В_работе\n"
        "Связи: ROAD-000001, PLAN-000001\n"
        "Источник: Первый current pass replicated product repo\n"
        f"Дата_создания: {ctx.current_date}\n"
        f"Дата_изменения: {ctx.current_date}\n\n"
        "##### Описание\n"
        "Собрать явные ответы пользователя в `Docs/Discovery/Interview.md`, подтвердить границы first pass и только после этого открыть предметный product pass вне discovery-only contour.\n\n"
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
        "Основание: Bootstrap materialize first-usable replicated product repo; первый pass должен подтвердить discovery current truth ответами пользователя и не трактовать placeholders как разрешение на implementation.\n"
        "Связанные_требования:\n"
        "Связанные_backlog: BACK-000001\n"
        "Связанные_ADR:\n\n"
        "## Шаги\n"
        "1. Открыть task-ветку до первого writable action, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`.\n"
        "   - DoD: первый product-start pass не идёт из `develop` или `main`.\n"
        "2. Подтвердить current truth в `Docs/Discovery/Interview.md` явными ответами пользователя или узким delta-интервью в том же numbered / lettered / recommended format.\n"
        "   - DoD: статус current truth больше не остаётся bootstrap-placeholder, а свободноформатная замена structured choice не используется.\n"
        "3. Синхронизировать discovery-only contour с `Plans/*` и `Logs/*`.\n"
        "   - DoD: planning/log route отражает подтверждённую current truth без выхода в product docs или implementation.\n"
        "4. Открыть следующий предметный pass только после подтверждённой current truth.\n"
        "   - DoD: следующий scope сформулирован отдельно и не смешан с bootstrap placeholders.\n\n"
        "## Риски\n"
        "- bootstrap placeholders могут быть ошибочно приняты за утверждённый scope;\n"
        "- отсутствие явных ответов пользователя заблокирует предметный pass.\n\n"
        "## Артефакты\n"
        "- AGENTS.md\n- Docs/*\n- Plans/*\n- Logs/*\n- Profiles/Product.md\n- Adapters/*\n- scripts/*\n\n"
        "## DoD\n"
        "Bootstrap-created current truth подтверждена, discovery-only gate снят явным решением, а следующий предметный pass открыт отдельно.\n",
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
        "- `integration-smoke.sh` — controlled integration handoff route через `BYTEPRESS_ROOT` с runtime-local report artifact в `Runtime/Integration_Smoke_Report.json`.\n"
        "- `reset-product-start.sh` — cleanup route failed early product-start с drift report.\n"
        "- report artifact по умолчанию остаётся вне baseline commit и force-add допускается только при явном evidence-preservation решении текущего pass.\n",
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
        "REPORT_PATH=\"$ROOT_DIR/Runtime/Integration_Smoke_Report.json\"\n"
        "if [[ ! -f \"$SMOKE_SCRIPT\" ]]; then\n"
        "  echo \"BytePress integration smoke script not found at: $SMOKE_SCRIPT\"\n"
        "  exit 1\n"
        "fi\n\n"
        "python3 \"$SMOKE_SCRIPT\" --repo \"$ROOT_DIR\" --report \"$REPORT_PATH\"\n"
        "echo \"Integration smoke report written to: $REPORT_PATH\"\n",
    )
    write_executable(
        target / "scripts/reset-product-start.sh",
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n\n"
        "ROOT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"\n"
        "REPORT_PATH=\"$ROOT_DIR/Runtime/Integration_Smoke_Report.json\"\n"
        "if [[ -f \"$REPORT_PATH\" ]]; then\n"
        "  rm -f \"$REPORT_PATH\"\n"
        "  echo \"Removed runtime-local smoke artifact: $REPORT_PATH\"\n"
        "else\n"
        "  echo \"No runtime-local smoke artifact to remove.\"\n"
        "fi\n\n"
        "if ! command -v git >/dev/null 2>&1; then\n"
        "  echo \"Git is not available; runtime cleanup completed, but tracked drift was not inspected.\"\n"
        "  exit 0\n"
        "fi\n\n"
        "cd \"$ROOT_DIR\"\n"
        "if ! git rev-parse --show-toplevel >/dev/null 2>&1; then\n"
        "  echo \"Runtime cleanup completed. Git repository is not initialized yet, so tracked drift was not inspected.\"\n"
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
        "  echo \"Tracked or untracked drift exists outside the early discovery-only contour:\"\n"
        "  printf '%s\n' \"$OUT_OF_GATE\"\n"
        "  echo \"Canonical reset route: discard this repo and materialize a fresh target with BytePress bootstrap.\"\n"
        "  exit 1\n"
        "fi\n\n"
        "echo \"Remaining drift is limited to Docs/Discovery, Plans, or Logs. Review those edits explicitly before continuing.\"\n",
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

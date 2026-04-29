# PLAN-000084 — Semantic cleanup after retired domain removal

ID: PLAN-000084
Название: Semantic cleanup after retired domain removal
Статус: В_работе
Связи: ROAD-000031, BACK-000096, ADR-000024
Источник: Запрос владельца от 2026-04-30
Дата_создания: 2026-04-30
Дата_изменения: 2026-04-30
Основание: После удаления преждевременных доменов в активном слое остались прямые ссылки, дубли планового контура, раздробленный каталог правил и незафиксированное правило семантического именования путей и файлов.
Связанные_требования:
- AGENTS.md
- Pipeline/Workflows.md
- Rules/*
- Docs/Technical/Domain_Model_Migration_Plan.md
- Tools/bp_bootstrap.py
- Tools/bp_lint.py
Связанные_backlog:
- BACK-000096
Связанные_ADR:
- ADR-000024
Артефакты:
- AGENTS.md
- README.md
- Rules/*
- Docs/*
- Pipeline/*
- Templates/*
- Schemas/*
- Tools/*
- Plans/*
- Logs/*
Риски:
- Исторические архивы могут сохранять ссылки на retired domains как факты прошлого.
- Переименование правил требует синхронизации прямых ссылок и generated product skeleton.
- Проверки fresh/developed product repo не должны быть ослаблены.
DoD:
- Дублирование `PLAN-000082` устранено без переписывания исторического смысла.
- Активные ссылки на `Adapters`, `Memory`, `MCP`, `Runtime`, `Roles`, `Skills`, `Standards` удалены или заменены владельцами смысла.
- `Rules/*` сгруппирован как каталог предметных правил с короткими именами файлов.
- Правило семантического именования путей и файлов закреплено в действующем owner-domain.
- `bp_bootstrap.py` и `bp_lint.py` синхронизированы с новыми правилами и retired domains.
- Обязательные проверки из запроса пройдены.
- Плановый и журнальный контур закрыт.

## Шаги
1. Исправить дублирование `PLAN-000082`.
   - DoD: ошибочный архивный проход получает уникальный ID и собственные связи.
2. Провести ревизию retired domain references.
   - DoD: активный слой не ссылается на удалённые домены как на действующие владельцы смысла.
3. Упорядочить `Rules/*`.
   - DoD: правила сгруппированы по областям договора, ID и обязательные условия сохранены.
4. Закрепить semantic path/file naming.
   - DoD: правило находится в подходящем владельце смысла и проверяется tooling/doc links.
5. Синхронизировать tools и generated product skeleton.
   - DoD: fresh/developed/auto checks не ослаблены и generated `AGENTS.md` / `Pipeline` не ссылаются на retired domains.
6. Закрыть logs, checks, commits, push and PR.
   - DoD: `ChangeLog`, `QualityLog`, planning archive и PR в `develop` согласованы.

## Результат
Не заполнено до завершения прохода.

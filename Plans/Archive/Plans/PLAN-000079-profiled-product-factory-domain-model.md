# PLAN-000079 — Профильная фабрика продуктовых каркасов и сокращение доменной модели

ID: PLAN-000079
Название: Профильная фабрика продуктовых каркасов и сокращение доменной модели
Статус: Завершено
Связи: ROAD-000026, BACK-000091, ADR-000022, CHG-000091, QL-000086
Источник: Решение владельца от 2026-04-28
Дата_создания: 2026-04-28
Дата_изменения: 2026-04-28
Основание: Принято решение перейти от разросшейся доменной модели к профильной фабрике самодостаточных продуктовых каркасов.
Связанные_требования:
- AGENTS.md
Связанные_backlog:
- BACK-000091
Связанные_ADR:
- ADR-000022
Артефакты:
- Logs/ADRlog.md
- Docs/Technical/Architecture.md
- Docs/Technical/Model.md
- Docs/Technical/Interfaces.md
- Docs/Technical/System_Invariants.md
- Docs/Technical/README.md
- Docs/Technical/Product_Bootstrap_Contract.md
- Docs/Technical/Product_Bootstrap_Domain_Matrix.md
- Docs/Technical/Domain_Model_Migration_Plan.md
- Rules/README.md
- Rules/Premature_Domains_Are_Removed.md
- Standards/README.md
- Pipeline/README.md
- Tools/README.md
- Plans/Roadmap.md
- Plans/Backlog.md
- Plans/Archive/Backlog/ROAD-000026.md
- Logs/ChangeLog.md
- Logs/QualityLog.md
Риски:
- Target matrix временно расходится с текущей реализацией `bp_bootstrap.py` и `bp_lint.py` до отдельного tool-migration pass.
- Сокращение доменов может сломать structural lint, если удалить files до обновления checks.
- Перенос `scripts/*` в product-local `Tools/*` требует отдельного service-update route для уже созданных продуктов.
DoD:
- `ADR-000022` фиксирует архитектурное решение.
- Target package matrix и migration plan оформлены документно.
- Owner-documents синхронизированы вокруг целевой модели.
- Домены не удалены в этом pass.
- `Minesweeper`, `bp_bootstrap.py` и `bp_lint.py` не изменены.
- `Plans/*` и `Logs/*` закрыты.
- `git diff --check` и `python3 Tools/bp_lint.py --repo .` пройдены.

## Шаги
1. Зафиксировать архитектурное решение
   - Описание: добавить ADR о профильной фабрике и self-contained product skeleton.
   - DoD: ADR содержит контекст, решение и последствия.
2. Обновить owner-documents
   - Описание: синхронизировать architecture/model/interfaces/bootstrap matrix/rules/tools/pipeline с target model.
   - DoD: документы различают текущую реализацию и целевую миграцию.
3. Подготовить migration plan
   - Описание: описать удаления, переносы, объединения, проверки и риски.
   - DoD: массовое удаление не выполняется, порядок будущих passes понятен.
4. Закрыть планово-журнальный контур
   - Описание: обновить `Roadmap`, `Backlog`, archive plan/backlog, `ChangeLog`, `QualityLog`.
   - DoD: `ROAD/BACK/PLAN` согласованы и нет активного dangling plan.
5. Проверить и подготовить PR
   - Описание: выполнить обязательные checks, commit, push и PR.
   - DoD: проверки из запроса пройдены, ветка pushed, PR открыт в `develop`.

## Результат
Целевая доменная модель `BytePress` зафиксирована как профильная фабрика самодостаточных продуктовых каркасов. Подготовлен безопасный migration plan без массового удаления доменов и без изменения инструментов текущего bootstrap/lint contour.

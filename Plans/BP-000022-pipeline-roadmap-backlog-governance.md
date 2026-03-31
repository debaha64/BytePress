# PLAN-000022 — Pipeline, roadmap, and backlog governance

ID: PLAN-000022
Название: Обновить Pipeline, Roadmap и Backlog под governance canon
Статус: В_работе
Связи: BACK-000032
Источник: Strategic governance pass после уточнения domain participation contract
Дата_создания: 2026-03-31
Дата_изменения: 2026-03-31
Основание: Текущие `Pipeline.md`, `Roadmap.md` и `Backlog.md` больше не соответствуют принятому канону непрерывного дальнего пути, порождения backlog-задач из этапов roadmap и полного порядка фаз конвейера. Нужно обновить governance-layer одним проходом без новых шаблонов, без новых артефактов `Discussion/Research/Requirements` и без выхода в большой repo-wide audit.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000032
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Добавить backlog-item текущей governance-задачи и отдельный plan-file.
   - DoD: `Plans/Backlog.md` и `Plans/BP-000022-pipeline-roadmap-backlog-governance.md` отражают scope и ограничения текущего pass.
2. Выровнять `Pipeline` и `Roadmap`.
   - Описание: Зафиксировать полный канон фаз, правило `Roadmap -> Backlog -> Plan` и переписать `Plans/Roadmap.md` в непрерывный дальний путь `ROAD-000001`...`ROAD-000014`.
   - DoD: `Pipeline.md` и `Roadmap.md` согласованы с принятым governance canon без дублирования lifecycle contract.
3. Перестроить `Backlog` как производный слой roadmap.
   - Описание: Перегруппировать backlog по `ROAD-*`, исправить индекс и порядок, завести активные задачи для `ROAD-000007`, а для будущих этапов оставить только кандидаты задач без `BACK-ID`.
   - DoD: `Backlog.md` следует `Roadmap.md`, хранит историю закрытых задач и не допускает произвольного пополнения вне этапов roadmap.
4. Закрыть pass в плановом и журнальном контуре.
   - Описание: Обновить `ChangeLog` и `QualityLog`, а `ADR` и `bp_lint.py` менять только при доказанной необходимости.
   - DoD: `python3 Tools/bp_lint.py --repo .` проходит, backlog-item и plan переведены в финальный статус по факту результата.

## Риски
- переписывание governance-layer без строгого ограничения scope легко превратится в большой planning refactor;
- несогласованность между `Roadmap` и `Backlog` разрушит новый канон производного слоя;
- добавление будущих артефактов и шаблонов в этом pass выведет задачу за пределы согласованного scope.

## Артефакты
- `Plans/Backlog.md`
- `Plans/BP-000022-pipeline-roadmap-backlog-governance.md`
- `Docs/Technical/Pipeline.md`
- `Plans/Roadmap.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- `Pipeline.md` содержит полный канон фаз и правило `Roadmap -> Backlog -> Plan`.
- `Roadmap.md` приведён к непрерывной нумерации `ROAD-000001`...`ROAD-000014`.
- `Backlog.md` перегруппирован по `ROAD-*`, с секциями `Активные` и `Завершённые`.
- порядок и индекс backlog исправлены.
- у `ROAD-000007` есть реальные активные задачи.
- для будущих этапов заведены кандидаты задач без `BACK-ID`.
- правило по шаблонам не нарушено.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только если реально нужен.
- `bp_lint.py` меняется только если обязательный contract действительно изменяется.

# PLAN-000044 — Clarify technical interfaces core

ID: PLAN-000044
Название: Пересобрать Interfaces.md как interface-contract
Статус: Завершено
Связи: BACK-000056
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После boundary-pass, contract-map pass, architecture-core pass, model-core pass и artifact-lifecycle pass required core technical-layer уже получил entrypoint, карту доменов, модель сущностей и lifecycle-contract, но `Docs/Technical/Interfaces.md` остаётся кратким legacy-list без явной карты внутренних и внешних интерфейсов, классификации stable/service/derived interfaces и без ясного разведения interface-layer с architecture-, model-, lifecycle- и process-layer.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000056
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать interfaces-core pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `Interfaces.md`.
   - DoD: `ROAD-000010`, `BACK-000056` и `PLAN-000044` согласованы как текущий stage/task/pass.
2. Провести audit текущего interface-contract.
   - Описание: Проверить `Docs/Technical/Interfaces.md` на пробелы и смысловые пересечения с `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`.
   - DoD: подтверждены реальные gaps текущего `Interfaces.md`, а не открыт новый redesign technical-layer.
3. Пересобрать `Interfaces.md` как канонический contract интерфейсов.
   - Описание: Зафиксировать внутренние и внешние интерфейсы `BytePress`, допустимые точки стыка между доменами, stable/service/derived classes и недопустимые обходы границ.
   - DoD: читателю ясно, чем `Interfaces.md` отличается от `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md` и `Pipeline/*`, без дублирования process-canon.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужен ли update `bp_lint.py`.
   - DoD: tooling меняется только если interfaces-core pass реально меняет обязательный contract check.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000056`, индекс backlog, `ROAD-000010`, `PLAN-000044` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md` и других technical-documents;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`.

## Риски
- если `Interfaces.md` останется коротким списком связей, required core technical-layer останется неполным по interface-contract и точкам стыка;
- если перенести в `Interfaces.md` архитектурную карту, ownership-модель или lifecycle-checklist, pass снова смешает interface-layer с `Architecture.md`, `Model.md` и `Artifact_Lifecycle.md`;
- если менять unrelated standards или lint без фактической необходимости, interfaces-core pass выйдет за узкий scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000044-clarify-technical-interfaces-core.md`
- `Plans/Archive/PLAN-000043-clarify-technical-artifact-lifecycle.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Pipeline.md`
- `Pipeline/README.md`
- `Pipeline/Artifacts.md`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для interfaces-core pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/Interfaces.md` является ясным contract интерфейсов текущей системы.
- разведение `Interfaces.md`, `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md` и `Pipeline/*` описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Interfaces.md` пересобран как канонический interface-contract текущего `BytePress`: в одном document теперь явно разведены внутренние и внешние интерфейсы, stable/service/derived classes, допустимые touchpoints и недопустимые обходы границ.
- `Interfaces.md` больше не выглядит как короткий legacy-list связей: отношение interface-layer к `Plans/*`, `Runtime/*`, `Logs/*` и `Pipeline/*` зафиксировано отдельно от архитектурной карты, ownership-модели и lifecycle-contract.
- `Pipeline/README.md` минимально синхронизирован, чтобы process-domain оставался источником истины именно для process-canon и не спорил с уже зафиксированными technical contracts.
- дополнительные изменения в `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/Pipeline.md`, `Standards/*`, `Plans/README.md` и `bp_lint.py` не потребовались: audit не подтвердил другого active-layer contradiction за пределами `Interfaces.md` и одной прямой формулировки в `Pipeline/README.md`.
- `bp_lint contract unaffected`

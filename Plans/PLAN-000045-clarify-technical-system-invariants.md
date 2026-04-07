# PLAN-000045 — Clarify technical system invariants

ID: PLAN-000045
Название: Пересобрать System_Invariants.md как invariant-contract
Статус: В_работе
Связи: BACK-000057
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: Required core technical-layer уже включает `System_Invariants.md` в `Docs/Technical/README.md`, bootstrap product skeleton уже materialize этот singleton document, но текущий active `Docs/Technical/System_Invariants.md` остаётся legacy-list без явного места в required core, без разведения с `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md` и без ясной карты нарушений и поддерживающих контуров для текущего `BytePress`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000057
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать system-invariants pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `System_Invariants.md`.
   - DoD: `ROAD-000010`, `BACK-000057` и `PLAN-000045` согласованы как текущий stage/task/pass.
2. Провести audit текущего invariant-core состояния.
   - Описание: Проверить `Docs/Technical/System_Invariants.md`, его место в required core, связанный `Templates/Document.md` и пересечения с `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`.
   - DoD: подтверждены реальные gaps legacy `System_Invariants.md`, а не открыт новый redesign technical-layer.
3. Пересобрать `System_Invariants.md` как канонический invariant-contract.
   - Описание: Собрать системные инварианты `BytePress`, нарушения, supporting contours и отношение invariants к planning, runtime, logs и process-layer.
   - DoD: читателю ясно, чем `System_Invariants.md` отличается от архитектурной карты, ownership-модели, lifecycle-contract и interface-contract.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужны ли updates в `bp_lint.py` и `bp_bootstrap.py`.
   - DoD: tooling меняется только там, где invariant-core contract становится обязательным в active layer.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000057`, индекс backlog, `ROAD-000010`, `PLAN-000045` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md` и других technical-documents;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`;
- без создания отдельного шаблона, если достаточен `Templates/Document.md`.

## Риски
- если `System_Invariants.md` останется legacy-list, required core technical-layer будет неполным по invariant-contract и границам ненарушаемых свойств системы;
- если перенести в `System_Invariants.md` архитектурную карту, ownership-модель, lifecycle-checklist или process-canon, pass снова смешает invariant-layer с соседними core contracts;
- если затронуть bootstrap или lint шире фактической необходимости, pass выйдет за узкий scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000045-clarify-technical-system-invariants.md`
- `Plans/Archive/PLAN-000044-clarify-technical-interfaces-core.md`
- `Docs/Technical/System_Invariants.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Interfaces.md`
- `Templates/Document.md`
- `Tools/bp_lint.py`
- `Tools/bp_bootstrap.py`

## DoD
- создана одна узкая backlog-задача только для system-invariants pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/System_Invariants.md` является ясным invariant-contract текущей системы.
- разведение `System_Invariants.md`, `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md` и `Pipeline/*` описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

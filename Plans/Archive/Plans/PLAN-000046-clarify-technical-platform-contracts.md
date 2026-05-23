# PLAN-000046 — Clarify technical platform contracts

ID: PLAN-000046
Название: Пересобрать Platform_Contracts.md как platform-contract
Статус: Завершено
Связи: BACK-000058
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После boundary, architecture, model, lifecycle, interfaces и invariants passes technical-layer уже удерживает карту доменов, ownership, sync-loop, interface boundaries и required core integrity, но `Docs/Technical/Platform_Contracts.md` остаётся legacy-сводкой без явного contract рабочей платформы, execution environment, supported tool perimeter и platform anti-patterns для текущего `BytePress`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000058
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать platform-contract pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `Platform_Contracts.md`.
   - DoD: `ROAD-000010`, `BACK-000058` и `PLAN-000046` согласованы как текущий stage/task/pass.
2. Провести audit platform assumptions и tool perimeter.
   - Описание: Проверить текущий `Docs/Technical/Platform_Contracts.md`, `Tools/*`, `Pipeline/*`, planning/runtime touchpoints и уже зафиксированные execution assumptions.
   - DoD: подтверждены реальные gaps legacy platform-contract, а не открыт новый redesign technical-layer или process-layer.
3. Пересобрать `Platform_Contracts.md` как канонический contract рабочей платформы.
   - Описание: Зафиксировать supported execution environment, mandatory platform assumptions, tool perimeter, роли ключевых инструментов, допустимые режимы platform usage и недопустимые отклонения.
   - DoD: читателю ясно, чем `Platform_Contracts.md` отличается от `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md`, `System_Invariants.md` и `Pipeline/*`.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужны ли updates в `bp_lint.py` и `bp_bootstrap.py`.
   - DoD: tooling меняется только там, где platform-contract становится обязательным или иначе остаётся прямое противоречие.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000058`, индекс backlog, `ROAD-000010`, `PLAN-000046` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md` и `System_Invariants.md`;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`;
- без создания новых technical-documents без прямой необходимости.

## Риски
- если `Platform_Contracts.md` останется legacy-сводкой, technical-layer сохранит разрыв между system contracts и фактическим execution/tool perimeter;
- если перенести в `Platform_Contracts.md` архитектурную карту, ownership-модель, lifecycle-checklist, interface registry или process-canon, pass снова смешает platform-layer с соседними contracts;
- если затронуть bootstrap или lint шире фактической необходимости, pass выйдет за узкий scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000046-clarify-technical-platform-contracts.md`
- `Plans/Archive/Plans/PLAN-000045-clarify-technical-system-invariants.md`
- `Docs/Technical/Platform_Contracts.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Technical/System_Invariants.md`
- `Docs/Technical/Pipeline.md`
- `Pipeline/*`
- `Tools/*`
- `Tools/bp_lint.py`
- `Tools/bp_bootstrap.py`

## DoD
- создана одна узкая backlog-задача только для platform-contract pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/Platform_Contracts.md` является ясным contract платформы и среды исполнения текущей системы.
- разведение `Platform_Contracts.md`, `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md`, `System_Invariants.md` и `Pipeline/*` описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Platform_Contracts.md` пересобран как канонический platform-contract текущего `BytePress`: теперь он явно фиксирует supported execution environment, platform assumptions, supported tool perimeter, роли ключевых инструментов, допустимые режимы platform usage и недопустимые anti-patterns без смешения с architecture, model, lifecycle, interfaces, invariants или process-canon.
- `Docs/Technical/README.md` синхронизирован минимально: supporting role `Platform_Contracts.md` теперь описана как канонический platform/tool contract, а не как расплывчатый контекстный document.
- `bp_bootstrap.py` не менялся, потому что `Platform_Contracts.md` остаётся supporting technical-document и текущий bootstrap contract не требует materialize его как обязательный active artifact.
- `bp_lint.py` не менялся, потому что audit не подтвердил необходимости переводить `Platform_Contracts.md` в required core или делать его обязательным structural check.
- `bp_lint contract unaffected`

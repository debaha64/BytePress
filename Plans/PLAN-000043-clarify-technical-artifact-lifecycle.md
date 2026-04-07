# PLAN-000043 — Clarify technical artifact lifecycle

ID: PLAN-000043
Название: Пересобрать Artifact_Lifecycle.md как lifecycle-contract
Статус: Завершено
Связи: BACK-000055
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После boundary-pass, contract-map pass, architecture-core pass и model-core pass technical-layer уже получил entrypoint, карту слоёв и модель сущностей, но `Docs/Technical/Artifact_Lifecycle.md` остаётся слишком коротким sync-note. Он не даёт полной карты артефактных групп, допустимых переходов между active, archive, runtime и log слоями, обязательного closure-loop перед завершением pass и недопустимых lifecycle-пропусков для текущего `BytePress`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000055
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать artifact-lifecycle pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `Artifact_Lifecycle.md`.
   - DoD: `ROAD-000010`, `BACK-000055` и `PLAN-000043` согласованы как текущий stage/task/pass.
2. Провести audit текущего lifecycle-contract.
   - Описание: Проверить `Docs/Technical/Artifact_Lifecycle.md` на пробелы и смысловые пересечения с `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`.
   - DoD: подтверждены реальные gaps текущего `Artifact_Lifecycle.md`, а не открыт новый redesign technical-layer.
3. Пересобрать `Artifact_Lifecycle.md` как канонический lifecycle-contract.
   - Описание: Зафиксировать ключевые артефактные группы, источники истины, обязательные sync-loop, допустимые переходы между слоями и недопустимые lifecycle-пропуски для текущего `BytePress`.
   - DoD: читателю ясно, чем `Artifact_Lifecycle.md` отличается от `README.md`, `Architecture.md`, `Model.md` и `Pipeline/*`, без дублирования process-canon.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужен ли update `bp_lint.py`.
   - DoD: tooling меняется только если artifact-lifecycle pass реально меняет обязательный contract check.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000055`, индекс backlog, `ROAD-000010`, `PLAN-000043` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `README.md`, `Architecture.md`, `Model.md` и других technical-documents;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`.

## Риски
- если `Artifact_Lifecycle.md` останется только коротким sync-note, required core technical-layer будет неполным по lifecycle-contract и closure-loop;
- если начать переносить в `Artifact_Lifecycle.md` архитектурную карту, ownership-модель или process-canon, pass снова смешает lifecycle-layer с `Architecture.md`, `Model.md` и `Pipeline/*`;
- если менять unrelated standards или lint без фактической необходимости, artifact-lifecycle pass выйдет за узкий scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000043-clarify-technical-artifact-lifecycle.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/Pipeline.md`
- `Pipeline/README.md`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для artifact-lifecycle pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/Artifact_Lifecycle.md` является ясным lifecycle-contract текущей системы.
- разведение `Artifact_Lifecycle.md`, `README.md`, `Architecture.md`, `Model.md` и `Pipeline/*` описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Artifact_Lifecycle.md` пересобран как канонический lifecycle-contract текущего `BytePress`: в одном document теперь явно разведены артефактные группы, источники истины, обязательные sync-loop, допустимые переходы между active, archive, runtime и log слоями и недопустимые lifecycle-пропуски.
- `Artifact_Lifecycle.md` больше не выглядит как короткий sync-note: closure-loop перед завершением pass, допустимые layer transitions и границы между lifecycle-layer, architecture-layer, model-layer и process-layer зафиксированы явно.
- дополнительные изменения в `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Standards/*`, `Plans/README.md` и `bp_lint.py` не потребовались: audit не подтвердил реального active-layer contradiction за пределами самого `Artifact_Lifecycle.md`.
- `bp_lint contract unaffected`

# PLAN-000042 — Clarify technical model core

ID: PLAN-000042
Название: Пересобрать Model.md как каноническую модель системы
Статус: В_работе
Связи: BACK-000054
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После boundary-pass, contract-map pass и architecture-core pass technical-layer уже получил entrypoint, required/supporting split и каноническую карту доменов и слоёв, но `Docs/Technical/Model.md` остаётся устаревшей смесью profile policy, naming migration и общей иерархии. Он не даёт ясной модели ключевых сущностей `BytePress`, ownership состояния и основных связей между `Docs/Technical/*`, `Plans/*`, `Runtime/*`, `Logs/*` и `Pipeline/*`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000054
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать model-core pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `Model.md`.
   - DoD: `ROAD-000010`, `BACK-000054` и `PLAN-000042` согласованы как текущий stage/task/pass.
2. Провести audit текущей модели.
   - Описание: Проверить `Docs/Technical/Model.md` на пробелы и смысловые пересечения с `Docs/Technical/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`.
   - DoD: подтверждены реальные gaps текущего `Model.md`, а не открыт новый redesign technical-layer.
3. Пересобрать `Model.md` как каноническую модель системы.
   - Описание: Зафиксировать ключевые сущности, ownership состояния, основные связи, допустимые зависимости и недопустимые смешения ответственности для текущего `BytePress`.
   - DoD: читателю ясно, чем `Model.md` отличается от `Architecture.md`, `Artifact_Lifecycle.md` и `Pipeline/*`, без дублирования process-canon и lifecycle rules.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужен ли update `bp_lint.py`.
   - DoD: tooling меняется только если model-core pass реально меняет обязательный contract check.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000054`, индекс backlog, `ROAD-000010`, `PLAN-000042` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `Architecture.md`, `Artifact_Lifecycle.md` и других technical-documents;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`.

## Риски
- если `Model.md` останется смесью naming policy и общих тезисов, required core technical-layer будет неполным по модели сущностей и ownership;
- если начать переносить в `Model.md` lifecycle rules или process-canon, pass снова смешает model-layer с `Artifact_Lifecycle.md` и `Pipeline/*`;
- если менять unrelated standards или lint без фактической необходимости, model-core pass выйдет за узкий scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000042-clarify-technical-model-core.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Pipeline.md`
- `Pipeline/README.md`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для model-core pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/Model.md` является ясной моделью сущностей, владельцев состояния и связей системы.
- разведение `Model.md`, `Architecture.md`, `Artifact_Lifecycle.md` и `Pipeline/*` описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

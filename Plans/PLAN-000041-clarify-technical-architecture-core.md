# PLAN-000041 — Clarify technical architecture core

ID: PLAN-000041
Название: Пересобрать Architecture.md как карту доменов и слоёв
Статус: В_работе
Связи: BACK-000053
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После boundary-pass и contract-map pass technical-layer уже получил entrypoint и явное разведение required/supporting documents, но `Docs/Technical/Architecture.md` остаётся старой общей сводкой и не даёт канонической архитектурной карты текущего `BytePress`: в нём не хватает явной карты слоёв, направлений связей, границ ответственности и недопустимых подмен между `Docs/Technical/*`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000053
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать architecture-core pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `Architecture.md`.
   - DoD: `ROAD-000010`, `BACK-000053` и `PLAN-000041` согласованы как текущий stage/task/pass.
2. Провести audit архитектурной карты.
   - Описание: Проверить текущий `Docs/Technical/Architecture.md` на пробелы и смысловые пересечения с `Docs/Technical/README.md`, `Docs/Technical/Pipeline.md`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`.
   - DoD: подтверждены реальные gaps текущего `Architecture.md`, а не придуман новый redesign technical-layer.
3. Пересобрать `Architecture.md` как каноническую карту системы.
   - Описание: Зафиксировать карту доменов, карту слоёв, границы ответственности, допустимые направления связей и недопустимые подмены для текущего `BytePress`.
   - DoD: читателю ясно, что относится к `Docs/Technical/*`, `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, без дублирования process-canon.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужен ли update `bp_lint.py`.
   - DoD: tooling меняется только если architecture-core pass реально меняет обязательный contract check.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000053`, индекс backlog, `ROAD-000010`, `PLAN-000041` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `Model.md`, `Artifact_Lifecycle.md` и других technical-documents;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`.

## Риски
- если `Architecture.md` останется общей сводкой без явной карты слоёв и доменов, required core technical-layer останется неполным;
- если начать переносить в `Architecture.md` process-canon или planning-state, pass создаст новый semantic overlap вместо снятия старого;
- если менять unrelated standards или lint без фактической необходимости, architecture-core pass выйдет за узкий scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000041-clarify-technical-architecture-core.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Pipeline.md`
- `Pipeline/README.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для architecture-core pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/Architecture.md` является ясной картой доменов, слоёв и границ системы.
- разведение `Docs/Technical/*` и `Pipeline/*` описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

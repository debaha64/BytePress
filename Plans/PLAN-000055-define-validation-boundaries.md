# PLAN-000055 — Define validation boundaries

ID: PLAN-000055
Название: Зафиксировать границы validation-layer
Статус: В_работе
Связи: BACK-000067
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08
Основание: Verification-layer уже зафиксирован через boundaries, contract map, levels, tooling boundary и evidence contract, но общий validation-layer пока не выделен как отдельный contract. Нужен узкий pass, который введёт `Docs/Technical/Validation.md` и разведёт validation с verification, evidence, pass-close contour и process gates без реализации нового toolchain.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000067
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-contour под новый validation pass.
   - Описание: Оставить `ROAD-000011` активным, создать одну реальную backlog-задачу и один новый current `Plan`, а предыдущий завершённый `Plan` вывести в archive.
   - DoD: `ROAD-000011`, `BACK-000067` и `PLAN-000055` согласованы как текущий stage/task/pass.
2. Провести audit validation perimeter.
   - Описание: Проверить `Verification.md`, `Verification_Levels.md`, `Verification_Evidence.md`, `Artifact_Lifecycle.md`, `Pipeline/Phase_Gates.md` и `Tools/README.md` только на реальные противоречия по границе между validation, verification, evidence и gate contour.
   - DoD: зафиксировано, какие validation assumptions уже подразумеваются contracts и что нужно вынести в отдельный validation document.
3. Ввести `Docs/Technical/Validation.md`.
   - Описание: Создать singleton technical document на базе `Templates/Document.md` и описать назначение validation-layer, его inputs/outputs, evidence usage, ownership результата и связь с pass-close contour и phase gates.
   - DoD: читателю ясно, чем validation отличается от verification и что validation не должно подменять.
4. Подтвердить минимальный contract impact.
   - Описание: Проверить, нужны ли точечные updates в `Verification.md`, `Verification_Evidence.md`, `Docs/Technical/README.md`, `Pipeline/Phase_Gates.md`, `Tools/README.md` или `bp_lint.py`.
   - DoD: меняются только реально противоречащие линии; tooling не реализуется.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000011`, текущего `Plan` и self-check.
   - DoD: `BACK-000067`, индекс backlog, `ROAD-000011`, `PLAN-000055` и self-check полностью согласованы.

## Ограничения
- без реализации `bp_check / bp_verify`;
- без рефакторинга всего `Tools/*`;
- без открытия `ROAD-000012`;
- без широкого переписывания `Docs/Technical/*`.

## Риски
- если validation-layer останется неявным, verification evidence и gate handoff снова смешаются с validation result;
- если validation будет описан как ещё один automatic tool boundary, pass откроет преждевременный redesign toolchain;
- если разведение validation и verification не будет зафиксировано в supporting contracts, следующий pass снова начнёт спорить о том, кто владеет acceptance interpretation.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000055-define-validation-boundaries.md`
- `Plans/Archive/PLAN-000054-define-verification-evidence-contract.md`
- `Docs/Technical/Validation.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Verification_Evidence.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Pipeline/Phase_Gates.md`
- `Tools/README.md`

## DoD
- `ROAD-000011` остаётся в `В_работе`.
- создана одна узкая задача этого pass.
- создан один current `Plan`.
- `Validation.md` фиксирует границы validation-layer.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- В работе.

# PLAN-000048 — Clarify product bootstrap validation

ID: PLAN-000048
Название: Пересобрать Product_Bootstrap_Validation.md как validation-contract
Статус: Завершено
Связи: BACK-000060
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После bootstrap-contract pass `Docs/Technical/Product_Bootstrap_Contract.md` уже фиксирует bootstrap obligations и minimal outcome, но `Docs/Technical/Product_Bootstrap_Validation.md` остаётся legacy-note про один test run без явного validation-scope, acceptance criteria, автоматических и процедурных checks и без ясной границы относительно bootstrap-contract, platform-layer и lint perimeter.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000060
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать validation-pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `Product_Bootstrap_Validation.md`.
   - DoD: `ROAD-000010`, `BACK-000060` и `PLAN-000048` согласованы как текущий stage/task/pass.
2. Провести audit validation perimeter bootstrap-result.
   - Описание: Проверить текущий `Product_Bootstrap_Validation.md`, `Product_Bootstrap_Contract.md`, `Tools/bp_bootstrap.py`, `Tools/bp_lint.py` и active references на bootstrap-result и acceptance criteria.
   - DoD: подтверждены реальные gaps validation-contract и зоны двусмысленности между bootstrap obligations, validation scope и фактическими automatic/procedural checks.
3. Пересобрать `Product_Bootstrap_Validation.md` как канонический validation-contract.
   - Описание: Зафиксировать validation-scope, acceptance criteria bootstrap-result, обязательные validation checks, automatic/procedural split и недопустимые validation-пропуски.
   - DoD: читателю ясно, чем bootstrap-validation отличается от bootstrap-contract, platform-contract, lifecycle-contract и interface-layer.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужны ли updates в `bp_bootstrap.py` и `bp_lint.py`.
   - DoD: tooling меняется только там, где validation contract и фактический active check perimeter иначе спорят друг с другом.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000060`, индекс backlog, `ROAD-000010`, `PLAN-000048` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md`, `System_Invariants.md`, `Platform_Contracts.md` и `Product_Bootstrap_Contract.md`;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`;
- без создания новых technical-documents без прямой необходимости.

## Риски
- если `Product_Bootstrap_Validation.md` останется legacy-note про отдельный test run, validation-layer продолжит путаться с bootstrap-contract и не удержит acceptance perimeter bootstrap-result;
- если перенести в validation-contract сами bootstrap obligations, process-canon или platform assumptions, pass снова смешает validation-layer с соседними contracts;
- если расширить `bp_lint.py` или `bp_bootstrap.py` без доказанной необходимости, узкий pass превратится в redesign verification/tooling perimeter.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/PLAN-000048-clarify-product-bootstrap-validation.md`
- `Plans/Archive/PLAN-000047-clarify-product-bootstrap-contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Platform_Contracts.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для product-bootstrap-validation pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/Product_Bootstrap_Validation.md` является ясным validation-contract bootstrap-result текущей системы.
- разведение `Product_Bootstrap_Validation.md`, `Product_Bootstrap_Contract.md`, `Platform_Contracts.md`, `Artifact_Lifecycle.md`, `Interfaces.md`, `System_Invariants.md` и других technical-documents описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Product_Bootstrap_Validation.md` пересобран как канонический validation-contract bootstrap-result текущего `BytePress`: документ теперь явно фиксирует validation-scope, acceptance criteria, automatic/procedural split и недопустимые validation-пропуски.
- validation-layer теперь явно разведен с bootstrap-contract: `Product_Bootstrap_Contract.md` владеет bootstrap obligations, а `Product_Bootstrap_Validation.md` владеет критериями и режимом проверки результата.
- `Docs/Technical/README.md` и `Docs/Technical/Product_Bootstrap_Contract.md` синхронизированы минимально, чтобы active technical-layer больше не описывал validation document как legacy evidence note.
- `bp_bootstrap.py` не менялся, потому что audit не подтвердил расхождения между bootstrap-contract, validation-contract и фактическим bootstrap behavior.
- `bp_lint.py` не менялся, потому что текущий automatic structural perimeter уже покрывает обязательный bootstrap minimum, а этот pass не доказал необходимость расширять lint до procedural validation.
- `bp_lint contract unaffected`

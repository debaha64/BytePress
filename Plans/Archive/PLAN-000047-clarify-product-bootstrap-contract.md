# PLAN-000047 — Clarify product bootstrap contract

ID: PLAN-000047
Название: Пересобрать Product_Bootstrap_Contract.md как bootstrap-contract
Статус: Завершено
Связи: BACK-000059
Источник: Следующий узкий pass этапа `ROAD-000010`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07
Основание: После passes по architecture/model/lifecycle/interfaces/invariants/platform technical-layer уже удерживает карту системы и рабочего периметра, но `Docs/Technical/Product_Bootstrap_Contract.md` остаётся короткой legacy-сводкой без явной карты bootstrap obligations, minimal initialized product state, bootstrap boundaries и явного разведения с validation-layer и фактическим behavior `Tools/bp_bootstrap.py`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000059
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать bootstrap-contract pass внутри `ROAD-000010`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для пересборки `Product_Bootstrap_Contract.md`.
   - DoD: `ROAD-000010`, `BACK-000059` и `PLAN-000047` согласованы как текущий stage/task/pass.
2. Провести audit bootstrap perimeter.
   - Описание: Проверить текущий `Product_Bootstrap_Contract.md`, `Product_Bootstrap_Validation.md`, `Tools/bp_bootstrap.py`, `Tools/bp_lint.py` и active references на bootstrap outcome.
   - DoD: подтверждены реальные gaps bootstrap-contract и зоны двусмысленности между contract, validation и фактическим tooling behavior.
3. Пересобрать `Product_Bootstrap_Contract.md` как канонический bootstrap-contract.
   - Описание: Зафиксировать minimal product repo outcome, bootstrap obligations, bootstrap boundaries, допустимые упрощения и недопустимые пропуски.
   - DoD: читателю ясно, чем bootstrap-contract отличается от validation, platform-contract, lifecycle-contract и interface-layer.
4. Подтвердить минимальный tooling impact.
   - Описание: Проверить, нужны ли updates в `bp_bootstrap.py` и `bp_lint.py`.
   - DoD: tooling меняется только там, где contract и фактическое materialization behavior иначе спорят друг с другом.
5. Закрыть pass governance-сверкой.
   - Описание: Перевести backlog-задачу и `Plan` в финальные статусы только после согласования индекса backlog, `ROAD-000010`, текущего `Plan` и self-check.
   - DoD: `BACK-000059`, индекс backlog, `ROAD-000010`, `PLAN-000047` и self-check полностью согласованы.

## Ограничения
- без широкого рефакторинга всего `Docs/Technical/*`;
- без массового переписывания `README.md`, `Architecture.md`, `Model.md`, `Artifact_Lifecycle.md`, `Interfaces.md`, `System_Invariants.md` и `Platform_Contracts.md`;
- без redesign `Pipeline/*`;
- без открытия `ROAD-000011`;
- без создания новых technical-documents без прямой необходимости.

## Риски
- если `Product_Bootstrap_Contract.md` останется краткой legacy-сводкой, bootstrap perimeter продолжит держать существенную часть канона только в `bp_bootstrap.py` и `bp_lint.py`;
- если перенести в bootstrap-contract validation-результаты, process-canon или lifecycle-checklist, pass снова смешает bootstrap-layer с соседними contracts;
- если менять bootstrap или lint шире фактической необходимости, pass выйдет за узкий scope.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/PLAN-000047-clarify-product-bootstrap-contract.md`
- `Plans/Archive/PLAN-000046-clarify-technical-platform-contracts.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/README.md`
- `Docs/Technical/Platform_Contracts.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`

## DoD
- создана одна узкая backlog-задача только для product-bootstrap-contract pass.
- создан новый текущий `Plan` только под этот pass.
- `Docs/Technical/Product_Bootstrap_Contract.md` является ясным bootstrap-contract текущей системы.
- разведение `Product_Bootstrap_Contract.md`, `Product_Bootstrap_Validation.md`, `Platform_Contracts.md`, `Artifact_Lifecycle.md`, `Interfaces.md` и других technical-documents описано ясно и без новой двусмысленности.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Результат
- `Docs/Technical/Product_Bootstrap_Contract.md` пересобран как канонический bootstrap-contract текущего `BytePress`: теперь он явно фиксирует CLI contract, minimal product repo outcome, обязательные создаваемые артефакты, bootstrap boundaries, допустимые упрощения и недопустимые bootstrap-пропуски.
- bootstrap-contract теперь прямо разводит contract obligations, platform assumptions, lifecycle rules и validation result: `Product_Bootstrap_Validation.md` остаётся evidence document, а не substitute для самого contract.
- `bp_bootstrap.py` не менялся, потому что audit не подтвердил расхождения между документным contract и фактическим materialization behavior.
- `bp_lint.py` не менялся, потому что bootstrap result contract и его structural checks уже согласованы и pass не меняет обязательный lint surface.
- `bp_lint contract unaffected`

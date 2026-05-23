# PLAN-000021 — Domain participation contract

ID: PLAN-000021
Название: Уточнить participation contract доменов Runtime, Pipeline, Adapters, Memory и MCP
Статус: Завершено
Связи: BACK-000031, CHG-000033, QL-000028
Источник: Technical cleanup pass после artifact lifecycle contract
Дата_создания: 2026-03-29
Дата_изменения: 2026-03-29
Основание: В текущем каноне `BytePress` роли доменов `Runtime/`, `Pipeline/`, `Adapters/`, `Memory/` и `MCP/` уже частично зафиксированы, но распределены между архитектурой, моделью, lifecycle contract и локальными README. Нужно коротко выровнять их участие в системе и lifecycle без нового technical domain и без большого рефакторинга.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000031
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Добавить backlog-item текущей задачи и отдельный plan-file для participation pass.
   - DoD: `Plans/Backlog.md` и `Plans/Archive/Plans/PLAN-000021-domain-participation-contract.md` отражают scope без лишнего расширения.
2. Выровнять общий technical contract.
   - Описание: Минимально обновить `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/README.md` и `README.md` только там, где роли доменов остаются двусмысленными.
   - DoD: участие `Runtime/`, `Pipeline/`, `Adapters/`, `Memory/` и `MCP/` в системе и lifecycle описано коротко и согласованно.
3. Выровнять README доменов.
   - Описание: Минимально обновить `Pipeline/README.md`, `Runtime/README.md`, `Adapters/README.md`, `Memory/README.md` и `MCP/README.md` без новых сущностей и без расширения scope.
   - DoD: README доменов коротко отвечают на вопросы о назначении, статусе, источнике истины, моменте участия в lifecycle и границах подмены.
4. Закрыть pass в плановом и журнальном контуре.
   - Описание: Обновить `ChangeLog` и `QualityLog`, а `ADR` и `bp_lint.py` менять только при доказанной необходимости.
   - DoD: `python3 Tools/bp_lint.py --repo .` проходит, backlog и plan переведены в финальный статус, а новый ADR не появляется без нового устойчивого решения.

## Риски
- попытка превратить проход в общий audit интеграционного контура выведет задачу за пределы согласованного scope;
- повторение одного и того же контента в architecture, model, lifecycle и README доменов усилит process-noise вместо его снижения;
- необоснованное изменение `bp_lint.py` создаст лишний contract drift без изменения обязательных путей и доменов.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000021-domain-participation-contract.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/README.md`
- `README.md`
- `Pipeline/README.md`
- `Runtime/README.md`
- `Adapters/README.md`
- `Memory/README.md`
- `MCP/README.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- роль `Runtime/`, `Pipeline/`, `Adapters/`, `Memory/` и `MCP/` в системе и lifecycle зафиксирована ясно и без двусмысленности.
- `Docs/Technical/*` и README этих доменов согласованы с текущим каноном.
- `python3 Tools/bp_lint.py --repo .` проходит.
- новый `ADR` создаётся только если реально нужен.
- `bp_lint.py` меняется только если обязательный contract действительно изменяется.

## Фактический результат
- `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md` и `Docs/Technical/README.md` теперь коротко и согласованно описывают назначение, статус `0.1.0`, участие в lifecycle, признак источника истины и границы подмены для `Runtime/`, `Pipeline/`, `Adapters/`, `Memory/` и `MCP/`.
- `Pipeline/README.md`, `Runtime/README.md`, `Adapters/README.md`, `Memory/README.md` и `MCP/README.md` приведены к тому же краткому participation contract без новых сущностей и без расширения scope.
- `README.md` не менялся, потому что после выравнивания technical layer корневая карта не содержала оставшейся двусмысленности.
- `bp_lint.py` не менялся, потому что обязательные пути, шаблоны и домены в этом проходе не изменялись.

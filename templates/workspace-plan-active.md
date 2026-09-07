# WPLAN-<ID>-<slug>

Статус: active
WPLAN ID: WPLAN-<ID>
WROAD: WROAD-<ID>
WBACK: WBACK-<ID>

Фаза SDLC: <фаза>
Операционный режим: <product-work | system-editing>
Предмет прохода: <предмет работы Workspace>
Класс изменения: <S0 | S1 | S2>
Владелец спецификации: <точный текущий путь/якорь | не применяется для S0>
REQ/INV/SCN: <точные применимые ID | none>
Impact Scan / набор изменений: <точные CREATE/UPDATE/PRESERVE/REMOVE>
Прослеживаемость: <REQ/INV/SCN → проектное решение → тесты → реализация → свидетельства>
Уровень свидетельств: <S0 контрольное чтение | S1 целевые проверки | S2 машинные/инженерные/для владельца>
Consistency Closure: <pending | PASS с четырьмя нулевыми наборами>

Текущая точка контроля: <точка контроля>
Текущая контрольная отметка: <контрольная отметка>
Блокирующее условие: <отсутствует | точное блокирующее условие>

INTERVIEW_EVIDENCE_REF: <none | IE-000001>
OWNER_DECISION_REFS: <none | OD-000001[,OD-000002]>
ALLOWED_SURFACES: <none | точные относительные пути,деревья,исключения полей>

SDLC_TRANSITION: v1
TRANSITION_STATE: <in-progress | complete>
FROM_PHASE: <каноническая фаза>
FROM_ROLE: <roles/path.md>
PHASE_COMPLETION: <pending | complete>
EVIDENCE_KIND: <канонический требуемый вид свидетельства из phase-gates.md>
EVIDENCE_REFS: <none | path#token[,path#token]>
TRANSITION_CHECKPOINT: <точная контрольная отметка>
HANDOFF_REF: <none | path#token>
TO_PHASE: <каноническая следующая фаза | retired>
TO_ROLE: <roles/path.md | none>
FROM_ROLE_AUTHORITY: <active | relinquished>
TO_ROLE_AUTHORITY: <withheld | granted | not-applicable>
AUTHORITY_REF: <OD-000001>
OWNER_GATE: <none | gate>
OWNER_GATE_STATUS: <not-applicable | pending | satisfied>
OWNER_GATE_REF: <none | OD-000001 | PA-000001 | logs/decisions.md#exact-release-token>
VERIFICATION_STATUS: <pending | unverified | pass | fail>
VERIFICATION_REF: <none | path#token>
VALIDATION_STATUS: <not-performed | pass | fail>
VALIDATION_REF: <none | path#token>
PRODUCT_ACCEPTANCE_STATUS: <not-performed | accepted | rejected>
PRODUCT_ACCEPTANCE_REF: <none | PA-000001>
RELEASE_AUTHORIZATION_STATUS: <not-performed | authorized | denied>
RELEASE_AUTHORIZATION_REF: <none | logs/decisions.md#RELEASE_AUTHORIZATION-token>

Для `PRODUCT_ACCEPTANCE_STATUS: accepted` ссылка `PRODUCT_ACCEPTANCE_REF` может указывать на accepted PA предыдущего WPLAN; provenance сохраняется. Scope текущего owner gate проверяется отдельно по `docs/technical/phase-gates.md#границы-product-acceptance`.

`EVIDENCE_KIND`, `OWNER_GATE` и ссылки на решения являются проекциями. Точное соответствие `transition -> Required owner decision kind` читается только из `docs/technical/phase-gates.md`; отдельного WPLAN-поля для него нет, а имя точки контроля не выбирает вид решения.

## Точный манифест изменений

### CREATE — <count>

1. `<relative path>` — `<file:mode | directory:mode>`.

### UPDATE — <count>

1. `<relative path>` — `<непустое подмножество content,mode,type>`.

### PRESERVE — <count>

1. `<relative path | relative tree/**>`.

### REMOVE — <count>

1. `<relative path>` — `<file | directory>`.

## Documentation Impact

Disposition: <affected | not affected>
Owners: <точные относительные пути владельцев смысла через запятую>
Reason: <влияние на читателя, связанные формы/термины либо причина отсутствия влияния>

## Назначение

<одно назначение WPLAN>

## Разрешённые поверхности

1. <точный файл, каталог или действие>

## Запрещённые действия

1. <запрет>

## Критерии PASS

1. <проверяемый критерий>

## Bugfixes

1. <только небольшой причинно связанный дефект>

## Проверки

1. <команда или ручная сверка>

Этот шаблон материализуется только в `WS_<Slug>/plans/active/`; поставка BytePress не содержит активного WPLAN.

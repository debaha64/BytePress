# Точки контроля фаз

Точка контроля фазы (`phase gate`) — смысловая точка контроля в Конвейере разработки (SDLC). Она отделяет состояния работы и фиксирует, где нужен владелец, `Verification Engineer` или отдельный управляемый проход.

## Фаза

Фаза использует одно из `21` канонических машинных значений из [полного каталога SDLC](sdlc.md): `intent`, `discussion`, `interview`, `research`, `requirements`, `basis`, `architecture`, `design`, `planning`, `approval`, `implementation`, `verification`, `owner-review`, `product-acceptance`, `release-readiness`, `release`, `handoff`, `operation`, `maintenance`, `retrospective`, `decommissioning`. `discovery` и `product discovery` нормализуются в `research` как совместимые имена стартового прохода. Фаза не является командой к действию сама по себе; `decommissioning` переводит продукт в `retired` только после отдельного решения владельца.

## Точка контроля

Точка контроля (`gate`) показывает, какие условия и свидетельства связаны с переходом. Она не является автоматическим разрешением на изменение границ, код, выпуск и тег, GitHub-действия или продуктовую приёмку.

`discovery-complete` требует, чтобы обязательные слои стартового исследования были завершены или явно отложены как `deferred` с причиной. Вопрос о следующем переходе не задаётся до этой точки контроля.

Правила продолжения работы и смены маршрута принадлежат [project-management](../../sops/project-management.md); точка контроля сама не выполняет переход.

## Контракт переходов

Для перехода нужны свидетельства завершения исходной фазы, точная контрольная отметка, передача результата и прекращение полномочий исходной роли на изменение файлов. Столбец `Required evidence kind` задаёт требуемый вид свидетельства, а `Required owner decision kind` — единственное нормативное соответствие перехода и вида решения владельца. WPLAN ссылается на свидетельство через `EVIDENCE_KIND`. Проверяющий инструмент читает оба вида и политику из одной строки; название точки контроля или произвольное положительное значение их не переопределяют.

`none` означает, что политика перехода не требует решения владельца. Поддерживаются только принятые контракты: `implementation`, `product_acceptance`, `release_authorization`, `decommissioning_authorization`, `retirement_authorization`. `implementation`, `decommissioning_authorization` и `retirement_authorization` — значения `DECISION_KIND` одного семейства записей `owner_decision` / `OD-*`; `product_acceptance` — отдельный `product_acceptance` / `PA-*`; `release_authorization` сохраняет собственный контракт. Политика `owner-open` оставляет точку контроля в состоянии `pending`; решение проверяется строкой `owner-decision`, которая его требует.

| From | To | Required evidence kind | Owner gate policy | Required owner decision kind |
|---|---|---|---|---|
| `intent` | `discussion` | `intent-record` | `none` | `none` |
| `discussion` | `interview` | `discussion-outcome` | `none` | `none` |
| `interview` | `research` | `owner-answers` | `none` | `none` |
| `research` | `requirements` | `research-closure` | `none` | `none` |
| `requirements` | `basis` | `req-inv-scn` | `none` | `none` |
| `basis` | `architecture` | `traceable-basis` | `none` | `none` |
| `architecture` | `design` | `architecture-contract` | `none` | `none` |
| `design` | `planning` | `design-and-test-plan` | `none` | `none` |
| `planning` | `approval` | `bounded-wback-wplan` | `owner-open` | `none` |
| `approval` | `implementation` | `owner-implementation-authorization` | `owner-decision` | `implementation` |
| `implementation` | `verification` | `implementation-red-green-delta` | `none` | `none` |
| `verification` | `owner-review` | `technical-verdict-and-traceability` | `owner-open` | `none` |
| `owner-review` | `product-acceptance` | `owner-review-decision` | `owner-open` | `none` |
| `product-acceptance` | `release-readiness` | `product-acceptance-decision` | `owner-decision` | `product_acceptance` |
| `release-readiness` | `release` | `release-readiness-evidence` | `owner-decision` | `release_authorization` |
| `release` | `handoff` | `release-identity` | `none` | `none` |
| `handoff` | `operation` | `handoff-record` | `none` | `none` |
| `operation` | `maintenance` | `operational-evidence` | `none` | `none` |
| `maintenance` | `retrospective` | `maintenance-evidence` | `none` | `none` |
| `retrospective` | `decommissioning` | `retrospective-and-decommission-authorization` | `owner-decision` | `decommissioning_authorization` |
| `decommissioning` | `retired` | `decommissioning-evidence` | `owner-decision` | `retirement_authorization` |

Verification подтверждает техническое соответствие спецификации, проектному решению и тестам. Validation оценивает пригодность для намерения владельца. Product Acceptance и Release Authorization — отдельные решения о приёмке продукта и разрешении выпуска. Ни один из этих фактов автоматически не создаёт другой.

## Связь с WROAD -> WBACK -> WPLAN

`WROAD` задаёт этап, `WBACK` фиксирует задачу, `WPLAN` задаёт границы исполняемого прохода. Точка контроля имеет силу только внутри этой связки и не заменяет решение владельца.

## Где процедура

Исполнение точки контроля и порядок управляемого прохода принадлежат [управлению проектом](../../sops/project-management.md).

Технический PASS завершает Verification в проверенной области. Обсуждение с владельцем, приёмка, разрешение выпуска, тег и выпуск остаются отдельными точками контроля.

## Передача результата фазы

Решения владельца, WROAD/WBACK/WPLAN, журналы, внутренние исследования и свидетельства принадлежат Workspace. Документация, тесты, код и манифесты продукта принадлежат корню Product Unit. Внешний материал становится источником истины после принятия владельцем и размещения у соответствующего владельца смысла.

Результат завершённой фазы — согласованная запись WPLAN: ссылки на свидетельства разрешаются, контрольная отметка совпадает с маршрутом, передача результата зафиксирована, прежние полномочия прекращены, новые выданы только указанной роли. Ожидающая решения владельца точка контроля остаётся `pending` независимо от технического PASS.

## Границы Product Acceptance

Для owner gate `product-acceptance -> release-readiness` требуется accepted `PA-*`, полученный в том же WPLAN: `PA.WPLAN_ID == current WPLAN_ID`. PA другого WPLAN не удовлетворяет этому gate.

После успешного перехода accepted `PA-*` является постоянной ссылкой на принятый результат (`durable reference`). Последующий WPLAN может использовать `PRODUCT_ACCEPTANCE_STATUS: accepted` и `PRODUCT_ACCEPTANCE_REF: PA-*`; `PA.WPLAN_ID` сохраняет происхождение приёмки и не обязан совпадать с текущим WPLAN. Это status projection, а не новое решение владельца.

Для projection проверяются единственная структурно валидная запись, `RECORD_TYPE: product_acceptance`, точный `RECORD_ID` вида `PA-<6 digits>`, provenance `WPLAN_ID` вида `WPLAN-<6 digits>` и соответствие `DECISION_VALUE` заявленному статусу. Значения `pending` и `rejected` не подтверждают `accepted`. Отсутствие или подмена записи/ссылки не допускается; scope текущего WPLAN дополнительно проверяется только у owner gate.

Generic Workspace checker проверяет эти Workspace contracts. Сопоставление точного кандидата с принятым Product принадлежит [выпускной процедуре](../../sops/release-management.md) и не требует чтения или исполнения Product этим checker.

## Полномочия работы и решения перехода

WPLAN задаёт разрешённую работу; решение владельца о реализации имеет отдельное назначение. `ALLOWED_SURFACES` — непустая точная граница любого active WPLAN, независимо от наличия OD. Она не отменяет защиту Product Unit. `AUTHORITY_REF: none | OD-*` проецирует только требуемое разрешение реализации; отдельный универсальный research OD не вводится.

1. `REQ-BP-BOOT-001`: первый research WPLAN работает с `AUTHORITY_REF: none` и `OWNER_DECISION_REFS: none`, если иных решений нет. Project Start только с WROAD имеет transition `NOT_APPLICABLE` и не требует OD.
2. `REQ-BP-BOOT-002`: до завершения перехода в `implementation` WPLAN не разрешает изменение Product root или его потомков — ни через ALLOWED_SURFACES, ни через CREATE/UPDATE/REMOVE. Product root и его policy принадлежат `SYSTEM.md`, `registry:protected-surfaces`; Profile задаёт Slug. Planning scope не снимает эту защиту.
3. `REQ-BP-BOOT-003`: работа исходной фазы `implementation`, включая завершённый handoff в verification, требует действительного current implementation OD. Его kind/value/status/WPLAN/route/evidence/projection проверяются строго. В `approval -> implementation` такая authority допустима и обязательна только при `OWNER_GATE_STATUS: satisfied`, со ссылкой на то же решение в OWNER_GATE_REF; сама Product work начинается после complete handoff. Pending approval работает с none.
4. `REQ-BP-BOOT-004`: в остальных фазах `AUTHORITY_REF` равен `none`; преждевременный или неверно применённый implementation OD даёт FAIL. Исторические OWNER_DECISION_REFS не превращаются в текущую authority. Проверка работы implementation и required decision перехода раздельны: строка с required decision `none` не наследует implementation OD; OD в implementation -> verification проверяет только выполненную implementation work.
5. `REQ-BP-BOOT-005`: форма active WPLAN явно выражает `AUTHORITY_REF: <none | OD-000001>` без legacy implementation fallback. Technical PASS не создаёт owner decision.

Допустимая цепочка bootstrap: Project Start -> research без OD -> verified research checkpoint и последовательные canonical preparation transitions -> новое отдельное разрешение владельца в implementation gate -> implementation-open -> implementation work. Discovery, выбор результата и разрешение реализации не синтезируются из создания WPLAN; фактическое post-discovery решение фиксируется по существующему typed contract. Проверка требований принадлежит fresh bootstrap fixtures, matrix21 и negative authority injections; Product Acceptance, Release Authorization и lifecycle gates сохраняют исходные отдельные контракты.

Canonical graph остаётся однонаправленным. `changes requested` в owner review не добавляет backward edge: завершение итерации и новый corrective WPLAN следуют [route semantics](../../sops/project-management.md#доработка-после-owner-review); Product correction получает fresh implementation OD нового WPLAN.

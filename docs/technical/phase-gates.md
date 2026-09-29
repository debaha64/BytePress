# Условия действий и совместимость фаз

Новая работа разделяет продуктовые факты, разрешённый WPLAN и сессию по [рабочему договору](task-flow.md#рабочий-договор). Инженерные этапы выбираются по задаче; обязательного движения по графу в короткой форме нет. Решения принимает владелец. Название роли, ACTION или технический PASS само по себе не разрешает запись.

## Условия действий

Эта таблица — единственный владелец требуемого вида решения для `WORK_CONTRACT: v1`. `none` означает отсутствие дополнительного типизированного решения, но не отсутствие прямого запроса, WPLAN и точной границы. `AUTHORITY_REF` записывается только при применимости. Решения implementation и вывода из эксплуатации сохраняют kind/value/status/WPLAN/route scope; Product Acceptance сохраняет своё происхождение и exact result. Выпускная процедура дополнительно связывает принятого кандидата, текущую политику и точное действие.

| Действие | Решение |
|---|---|
| `research` | `none` |
| `implementation` | `implementation` |
| `verification` | `none` |
| `owner-review` | `none` |
| `product-acceptance` | `none` |
| `release-readiness` | `product_acceptance` |
| `release` | `release_authorization` |
| `decommissioning` | `decommissioning_authorization` |
| `retired` | `retirement_authorization` |

`research` включает подготовительную работу с фактами, требованиями и конструкцией без изменения Product. `implementation` требует scoped OD и точной границы до записи. `product-acceptance` разрешает подготовку рассмотрения: accepted PA создаётся только по отдельному явному решению владельца. Release Readiness потребляет существующий accepted PA; новый WPLAN не переписывает его provenance. Проверки и роли не выдают новые решения. Для реализации сохраняются применимые specification/design, tests-first, Bugfixes и проверки; отсутствие графа не отменяет эти инженерные условия.

`implementation`, `decommissioning` и `retired` допускают только точные операции Product из CREATE/UPDATE/REMOVE при действительном решении соответствующего вида из таблицы. Обычное разрешение реализации не заменяет разрешения вывода из эксплуатации или прекращения поддержки; обратная подмена также запрещена. Другие ACTION не снимают защиту Product. Неиспользованное разрешение REMOVE допустимо, но обязательное удаление проверяется отдельно как результат.

## Совместимость прежней формы

Следующие разделы применяются только к существующему `SDLC_TRANSITION: v1`, а не к новой короткой форме. Они сохраняют чтение старого активного WPLAN, его продолжение и завершение без переписывания completed history. При переходе незавершённого WPLAN на короткую форму граф больше не определяет следующее действие; сохраняются исходные решения, их границы и факты. Прежняя таблица остаётся владельцем только проверки прежнего представления.

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

WPLAN задаёт разрешённую работу; решение владельца о реализации имеет отдельное назначение. `CREATE ∪ UPDATE ∪ REMOVE` задаёт непустую точную границу active WPLAN, независимо от наличия OD. Она не отменяет защиту Product Unit. `AUTHORITY_REF: none | OD-*` проецирует только требуемое разрешение реализации; отдельный универсальный research OD не вводится.

1. `REQ-BP-BOOT-001`: первый research WPLAN работает с `AUTHORITY_REF: none` и `OWNER_DECISION_REFS: none`, если иных решений нет. Project Start только с WROAD имеет transition `NOT_APPLICABLE` и не требует OD.
2. `REQ-BP-BOOT-002`: до завершения перехода в `implementation` WPLAN не разрешает изменение Product root или его потомков — через CREATE/UPDATE/REMOVE. Product root и его policy принадлежат `SYSTEM.md`, `registry:protected-surfaces`; Profile задаёт Slug. Planning scope не снимает эту защиту.
3. `REQ-BP-BOOT-003`: работа исходной фазы `implementation`, включая завершённый handoff в verification, требует действительного current implementation OD. Его kind/value/status/WPLAN/route/evidence/projection проверяются строго. В `approval -> implementation` такая authority допустима и обязательна только при `OWNER_GATE_STATUS: satisfied`, со ссылкой на то же решение в OWNER_GATE_REF; сама Product work начинается после complete handoff. Pending approval работает с none.
4. `REQ-BP-BOOT-004`: в остальных фазах `AUTHORITY_REF` равен `none`; преждевременный или неверно применённый implementation OD даёт FAIL. Исторические OWNER_DECISION_REFS не превращаются в текущую authority. Проверка работы implementation и required decision перехода раздельны: строка с required decision `none` не наследует implementation OD; OD в implementation -> verification проверяет только выполненную implementation work.
5. `REQ-BP-BOOT-005`: форма active WPLAN явно выражает `AUTHORITY_REF: <none | OD-000001>` без legacy implementation fallback. Technical PASS не создаёт owner decision.

Допустимая цепочка bootstrap: Project Start -> research без OD -> verified research checkpoint и последовательные canonical preparation transitions -> новое отдельное разрешение владельца в implementation gate -> implementation-open -> implementation work. Discovery, выбор результата и разрешение реализации не синтезируются из создания WPLAN; фактическое post-discovery решение фиксируется по существующему typed contract. Проверка требований принадлежит fresh bootstrap fixtures, matrix21 и negative authority injections; Product Acceptance, Release Authorization и lifecycle gates сохраняют исходные отдельные контракты.

В прежнем SDLC_TRANSITION граф проверяется как исторический формат; он не добавляет обратного перехода. Доработка может продолжаться в прежней разрешённой границе незавершённого WPLAN или после его согласованного перевода в короткую форму. Решения и история сохраняются по [PM](../../sops/project-management.md#доработка-после-owner-review).

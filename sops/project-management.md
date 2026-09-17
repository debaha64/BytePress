# Управление проектом

Workspace ведёт контур `WROAD -> WBACK -> WPLAN` в `WS_<Slug>/plans/`; Product Unit не хранит и не исполняет этот маршрут.

## ID плана

1. WPLAN ID уникален и не переиспользуется.
2. Имя файла и заголовок содержат один ID.
3. Перенос в `plans/completed/` не меняет ID.
4. Префикс `COMPLETED-` запрещён.
5. Новый активный WPLAN получает следующий свободный ID по активным и завершённым WPLAN.

## Активный WPLAN

В `plans/active/` допускается от нуля до одного `WPLAN-*.md` со значением:

```text
Статус: active
```

Минимальные машинные поля:

```text
INTERVIEW_EVIDENCE_REF: none | IE-000001
OWNER_DECISION_REFS: none | OD-000001,OD-000002
PRODUCT_ACCEPTANCE_REF: none | PA-000001
ALLOWED_SURFACES: <non-empty exact relative paths, trees, field exceptions>
```

Проверить `AUTHORITY_REF` по текущей фазе и canonical [phase-gates](../docs/technical/phase-gates.md): `none` для research и иных фаз без implementation authority, либо ровно один `OD-*` из `OWNER_DECISION_REFS` там, где требуется реализация. Для реализации запись должна иметь `DECISION_KIND: implementation`, `DECISION_VALUE: approved`, текущий `WPLAN_ID`, тот же `EVIDENCE_REF`, статус `active|applied` и `ROUTE_REF: none|<current WBACK>`.

Для переходов жизненного цикла то же семейство `OD-*` использует `DECISION_KIND: decommissioning_authorization | retirement_authorization`; вид решения для конкретного перехода берётся только из [phase-gates](../docs/technical/phase-gates.md). `PRODUCT_ACCEPTANCE_REF` ссылается на отдельный `PA-*`; Release Authorization сохраняет собственный контракт.

Сверить `ALLOWED_SURFACES` с точными разделами `CREATE/UPDATE` WPLAN. Это краткое представление того же разрешённого набора; при расхождении действует более узкая граница, а проверяющий инструмент даёт FAIL.

WPLAN также содержит один целевой продукт, `Фаза SDLC`, `Операционный режим` и связь с существующими WROAD/WBACK.

`ALLOWED_SURFACES` принимает:

1. точный относительный путь;
2. явно разрешённое дерево корня продукта без предположения об обязательном `src/`;
3. точные исключения `<Slug>.profile:sot_mode` и `AGENTS.md::SOT_GITHUB_REPOSITORY`;
4. непустой набор этих поверхностей для active WPLAN; `none` не задаёт рабочую границу.

Внешняя граница может быть только сужена.

## Точка контроля реализации

Реализация разрешена, если:

1. обязательное интервью завершено или допустимо отложено;
2. активный WPLAN ссылается на действительное `interview_evidence`, если оно требуется интервью; при допустимом отсутствии IE используется `INTERVIEW_EVIDENCE_REF: none`, без synthetic record;
3. активный WPLAN ссылается на отдельное решение владельца `DECISION_KIND: implementation`;
4. решение имеет `DECISION_VALUE: approved` и относится к тому же WPLAN и IE;
5. идентичность продукта согласована между кратким описанием и WPLAN;
6. непустой `ALLOWED_SURFACES` задаёт точные рабочие поверхности; Product разрешён только после implementation gate.

Полный `PRODUCT_INPUT`, начальный pre-discovery запрос и команда «Продолжай» не разрешают реализацию. Отдельное явное post-discovery разрешение конкретного fix фиксируется по фактическому ответу владельца согласно interview и phase-gates.

## Фаза активного WPLAN

Фаза отражает текущее состояние и использует канонический каталог `01–21` из `docs/technical/sdlc.md`. После технической проверки допустимы `verification`, `owner-review` или закрытие WPLAN. Состояние продукта выводится из текущего активного WPLAN, наличия продукта и существующего принятого завершённого основания без реконструкции истории.

## Продуктовая приёмка

Переход `owner-review -> product-acceptance` открывает фазу по каноническому контракту `owner-open` в [phase-gates](../docs/technical/phase-gates.md) и не требует заранее существующего `PA-*`. Внутри фазы `Product Acceptance Coordinator` подготавливает пакет свидетельств, а явное решение владельца фиксируется отдельной записью `RECORD_TYPE: product_acceptance` с ID `PA-*`.

Для текущего owner gate `product-acceptance -> release-readiness` требуется `PA-* accepted` того же WPLAN. Отсутствующий, `pending`, `rejected` или относящийся к другому WPLAN `PA-*` не разрешает именно этот переход; разрешение реализации, решения жизненного цикла `OD-*`, Verification и Release Authorization его не заменяют. Технический PASS не создаёт `PA-*`.

После успешного перехода последующий WPLAN может использовать accepted `PA-*` как durable reference принятого результата. Его provenance `WPLAN_ID` не меняется; статус и ссылку проверяют по [границам Product Acceptance](../docs/technical/phase-gates.md#границы-product-acceptance), без требования совпасть с текущим WPLAN.

## Защищённые поверхности

Канонический реестр находится в `SYSTEM.md`. В `product-work` защищённые поверхности запрещены, кроме точных исключений `<Slug>.profile:sot_mode` и `AGENTS.md::SOT_GITHUB_REPOSITORY`, уже разрешённых владельцем и WPLAN для одной контрольной отметки перехода.

При запрещённом изменении или дефекте Harness агент выводит:

```text
HARNESS_BLOCKER: <краткое описание>
```

и прекращает изменения. Агент не проектирует исправление, не запрашивает `system-editing WPLAN`, не предлагает повторное исполнение, не создаёт исследование Harness и не управляет Workspace.

## SoT и локальная Git-работа

Project Profile `sot_mode=sot_git` сам по себе разрешает только начальную настройку отсутствующего неизменённого репозитория. Переход режима и `local_git_route` являются разными решениями владельца. Для одного WBACK существует не более одного `local_git_route`; WPLAN сужает его через `ALLOWED_SURFACES`.

Проверку режима и разрешённые действия выполнить по [SoT](sot.md); точные условия локального состояния принадлежат [справке Git](../docs/technical/git.md). Управление проектом не вводит вторую процедуру подготовки репозитория.

Для `S1/S2` кратко зафиксировать в WPLAN класс, владельца спецификации и применимые `REQ/INV/SCN`; для `S2` — также точный анализ влияния и набор изменений, прослеживаемость, уровень свидетельств и Consistency Closure. Полную спецификацию WPLAN не копирует. Порядок работы: основные действия → Bugfixes → Consistency Closure → проверка и контрольное чтение → точка решения владельца.

## Исполнение перехода фазы

Для `in-progress` завершённость, свидетельства и передача результата остаются `pending/none`, полномочия текущей роли — `active`, следующей — `withheld`. Завершённый переход требует конкретных ссылок на свидетельства, точной контрольной отметки и передачи результата, `relinquished` исходной и `granted` следующей роли. Перед следующей работой повторно проверить право целевой роли; полномочия `owner-review` разрешают подготовить обзор, но не означают принятие владельцем.

1. До работы в фазе проверить `FROM_PHASE/FROM_ROLE`, `AUTHORITY_REF: none | OD-*` по contract phase-gates, отдельно от required owner decision перехода, а также отсутствие преждевременно выданных полномочий следующей роли.
2. После работы связать точный `EVIDENCE_KIND` из [phase-gates](../docs/technical/phase-gates.md) и конкретные `EVIDENCE_REFS` со структурированным блоком свидетельств того же WPLAN и вида, а также с `REQ/INV/SCN`, не копируя содержимое в WPLAN.
3. Только при готовом результате поставить `PHASE_COMPLETION: complete`, точную контрольную отметку и существующий `HANDOFF_REF`; исходные полномочия перевести в `relinquished`, целевую — в `granted`.
4. Сверить переход, политику точки решения владельца и точный `Required owner decision kind` по одной строке [phase-gates](../docs/technical/phase-gates.md). `owner-open` допускает только точку контроля `pending` в данном переходе; `owner-decision` требует решения в соответствующих границах с точными каноническими видом и значением. `PA-*`, решения реализации и жизненного цикла `OD-*`, Release Authorization, другой WPLAN и Verification не взаимозаменяемы.
5. Проверить независимые статусы Verification, Validation, Product Acceptance и Release Authorization. Технический PASS не закрывает WPLAN и не открывает следующий маршрут сам по себе.

## Передача выпускных свидетельств

[Выпускная процедура](release-management.md) владеет предварительной проверкой текущего внешнего состояния, оценкой цепочки участников и независимым контрольным чтением. [Спецификация свидетельств](../docs/technical/release-evidence.md) разделяет снимок, кандидата, Product Acceptance, Release Authorization и публикацию. Полномочия фаз и решений задаёт phase-gates. Предварительная проверка никогда не повышает состояние автоматически.

## Доработка после owner review

`REQ-BP-REWORK-001`: canonical phase graph однонаправлен. Если результат допускается к следующему gate, выполняется обычный `owner-review -> product-acceptance`. При `changes requested` обратный переход не выполняется:

1. Зафиксировать обычный owner review result append-only с exact candidate identity и замечаниями; это не новый DECISION_KIND и не `PA-* rejected`.
2. Только по явному решению владельца завершить текущую итерацию WPLAN same-ID, сохранив прежние evidence и frozen result; добавить terminal disposition `changes requested / superseded / not accepted`. Product Acceptance и release остаются `not performed`, если их не было.
3. Оставить тот же WBACK active. После разрешения владельца и active WPLAN count `0` первой mutation нового прохода создать следующий corrective WPLAN. Завершённый WPLAN не переоткрывается.
4. Для Product correction новый WPLAN открывается в `approval` с pending implementation gate. После существования WPLAN записать fresh typed implementation OD именно этого WPLAN и штатно выполнить `approval -> implementation`. Старый OD сохраняет provenance предыдущей итерации и не даёт authority новой.

Закрытие итерации не является фазовым переходом назад, Product Acceptance или закрытием WBACK. Полномочия и evidence новых forward gates проверяются обычным checker; отдельный rework framework не вводится.

Обычное правило active WPLAN относится к project/system-editing work. Отдельная внешняя операция [Workspace Update](change-management.md#внешняя-граница-workspace-update) выполняется только в её frozen/quiescent/owner-authorized границе и не разрешает Product work.

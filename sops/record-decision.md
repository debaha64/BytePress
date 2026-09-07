# Запись решения владельца

Целевой артефакт: `logs/decisions.md`.
Шаблон или формат: `templates/decision-record.md`.
Способ записи: дозапись.

Канонический источник исполнения `SOURCE_REF` новых типизированных решений использует точный конечный диапазон долговечного `codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>`. Очищенный `.log` является представлением свидетельства и не обещает совпадения строк. Существующие обычные принятые IE/OD/PA сохраняют действительность корректной ссылки на существующий очищенный `.log` без миграции или нового поля. Локальная схема `owner_decision` или `product_acceptance` и `SOURCE_KIND: owner_response` задаёт ожидаемый класс источника.

`owner_decision` / `OD-*` сохраняет существующие виды `implementation`, `sot_transition`, `local_git_route` и допускает два вида решений жизненного цикла: `decommissioning_authorization`, `retirement_authorization`. OD жизненного цикла требует `DECISION_VALUE: approved`, текущий `WPLAN_ID`, текущий либо `none` в `ROUTE_REF` и `STATUS: active | applied`. Точный вид решения для перехода фазы читается из `docs/technical/phase-gates.md`.

`product_acceptance` / `PA-*` и Release Authorization остаются отдельными существующими контрактами. Ни один из них не заменяет вид OD, а OD жизненного цикла не заменяет `PA-*` или Release Authorization.

`local_git_route` и `sot_transition` перехода принятого продукта обязаны ссылаться через `EVIDENCE_REF` на IE текущей задачи класса `transition`, иметь тот же `SESSION_ID` и один необработанный источник выбора `B`; `PRODUCT_INPUT_REF` этого IE расположен раньше выбора. Исторический IE принятого продукта из предыдущей сессии не подходит.

Любой последующий `owner_decision`, чей `EVIDENCE_REF` указывает IE перехода, также обязан использовать существующий конечный диапазон необработанного источника. Более позднее разрешение реализации может находиться в другом необработанном файле. Если продуктовая приёмка относится к WPLAN с `INTERVIEW_EVIDENCE_REF` на IE перехода, `PA.SOURCE_REF` обязан использовать долговечный необработанный файл, который также может отличаться от источника перехода.

`owner_decision.SOURCE_REF` указывает фактическую реплику решения владельца, а `product_acceptance.SOURCE_REF` — фактическую реплику продуктовой приёмки. Итоговая техническая проверка фиксируется отдельно и не подменяет приёмку.

## Жизненный цикл записи и область маршрута

Для реализации `WPLAN_ID` указывает исполняемый WPLAN, `EVIDENCE_REF` — IE получения ответа либо переиспользуемый IE перехода. Обычный IE хранит WPLAN фактического получения ответа; поля `BASIS_WPLAN_ID/CAPTURE_WPLAN_ID` не вводятся.

`implementation`, `decommissioning_authorization`, `retirement_authorization`, `sot_transition`: `active -> applied | revoked`. `local_git_route`: `active -> suspended -> active`, `active -> closed | revoked`, `suspended -> closed | revoked`.

Для одного `ROUTE_REF` создаётся одна запись `local_git_route`. Последующие WPLAN того же WBACK используют её до окончательного закрытия; `closed` остаётся историческим свидетельством. В контрольной отметке перехода `WPLAN_ID` указывает WPLAN перехода; IE и обе OD впервые фиксируются вместе в одном коммите перехода и `SESSION_ID`. Проверка ссылки при исполнении не требует внешнего индекса.

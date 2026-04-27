# Product Bootstrap Validation

## Назначение
`Docs/Technical/Product_Bootstrap_Validation.md` является каноническим validation-contract bootstrap-result текущего `BytePress`.

Этот document отвечает на вопросы:
- как validating сторона определяет, что результат `Tools/bp_bootstrap.py` соответствует bootstrap-contract;
- как validating сторона подтверждает hard first product-start gate и reset/cleanup route;
- какие acceptance criteria для bootstrap-result обязательны;
- что проверяется автоматически, что проверяется процедурно, а что остаётся вне scope validation;
- какие validation-пропуски считаются недопустимыми.

## Место документа в technical-layer
`Product_Bootstrap_Validation.md` является supporting technical-document, а не частью required core.

Его роль:
- фиксировать validation-scope и acceptance criteria bootstrap-result;
- удерживать границу между bootstrap obligations и проверкой их выполнения;
- не дублировать `README.md` как карту technical-layer;
- не дублировать `Product_Bootstrap_Contract.md` как contract того, что bootstrap обязан materialize;
- не дублировать `Platform_Contracts.md` как execution perimeter и tool assumptions;
- не дублировать `Artifact_Lifecycle.md` как lifecycle и sync-loop matrix;
- не дублировать `Interfaces.md` как карту touchpoints;
- не дублировать `System_Invariants.md` как список ненарушаемых свойств системы.

## Чем validation-contract отличается от соседних документов
- `README.md` отвечает за карту technical-layer и required/supporting split.
- `Product_Bootstrap_Contract.md` отвечает за bootstrap obligations, minimal repo outcome и bootstrap boundaries.
- `Product_Bootstrap_Domain_Matrix.md` отвечает за top-level replication canon и routing default/later/BytePress-only domains.
- `Platform_Contracts.md` отвечает за execution environment, platform assumptions и tool perimeter.
- `Artifact_Lifecycle.md` отвечает за источники истины, допустимые transitions и обязательные sync-loop.
- `Interfaces.md` отвечает за interface boundaries и touchpoints.
- `System_Invariants.md` отвечает за ненарушаемые системные свойства.
- `Product_Bootstrap_Validation.md` отвечает только за то, по каким критериям bootstrap-result признаётся корректным и достаточно валидированным.

## Связь с `Tools/bp_bootstrap.py`, `Tools/bp_lint.py` и bootstrap-contract
`Tools/bp_bootstrap.py` materialize bootstrap-result.

`Docs/Technical/Product_Bootstrap_Contract.md` задаёт, что bootstrap обязан materialize.

`Tools/bp_lint.py` автоматизирует часть structural validation, но не заменяет весь validation-contract. Для product repo он различает fresh bootstrap check и developed product check; режим `auto` выбирает их по состоянию `Docs/Discovery/Interview.md`.

Это означает:
- validation проверяет результат materialization, а не подменяет bootstrap obligations;
- `bp_lint.py` покрывает только автоматизируемый structural минимум текущего active contract;
- procedural validation остаётся обязательной там, где один structural check не способен подтвердить соблюдение contract;
- procedural validation обязана отдельно подтвердить, что current bootstrap default следует matrix `Default / Later product-pass / BytePress-only` и не materialize лишние top-level domains;
- расхождение между bootstrap-contract, validation-contract и tooling считается active contradiction и должно быть синхронизировано явно.

## Validation scope
Validation-contract покрывает только bootstrap-result, materialized `BytePress` bootstrap tooling.

В scope входят:
- корректность CLI-level outcome при использовании обязательных параметров `--name`, `--product-code`, `--brand-profile`, `--target`;
- корректность first-usable replicated product repo outcome;
- корректность minimal discovery-layer generated product repo;
- корректность minimal integration smoke route generated product repo;
- наличие обязательных directories, singleton artifacts и bootstrap-created skeleton files;
- корректность baseline profile, initial planning contour и базового structural check;
- различие между automatic checks и procedural checks.

В scope не входят:
- предметная полнота `Docs/Product/*`;
- предметная оценка последующих продуктовых passes после initial product initialization; при этом structural consistency developed product repo после закрытия first pass входит в automatic perimeter `bp_lint.py`;
- полная verification-model продукта;
- runtime behavior будущего продукта beyond bootstrap skeleton;
- расширение bootstrap на новые домены, не входящие в текущий contract.

## Acceptance criteria bootstrap-result
Bootstrap-result считается принятым только если одновременно выполняются все условия:
- bootstrap создаёт отдельный product repo вне дерева самого `BytePress`;
- bootstrap требует и валидирует обязательные CLI параметры без silent fallback;
- bootstrap materialize first-usable replicated repo outcome, описанный в `Product_Bootstrap_Contract.md`;
- bootstrap materialize отдельный `scripts/integration-smoke.sh`, который проверяет controlled integration handoff без реальных внешних подключений;
- bootstrap materialize route, в котором `scripts/integration-smoke.sh` выпускает deterministic report artifact `Runtime/Integration_Smoke_Report.json`, а его verdict согласован со smoke result;
- bootstrap materialize `scripts/reset-product-start.sh` как canonical failed-start cleanup route;
- создаются `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md` как minimal current-truth route generated repo;
- generated product `AGENTS.md` требует наблюдаемый стартовый отчёт первого ответа с режимом запуска, scope, статусом ветки, действием с веткой/стартовым маршрутом, planning-state, доменами-владельцами первого чтения и первым конкретным шагом;
- generated product `AGENTS.md` оформляет этот стартовый отчёт коротким блоком с приветствием и семью полями, а не длинным регламентом;
- generated product `AGENTS.md` удерживает hard first product-start gate: пока `Docs/Discovery/Interview.md` имеет `Статус_текущей_истины: Не_подтверждена`, agent остаётся только в аналитическом контуре, не трактует bootstrap-заготовки как разрешение на implementation и не делает записываемые изменения до открытия task-ветки;
- `Docs/Discovery/Interview.md` generated repo остаётся владельцем текущей истины и содержит 8–10 ключевых вопросов первого pass; и full interview, и допустимый delta-интервью используют нумерованные вопросы, буквенные варианты там, где выбор ограничен, рекомендуемый вариант там, где он нужен, смысловые классы `Контекст`, `Граница`, `Ограничение`, `Владение`, `Переход` и правило `блокирующее сразу / неблокирующее в следующую фазу`;
- `Docs/Discovery/Interview.md` generated repo явно фиксирует `Статус_текущей_истины: Не_подтверждена` и запрет трактовать bootstrap-заготовки как подтверждённую текущую истину;
- generated repo получает `Docs/Terms/Base_Terms.md` со стартовым пакетом терминов вместо полного term-layer `BytePress`;
- создаются `AGENTS.md` и обязательный `Docs/User/*` contour replicated repo;
- создаётся `Profiles/Product.md` с `Тип_профиля: product` и `ID: PROF-000001`;
- создаётся initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md` с внутренним `ID: PLAN-000001`;
- `Roadmap`, `Backlog`, `Plan` и product profile используют ожидаемый naming baseline bootstrap-result, а initial stage/task/pass находятся в `В_работе`;
- created repo проходит обязательный structural check текущего `bp_lint.py` в режиме fresh bootstrap или `auto`;
- bootstrap не подменяет contract лишними доменами, скрытым наследованием brand profile или auto-generated `product-code`.

## Обязательные validation checks
Обязательная validation должна подтвердить:
- bootstrap запускается только при наличии корректного brand profile внутри `BytePress`;
- invalid input завершает bootstrap явной ошибкой, а не partial guessed outcome;
- target repo получает все обязательные top-level and nested paths bootstrap-result;
- target repo получает минимальный human/agent entry contour: `AGENTS.md`, `Docs/User/*`, `README.md`, `Setup_Guide.md`;
- target repo получает minimal discovery contour: `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md`;
- target repo получает hard first product-start gate в `AGENTS.md`, initial `Plan` и discovery-layer, а не только общую startup prose; этот gate требует task-ветку до любых записываемых изменений, включая discovery/planning/log closure;
- target repo получает `Docs/Terms/Base_Terms.md` со стартовым пакетом терминов, достаточным для раннего product-start;
- target repo получает `.gitignore`, в котором `Runtime/Integration_Smoke_Report.json` остаётся runtime-local artifact и не попадает в baseline commit по умолчанию;
- bootstrap materialize минимальный technical subset продукта: `README.md`, `Architecture.md`, `Interfaces.md`, `System_Invariants.md`;
- bootstrap materialize minimal product layer `Docs/Product/README.md`, `JTBD.md`, `PRD.md`, `Delivery.md`;
- bootstrap materialize initial planning contour, logs, adapters и project scripts как first-usable replicated outcome;
- bootstrap materialize project-side integration smoke route без `MCP/*` внутри generated repo и без network-dependent behavior;
- bootstrap materialize `scripts/reset-product-start.sh` как canonical cleanup route failed early product-start;
- bootstrap materialize deterministic integration evidence/report artifact без превращения `Runtime/*` в новый source-of-truth layer;
- bootstrap-result проходит machine-check уровня `python3 Tools/bp_lint.py --repo <product-repo> --mode product-fresh` или `--mode auto`;
- bootstrap не пытается притвориться полным replica-contract самого `BytePress`.

## Automatic checks
Автоматически проверяемый минимум на текущем этапе:
- наличие обязательных top-level paths product repo;
- наличие `AGENTS.md` и mandatory `Docs/User/*` documents;
- наличие `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md`;
- наличие наблюдаемого стартового отчёта первого ответа в generated product `AGENTS.md`;
- наличие в generated product `AGENTS.md` приветствия и короткого стартового блока;
- наличие hard first product-start gate в generated product `AGENTS.md`, который требует task-ветку до любых записываемых изменений;
- наличие в generated `Docs/Discovery/Interview.md` 8–10 ключевых вопросов, буквенных вариантов, рекомендуемого варианта там, где это уместно, смысловых классов вопросов и explicit delta-интервью contract в том же формате;
- наличие в generated `Docs/Discovery/Interview.md` статуса `Статус_текущей_истины: Не_подтверждена` и явного запрета трактовать bootstrap-заготовки как подтверждённую текущую истину;
- наличие в generated `Docs/Terms/Base_Terms.md` стартового пакета терминов;
- наличие обязательных product-layer, technical-layer, terms-layer, plans-layer, logs-layer, adapters-layer и scripts-layer files;
- наличие `scripts/integration-smoke.sh` и его executable mode;
- наличие `scripts/reset-product-start.sh` и его executable mode;
- наличие `.gitignore`, который удерживает `Runtime/Integration_Smoke_Report.json` вне baseline commit по умолчанию;
- наличие `Profiles/Product.md`;
- наличие initial plan filename `Plans/<PRODUCT_CODE>-000001-product-initialization.md`;
- наличие `ID: PLAN-000001` в initial plan file;
- наличие initial stage/task/pass в состоянии `В_работе`;
- наличие `Тип_профиля: product` и `ID: PROF-000001` в `Profiles/Product.md`.

Текущий automatic perimeter реализуется в `Tools/bp_lint.py`.

## Developed product structural check
После подтверждения текущей истины и закрытия first product-start pass тот же product repo больше не обязан сохранять fresh bootstrap markers.

`bp_lint.py` в режиме `product-developed` проверяет, что:
- `Docs/Discovery/Interview.md` имеет `Статус_текущей_истины: Подтверждена`;
- bootstrap-заготовки ответов больше не остаются в текущей истине;
- `ROAD-000001`, `BACK-000001` и `PLAN-000001` закрыты как first pass contour;
- после `PLAN-000001` есть следующий active или completed plan;
- `Logs/ChangeLog.md` и `Logs/QualityLog.md` содержат факты closure первого pass.

Этот режим не оценивает предметное качество продукта и не превращает `bp_lint.py` в semantic auditor. Его задача — отличить нормальный lifecycle transition от реального contradiction между `Docs/Discovery/Interview.md`, `Plans/*` и `Logs/*`.

Служебное обновление уже созданного developed product repo валидируется как product-side pass, а не как новый bootstrap-result. Для обновлений уровня `scripts/dev-test.sh` и `scripts/README.md` validating сторона проверяет, что:
- product repo не пересоздавался через fresh bootstrap;
- изменён только нужный служебный delta;
- предметные артефакты и подтверждённая текущая истина не потеряны;
- `--mode auto` или explicit `product-developed` подтверждает developed state;
- fresh bootstrap gate не используется как основание требовать возврат к initial заготовкам.

## Procedural checks
Процедурная validation остаётся обязательной для подтверждения того, что:
- bootstrap действительно выполняется против отдельного target directory, а не против дерева `BytePress`;
- выбранный `brand profile` является допустимым bootstrap input и использован без скрытой подмены;
- CLI behavior соответствует contract при валидных и невалидных параметрах;
- созданные заготовки остаются first-usable replicated contour, а не случайным смешением bootstrap и последующего предметного наполнения;
- незаполненный discovery не трактуется validating стороной как implicit approval для implementation;
- bootstrap не materialize домены, которые contract прямо относит вне bootstrap perimeter.

Процедурная validation может выполняться агентом или человеком, но не может считаться необязательной только потому, что structural lint прошёл.

## Что validation не обязана делать
Validation-layer не обязана:
- перепроверять всю архитектурную, модельную или interface-карту системы;
- заменять bootstrap-contract новым списком obligations;
- доказывать release readiness product repo;
- валидировать будущие passes после `PLAN-000001` продукта;
- подменять `Platform_Contracts.md` или полный verification contour будущего `ROAD-000011`.

## Недопустимые validation-пропуски
Считаются недопустимыми:
- принимать bootstrap-result только по факту успешного запуска `bp_bootstrap.py` без проверки materialized outcome;
- считать один `bp_lint.py` исчерпывающей validation-моделью, если procedural checks пропущены;
- считать bootstrap-заготовки или незаполненный discovery достаточным основанием для перехода к implementation;
- проверять bootstrap-result по устаревшему contract после изменения `Product_Bootstrap_Contract.md`;
- считать bootstrap валидированным, если обязательные singleton artifacts отсутствуют, но repo выглядит частично собранным;
- смешивать validation-result с предметной оценкой качества продукта или с будущими lifecycle-переходами.

## Validation boundaries
Validation-layer отвечает за доказательство корректности bootstrap-result.

Validation-layer не отвечает за:
- изменение bootstrap behavior вместо отдельного tooling pass;
- расширение bootstrap perimeter;
- ведение planning-state или runtime-state;
- подмену log-layer фактическими evidence records без явной фиксации в `Logs/*`.

## Отношение validation-layer к соседним контурам
### К `Plans/*`
`Plans/*` задаёт stage/task/pass и governance contour работы. Validation-layer использует этот контур как источник управляющего pass, но не владеет planning-state.

### К `Tools/bp_bootstrap.py`
`bp_bootstrap.py` materialize bootstrap-result. Validation-layer не задаёт новые обязанности инструменту, а проверяет уже утверждённый expected outcome.

### К `Tools/bp_lint.py`
`bp_lint.py` остаётся автоматическим structural gate bootstrap-result. Validation-layer определяет, где lint достаточен, а где нужен procedural check поверх него.

### К `Product_Bootstrap_Contract.md`
Bootstrap-contract отвечает за обязательства и expected outcome. Validation-contract отвечает за критерии и способ проверки этого outcome.

### К `Pipeline/*`
`Pipeline/*` может задавать общий verification/workflow context, но не является primary source bootstrap acceptance criteria.

## Граница документа
`Product_Bootstrap_Validation.md` не является:
- bootstrap-contract document;
- platform-contract document;
- lifecycle-checklist для всего репозитория;
- общей verification policy всего `BytePress`;
- evidence log конкретного запуска bootstrap.

Он остаётся каноническим validation-contract bootstrap-result текущего `BytePress`.

## Связи
- `PLAN-000005`
- `PLAN-000010`
- `PLAN-000047`
- `ADR-000009`
- `CHG-000009`
- `CHG-000019`

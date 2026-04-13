# Product Bootstrap Contract

## Назначение
`Docs/Technical/Product_Bootstrap_Contract.md` является каноническим bootstrap-contract текущего `BytePress`.

Этот document отвечает на вопросы:
- какой first-usable replicated product repo обязан materialize `Tools/bp_bootstrap.py`;
- какие артефакты bootstrap обязан создать сразу;
- какие слои bootstrap инициализирует только как каркас;
- где проходит граница bootstrap-ответственности;
- какие bootstrap-пропуски и упрощения считаются допустимыми или недопустимыми.

## Место документа в technical-layer
`Product_Bootstrap_Contract.md` является supporting technical-document, а не частью required core.

Его роль:
- фиксировать expected outcome bootstrap replication;
- удерживать один канонический contract first-usable replicated product repo;
- не дублировать `README.md` как карту technical-layer;
- не дублировать `Platform_Contracts.md` как contract среды и tool perimeter;
- не дублировать `Artifact_Lifecycle.md` как lifecycle и sync-loop matrix;
- не дублировать `Interfaces.md` как карту touchpoints;
- не дублировать `Product_Bootstrap_Validation.md` как документ фактической проверки результата.

## Чем bootstrap-contract отличается от соседних документов
- `README.md` отвечает за карту technical-layer и его required/supporting split.
- `Platform_Contracts.md` отвечает за рабочую платформу, execution assumptions и supported tool perimeter.
- `Artifact_Lifecycle.md` отвечает за источники истины и обязательные sync-loop.
- `Interfaces.md` отвечает за допустимые точки стыка и service interfaces.
- `Product_Bootstrap_Contract.md` отвечает за то, что именно должен создать bootstrap и где заканчивается его ответственность.
- `Product_Bootstrap_Validation.md` отвечает не за обязательства, а за validation-scope, acceptance criteria и подтверждение корректности bootstrap-result.

## Связь с `Tools/bp_bootstrap.py`
`Tools/bp_bootstrap.py` является materializer этого контракта.

Это означает:
- contract первичен как человеко-читаемое описание ожидаемого bootstrap outcome;
- `bp_bootstrap.py` обязан оставаться согласованным с этим document;
- расширение bootstrap behavior без документной синхронизации считается contract drift;
- validation проходит против materialized result, а не заменяет сам contract.

## CLI contract bootstrap
### Обязательные параметры
- `--name`
- `--product-code`
- `--brand-profile`
- `--target`

### Обязательные правила параметров
- `--name` не должен быть пустым;
- `--product-code` обязателен и содержит 2-3 символа верхнего регистра;
- `--product-code` не генерируется автоматически;
- `--brand-profile` обязателен и должен ссылаться на существующий brand profile в `BytePress`;
- указанный profile должен иметь `Тип_профиля: brand`;
- brand profile обязан содержать `Язык_взаимодействия`;
- при нарушении этих условий bootstrap завершается явной ошибкой, а не создаёт частично догаданный outcome.

## First-usable replicated outcome bootstrap
Bootstrap materialize отдельный product repo с first-usable initialized state, пригодным для первого предметного pass и согласованным с current human/agent entry contour `BytePress`.

Outcome включает:
- отдельный target-репозиторий продукта вне дерева самого `BytePress`;
- top-level human/agent entry files `README.md`, `AGENTS.md`, `Setup_Guide.md`, `.gitignore`;
- базовую структуру каталогов `Docs/`, `Runtime/`, `Plans/`, `Logs/`, `Profiles/`, `Adapters/`, `scripts/`;
- минимальный, но first-usable `Docs/User/*` contour;
- минимальный product-layer с базовыми content placeholders;
- минимальный technical-layer продукта только в объёме стартовых singleton docs;
- initial planning contour продукта в состоянии first current stage/task/pass;
- базовые logs, adapter registry/policy и project entry scripts.

Bootstrap не обязан делать product repo предметно завершённым; он обязан сделать его first-usable, согласованным и пригодным к следующему управляемому pass без ручной пересборки entry contour.

## Обязательные создаваемые артефакты и слои
### Репозиторный каркас
Bootstrap обязан создать:
- `.gitignore`
- `README.md`
- `AGENTS.md`
- `Setup_Guide.md`

### Product knowledge layer
Bootstrap обязан создать:
- `Docs/User/README.md`
- `Docs/User/Operating_Mode.md`
- `Docs/User/First_Start.md`
- `Docs/User/Pass_Request.md`
- `Docs/User/Usage_Scenarios.md`
- `Docs/Product/README.md`
- `Docs/Product/JTBD.md`
- `Docs/Product/PRD.md`
- `Docs/Product/Delivery.md`

Эти документы создаются как first-usable startup contour и content skeleton, а не как полностью предметно заполненный product package.

### Technical layer продукта
Bootstrap обязан создать:
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Technical/System_Invariants.md`

Bootstrap не обязан создавать для product repo полный `BytePress` technical core. В текущем contract он materialize только минимальный стартовый technical subset, достаточный для первого product initialization pass.

### Terminology layer
Bootstrap обязан создать:
- `Docs/Terms/README.md`
- `Docs/Terms/Base_Terms.md`

### Runtime layer
Bootstrap обязан создать:
- `Runtime/README.md`
- `Runtime/Context.md`
- `Runtime/Task.md`
- `Runtime/Session_Log.md`
- `Runtime/Handover.md`

Эти артефакты инициализируют runtime-carrier, но не заполняют его фактическим состоянием beyond bootstrap baseline.

### Planning layer
Bootstrap обязан создать:
- `Plans/README.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md`

Planning outcome должен удовлетворять текущему bootstrap contract:
- roadmap использует `ROAD-000001`;
- backlog использует `BACK-000001`;
- initial plan имеет внутренний `ID: PLAN-000001`;
- filename initial plan использует product code prefix, а не filename вида `PLAN-000001-*`.
- initial `Roadmap`, `Backlog` и `Plan` находятся в статусе `В_работе`.

### Fact layer
Bootstrap обязан создать:
- `Logs/README.md`
- `Logs/ChangeLog.md`
- `Logs/ADRlog.md`
- `Logs/QualityLog.md`
- `Logs/ReleaseLog.md`
- `Logs/SupportLog.md`

### Governance and integration skeleton
Bootstrap обязан создать:
- `Profiles/Product.md`
- `Adapters/README.md`
- `Adapters/Policy.md`
- `Adapters/Registry.md`
- `Adapters/Codex/README.md`
- `Adapters/Claude/README.md`
- `Adapters/Gemini/README.md`
- `Adapters/Local/README.md`

### Project entry scripts
Bootstrap обязан создать:
- `scripts/README.md`
- `scripts/dev-up.sh`
- `scripts/dev-down.sh`
- `scripts/dev-test.sh`

Project scripts materialize first-usable project entry skeleton. `dev-test.sh` обязан давать явный route к structural check replicated repo через `BytePress`, а не оставаться немым placeholder.

## Что bootstrap materialize только как каркас
Bootstrap создаёт каркас, но не завершённое содержательное состояние, для:
- `AGENTS.md` продукта — только minimal agent entry point replicated repo, а не копию `AGENTS.md` самого `BytePress`;
- `Docs/User/*` продукта — только minimal human-facing contour, а не полный manual;
- `Docs/Product/*` — только стартовый first-version content skeleton;
- `Docs/Technical/*` продукта — только minimal startup subset, а не полный system contract map;
- `Runtime/*` — только carrier для дальнейшего execution context;
- `Plans/*` — только начальный stage/task/pass baseline, а не готовый предметный backlog;
- `Logs/*` — только empty or near-empty fact containers;
- `Adapters/*` и `scripts/*` — только managed entry skeleton без полноценной интеграционной логики.

## Что bootstrap сознательно не обязан делать
Bootstrap не обязан:
- копировать в product repo полный доменный состав самого `BytePress`;
- создавать `Pipeline/`, `Rules/`, `Standards/`, `Schemas/`, `Templates/`, `Skills/`, `Memory/` или `MCP/` внутри product repo;
- materialize `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/Platform_Contracts.md` или другие advanced technical contracts продукта;
- создавать предметно завершённые product requirements, delivery model или terminology base;
- открывать несколько roadmap stages, backlog items или plans;
- автоматически генерировать `product-code`, brand inheritance beyond allowed fields или скрытые external integrations;
- превращать product repo в копию operational/governance contour самого `BytePress`.

## Bootstrap boundaries
### Граница ответственности
Bootstrap отвечает за:
- создание first-usable согласованного product repo;
- соблюдение naming/profile/date baseline текущего контракта;
- materialization только того skeleton, который нужен для первого управляемого product pass.

Bootstrap не отвечает за:
- предметное наполнение продукта;
- полный technical normalization product repo;
- release readiness продукта;
- продуктовую verification-model beyond base structural check;
- последующие passes после initial product initialization.

### Допущения
Bootstrap предполагает, что:
- target path доступен для записи;
- `BytePress` выступает source repo для bootstrap;
- выбранный brand profile уже существует и валиден;
- дальнейшее предметное наполнение выполнит следующий pass, а не сам bootstrap.

## Допустимые и недопустимые упрощения
### Допустимые упрощения
- создавать product docs как короткие стартовые placeholders;
- ограничивать technical layer продукта минимальным subset;
- ограничивать planning layer одной стартовой stage/task/pass цепочкой;
- materialize product repo с minimal human/agent entry contour вместо полного governance copy;
- ограничивать brand inheritance полями `Брендовый_профиль` и `Язык_взаимодействия`;
- создавать logs как пустые или почти пустые singleton containers.

### Недопустимые упрощения и пропуски
- не создавать один из обязательных singleton artifacts минимального outcome;
- не создавать `AGENTS.md` или обязательный `Docs/User/*` contour replicated repo;
- создавать initial plan без внутреннего `ID: PLAN-000001`;
- оставлять initial stage/task/pass в пассивном или двусмысленном состоянии, если репозиторий заявлен как first-usable;
- пропускать `Profiles/Product.md` или нарушать `Тип_профиля: product`;
- silently подставлять отсутствующий `brand profile` или auto-generate `product-code`;
- считать bootstrap завершённым, если product repo не проходит базовый structural check или если human/agent entry contour не materialized;
- переносить в bootstrap contract обязанности validation-layer или последующих предметных passes.

## Связь с validation-layer
`Product_Bootstrap_Contract.md` задаёт expected bootstrap obligations.

`Product_Bootstrap_Validation.md`:
- фиксирует validation-scope и acceptance criteria bootstrap-result;
- разделяет automatic и procedural checks вокруг bootstrap behavior;
- подтверждает sync между contract и реализованным bootstrap behavior;
- не заменяет сам contract и не задаёт новые bootstrap obligations.

Если validation document и `bp_bootstrap.py` расходятся, каноническое исправление должно сначала синхронизировать contract или bootstrap behavior, а не подменять contract одним validation result.

## Отношение bootstrap-contract к соседним контурам
### К `Plans/*`
Bootstrap обязан materialize только initial planning contour продукта. Дальнейший planning-state создаётся уже внутри product repo и не принадлежит bootstrap contract `BytePress`.

### К `Platform_Contracts.md`
Platform contract задаёт execution perimeter и tool assumptions. Bootstrap contract задаёт expected product repo outcome внутри этого периметра.

### К `Artifact_Lifecycle.md`
Lifecycle contract задаёт sync-loop и source-of-truth matrix. Bootstrap contract задаёт только initial materialized product state до дальнейших lifecycle-переходов.

### К `Interfaces.md`
Interface contract задаёт touchpoints между доменами. Bootstrap contract задаёт, какие минимальные domain entrypoints и skeleton files должны появиться после bootstrap.

## Граница документа
`Product_Bootstrap_Contract.md` не является:
- картой technical-layer как каталога;
- platform-contract document;
- lifecycle-checklist;
- validation report;
- process-canon document.

Он остаётся каноническим contract того, какой first-usable replicated product repo обязан materialize `BytePress` bootstrap.

## Связи
- `ADR-000009`
- `CHG-000009`

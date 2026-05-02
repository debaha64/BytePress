# Product Bootstrap Contract

## Назначение
`Docs/Technical/Product_Bootstrap_Contract.md` является каноническим bootstrap-contract текущего `BytePress`.

Этот document отвечает на вопросы:
- какой first-usable replicated product repo обязан materialize `Tools/bp_bootstrap.py`;
- как классифицирован каждый top-level domain `BytePress` для product bootstrap;
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
- `Product_Bootstrap_Domain_Matrix.md` отвечает за top-level replication canon и не подменяет bootstrap obligations по конкретным артефактам.
- `Product_Bootstrap_Validation.md` отвечает не за обязательства, а за scope проверки, acceptance criteria и подтверждение корректности bootstrap-result.

## Связь с `Tools/bp_bootstrap.py`
`Tools/bp_bootstrap.py` является materializer этого контракта.

Это означает:
- contract первичен как человеко-читаемое описание ожидаемого bootstrap outcome;
- `bp_bootstrap.py` обязан оставаться согласованным с этим document;
- расширение bootstrap behavior без документной синхронизации считается contract drift;
- validation проходит против materialized result, а не заменяет сам contract.

## Целевой переход к профильной фабрике
Решение `ADR-000022` меняет целевую модель bootstrap: продуктовый каркас должен зависеть от product profile и быть самодостаточным после создания.

Целевое состояние:
- продукт всегда получает лёгкий локальный `Pipeline/*`;
- продукт получает локальный `Tools/*`, а прежние generated `scripts/*` переносятся в product tools или остаются только тонкими aliases;
- продукт получает `Templates/*` только для артефактов, которые есть в каркасе;
- продукт получает `Schemas/*` только для артефактов, которые local product tools реально проверяют;
- retired domains не входят в product baseline;
- `Rules/*` в продукте допускается только как сокращённый профильный пакет обязательных project-specific rules.

Текущий `bp_bootstrap.py` начал переходную реализацию этой модели: новый продукт получает local `Tools/*`, lightweight `Pipeline/*`, bounded `Templates/*` и `Schemas/*`, а legacy `scripts/*` остаётся только совместимой оболочкой.

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
Bootstrap materialize отдельный product repo с first-usable initialized state, пригодным для первого управляемого product-start pass и согласованным с current human/agent entry contour `BytePress`.

Каноническая классификация всех top-level доменов `BytePress` для этого outcome живёт в `Docs/Technical/Product_Bootstrap_Domain_Matrix.md`.

Current implemented bootstrap default materialize только тот domain subset, который нужен для controlled раннего product-start contour. Наличие стартовых заготовок не означает, что generated repo сразу разрешает предметную реализацию.

Outcome включает:
- отдельный target-репозиторий продукта вне дерева самого `BytePress`;
- top-level human/agent entry files `README.md`, `AGENTS.md`, `Setup_Guide.md`, `.gitignore`;
- базовую структуру каталогов `Docs/`, `Plans/`, `Logs/`, `Pipeline/`, `Tools/`, `Templates/`, `Schemas/` и совместимый `scripts/` layer;
- минимальный `Docs/Discovery/*` contour для first current-truth route;
- hard first product-start gate, который удерживает initial pass только в аналитическом контуре до ответов пользователя;
- минимальный, но first-usable `Docs/User/*` contour;
- минимальный product-layer с базовыми content-заготовками;
- минимальный technical-layer продукта только в объёме стартовых singleton docs;
- initial planning contour продукта в состоянии first current stage/task/pass;
- базовые logs и локальный product `Tools/*`;
- совместимые shell wrappers в `scripts/*`, которые вызывают локальный `Tools/*`;
- local smoke route без зависимости от `BYTEPRESS_ROOT`.

Bootstrap не обязан делать product repo предметно завершённым; он обязан сделать его first-usable, согласованным и пригодным к следующему управляемому pass без ручной пересборки entry contour.

## Обязательные создаваемые артефакты и слои
### Репозиторный каркас
Bootstrap обязан создать:
- `.gitignore`
- `README.md`
- `AGENTS.md`
- `Setup_Guide.md`

### Discovery layer
Bootstrap обязан создать:
- `Docs/Discovery/README.md`
- `Docs/Discovery/Interview.md`

Этот discovery minimum даёт first current-truth route продукта и не materialize полный discovery package `BytePress`.

Discovery minimum раннего product-start contour обязан явно фиксировать:
- что `Docs/Discovery/Interview.md` остаётся owner текущей аналитической истины generated product repo;
- что bootstrap-created interview стартует в состоянии `Статус_текущей_истины: Не_подтверждена`;
- что bootstrap-заготовки не считаются подтверждённой текущей истиной;
- что до ответов пользователя generated repo остаётся только в аналитическом контуре и не открывает product docs/code/runtime implementation;
- что первое записываемое действие generated product repo допускается только после открытия рабочей ветки, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`;
- что bootstrap-created interview содержит 8–10 ключевых вопросов первого pass;
- что вопросы собраны по классам `Контекст`, `Граница`, `Ограничение`, `Владение`, `Переход`;
- что буквенные варианты ответа используются там, где выбор ограничен;
- что рекомендуемый вариант помечается там, где есть предпочтительный route;
- что блокирующие вопросы задаются сразу, а неблокирующие накапливаются для следующей фазы;
- что допустимый узкое интервью route не отменяет structured format и использует тот же numbered / lettered / recommended contract.

### User and product knowledge layer
Bootstrap обязан создать:
- `Docs/User/README.md`
- `Docs/User/Operating_Mode.md`
- `Docs/User/First_Start.md`
- `Docs/User/Pass_Request.md`
- `Docs/User/Usage_Scenarios.md`
- `Docs/Product/README.md`
- `Docs/Product/Product_Passport.md`
- `Docs/Product/JTBD.md`
- `Docs/Product/PRD.md`
- `Docs/Product/Delivery.md`

Эти документы создаются как first-usable startup contour и content skeleton, а не как полностью предметно заполненный product package.

`Docs/Product/Product_Passport.md` фиксирует минимальный паспорт созданного каркаса без materialization домена `Profiles/*` внутри продукта.

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

`Docs/Terms/Base_Terms.md` generated product repo обязан содержать минимальный стартовый пакет терминов и не копировать весь словарь `BytePress`.

Минимальный стартовый пакет терминов включает:
- `TERM-000019` — `Каркас репозитория`;
- `TERM-000020` — `Текущая истина`;
- `TERM-000021` — `Рабочая ветка`;
- `TERM-000007` — `Дорожная карта`;
- `TERM-000008` — `Реестр работ`;
- `TERM-000009` — `План`.

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

### Lightweight Pipeline layer
Bootstrap обязан создать:
- `Pipeline/README.md`
- `Pipeline/Phases.md`
- `Pipeline/Workflows.md`
- `Pipeline/Gates.md`

Этот слой фиксирует минимальный process contour продукта без копирования полного `Pipeline/*` самого `BytePress`.

Generated `Pipeline/*` обязан описывать:
- основной путь продукта;
- рабочий поток первого `product-start`;
- рабочий поток предметного прохода;
- гейты;
- уровни проверок: структура, тесты, запуск, GUI-запуск и ручная проверка;
- журнальное закрытие;
- PR-маршрут через `gh`.

### Product-local Tools layer
Bootstrap обязан создать:
- `Tools/README.md`
- `Tools/product_check.py`
- `Tools/product_bootstrap_smoke.py`

Product-local `Tools/*` является основной служебной точкой продукта. `product_check.py` проверяет fresh/developed lifecycle state без `BYTEPRESS_ROOT`, а `product_bootstrap_smoke.py` выпускает deterministic report в ignored `Tools/.reports/`.

### Bounded Templates and Schemas layer
Bootstrap обязан создать `Templates/*` только для materialized artifacts продукта и `Schemas/*` только для artifacts, которые проверяются local `Tools/*`.

Текущий bounded subset:
- `Templates/Interview.md`, `Roadmap.md`, `Backlog.md`, `Plan.md`, `ChangeLog.md`, `ADRlog.md`, `QualityLog.md`;
- `Schemas/roadmap_item.schema.json`, `backlog_item.schema.json`, `plan.schema.json`, `changelog_entry.schema.json`, `adr_entry.schema.json`.

### Project entry scripts
Bootstrap обязан создать:
- `scripts/README.md`
- `scripts/dev-up.sh`
- `scripts/dev-down.sh`
- `scripts/dev-test.sh`
- `scripts/integration-smoke.sh`
- `scripts/reset-product-start.sh`

Project scripts являются переходным совместимым слоем. Основной служебный вход — `Tools/*`. `dev-test.sh` вызывает `Tools/product_check.py`, `integration-smoke.sh` вызывает `Tools/product_bootstrap_smoke.py`, а `reset-product-start.sh` очищает `Tools/.reports/` и показывает drift report. `scripts/*` можно удалить после первого прохода обновления служебного слоя или когда продукту больше не нужны shell-оболочки.

`scripts/*` не является основным служебным слоем продукта. Generated `scripts/README.md` обязан явно фиксировать переходный статус и условие удаления: после обновления служебного слоя созданного продукта, если продукту не нужны shell-оболочки. Главный служебный вход — локальный `Tools/*`.

### Обновление служебных файлов уже созданного product repo
Если product repo уже создан и прошёл первый product-start pass, canonical route обновления служебного слоя — точечный product-side pass, а не повторный bootstrap.

Канонический маршрут описан в `Docs/Technical/Product_Service_Update_Route.md`. Минимальный путь для local `Tools/*` и совместимых `scripts/*`:
1. взять основание из текущего `BytePress` contract и фактического generated skeleton;
2. открыть рабочую ветку внутри product repo;
3. перенести только служебный delta в `Tools/*`, lightweight `Pipeline/*`, bounded `Templates/*`/`Schemas/*` и thin wrappers `scripts/*`;
4. удалить только placeholder legacy service domains старого каркаса, если они не содержат предметного смысла продукта;
5. не пересоздавать product repo и не переписывать `Docs/Product/*`, `Docs/Discovery/*`, `Plans/*`, `Logs/*` или предметный код вне прямой необходимости pass;
6. проверить product repo через `python3 Tools/product_check.py --repo . --mode auto`, `scripts/dev-test.sh` и `python3 <BytePress>/Tools/bp_lint.py --repo <product-repo> --mode auto`;
7. зафиксировать product-side planning/log closure.

Короткий канонический пример developed product state после первого прохода:
- `Docs/Discovery/Interview.md` имеет `Статус_текущей_истины: Подтверждена`;
- `ROAD-000001`, `BACK-000001` и `PLAN-000001` закрыты;
- есть следующий active или completed plan;
- `Logs/ChangeLog.md` и `Logs/QualityLog.md` содержат closure facts первого pass;
- `Tools/product_check.py --mode auto` проходит developed product gate без возврата к fresh bootstrap markers.

## Что bootstrap materialize только как каркас
Bootstrap создаёт каркас, но не завершённое содержательное состояние, для:
- `AGENTS.md` продукта — только minimal agent entry point replicated repo, а не копию `AGENTS.md` самого `BytePress`; при этом product `AGENTS.md` обязан требовать наблюдаемый стартовый отчёт первого ответа с режимом запуска, областью, статусом ветки, действием с веткой/стартовым маршрутом, состоянием планирования, доменами-владельцами первого чтения и первым конкретным шагом;
- product `AGENTS.md` обязан требовать короткий стартовый отчёт блоком с приветствием, текущей фазой, рабочим потоком, гейтом, режимом запуска, областью, статусом ветки, действием с веткой/стартовым маршрутом, состоянием планирования, доменами-владельцами первого чтения и первым конкретным шагом;
- product `AGENTS.md` обязан направлять агента в generated `Pipeline/Workflows.md` как владельца рабочего процесса и не подменять Pipeline;
- product `AGENTS.md` обязан явно удерживать гейт текущей истины: пока `Docs/Discovery/Interview.md` находится в состоянии `Статус_текущей_истины: Не_подтверждена`, первое записываемое действие допускается только после открытия рабочей ветки с типом `chore/`, `feature/`, `fix/` или `docs/`, а discovery/planning/log updates не являются исключением из гейта рабочей ветки;
- `Docs/Discovery/*` продукта — только minimal current-truth route, а не полный discovery-program;
- `Docs/User/*` продукта — только minimal human-facing contour, а не полный manual;
- `Docs/Product/*` — только стартовый first-version content skeleton;
- `Docs/Technical/*` продукта — только minimal startup subset, а не полный system contract map;
- `Docs/Terms/*` продукта — только `README.md` и `Base_Terms.md` со стартовым пакетом терминов, а не весь term-layer `BytePress`;
- `Plans/*` — только начальный stage/task/pass baseline, а не готовый предметный backlog; после подтверждения текущей истины developed product repo может закрыть `PLAN-000001` и вести следующий active или completed plan без нарушения bootstrap-contract;
- `Logs/*` — только empty or near-empty fact containers;
- `Pipeline/*` — только lightweight local process contour;
- `Tools/*` — только local service layer продукта;
- `Templates/*` и `Schemas/*` — только bounded subset для materialized/checkable artifacts;
- `scripts/*` — только transition wrappers к `Tools/*`.

## Что bootstrap сознательно не обязан делать
Bootstrap не обязан:
- копировать в product repo полный доменный состав самого `BytePress`;
- materialize domains, не выбранные product profile;
- создавать retired domains внутри product repo;
- materialize `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Docs/Technical/Platform_Contracts.md` или другие advanced technical contracts продукта;
- создавать предметно завершённые product requirements, delivery model или terminology base;
- переносить в generated repo полный словарь `BytePress` вместо стартового пакета терминов;
- открывать несколько roadmap stages, backlog items или plans;
- автоматически генерировать `product-code`, brand inheritance beyond allowed fields или скрытые external integrations;
- превращать product repo в копию operational/governance contour самого `BytePress`.

Lightweight `Pipeline/*`, bounded `Templates/*`, bounded `Schemas/*` и local `Tools/*` являются allowed product packages текущего переходного bootstrap.

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
- первый предметный product pass начинается только после подтверждённой текущей истины, а не сразу после bootstrap;
- дальнейшее предметное наполнение выполнит следующий pass, а не сам bootstrap.

Целевой profile bootstrap дополнительно предполагает, что выбранный product profile явно задаёт package set и версию package contract.

## Failed first-start reset/cleanup route
Bootstrap outcome обязан иметь канонический cleanup route для failed early product-start:
1. generated repo удаляет local tool reports через `scripts/reset-product-start.sh`;
2. script явно показывает, есть ли tracked drift вне разрешённого раннего contour `Docs/Discovery/*`, `Plans/*`, `Logs/*`;
3. если out-of-gate drift подтверждён, canonical reset route — fresh bootstrap в новый target, а не salvage текущего baseline.

## Допустимые и недопустимые упрощения
### Допустимые упрощения
- создавать product docs как короткие стартовые заготовки;
- ограничивать technical layer продукта минимальным subset;
- ограничивать planning layer одной стартовой stage/task/pass цепочкой;
- materialize product repo с minimal human/agent entry contour вместо полного governance copy;
- materialize стартовые заготовки для `Docs/Product/*` и `Docs/Technical/*` при условии, что hard first product-start gate не разрешает трактовать их как approval для немедленной реализации;
- materialize product repo с local smoke route вместо реальных внешних connectors;
- держать `Tools/.reports/*` вне bootstrap baseline commit и materialize его только при фактическом smoke run;
- ограничивать brand inheritance полями `Брендовый_профиль` и `Язык_взаимодействия`;
- создавать logs как пустые или почти пустые singleton containers.
- держать generated `scripts/*` только как transition wrappers к product-local `Tools/*`.

### Недопустимые упрощения и пропуски
- не создавать один из обязательных singleton artifacts минимального outcome;
- не создавать minimal `Docs/Discovery/*`, если replicated repo заявлен как first-usable current-truth contour;
- создавать generated product `AGENTS.md` без явного observable startup-handshake contract первого ответа;
- создавать generated repo без hard first product-start gate, который держит initial pass только в аналитическом контуре до ответов пользователя;
- создавать bootstrap interview с 1–3 общими вопросами вместо исполнимого first-pass current-truth minimum из 8–10 вопросов;
- использовать bootstrap-заготовки как скрытое разрешение на изменение `Docs/Product/*`, `Docs/Technical/*`, `Tools/*`, `Pipeline/*` или предметного кода до ответов пользователя;
- не создавать `AGENTS.md` или обязательный `Docs/User/*` contour replicated repo;
- не создавать `Tools/product_check.py`, если bootstrap заявляет self-contained product tools contour;
- не создавать `Tools/product_bootstrap_smoke.py`, если bootstrap заявляет local smoke route;
- не выпускать детерминированный smoke report, если bootstrap заявляет передачу доказательства в проверочный контур;
- materialize `Tools/.reports/*` уже в baseline generated repo без фактического smoke run или без явного hygiene-canon;
- создавать initial plan без внутреннего `ID: PLAN-000001`;
- оставлять initial stage/task/pass в пассивном или двусмысленном состоянии, если репозиторий заявлен как first-usable;
- silently подставлять отсутствующий `brand profile` или auto-generate `product-code`;
- считать bootstrap завершённым, если product repo не проходит базовый structural check или если human/agent entry contour не materialized;
- переносить в bootstrap contract обязанности проверки результата или последующих предметных passes.
- после внедрения profile bootstrap оставлять created product repo зависимым от `BYTEPRESS_ROOT` для обычной структурной проверки.

## Связь с проверкой результата
`Product_Bootstrap_Contract.md` задаёт expected bootstrap obligations.

`Product_Bootstrap_Validation.md`:
- фиксирует scope проверки и acceptance criteria bootstrap-result;
- разделяет automatic и procedural checks вокруг bootstrap behavior;
- подтверждает sync между contract и реализованным bootstrap behavior;
- не заменяет сам contract и не задаёт новые bootstrap obligations.

Если документ проверки и `bp_bootstrap.py` расходятся, каноническое исправление должно сначала синхронизировать contract или bootstrap behavior, а не подменять contract одним результатом проверки.

## Отношение bootstrap-contract к соседним контурам
### К `Plans/*`
Bootstrap обязан materialize только initial planning contour продукта. Дальнейший planning-state создаётся уже внутри product repo и не принадлежит bootstrap contract `BytePress`.

### К profile package matrix
`Product_Bootstrap_Domain_Matrix.md` задаёт package composition. Текущий `bp_bootstrap.py` реализует `Core` subset переходной модели; дальнейшие profile packages требуют отдельных passes.

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

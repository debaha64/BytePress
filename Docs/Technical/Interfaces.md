# Interfaces

## Назначение
`Docs/Technical/Interfaces.md` является каноническим interface-contract текущего `BytePress`.

Этот document отвечает на вопросы:
- какие внутренние интерфейсы связывают домены системы;
- какие внешние интерфейсы выводят систему во внешнюю среду;
- какие точки стыка считаются допустимыми;
- какие интерфейсы считаются стабильными, служебными и производными;
- какие прямые обходы границ и смешения ответственности недопустимы.

## Место документа в required core
`Interfaces.md` входит в required core `Docs/Technical/*`.

Его роль:
- фиксировать точки взаимодействия между доменами и слоями;
- удерживать contract интерфейсов поверх уже определённых архитектурных границ и ownership состояния;
- не дублировать `Docs/Technical/README.md` как карту technical-layer;
- не дублировать `Docs/Technical/Architecture.md` как карту доменов и слоёв;
- не дублировать `Docs/Technical/Model.md` как модель сущностей и ownership;
- не дублировать `Docs/Technical/Artifact_Lifecycle.md` как lifecycle и sync-loop;
- не дублировать `Pipeline/*` как process-canon.

## Чем interface-contract отличается от соседних документов
- `README.md` отвечает за границы technical-layer и required core.
- `Architecture.md` отвечает за domain map, layer map и архитектурные запреты.
- `Model.md` отвечает за сущности, ownership состояния и основные связи.
- `Artifact_Lifecycle.md` отвечает за источники истины, обязательные синхронизации и lifecycle-переходы.
- `Interfaces.md` отвечает за допустимые способы взаимодействия между доменами и за классификацию самих интерфейсов.
- `Pipeline/*` отвечает за фазы, переходы, gates, входы и выходы process-layer.

## Классы интерфейсов
### Стабильные интерфейсы
Стабильные интерфейсы описывают канонические точки стыка active system-contract, которые не должны меняться ситуативно от pass к pass.

К ним относятся:
- `Plans/Roadmap.md`, `Plans/Backlog.md` и active `Plan` как planning-interface между stage, task и pass;
- `Pipeline/*` как process interface фаз, переходов, gates и process IO;
- `Docs/Technical/*` как interface knowledge-layer к техническим контрактам системы;
- `Logs/*` как fact interface для подтверждённых результатов;
- canonical internal `ID` links между сущностями доменов.

### Служебные интерфейсы
Служебные интерфейсы поддерживают работу системы, но не являются основным смысловым contract entrypoint.

К ним относятся:
- `Tools/*` как service interface materialization и checks;
- local product `Tools/*` как независимый service interface созданного продукта;
- `Templates/*` и `Schemas/*` как support interfaces формы и валидации только для включённых и проверяемых артефактов;
- `Profiles/*` и `Rules/*` как profile/package и mandatory-rule interfaces.

### Производные интерфейсы
Производные интерфейсы зависят от stable или service interfaces и не должны объявляться отдельным source of truth.

К ним относятся:
- README-карты доменов, которые агрегируют ссылки на canonical files;
- technical views вроде `Docs/Technical/Pipeline.md`;
- ссылочные карты и traceability sections внутри планов и журналов;
- derived path references, которые служат навигацией поверх canonical `ID` и domain contracts.

## Внутренние интерфейсы между доменами
### `Docs/Discovery/*` -> `Plans/*`
Аналитическая текущая истина передаётся в planning-contour через требования к этапам и задачам.

Допустимый contract:
- discovery формирует основание для `Roadmap`, `Backlog` и active `Plan`;
- planning artifacts ссылаются на discovery truth как на основание изменений.

Недопустимо:
- хранить текущий stage/task/pass прямо в discovery-layer;
- заменять planning decisions содержимым discovery-document без синхронизации `Plans/*`.

### `Docs/Technical/*` -> `Plans/*`
Technical-layer предоставляет planning-contour технические contracts, ограничения границ и точки проверки.

Допустимый contract:
- active `Plan` и backlog-задачи могут ссылаться на technical contracts как на scope и критерии проверки;
- `Roadmap` может ссылаться на technical horizon уровня этапа.

Недопустимо:
- переносить текущий backlog-state или pass-state в technical-layer;
- использовать `Docs/Technical/*` как substitute для active `Plan`.

### `Pipeline/*` -> `Plans/*`
Process-layer задаёт planning-layer process frame, но не владеет planning-state.

Допустимый contract:
- `Pipeline/*` определяет, какие planning artifacts появляются на фазах `Roadmap`, `Backlog` и `Plan`;
- `Plans/*` использует process-canon как ограничение порядка движения работы.

Недопустимо:
- хранить stage/task/pass внутри `Pipeline/*`;
- трактовать `Pipeline/*` как substitute для `Roadmap`, `Backlog` или active `Plan`.

### `Plans/*` -> `Tools/*` -> `Logs/*`
Утверждённый active `Plan` открывает проверяемое исполнение через deterministic tools, а подтверждённый результат фиксируется в fact-layer.

Допустимый contract:
- tools опираются на текущий `Plan` и active contracts;
- временные tool outputs хранятся только в ignored paths;
- проверенный результат pass фиксируется в `Logs/*`.

Недопустимо:
- создавать в tools новый канонический план;
- считать tool output самодостаточным фактом без log closure;
- хранить runtime-state как отдельный source-of-truth domain без реального execution mechanism.

### `Plans/*` -> `Logs/*`
Planning-contour связывается с fact-layer через фиксацию результата, а не через передачу владения состоянием.

Допустимый contract:
- `Logs/ChangeLog.md` и `Logs/QualityLog.md` фиксируют результат pass и проверки;
- журналы могут ссылаться на `BACK-*`, `PLAN-*` и связанные contracts.

Недопустимо:
- использовать `Logs/*` как место хранения будущего scope;
- подменять закрытие backlog-задачи одной записью в логе без синхронизации `Plans/*`.

### `Profiles/*` -> package matrix, `Rules/*`, `Templates/*`, `Schemas/*`
Профиль задаёт package set продуктового каркаса через governance and package interfaces.

Допустимый contract:
- profile references указывают выбранные packages и обязательные `RULE-*`;
- profile включает `Templates/*` только для materialized artifacts;
- profile включает `Schemas/*` только для artifacts, которые local product `Tools/*` проверяет.

Недопустимо:
- использовать profile как substitute для rule;
- включать placeholder domains `Adapters`, `Memory`, `MCP`, `Runtime`, `Roles`.

### `Schemas/*` + `Templates/*` -> канонические артефакты
Supporting contract layer поставляет form/validation interfaces для нормируемых документов.

Допустимый contract:
- schema задаёт структуру, template задаёт читаемую форму, а канонический доменный document остаётся source of truth;
- tools могут использовать schema/template pair для checks и materialization.

Недопустимо:
- считать template каноническим документом вместо доменного артефакта;
- считать schema owner'ом содержательного состояния документа.

### `Tools/*` -> active domains
Инструменты подключаются к доменам через service interfaces проверки, bootstrap и materialization.

Допустимый contract:
- `Tools/*` читает canonical contracts и проверяет их соблюдение;
- tooling updates следуют за документным contract, а не объявляют его первично.
- product-local `Tools/*` после bootstrap проверяет продукт без `BYTEPRESS_ROOT`.

Недопустимо:
- задавать source of truth только скриптом без синхронизации документов;
- обходить domain contracts через ad hoc tool behavior.

## Внешние интерфейсы системы
### Файловая рабочая среда
Основной внешний интерфейс `BytePress` — файловое дерево репозитория.

Стабильный contract:
- домены взаимодействуют через файлы, каталоги, path-contracts и canonical IDs;
- системное состояние читается из репозитория, а не из отдельного сервиса.

### Git и PR contour
Внешний delivery interface системы проходит через task-ветки, push и PR в `develop`.

Стабильный contract:
- work moves through git branch and PR workflow;
- merge завершает pass на уровне репозитория, но не меняет ownership доменных source-of-truth.

### Product-local tools contour
Целевой generated product repo получает local `Tools/*` вместо зависимости от `BYTEPRESS_ROOT` и product `scripts/*`.

Служебный contract:
- `BytePress` materialize локальные product tools из profile package contract;
- product tools проверяют только те packages, которые есть в продукте;
- product tools пишут временные отчёты только в ignored tool-output path;
- после bootstrap продукт не требует `BytePress` для обычного `dev-test` или structural check.

Недопустимо:
- оставлять созданный продукт runtime-зависимым от `BytePress` tooling;
- materialize retired domains `Adapters/*`, `MCP/*`, `Memory/*`, `Runtime/*` или `Roles/*` как placeholder integration contour;
- вызывать внешние connectors без отдельного mechanism contract.

### Product contour
Продукт и его deliverables остаются внешними по отношению к самой файловой фабрике `BytePress`.

Производный contract:
- `BytePress` управляет knowledge, process, planning и contracts;
- поставляемый продукт не становится частью технического ядра фабрики автоматически.

## Допустимые точки стыка
- knowledge domains могут входить в planning-contour через canonical documents и explicit references;
- technical contracts могут ограничивать planning, tooling и quality checks, не забирая их ownership;
- process-layer может задавать порядок движения planning artifacts, не владея их статусом;
- runtime может брать вход из active `Plan` и отдавать подтверждённый результат в `Logs/*`;
- logs могут ссылаться на active contracts и closed passes как на источник контекста факта;
- governance/supporting domains могут настраивать и проверять active layer, не подменяя source-of-truth сущности.

## Недопустимые прямые обходы и смешения
- прямой обход `Plans/*` через ignored tool-output paths для изменения stage/task/pass state;
- прямой обход `Logs/*` как substitute для закрытия pass без sync в backlog и plan;
- перенос process-canon из `Pipeline/*` в `Docs/Technical/*`;
- перенос ownership сущностей из `Model.md` в `Interfaces.md`;
- перенос lifecycle-checklist и source-of-truth matrix из `Artifact_Lifecycle.md` в `Interfaces.md`;
- использование `Tools/*` как единственного места, где живёт contract;
- чтение archive artifacts как current interface source вместо active layer;
- прямая подмена canonical `ID` свободным текстом там, где у сущности уже есть утверждённый ID.

## Отношение interface-layer к соседним слоям
### К `Plans/*`
`Interfaces.md` фиксирует, как planning-contour стыкуется с соседними доменами, но не владеет stage/task/pass state.

### К ignored tool-output paths
`Interfaces.md` фиксирует runtime как service interface активного pass, а не как source-of-truth слой.

### К `Logs/*`
`Interfaces.md` фиксирует logs как fact interface системы, а не как planning или technical substitute.

### К `Pipeline/*`
`Interfaces.md` фиксирует `Pipeline/*` как отдельный process supplier и consumer сигналов/артефактов, но не повторяет phase canon, gates или IO matrix как primary source.

## Граница документа
`Interfaces.md` не является:
- картой technical-layer как каталога;
- картой доменов и слоёв системы;
- моделью сущностей и ownership состояния;
- lifecycle-checklist или source-of-truth matrix;
- process-canon document.

Он остаётся каноническим contract интерфейсов текущего `BytePress`.

## Связи
- `RULE-000003`
- `RULE-000007`
- `RULE-000009`

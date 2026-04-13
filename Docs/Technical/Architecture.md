# Architecture

## Назначение
`Docs/Technical/Architecture.md` является канонической архитектурной картой текущего `BytePress`.

Этот document отвечает не за карту technical-layer как каталога, а за карту самой системы:
- какие домены в ней существуют;
- в какие слои они собираются;
- за что отвечает каждый слой;
- какие связи между слоями допустимы;
- какие подмены и пересечения недопустимы.

## Место документа в required core
`Architecture.md` входит в required core `Docs/Technical/*`.

Его роль:
- зафиксировать архитектурную форму системы поверх domain map;
- удерживать границы между knowledge-layer, process-layer, planning-layer, runtime-layer и fact-layer;
- не дублировать `Docs/Technical/README.md`, `Docs/Technical/Pipeline.md` и `Pipeline/*`, а связывать их в одну системную карту.

## Архитектурный принцип BytePress
`BytePress` построен как файловая система доменов, где каждый активный домен хранит только свой тип состояния:
- знание хранится в `Docs/*`;
- технические системные контракты хранятся в `Docs/Technical/*`;
- движение работы моделируется в `Pipeline/*`;
- утверждённое намерение и статус этапа хранятся в `Plans/*`;
- временный рабочий контекст живёт в `Runtime/*`;
- подтверждённые факты хранятся в `Logs/*`;
- ограничения и нормативы вынесены в `Rules/*` и `Standards/*`;
- формальные и шаблонные supporting contracts вынесены в `Schemas/*` и `Templates/*`.

Архитектура считается корректной только пока эти типы состояния не начинают подменять друг друга.

## Карта доменов
### Knowledge domains
- `Docs/Discovery/` — current-truth аналитический слой.
- `Docs/Product/` — продуктовое знание и описание продукта.
- `Docs/Terms/` — терминологический слой.
- `Docs/User/` — пользовательский слой.

### Technical knowledge domain
- `Docs/Technical/` — техническая карта системы и устойчивые системные контракты.

### Process and planning domains
- `Pipeline/` — process-domain модели движения работы.
- `Plans/` — planning/governance domain со stage, task и pass.

### Execution and fact domains
- `Runtime/` — временный контекст исполнения.
- `Logs/` — журналы фактов, проверок и решений.

### Governance domains
- `Profiles/` — режимы системы и состав активного рабочего контура.
- `Roles/` — поведенческие точки сборки.
- `Rules/` — обязательные запреты и ограничения.
- `Standards/` — нормативы качества и представления.

### Supporting contract domains
- `Schemas/` — формальные контракты данных.
- `Templates/` — шаблоны повторяющихся артефактов.
- `Tools/` — детерминированные инструменты materialization и checks.
- `Skills/` — процедурные способности и операционные инструкции.

### Extension domains
- `Adapters/` — каркас подключения моделей и движков.
- `Memory/` — каркас будущей долговременной памяти.
- `MCP/` — каркас подключений и интеграционной политики.

## Карта слоёв
### Knowledge layer
- `Docs/Discovery/`
- `Docs/Product/`
- `Docs/Terms/`
- `Docs/User/`

Роль слоя: хранить долговременное предметное знание, описания продукта, терминов и пользовательского слоя.

### Technical layer
- `Docs/Technical/`

Роль слоя: описывать устройство системы `BytePress`, доменные границы, интерфейсы, системные инварианты и архитектурные связи между соседними слоями.

### Process layer
- `Pipeline/`

Роль слоя: задавать фазы, переходы, gates, входы и выходы движения работы без хранения фактического статуса исполнения.

### Planning layer
- `Plans/`

Роль слоя: хранить утверждённые stage, task и pass, а также archive planning-history.

### Execution layer
- `Runtime/`

Роль слоя: держать только временный рабочий контекст между утверждённым `Plan` и фиксацией результата.

### Fact layer
- `Logs/`

Роль слоя: фиксировать подтверждённые факты изменений, качества, решений, выпуска и поддержки.

### Governance layer
- `Profiles/`
- `Roles/`
- `Rules/`
- `Standards/`

Роль слоя: ограничивать и направлять поведение системы, но не подменять знание, планирование или журналы фактов.

### Supporting contract layer
- `Schemas/`
- `Templates/`
- `Tools/`
- `Skills/`

Роль слоя: материализовать, проверять и поддерживать contracts активных доменов.

### Extension layer
- `Adapters/`
- `Memory/`
- `MCP/`

Роль слоя: удерживать controlled integration contour и границы будущих расширений, не подменяя active core системы в `0.2.0`.

## Границы ответственности по ключевым доменам
- `Docs/Technical/*` отвечает за архитектурную и контрактную карту системы, но не за process-canon, planning-state, runtime-state или факт выполнения.
- `Pipeline/*` отвечает за process-canon, но не владеет stage/task/pass и не хранит фактическое состояние конкретной работы.
- `Plans/*` отвечает за утверждённое намерение и статусы planning-contour, но не заменяет knowledge-layer и не превращается в журнал фактов.
- `Runtime/*` отвечает только за временный контекст исполнения и не становится источником истины.
- `Logs/*` отвечают только за факты и результаты проверок, а не за планирование будущей работы.

## Допустимые направления связей
- `Docs/Technical/*` может ссылаться на `Pipeline/*`, `Plans/*`, `Runtime/*`, `Logs/*`, чтобы описывать архитектурные границы между ними.
- `Pipeline/*` может определять, какие домены участвуют в фазах и переходах, но не забирает у них владение состоянием.
- `Plans/*` может ссылаться на `Docs/Technical/*`, `Logs/*`, `Rules/*` и `Standards/*` как на contracts и факты, нужные для текущего pass.
- `Runtime/*` может опираться на active `Plan`, но после завершения pass не становится архивом знания или фактов.
- `Logs/*` могут ссылаться на `Plans/*` и `Docs/Technical/*`, чтобы фиксировать факт изменения и проверки конкретного контракта.

Допустимая общая схема направления такова:
`Docs/*` и `Docs/Technical/*` задают знание и contracts -> `Pipeline/*` задаёт процессную рамку -> `Plans/*` задаёт утверждённый pass -> `Runtime/*` даёт временный контекст исполнения -> `Logs/*` фиксируют факт результата.

## Недопустимые подмены и пересечения
- `Docs/Technical/*` не подменяет `Pipeline/*` как process-canon.
- `Docs/Technical/*` не подменяет `Plans/*` как active planning-state.
- `Docs/Technical/*` не подменяет `Runtime/*` как место текущего исполнения.
- `Docs/Technical/*` не подменяет `Logs/*` как слой подтверждённых фактов.
- `Pipeline/*` не подменяет `Plans/*` как источник утверждённого stage/task/pass.
- `Pipeline/*` не подменяет `Docs/Technical/*` как архитектурную карту системы.
- `Plans/*` не подменяет `Logs/*` и не хранит факт вместо журнала.
- `Runtime/*` не подменяет `Plans/*`, `Docs/*` и `Logs/*`.
- `Rules/*` не подменяют `Standards/*`, а `Standards/*` не подменяют `Rules/*`.
- `Schemas/*` не подменяют `Templates/*`, а `Templates/*` не подменяют канонические документы доменов.
- `Tools/*` не подменяют source-of-truth документы, а materialize и проверяют их contracts.

## Отношение technical-layer к process, planning, runtime и facts
### К `Pipeline/*`
`Pipeline/*` — отдельный process-layer. `Architecture.md` фиксирует только его архитектурное место в системе и границы относительно соседних доменов.

`Architecture.md` не должен повторять:
- phase canon;
- gates;
- phase inputs/outputs;
- process matrix переходов.

### К `Plans/*`
`Plans/*` — отдельный planning/governance contour. `Architecture.md` фиксирует, что именно там хранятся stage, task и pass, а не переносит их в technical-layer.

### К `Runtime/*`
`Runtime/*` — execution-layer. `Architecture.md` фиксирует его как временный контекст и не даёт читать runtime как source of truth.

### К `Logs/*`
`Logs/*` — fact-layer. `Architecture.md` фиксирует, что архитектурные изменения подтверждаются журналами, но не делает сами журналы частью technical-layer.

## Отношение к required core technical-layer
- `README.md` задаёт карту самого technical-layer и required core.
- `Architecture.md` задаёт архитектурную карту системы поверх этих границ.
- `Model.md` раскрывает сущности и их отношения внутри уже определённой архитектурной формы.
- `Interfaces.md` раскрывает точки взаимодействия между доменами, уже разведёнными здесь.
- `System_Invariants.md` фиксирует, какие нарушения этой архитектуры недопустимы.
- `Artifact_Lifecycle.md` фиксирует, как изменения в этих слоях должны синхронизироваться.

## Граница документа
`Architecture.md` не является:
- README-картой каталога `Docs/Technical/*`;
- process-canon document для `Pipeline/*`;
- lifecycle checklist document;
- реестром текущих backlog-задач, pass или log entries.

Он остаётся канонической архитектурной картой текущей системы `BytePress`.

## Связи
- `ADR-000001`
- `ADR-000002`
- `ADR-000005`
- `RULE-000003`
- `RULE-000007`

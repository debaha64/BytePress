# Artifact_Lifecycle

## Назначение
`Docs/Technical/Artifact_Lifecycle.md` является каноническим lifecycle-contract текущего `BytePress`.

Этот document отвечает на вопросы:
- какие группы артефактов система считает ключевыми;
- где для каждой группы находится источник истины;
- какие синхронизации обязательны после изменения;
- какие переходы между active, archive, runtime и log слоями допустимы;
- какой closure-loop обязателен перед завершением pass;
- какие lifecycle-пропуски и смешения ответственности недопустимы.

## Место документа в required core
`Artifact_Lifecycle.md` входит в required core `Docs/Technical/*`.

Его роль:
- фиксировать lifecycle артефактов и обязательный порядок их синхронизации;
- не дублировать `Docs/Technical/README.md` как карту technical-layer;
- не дублировать `Docs/Technical/Architecture.md` как карту доменов и слоёв;
- не дублировать `Docs/Technical/Model.md` как модель сущностей и ownership;
- не дублировать `Pipeline/*` как process-canon.

## Чем lifecycle-contract отличается от соседних документов
- `README.md` отвечает за границы technical-layer и required core.
- `Architecture.md` отвечает за domain map, layer map и архитектурные запреты.
- `Model.md` отвечает за сущности, ownership состояния и основные связи.
- `Artifact_Lifecycle.md` отвечает за источники истины, обязательные sync-loop, допустимые переходы между слоями и pass-close contour.
- `Pipeline/*` отвечает за фазы, переходы, gates, входы и выходы process-layer.

## Ключевые группы артефактов
### Analytical truth
- `Docs/Discovery/Interview.md`

Роль:
- хранить текущую аналитическую истину о системе и продукте.
- для bootstrap-created product repo early product-start contour удерживать unanswered discovery-state до ответа пользователя, а не заменять его догадками агента.

Источник истины:
- `Docs/Discovery/Interview.md`.

### Technical contracts
- `Docs/Technical/*`

Роль:
- хранить устойчивые технические contracts системы.

Источник истины:
- соответствующий active technical-document внутри `Docs/Technical/*`.

### Planning artifacts
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- active `Plans/PLAN-<NNNNNN>-<slug>.md`
- archive `Plans/Archive/PLAN-<NNNNNN>-<slug>.md`
- archive `Plans/Archive/Backlog/ROAD-<NNNNNN>.md`

Роль:
- хранить stage, task, pass и historical planning-history.

Источники истины:
- `Roadmap.md` для stage-state;
- `Backlog.md` для task-state текущего этапа;
- active `Plan` для текущего pass;
- archive planning-files для завершённой planning-history.

### Process contracts
- `Pipeline/*`

Роль:
- хранить process-canon фаз, переходов, gates, inputs и outputs.

Источник истины:
- соответствующий file внутри `Pipeline/*`, в зависимости от process-topic.

### Runtime context
- `Runtime/*`

Роль:
- держать только временный рабочий контекст во время активного pass.
- для generated product repo early product-start contour сюда же относится runtime-local artifact `Runtime/Integration_Smoke_Report.json`, если он выпускается integration smoke route.

Источник истины:
- runtime не является source-of-truth слоем; это временный execution context.
- `Runtime/Integration_Smoke_Report.json` не входит в bootstrap baseline commit по умолчанию и не становится canonical evidence сам по себе; если отдельный pass явно сохраняет этот artifact в Git, такое решение должно быть зафиксировано current `Plan` и итоговым отчётом.

### Fact records
- `Logs/ADRlog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `Logs/ReleaseLog.md`
- `Logs/SupportLog.md`

Роль:
- фиксировать подтверждённые факты решений, изменений, проверок, выпуска и поддержки.

Источник истины:
- соответствующий singleton log-file и его serial log entries.

### Supporting contracts
- `Rules/*`
- `Standards/*`
- `Schemas/*`
- `Templates/*`
- `Tools/*`

Роль:
- ограничивать, нормировать, описывать форму и проверять активные артефакты системы.

Источник истины:
- соответствующий active file своего домена.

## Карта источников истины
- current analytical truth живёт в `Docs/Discovery/Interview.md`;
- stage-state живёт в `Plans/Roadmap.md`;
- task-state текущего этапа живёт в `Plans/Backlog.md`;
- current pass-state живёт в active `Plans/PLAN-<NNNNNN>-<slug>.md`;
- process-canon живёт в `Pipeline/*`;
- runtime-state живёт только временно в `Runtime/*`;
- fact-state живёт в `Logs/*`;
- architecture, model, lifecycle, interfaces и invariants живут в `Docs/Technical/*`;
- form and validation contracts живут в `Templates/*`, `Schemas/*`, `Rules/*`, `Standards/*` и `Tools/*`.

Если один и тот же факт можно прочитать в двух местах, каноническим считается только тот домен, который владеет соответствующим типом состояния.

## Обязательные синхронизации
### При изменении current analytical truth
Если меняется `Docs/Discovery/Interview.md`, обязательно проверить:
- `Plans/Roadmap.md`;
- `Plans/Backlog.md`;
- active `Plans/*`;
- релевантные `Docs/Product/*`;
- `Logs/ChangeLog.md`;
- `Logs/QualityLog.md`;
- `Logs/ADRlog.md`, если изменение приводит к новому устойчивому архитектурному решению.

### При изменении technical contracts
Если меняется `Docs/Technical/*`, обязательно проверить:
- связанные README-карты и прямые references;
- `Tools/bp_lint.py`, только если меняется обязательный contract check;
- `Logs/ChangeLog.md`;
- `Logs/QualityLog.md`;
- `Logs/ADRlog.md`, если изменение является новым устойчивым архитектурным решением.

### При изменении planning artifacts
Если меняется `Plans/Roadmap.md`, обязательно проверить:
- `Plans/Backlog.md`;
- active `Plans/*`;
- `Docs/Discovery/Interview.md`, если roadmap меняется от обновления analytical truth.

Если меняется `Plans/Backlog.md`, обязательно проверить:
- active `Plans/*`;
- `Plans/Roadmap.md`, если меняется связь stage/task;
- `Logs/ChangeLog.md`, если задача закрыта или переразмечена фактом выполненного pass.

Если меняется active `Plan`, обязательно проверить:
- `Plans/Backlog.md`;
- `Logs/ChangeLog.md`;
- `Logs/QualityLog.md`;
- релевантные contracts и direct references, если scope pass реально их затронул.

### При изменении process contracts
Если меняется `Pipeline/*`, обязательно проверить:
- `Docs/Technical/Pipeline.md`;
- `Docs/Technical/Artifact_Lifecycle.md`, если меняется process-touchpoint sync-loop;
- `Plans/*`, если process-canon меняет требования к planning-contour;
- `Logs/*`, если изменение уже подтверждено как факт.

### При изменении supporting contracts
Если меняются `Templates/*`, `Schemas/*`, `Rules/*`, `Standards/*` или `Tools/*`, обязательно проверить:
- документы и журналы, которые реально materialize или проверяются этим contract;
- `Tools/bp_bootstrap.py`, если меняется generation contract;
- `Tools/bp_lint.py`, если меняется обязательный check;
- релевантные `Docs/Technical/*`, если изменился сам technical contract системы.

## Допустимые переходы между слоями
### Active -> Runtime
Допустимо:
- active `Plan` порождает временный runtime context во время исполнения.

Недопустимо:
- runtime становится каноническим планом;
- runtime хранит утверждённую planning-history.

### Active -> Logs
Допустимо:
- завершённый результат pass фиксируется в `Logs/*` как факт изменения и проверки;
- при release/support реально затронутые результаты фиксируются в соответствующих log-files.

Недопустимо:
- лог заменяет `Backlog` или active `Plan` как место будущего намерения;
- лог создаётся как substitute для незакрытого pass без planning-sync.

### Active -> Archive
Допустимо:
- завершённый current `Plan` переходит в `Plans/Archive/`;
- backlog history завершённого stage хранится в `Plans/Archive/Backlog/ROAD-<NNNNNN>.md`.

Недопустимо:
- active `Plan` архивируется до завершения pass;
- historical backlog остаётся в active `Backlog.md` после закрытия этапа.

### Runtime -> Logs
Допустимо:
- подтверждённый результат исполнения переносится из runtime-context в `Logs/*` как факт.
- runtime-local `Runtime/Integration_Smoke_Report.json` может использоваться как локальный carrier smoke verdict до его явной фиксации в pass report или `Logs/*`.

Недопустимо:
- runtime считается самодостаточным фактом без log fixation.
- baseline generated product repo коммитится с уже materialized `Runtime/Integration_Smoke_Report.json` без отдельного evidence-preservation решения.

### Archive -> Active
Допустимо:
- historical artifacts читаются как reference/history.

Недопустимо:
- archive files используются как current source of truth вместо active layer.

## Обязательное замыкание контура перед завершением pass
Перед закрытием pass обязательно подтвердить:
- финальный статус backlog-задачи;
- финальный статус active `Plan`;
- синхронность индекса `Backlog.md`;
- синхронность `Roadmap.md` по текущему stage и его backlog-links;
- наличие фактической записи в `ChangeLog`, если pass привёл к содержательному изменению;
- наличие фактической записи в `QualityLog` о выполненной проверке;
- наличие фактической записи в `ReleaseLog`, если pass подтверждает уже состоявшийся release event по tag/history;
- прямые ссылки и README-карты обновлены только там, где изменение реально создало рассогласование.

Если одно из этих замыканий пропущено, lifecycle pass считается незавершённым.

## Недопустимые пропуски и смешения
- менять канонический source-of-truth и не проверять связанные active artifacts;
- в generated product repo закрывать unanswered discovery gaps предположениями агента или переводить discovery-first contour в write-state до ответов пользователя;
- закрывать pass без фиксации результата проверки в `QualityLog`;
- записывать в `ReleaseLog` release candidate, прогноз или намерение вместо factual release event;
- считать runtime контур завершённым результатом без фиксации факта в `Logs/*`;
- переносить process-canon в `Docs/Technical/*` вместо `Pipeline/*`;
- переносить ownership planning-state из `Plans/*` в `Docs/Technical/*` или `Logs/*`;
- использовать archive-layer как current source of truth;
- менять tooling contract без синхронизации технических документов, на которые он опирается.

## Отношение lifecycle-layer к planning, runtime, facts и process
### К `Plans/*`
`Plans/*` задаёт current stage/task/pass. `Artifact_Lifecycle.md` не владеет этими сущностями, а фиксирует, как они должны синхронизироваться с соседними слоями.

### К `Runtime/*`
`Runtime/*` остаётся только временным execution context. `Artifact_Lifecycle.md` фиксирует допустимый переход runtime -> logs, но не делает runtime источником истины.

### К `Logs/*`
`Logs/*` остаются fact-layer. `Artifact_Lifecycle.md` фиксирует, когда факт обязан быть записан, но не подменяет сами журналы.

### К `Pipeline/*`
`Pipeline/*` остаётся process-canon. `Artifact_Lifecycle.md` фиксирует только те точки, где процессный слой требует обязательной синхронизации соседних артефактов, но не повторяет phase canon, gates или inputs/outputs как primary source.

## Граница документа
`Artifact_Lifecycle.md` не является:
- картой technical-layer как каталога;
- архитектурной картой доменов и слоёв;
- моделью сущностей и ownership состояния;
- process-canon document;
- backlog, roadmap или plan registry.

Он остаётся каноническим lifecycle-contract текущего `BytePress`.

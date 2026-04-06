# Technical

`Docs/Technical/` содержит долговременное техническое знание о самой системе `BytePress`.

## Назначение слоя
`Docs/Technical/*` фиксирует устройство системы, технические границы доменов и устойчивые системные контракты.

Technical-layer нужен для ответа на вопросы:
- как устроен `BytePress` как система доменов;
- какие технические инварианты и интерфейсы у системы есть;
- какие домены участвуют в lifecycle и где проходит техническая граница между ними;
- какие bootstrap и platform contracts поддерживают рабочий периметр системы.

## Что входит в слой
В `Docs/Technical/*` входят только документы о технической системе `BytePress`:
- архитектура доменов и их границ;
- модель сущностей и их технических отношений;
- системные инварианты;
- внутренние и внешние интерфейсы;
- platform/bootstrap contracts;
- technical view на lifecycle и на участие `Pipeline/` в системе.

## Что не входит в слой
`Docs/Technical/*` не подменяет соседние домены:
- `Pipeline/*` не переносится сюда как рабочая модель движения работы по фазам;
- `Plans/*` не описываются здесь как текущий planning-state или как место хранения статусов;
- `Runtime/*` не описывается здесь как источник текущего исполнения или рабочего состояния;
- `Logs/*` не превращаются здесь в слой технических фактов по умолчанию;
- `Rules/*` и `Standards/*` не дублируются сюда как нормативный слой;
- `Docs/Product/*`, `Docs/Discovery/*` и `Docs/User/*` не становятся частью technical-layer только потому, что пересекаются с системой.

## Отношение к соседним доменам
- `Pipeline/*` — отдельный домен модели движения работы: он хранит фазы, переходы, входы и выходы изменения. `Docs/Technical/Pipeline.md` существует только как technical view на роль pipeline в системе и не подменяет `Pipeline/README.md`, `Pipeline/Phases.md`, `Pipeline/Artifacts.md` и другие pipeline-documents.
- `Plans/*` — отдельный planning/governance contour: `Roadmap`, `Backlog` и текущий `Plan` живут там и не переносятся в technical-layer.
- `Runtime/*` — временный рабочий контекст исполнения; technical-layer может фиксировать его границы, но не хранит оперативное состояние.
- `Logs/*` — слой фактов; technical-layer может задавать, когда их нужно синхронизировать, но не подменяет журналы.

## Минимальный required состав
Минимальное required ядро technical-layer в текущем `BytePress`:
- `README.md` — канонический entrypoint, границы и карта technical-layer;
- `Architecture.md` — карта доменов, архитектурные роли и запреты подмены;
- `Model.md` — техническая модель сущностей и их отношений;
- `Interfaces.md` — карта интерфейсов системы;
- `System_Invariants.md` — системные инварианты, нарушение которых недопустимо;
- `Artifact_Lifecycle.md` — technical contract источников истины и обязательной sync-проверки.

## Карта системных контрактов слоя
### Обязательные системные контракты
- `README.md`
  Роль: канонический entrypoint technical-layer и карта его границ.
- `Architecture.md`
  Роль: фиксирует состав доменов, слои системы и запреты подмены.
- `Model.md`
  Роль: описывает техническую модель сущностей и их отношений.
- `Interfaces.md`
  Роль: фиксирует внутренние и внешние интерфейсы доменов.
- `System_Invariants.md`
  Роль: задаёт недопустимые нарушения системного контракта.
- `Artifact_Lifecycle.md`
  Роль: фиксирует источники истины, обязательную sync-проверку и lifecycle технических артефактов.

Обязательное ядро нужно для сохранения технической целостности системы. Если один из этих документов пропадает или перестаёт быть согласованным, `Docs/Technical/*` перестаёт удерживать минимальный contract-map `BytePress`.

### Вспомогательные technical-documents
- `Pipeline.md`
  Роль: supporting technical view на участие `Pipeline/` в системе; не является каноническим phase registry и не заменяет `Pipeline/*`.
- `Platform_Contracts.md`
  Роль: контекстный contract среды выполнения и рабочего периметра.
- `Product_Bootstrap_Contract.md`
  Роль: специализированный technical contract минимального product bootstrap.
- `Product_Bootstrap_Validation.md`
  Роль: специализированная фиксация результата проверки bootstrap-контракта.

Вспомогательные документы не образуют required ядро сами по себе. Они уточняют специализированные части системы и могут меняться точечно, пока не ломают contracts обязательного ядра.

## Почему текущие документы находятся именно здесь
- `Architecture.md`, `Model.md`, `Interfaces.md` и `System_Invariants.md` находятся в `Docs/Technical/*`, потому что описывают устройство системы, а не процесс выполнения работы.
- `Artifact_Lifecycle.md` находится в `Docs/Technical/*`, потому что закрепляет технический contract источников истины и обязательной синхронизации артефактов, а не текущее состояние backlog или runtime.
- `Pipeline.md` находится в `Docs/Technical/*` только как supporting technical view на process-domain: он объясняет, как `Pipeline/*` участвует в технической системе, но не владеет самим process-canon.
- `Platform_Contracts.md`, `Product_Bootstrap_Contract.md` и `Product_Bootstrap_Validation.md` находятся здесь, потому что описывают технический рабочий периметр и его проверяемые контракты, а не пользовательский, плановый или журнальный слой.

## Границы
- этот каталог не хранит оперативное состояние исполнения;
- этот каталог не дублирует правила, стандарты, планы и журналы;
- этот каталог описывает устройство системы, участие доменов в lifecycle и технические contracts, а не ход конкретной задачи.

## Допустимые и недопустимые пересечения с Pipeline
Допустимые пересечения:
- technical-layer может фиксировать техническую роль `Pipeline/` в системе;
- technical-layer может ссылаться на `Pipeline/*` как на process-domain;
- technical-layer может указывать, какие lifecycle и interface touchpoints связывают `Pipeline/*` с `Plans/*`, `Runtime/*`, `Logs/*` и knowledge-domains.

Недопустимые пересечения:
- `Docs/Technical/*` не становится основным местом хранения phase canon;
- `Docs/Technical/*` не заменяет `Pipeline/Phases.md`, `Pipeline/Artifacts.md`, `Pipeline/Inputs_Outputs.md`, `Pipeline/Phase_Gates.md`;
- `Docs/Technical/*` не фиксирует gates, переходы и обязательные process-outputs как process-canon;
- `Docs/Technical/*` не описывает текущий planning-state, backlog-state или фактический статус движения работы.

## Короткая карта документов
- `Architecture.md` — домены, слои и архитектурные запреты.
- `Model.md` — сущности и отношения системы.
- `Interfaces.md` — интерфейсы и точки соприкосновения.
- `System_Invariants.md` — недопустимые нарушения системного контракта.
- `Artifact_Lifecycle.md` — порядок обязательной синхронизации и lifecycle технических артефактов.
- `Pipeline.md` — supporting technical view на роль `Pipeline/` в общей системе.
- `Platform_Contracts.md` — контракт среды выполнения и рабочего периметра.
- `Product_Bootstrap_Contract.md` — минимальный bootstrap contract продукта.
- `Product_Bootstrap_Validation.md` — зафиксированный результат проверки bootstrap-контракта.

## Связи
- конвейер как process-domain раскрыт в `../../Pipeline/`;
- planning/governance contour раскрыт в `../../Plans/`;
- порядок обязательной синхронизации артефактов раскрыт в `Artifact_Lifecycle.md`;
- аналитический current-truth слой раскрыт в `../Discovery/`;
- ограничения и запреты закреплены в `../../Rules/`;
- нормативы качества и оформления закреплены в `../../Standards/`;
- термины системы закреплены в `../Terms/`.

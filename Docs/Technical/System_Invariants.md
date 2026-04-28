# System_Invariants

## Назначение
`Docs/Technical/System_Invariants.md` является каноническим invariant-contract текущего `BytePress`.

Этот document отвечает на вопросы:
- какие свойства системы считаются обязательными и не должны нарушаться ни при каком pass;
- какие инварианты относятся к repository-as-source-of-truth;
- какие инварианты относятся к planning-contour и ownership состояния;
- какие инварианты относятся к active/archive separation;
- какие инварианты относятся к traceability и обязательным sync-loop;
- что именно считается нарушением и к чему оно приводит.

## Место документа в required core
`System_Invariants.md` входит в required core `Docs/Technical/*`.

Его роль:
- фиксировать ненарушаемые свойства текущего `BytePress`;
- связывать уже утверждённые contracts архитектуры, модели, интерфейсов и lifecycle на уровне integrity rules;
- не дублировать `Docs/Technical/README.md` как карту technical-layer;
- не дублировать `Docs/Technical/Architecture.md` как карту доменов и слоёв;
- не дублировать `Docs/Technical/Model.md` как модель сущностей и ownership;
- не дублировать `Docs/Technical/Artifact_Lifecycle.md` как lifecycle и sync-loop checklist;
- не дублировать `Docs/Technical/Interfaces.md` как карту touchpoints;
- не дублировать `Pipeline/*` как process-canon.

## Чем invariant-contract отличается от соседних документов
- `README.md` отвечает за границы technical-layer и required core.
- `Architecture.md` отвечает за domain map, layer map и архитектурные запреты подмены.
- `Model.md` отвечает за сущности, ownership состояния и основные связи.
- `Interfaces.md` отвечает за допустимые точки стыка и классы интерфейсов.
- `Artifact_Lifecycle.md` отвечает за источники истины, обязательные sync-loop и layer transitions.
- `System_Invariants.md` отвечает за те свойства системы, нарушение которых делает `BytePress` несогласованным даже если отдельные документы ещё существуют.
- `Pipeline/*` отвечает за process-canon, а не за перечень общесистемных integrity rules.

## Канонические системные инварианты
### INV-001 — Repository is the active source of truth
Свойство:
- текущее состояние `BytePress` читается из репозитория и его канонических active documents.

Поддерживающие контуры и документы:
- `Rules/Repository_As_Source_Of_Truth.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Artifact_Lifecycle.md`

Нарушением считается:
- вынесение активного состояния в внешний ad hoc контур;
- ситуация, где актуальный contract существует только в памяти исполнителя, в shell history или в tool output.

Последствие нарушения:
- система теряет проверяемость и воспроизводимость.

### INV-002 — Domain ownership is explicit and non-overlapping
Свойство:
- каждый активный домен хранит только свой тип состояния и не подменяет соседний домен.

Поддерживающие контуры и документы:
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Rules/Domain_Boundaries_Are_Explicit.md`

Нарушением считается:
- перенос planning-state в `Runtime/*` или `Logs/*`;
- перенос process-canon в `Docs/Technical/*`;
- перенос facts в `Plans/*` как substitute для журналов.

Последствие нарушения:
- ownership состояния перестаёт быть однозначным, а контуры начинают спорить друг с другом.

### INV-003 — Planning-contour remains canonical
Свойство:
- `Roadmap -> Backlog -> Plan` остаётся единственным каноническим planning-contour.

Поддерживающие контуры и документы:
- `Standards/Planning.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- active `Plans/PLAN-<NNNNNN>-<slug>.md`

Нарушением считается:
- создание pass без backlog-задачи;
- фиксация stage/task status вне `Plans/*`;
- дублирование planning-state в runtime, logs или technical-layer.

Последствие нарушения:
- стадия, задача и pass перестают согласованно описывать одну и ту же работу.

### INV-004 — Ownership state cannot move to runtime or logs
Свойство:
- legacy `Runtime/*` не хранит source of truth, а `Logs/*` хранят только подтверждённые факты. В целевой модели временные execution outputs принадлежат ignored tool-output paths, а не отдельному top-level domain.

Поддерживающие контуры и документы:
- `Docs/Technical/Model.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Rules/Runtime_Is_Temporary.md`
- `Rules/Logs_Record_Facts_Only.md`
- `Rules/Premature_Domains_Are_Removed.md`

Нарушением считается:
- чтение runtime как канонического плана;
- создание нового top-level runtime-domain в продукте без реального execution mechanism;
- хранение будущего scope в журнале;
- отсутствие переноса подтверждённого результата из runtime в logs, когда pass реально изменил систему.

Последствие нарушения:
- execution-layer и fact-layer перестают быть различимыми.

### INV-005 — Active and archive layers stay separated
Свойство:
- active artifacts остаются источником текущей истины, archive artifacts остаются history/reference layer.

Поддерживающие контуры и документы:
- `Plans/README.md`
- `Standards/Planning.md`
- `Docs/Technical/Artifact_Lifecycle.md`

Нарушением считается:
- использование archive `Plan` как current pass;
- хранение backlog history завершённых этапов в active `Backlog.md`;
- опора на archive files вместо active layer при изменении системы.

Последствие нарушения:
- исторический слой начинает подменять рабочую модель.

### INV-006 — Canonical IDs remain the reference contract
Свойство:
- если у сущности есть canonical `ID`, contract links должны опираться именно на него.

Поддерживающие контуры и документы:
- `Standards/Naming.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Terms/*`

Нарушением считается:
- подмена canonical `ID` свободным текстом в contract references;
- создание новых active artifacts вне утверждённой ID scheme своего домена.

Последствие нарушения:
- traceability и навигация по системе становятся хрупкими.

### INV-007 — Traceability must stay closed for completed passes
Свойство:
- завершённый pass должен оставлять согласованный traceability chain между task, plan, touched contracts и logs.

Поддерживающие контуры и документы:
- `Docs/Technical/Artifact_Lifecycle.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- active `Plan`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

Нарушением считается:
- закрытие backlog-задачи без закрытия `Plan`;
- изменение contract без нужной traceability в roadmap/backlog/plan;
- содержательный pass без проверки или без зафиксированного результата проверки.

Последствие нарушения:
- историю изменения нельзя надёжно проверить или восстановить.

### INV-008 — Required core technical-layer must stay complete
Свойство:
- required core `Docs/Technical/*` остаётся полным и согласованным.

Поддерживающие контуры и документы:
- `Docs/Technical/README.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Model.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Technical/System_Invariants.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Tools/bp_lint.py`

Нарушением считается:
- отсутствие одного из required core documents;
- ситуация, где required core document существует только как заготовка и не удерживает свой слой contract.

Последствие нарушения:
- technical-layer теряет минимальную системную карту и перестаёт быть достаточным для проверки целостности.

### INV-009 — Process-layer cannot rewrite system contracts alone
Свойство:
- `Pipeline/*` может задавать движение работы, но не может в одиночку переписать ownership, planning или fact contracts системы.

Поддерживающие контуры и документы:
- `Pipeline/*`
- `Docs/Technical/Pipeline.md`
- `Docs/Technical/Architecture.md`
- `Docs/Technical/Interfaces.md`

Нарушением считается:
- чтение phase canon как разрешения менять domain ownership;
- перенос system-contract definitions в process docs без sync в technical-layer.

Последствие нарушения:
- process-layer начинает подменять архитектуру и planning/governance contour.

### INV-010 — Tooling follows documents, not the reverse
Свойство:
- tooling materialize и проверяет уже утверждённые contracts, но не является единственным местом, где эти contracts живут.

Поддерживающие контуры и документы:
- `Tools/bp_lint.py`
- `Tools/bp_bootstrap.py`
- `Docs/Technical/*`
- `Rules/*`
- `Standards/*`

Нарушением считается:
- внедрение обязательного contract только в код проверки без документной фиксации;
- поведение bootstrap/lint, которое спорит с активными документами.

Последствие нарушения:
- человеко-читаемый и инструментальный контуры расходятся.

### INV-011 — Products become self-contained after bootstrap
Свойство:
- целевой product repo после создания имеет local `Tools/*` и не зависит от `BytePress` как runtime/tool dependency для обычной структурной проверки.

Поддерживающие контуры и документы:
- `Docs/Technical/Product_Bootstrap_Domain_Matrix.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Domain_Model_Migration_Plan.md`
- `Logs/ADRlog.md` / `ADR-000022`

Нарушением считается:
- generated product repo, которому нужен `BYTEPRESS_ROOT` для обычного `dev-test` после завершения profile bootstrap migration;
- копирование `Adapters/*`, `Memory/*`, `MCP/*`, `Runtime/*`, `Roles/*`, `Skills/*` или `Standards/*` в продукт как placeholder domains.

Последствие нарушения:
- продукт остаётся operational child фабрики и не является самодостаточным каркасом.

## Недопустимые нарушения по контурам
### К `Plans/*`
Недопустимо:
- иметь `BACK-*` и `PLAN-*` в несогласованных статусах;
- хранить current stage/task/pass вне `Plans/*`.

### К `Runtime/*`
Недопустимо:
- превращать runtime в источник истины;
- оставлять runtime как substitute для archive или logs.

### К `Logs/*`
Недопустимо:
- использовать logs как план работ;
- пропускать фиксацию факта проверки для завершённого pass.

### К `Pipeline/*`
Недопустимо:
- использовать process-layer как justification для обхода planning, technical или fact contours;
- дублировать process-canon в technical documents как primary source.

## Как invariants поддерживаются системой
- `Architecture.md` удерживает domain and layer boundaries.
- `Model.md` удерживает ownership состояния и допустимые зависимости сущностей.
- `Interfaces.md` удерживает допустимые touchpoints и запреты обходов.
- `Artifact_Lifecycle.md` удерживает source-of-truth map, sync-loop и closure rules.
- `Rules/*` и `Standards/*` закрепляют запреты и нормы представления.
- `bp_lint.py` проверяет минимальные structural contracts active layer.
- governance-сверка перед commit и push подтверждает, что planning-contour не спорит сам с собой.

## Граница документа
`System_Invariants.md` не является:
- картой technical-layer как каталога;
- картой доменов и слоёв;
- моделью сущностей и ownership состояния;
- картой интерфейсов;
- lifecycle-checklist;
- process-canon document.

Он остаётся каноническим contract системных инвариантов текущего `BytePress`.

## Связи
- `RULE-000001`
- `RULE-000003`
- `RULE-000004`
- `RULE-000006`
- `RULE-000008`
- `RULE-000009`
- `RULE-000010`
- `STD-000003`
- `STD-000006`

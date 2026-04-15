# Validation

ID: DOC-000002
Название: Validation
Статус: Действует
Связи: `ROAD-000011`, `BACK-000067`, `PLAN-000055`, `Docs/Technical/Verification.md`, `Docs/Technical/Verification_Evidence.md`, `Docs/Technical/Validation_Evidence.md`
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-11

## Назначение
`Docs/Technical/Validation.md` является каноническим singleton document, который фиксирует contract map validation-layer текущего `BytePress`.

Этот document отвечает на вопросы:
- какое место validation занимает в системе;
- чем validation отличается от verification;
- какие inputs validation читает;
- какие outputs validation produce;
- какие evidence использует validation;
- кто владеет интерпретацией validation result;
- как validation связано с pass-close contour и phase gates;
- что validation не должно подменять.

## Место документа в technical-layer
`Validation.md` является supporting technical-document verification and validation contour.

Его роль:
- фиксировать contract map validation-layer поверх уже выделенного verification-layer;
- разводить validation, verification, evidence package и gate approval;
- фиксировать classes validation result, inputs, outputs и ownership интерпретации;
- удерживать связь validation с pass-close contour без превращения validation в новый toolchain;
- не дублировать `Verification.md` как contract map verification checks;
- не дублировать `Validation_Levels.md` как operational levels validation;
- не дублировать `Validation_Evidence.md` как classes validation evidence, storage и sufficiency criteria;
- не дублировать `Verification_Levels.md` как operational levels verification;
- не дублировать `Verification_Evidence.md` как contract evidence classes, storage и sufficiency;
- не дублировать `Pipeline/Phase_Gates.md` как gate policy;
- не дублировать `Tools/*` как implementation machine-executable checks.

## Чем validation отличается от соседних contracts
- `Verification.md` отвечает за contract map verification-layer: checks, inputs, outputs, evidence forms и ownership verification result.
- `Verification_Levels.md` отвечает за operational levels verification и target split future `bp_check / bp_verify`.
- `Verification_Evidence.md` отвечает за upstream виды evidence, обязательность, storage и linkage к pass-close contour.
- `Validation_Evidence.md` отвечает за classes validation evidence, mandatory / optional status, sufficient / insufficient criteria и relation к validation levels.
- `Validation_Levels.md` отвечает за operational levels validation и relation этих уровней к evidence package и pass-close contour.
- `Pipeline/Phase_Gates.md` отвечает за manual gate decision и phase approval.
- `Tools/*` отвечают за implementation automatic checks.
- `Validation.md` отвечает за то, как validation-layer читает verification result и evidence package, какие verdict classes выдаёт и когда outcome считается подтверждённым относительно contract.

## Validation-layer в системе
Validation-layer находится после выполнения verification checks и до process-layer gate decision.

Его задача:
- интерпретировать verification result относительно expected contract outcome;
- проверить достаточность evidence package для конкретного closure claim;
- подтвердить или не подтвердить, что outcome действительно соответствует проверяемому contract;
- подготовить validation result как input для pass-close contour и, при необходимости, для gate handoff.

Validation-layer не является ни новым набором checks, ни отдельным process gate.

## Какие вопросы решает validation
Validation-layer отвечает на вопросы:
- достаточно ли verification evidence для подтверждения outcome;
- соответствует ли observed outcome ожидаемому contract, а не только structural/pass-fail сигналу;
- можно ли считать локальный pass outcome подтверждённым;
- готов ли evidence package к передаче в gate contour как input, если это требуется process-layer.

Validation-layer не отвечает на вопросы:
- какие checks вообще существуют;
- как они реализованы в `Tools/*`;
- утверждён ли phase transition;
- какие документы владеют planning-state;
- как выглядит полный process-canon.

## Validation inputs
Validation читает только уже существующие active sources of truth и готовое verification basis.

Основные inputs:
- verification result из `Docs/Technical/Verification.md` и связанных procedural/automatic checks;
- verification levels и target split из `Docs/Technical/Verification_Levels.md`;
- evidence package и sufficiency rules из `Docs/Technical/Verification_Evidence.md`;
- active contracts и реально затронутые документы текущего pass;
- current planning-state из `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`;
- process context из `Pipeline/Phase_Gates.md`, если validation result должен использоваться как gate input.

Недопустимые inputs:
- gate approval как substitute для validation;
- chat transcript как единственный basis;
- runtime notes без фиксации в active layer;
- raw shell output без привязки к verification evidence package.

## Validation outputs
Validation-layer не создаёт новый source-of-truth домен. Он produce validation result.

Основные outputs:
- verdict относительно конкретного outcome;
- явное объяснение, какого evidence хватает или не хватает;
- подтверждение, что pass-close claim может или не может быть сделан локально;
- validation handoff note для process gate, если process-layer требует такого input.

Validation output не равен:
- phase approval;
- автоматическому закрытию backlog-задачи;
- автоматическому обновлению `Roadmap`, `Backlog` или `Plan`.

## Classes validation result
Validation result должен читаться как ограниченный набор contract-level verdict classes.

### `validated`
Что означает:
- outcome подтверждён относительно проверяемого contract;
- evidence package достаточен для локального closure claim;
- validation result может использоваться как gate input, если process-layer этого требует.

Что не означает:
- automatic phase approval;
- автоматическое закрытие pass без planning sync.

### `not_validated`
Что означает:
- outcome не подтверждён;
- validation выявил contradiction, missing evidence или несоответствие contract outcome.

Что требует:
- pass не может считаться локально закрытым;
- handoff в gate contour считается неполным или некорректным.

### `validation_blocked`
Что означает:
- validation не может быть честно завершён, потому что verification basis или evidence package неполны;
- отсутствует достаточный input для verdict class `validated` / `not_validated`.

Типовые причины:
- нет обязательной governance-сверки;
- отсутствует связанный evidence package;
- verification result не зафиксирован в active layer.

### Почему classes ограничены
Validation-layer не должен плодить тонкие status-taxonomy вместо ясного contract verdict.

В текущем `BytePress` достаточно трёх классов:
- `validated`
- `not_validated`
- `validation_blocked`

Их хватает, чтобы развести:
- подтверждённый outcome;
- опровергнутый outcome;
- ситуацию, где basis для честного verdict ещё не собран.

## Какие evidence использует validation
Validation не определяет evidence classes заново. Он использует evidence package, уже определённый в `Verification_Evidence.md`.

Обычно validation опирается на:
- EVC-001 и EVC-002 как basis automatic and repo-state confirmation;
- EVC-003 как basis planning-state consistency;
- EVC-004, если verification факт зафиксирован в log-layer;
- EVC-005 и EVC-006, если validation result должен перейти в delivery/gate handoff contour.

Validation читает evidence package как bundle. Он не подменяет собой evidence contract и не требует по умолчанию нового storage outside already approved active domains.

## Кто владеет интерпретацией validation result
Validation result интерпретирует pass owner:
- человек;
- или агент, который ведёт текущий pass под governance rules репозитория.

Если validation result используется как gate input, process owner читает этот result, но не передаёт ownership обратно validation-layer.

Это означает:
- `Tools/*` не владеют validation interpretation;
- verification evidence может быть собран автоматически, но sufficiency и outcome confirmation остаются procedural;
- gate owner может принять или не принять handoff, но не подменяет локальную validation interpretation задним числом.

## Ownership интерпретации validation result
### Local pass context
В локальном pass context owner интерпретации validation result:
- pass owner.

Именно pass owner решает:
- достаточно ли inputs для завершения validation;
- какому result class соответствует текущий outcome;
- можно ли переводить backlog-задачу и current `Plan` в финальные статусы.

### Gate handoff context
Если validation result передаётся в process-layer:
- validation owner остаётся автором verdict;
- phase owner остаётся owner gate decision.

Это разделение обязательно:
- validation owner не принимает gate decision;
- phase owner не переписывает validation result задним числом, а либо принимает его как input, либо отклоняет handoff.

## Место validation в pass-close contour
Validation входит в pass-close contour после verification и до финального утверждения локального closure.

Нормальная последовательность:
1. Выполнить automatic и procedural verification.
2. Собрать evidence package.
3. Подтвердить через validation, что evidence package достаточен для closure claim.
4. Только после этого перевести backlog-задачу и current `Plan` в финальные статусы.

Следствия:
- pass-close не должен опираться только на успешный lint;
- pass-close не должен опираться только на наличие evidence без validation interpretation;
- validation result должен быть отражён в current `Plan` и user-facing отчёте как часть closure basis.

## Связь validation с phase gates
Validation не подменяет gate policy.

Граница проходит так:
- verification собирает checks и evidence;
- validation подтверждает или не подтверждает достаточность outcome;
- `Pipeline/Phase_Gates.md` остаётся owner решения о phase approval.

Это значит:
- validated outcome может стать gate input, но не становится gate approval автоматически;
- gate может требовать validation basis, но не обязан принимать его без отдельного process decision;
- отсутствие validation делает gate input неполным, если process-layer ждёт подтверждённый outcome, а не только raw evidence.

## Где validation заканчивается и начинается gate
Граница проходит так:
- validation отвечает за interpretation outcome относительно contract;
- gate отвечает за process decision о дальнейшем переходе.

Следствия:
- validation result class `validated` не равен approved gate;
- validation result class `not_validated` или `validation_blocked` делает gate input слабым или неполным, но сам process-layer всё равно владеет решением;
- gate policy остаётся в `Pipeline/Phase_Gates.md`, а не переносится сюда.

## Что validation не должно подменять
Validation-layer не должен:
- превращаться в общий verification map;
- вводить собственный toolchain вместо `Tools/*`;
- переопределять evidence classes и storage rules;
- становиться manual gate policy;
- владеть planning-state;
- подменять `Logs/*` как фактологический слой;
- маскировать engineering judgment под automatic verdict.

## Отношение к соседним контурам
### К `Verification.md`
`Verification.md` отвечает за то, как checks contour устроен и какие evidence forms он produce. `Validation.md` отвечает за то, когда результат этого contour считается подтверждённым относительно contract outcome.

### К `Verification_Evidence.md`
`Verification_Evidence.md` задаёт classes, storage и sufficiency rules evidence. `Validation.md` использует этот package как basis для outcome confirmation.

### К `Validation_Evidence.md`
`Validation_Evidence.md` задаёт, какой evidence package validation считает достаточным на разных уровнях interpretation, closure readiness и gate handoff readiness.

### К `Validation_Levels.md`
`Validation_Levels.md` раскладывает общую contract map validation-layer по уровням: sufficiency, outcome confirmation, pass-close readiness и gate handoff readiness.

### К `Plans/*`
`Plans/*` владеет stage/task/pass state. Validation использует planning-state как часть closure basis, но не владеет им.

### К `Pipeline/Phase_Gates.md`
`Pipeline/Phase_Gates.md` остаётся owner gate decision. Validation только готовит confirmed or rejected outcome basis для handoff.

### К `Tools/*`
`Tools/*` materialize automatic checks. Validation не описывает implementation commands и не вводит новый validation toolchain этим pass.

## Граница документа
`Docs/Technical/Validation.md` не является:
- tool implementation spec;
- gate policy;
- replacement для `Verification.md`, `Verification_Levels.md` или `Verification_Evidence.md`;
- replacement для `Validation_Levels.md` или `Validation_Evidence.md`;
- checklist каждого отдельного domain-specific validation case.

Он остаётся каноническим contract map validation-layer текущего `BytePress`.

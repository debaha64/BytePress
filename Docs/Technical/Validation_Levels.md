# Validation_Levels

ID: DOC-000003
Название: Validation Levels
Статус: Действует
Связи: `ROAD-000011`, `BACK-000069`, `PLAN-000057`, `Docs/Technical/Validation.md`, `Docs/Technical/Verification_Evidence.md`
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-08
Дата_изменения: 2026-04-08

## Назначение
`Docs/Technical/Validation_Levels.md` является каноническим singleton document, который фиксирует уровни validation-контура текущего `BytePress`.

Этот document отвечает на вопросы:
- какие уровни validation система различает;
- какая цель у каждого уровня;
- какие required inputs нужны на каждом уровне;
- какие expected outputs produce каждый уровень;
- как уровни связаны с `Validation.md`;
- как уровни используют `Verification_Evidence.md`;
- где уровни входят в pass-close contour;
- что не должно автоматизироваться;
- что не должно смешиваться с verification levels.

## Место документа в technical-layer
`Validation_Levels.md` является supporting technical-document validation-layer.

Его роль:
- детализировать validation contour поверх contract map из `Validation.md`;
- раскладывать validation по operational levels, не превращая это в validation toolchain;
- фиксировать relation уровней к evidence package и pass-close contour;
- не дублировать `Validation.md` как общую карту inputs/outputs/ownership;
- не дублировать `Verification_Evidence.md` как contract evidence classes и storage;
- не дублировать `Artifact_Lifecycle.md` как closure-loop и sync matrix;
- не дублировать `Pipeline/Phase_Gates.md` как gate policy;
- не дублировать `Tools/*` как implementation.

## Чем document отличается от соседних contracts
- `Validation.md` задаёт общую contract map validation-layer.
- `Validation_Levels.md` раскладывает validation contour по уровням и по relation к pass-close contour.
- `Verification_Evidence.md` задаёт classes, storage и sufficiency rules evidence package.
- `Verification_Levels.md` задаёт уровни verification, а не уровни outcome confirmation.
- `Artifact_Lifecycle.md` задаёт closure-loop и обязательные sync relations, но не делит validation на levels.
- `Pipeline/Phase_Gates.md` задаёт gate policy, но не описывает validation ladder.

## Уровни validation-контура
### Level 1. Evidence Sufficiency Validation
Цель:
- подтвердить, что evidence package вообще достаточен для перехода от verification result к validation interpretation.

Required inputs:
- verification evidence package из `Docs/Technical/Verification_Evidence.md`;
- outputs relevant verification checks и planning-state evidence;
- current `Plan` как носитель evidence summary текущего pass.

Expected outputs:
- verdict: `validated`, `not_validated` или `validation_blocked` на уровне sufficiency;
- явное указание, каких evidence хватает или не хватает.

Relation к `Validation.md`:
- реализует часть contract map, где validation читает evidence bundle и проверяет достаточность basis.

Relation к `Verification_Evidence.md`:
- опирается на EVC-001..EVC-006 как на уже утверждённые evidence classes;
- не создаёт новых evidence classes.

Relation к pass-close contour:
- если уровень не пройден, pass-close contour не может перейти к локальному closure claim;
- недостаточный evidence package блокирует дальнейшую validation interpretation.

### Level 2. Outcome Confirmation Validation
Цель:
- подтвердить, что observed outcome соответствует ожидаемому contract outcome, а не только имеет формально собранный evidence package.

Required inputs:
- result level 1;
- active contracts и реально затронутые documents текущего pass;
- verification result из `Validation.md` / `Verification.md`.

Expected outputs:
- verdict, подтверждающий или не подтверждающий outcome;
- краткое объяснение, какой contract outcome подтверждён или опровергнут.

Relation к `Validation.md`:
- реализует ту часть contract map, где validation подтверждает или отвергает outcome относительно contract.

Relation к `Verification_Evidence.md`:
- использует evidence package как basis, но не подменяет semantic interpretation самим presence evidence.

Relation к pass-close contour:
- это последний validation уровень, после которого pass owner может делать local closure claim;
- без него pass нельзя переводить в финальные planning-statuses.

### Level 3. Pass Closure Readiness
Цель:
- подтвердить, что validated outcome можно безопасно включить в локальный pass-close contour.

Required inputs:
- result levels 1-2;
- current planning-state из `Roadmap.md`, `Backlog.md` и current `Plan`;
- обязательная governance-сверка pass.

Expected outputs:
- readiness verdict для local pass-close;
- подтверждение, что validation result достаточно отражён в current `Plan` и user-facing отчёте.

Relation к `Validation.md`:
- реализует ту часть contract map, где validation входит в pass-close contour.

Relation к `Verification_Evidence.md`:
- использует planning-state evidence и repo-state evidence как closure basis;
- не заменяет governance-сверку отдельным validation shortcut.

Relation к pass-close contour:
- напрямую определяет, можно ли переводить backlog-задачу и current `Plan` в `Завершено`;
- без этого уровня завершение pass считается premature.

### Level 4. Gate Handoff Readiness
Цель:
- подготовить validated outcome как возможный input для gate, не подменяя gate decision.

Required inputs:
- result levels 1-3;
- handoff-ready evidence package;
- process context из `Pipeline/Phase_Gates.md`, если gate input действительно нужен.

Expected outputs:
- handoff-ready validation note;
- явное различение между validated outcome и approved phase transition.

Relation к `Validation.md`:
- реализует ту часть contract map, где validation граничит с process gates.

Relation к `Verification_Evidence.md`:
- использует gate-handoff evidence как готовый пакет, но не считает gate approval evidence substitute.

Relation к pass-close contour:
- не нужен для каждого pass как условие локального close;
- нужен только там, где process-layer ожидает formal gate input.

## Что не должно автоматизироваться
- outcome confirmation, требующее инженерного суждения;
- решение о достаточности evidence для local closure claim;
- decision о переводе stage/task/pass в финальные статусы;
- gate approval и любые phase transitions;
- переинтерпретация contradictions, требующая смыслового review wording.

## Что не должно смешиваться с verification levels
- verification levels отвечают за checks contour и evidence production; validation levels отвечают за interpretation outcome и readiness к closure;
- verification level `pass` не равен validation level `validated`;
- evidence sufficiency не равна самому факту выполнения checks;
- gate handoff readiness не равна gate approval;
- validation levels не должны становиться новой классификацией automatic checks.

## Отношение validation levels к соседним контурам
### К `Validation.md`
`Validation.md` удерживает общую contract map validation-layer. `Validation_Levels.md` раскладывает её по operational levels.

### К `Verification_Evidence.md`
`Verification_Evidence.md` задаёт, что считается evidence и как оно хранится. `Validation_Levels.md` показывает, на каких уровнях этот evidence bundle читается и интерпретируется.

### К `Verification_Levels.md`
`Verification_Levels.md` описывает, как собирается verification basis. `Validation_Levels.md` описывает, как этот basis превращается в validated or not validated outcome.

### К `Artifact_Lifecycle.md`
Lifecycle contract задаёт closure-loop. Validation levels определяют, на каких стадиях этого loop validation должен дать confirmed outcome.

### К `Tools/*`
`Tools/*` не получают новой implementation responsibility в этом pass. Document описывает только validation levels как contract, а не tool design.

## Граница документа
`Validation_Levels.md` не является:
- implementation spec validation tooling;
- заменой `Validation.md` или `Verification_Evidence.md`;
- gate policy;
- checklist каждого конкретного domain-specific validation case.

Он остаётся каноническим документом уровней validation-контура текущего `BytePress`.

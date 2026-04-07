# Verification

## Назначение
`Docs/Technical/Verification.md` является каноническим contract map verification-layer текущего `BytePress`.

Этот document отвечает на вопросы:
- какие классы verification checks система различает;
- какие inputs verification-layer читает из active layer;
- какие outputs и evidence forms verification-layer производит;
- кто владеет интерпретацией verification result;
- где verification result входит в pass-close contour;
- где verification заканчивается и начинается process gate.

## Место документа в technical-layer
`Verification.md` является supporting technical-document, а не частью required core.

Его роль:
- фиксировать contract map verification-layer поверх уже собранных system contracts;
- разводить automatic checks, procedural checks, evidence и process gates;
- фиксировать ownership интерпретации verification result;
- не дублировать `README.md` как карту technical-layer;
- не дублировать `Artifact_Lifecycle.md` как lifecycle matrix и sync-loop;
- не дублировать `Platform_Contracts.md` как execution perimeter и tool perimeter;
- не дублировать `Pipeline/*` как process-canon и gate policy;
- не дублировать `Tools/*` как implementation конкретных checks.

## Чем verification contract отличается от соседних документов
- `README.md` отвечает за карту technical-layer и required/supporting split.
- `Artifact_Lifecycle.md` отвечает за sources of truth, sync-loop и pass-close contour.
- `Platform_Contracts.md` отвечает за supported execution environment и tool perimeter.
- `Pipeline/Phase_Gates.md` отвечает за gates и manual phase approval.
- `Tools/*` отвечают за materialization machine-executable checks.
- `Verification.md` отвечает за сам contract checks contour: классы проверок, inputs, outputs, evidence и ownership результата.
- `Verification_Levels.md` отвечает за уровни verification-контура и target split будущих `bp_check / bp_verify`.
- `Verification_Evidence.md` отвечает за contract evidence: виды evidence, обязательность, storage и linkage к pass-close contour.
- `Validation.md` отвечает за boundary validation-layer: когда verification result и evidence package достаточно для подтверждения outcome, но ещё не превращаются в process gate decision.

## Verification-layer в системе
Verification-layer находится между system contracts, planning-contour, process-layer и tool perimeter.

Его место в системе:
- читает active contracts из `Docs/Technical/*`, `Rules/*`, `Standards/*`, `Plans/*` и реально затронутых active domains;
- использует `Tools/*` как execution perimeter automatic checks;
- использует `Pipeline/*` как process context, в котором verification result может стать gate input;
- возвращает verification result в pass-close contour через planning sync и fact logs.

Verification-layer не владеет ни process decision, ни tool implementation, ни lifecycle matrix. Он только определяет, как checks contour читается и интерпретируется в системе.

Validation-layer использует результат verification, но не совпадает с ним: verification отвечает за checks contour и evidence basis, а validation отвечает за confirmation достаточности этого basis относительно contract outcome.

## Классы verification checks
### Structural automatic checks
Назначение:
- проверить структурную полноту и базовые contract constraints репозитория машинным способом.

Текущие примеры:
- `python3 Tools/bp_lint.py --repo .`

Свойства:
- запускаются детерминированно;
- дают machine-readable success/failure outcome;
- не требуют ручного governance-решения для самого факта прохождения.

### Contract-specific automatic checks
Назначение:
- проверять отдельные deterministic contracts, если они явно materialized в `Tools/*`.

Текущий статус:
- допускаются архитектурой verification-layer, но не расширяются этим pass в новый toolchain.

Свойства:
- остаются implementation concern внутри `Tools/*`;
- не становятся каноническим contract только по факту существования script.

### Procedural governance checks
Назначение:
- проверить, что pass закрывается без скрытых contradictions между stage/task/pass, direct references и фактическим результатом.

Текущие примеры:
- сверка статуса backlog-задачи;
- сверка секций `Активные/Завершённые`;
- сверка backlog index;
- сверка статуса `ROAD-*` и `Связанные_backlog`;
- сверка статуса current `Plan`.

Свойства:
- требуют интерпретации человеком или агентом;
- могут опираться на automatic evidence, но не сводятся к нему.

### Procedural content checks
Назначение:
- проверить смысловую согласованность contracts, boundaries, ownership и direct references после изменения.

Текущие примеры:
- audit на отсутствие пересечения verification-layer и process gates;
- audit на отсутствие hidden contradictions между `Verification.md`, `Artifact_Lifecycle.md`, `Platform_Contracts.md` и `Pipeline/Phase_Gates.md`;
- review того, что contract wording не подменяет implementation или process approval.

Свойства:
- не автоматизируются надёжно текущим tool perimeter;
- остаются частью pass-level review work.

## Verification inputs
Verification-layer читает только те inputs, которые уже являются active source of truth для соответствующего типа состояния.

Основные inputs:
- `Docs/Technical/*` как contracts verification context;
- `Rules/*` и `Standards/*` как normative constraints;
- `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plans/PLAN-<NNNNNN>-<slug>.md` как planning-state для governance checks;
- `Pipeline/Phase_Gates.md` и связанные `Pipeline/*` как process context для gate boundary;
- `Tools/*` как execution entrypoint automatic checks;
- фактически затронутые active documents текущего pass.

Недопустимые inputs:
- archive files как current source of truth;
- chat transcript как единственный verification basis;
- runtime notes без фиксации в active layer;
- shell output без привязки к конкретному check.

## Verification outputs
Verification-layer не создаёт отдельный домен состояния. Он производит интерпретируемый verification result.

Основные outputs:
- verdict по automatic checks: `pass` / `fail`;
- verdict по procedural checks: `confirmed` / `not confirmed`;
- список найденных contradictions или подтверждение их отсутствия;
- решение о том, достаточно ли verification evidence для pass-close contour;
- вход для process gate, если текущая фаза требует approval.

Verification output сам по себе не равен:
- phase approval;
- изменению planning-state;
- записи в log без фактической фиксации.

## Формы evidence
Verification evidence допускается только в формах, которые могут быть прочитаны и перепроверены в system contour.

Допустимые evidence forms:
- stdout/stderr конкретного automatic check;
- чистый `git diff --check`;
- зафиксированное состояние active documents после pass;
- явная governance-сверка в user-facing report или `Plan`;
- факт выполнения проверок, зафиксированный в `Logs/QualityLog.md`, если pass приводит к содержательному изменению.

Недопустимые evidence forms:
- незафиксированное устное утверждение о проверке;
- ссылка на память исполнителя без воспроизводимого check;
- process approval без предъявления verification basis;
- raw tool output без связи с проверяемым contract.

Детализация evidence contract (classes, обязательность, storage, linkage) вынесена в `Docs/Technical/Verification_Evidence.md`.

## Ownership интерпретации результата
### Automatic checks
`Tools/*` владеет исполнением check, но не окончательной интерпретацией system outcome.

Интерпретацией результата владеет pass owner:
- человек;
- или агент, если pass исполняется агентом под governance rules репозитория.

### Procedural checks
Интерпретацией procedural result всегда владеет человек или агент, который закрывает текущий pass и отвечает за planning sync.

### Process gates
Интерпретацией того, достаточно ли verification result для phase transition, владеет process-layer approval по правилам `Pipeline/*`.

Это значит:
- verification result подготавливает evidence;
- pass owner решает, закрыт ли pass локально;
- phase owner утверждает или не утверждает переход.

## Где verification result входит в pass-close contour
Verification result входит в pass-close contour в следующих точках:
- после каждого локального commit через `git diff --check` и обязательный repo check;
- перед финальным commit через governance-сверку planning-state;
- перед `push` через повторную governance-сверку;
- в итоговом user-facing отчёте как явная фиксация выполненных checks;
- в `Logs/QualityLog.md`, если pass приводит к содержательному изменению и факт проверки должен быть зафиксирован как history.

Verification result не закрывает pass автоматически. Он только подтверждает, что у pass owner есть достаточное evidence basis для закрытия.

## Где verification заканчивается и начинается gate
Граница проходит так:
- verification отвечает за выполнение checks и интерпретацию evidence относительно contracts;
- gate отвечает за решение process-layer о переходе между фазами или следующими управляемыми шагами.

Следствия:
- успешный automatic check не открывает gate автоматически;
- завершённый procedural review не равен phase approval;
- gate может опираться на verification result, но не сводится к нему;
- если process-layer требует manual approval, verification не может подменить это approval даже при полном наборе evidence.

## Что verification-layer не должен подменять
Verification-layer не должен:
- превращаться в новый process-canon;
- забирать у `Pipeline/*` ownership gates и phase approval;
- забирать у `Artifact_Lifecycle.md` ownership sync matrix;
- забирать у `Platform_Contracts.md` ownership tool perimeter и execution assumptions;
- превращаться в design-spec tooling implementation;
- подменять `Logs/*` как фактологический слой;
- подменять `Plans/*` как owner stage/task/pass state.

## Минимальный target-state для будущего `bp_check / bp_verify`
Этот pass не создаёт новый toolchain, но фиксирует минимальный target-state.

Он должен оставаться таким:
- automatic checks materialize только те contracts, которые уже явно описаны;
- procedural checks остаются отдельным классом и не маскируются под shell automation;
- evidence формы и ownership результата читаются одинаково до и после возможного tooling expansion;
- future `bp_check / bp_verify` остаётся implementation layer поверх уже утверждённого verification contract map.

Детализация уровней verification и target split будущих commands вынесена в `Docs/Technical/Verification_Levels.md`.

## Отношение verification-layer к соседним контурам
### К `Plans/*`
`Plans/*` владеет stage/task/pass state. Verification-layer использует эти файлы как input для governance checks, но не владеет planning-state.

### К `Artifact_Lifecycle.md`
`Artifact_Lifecycle.md` определяет, что должно быть синхронизировано перед closure. Verification-layer определяет, какими checks и evidence это подтверждается.

### К `Platform_Contracts.md`
`Platform_Contracts.md` определяет, какие execution assumptions и tools считаются поддерживаемыми. Verification-layer определяет, как их результаты используются в checks contour.

### К `Pipeline/*`
`Pipeline/*` остаётся owner process gates. Verification-layer поставляет evidence для gate input, но не заменяет phase approval.

### К `Tools/*`
`Tools/*` исполняют automatic checks. Verification-layer не описывает код, а держит contract map того, как эти checks читаются в системе.

## Граница документа
`Docs/Technical/Verification.md` не является:
- gate policy document;
- lifecycle matrix;
- tool implementation spec;
- полным procedural manual для каждого типа работы;
- roadmap для `ROAD-000012`.

Он остаётся каноническим contract map verification-layer текущего `BytePress`.

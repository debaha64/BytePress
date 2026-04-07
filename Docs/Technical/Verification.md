# Verification

## Назначение
`Docs/Technical/Verification.md` является каноническим boundary-document verification-layer текущего `BytePress`.

Этот document отвечает на вопросы:
- где verification contour находится в системе;
- что относится к automatic checks, а что относится к procedural checks;
- где заканчиваются verification responsibilities и начинаются process gates;
- что остаётся реализацией в `Tools/*`, а не contract-описанием в technical-layer;
- каким должен быть минимальный target-state verification contour до будущего отдельного tooling pass.

## Место документа в technical-layer
`Verification.md` является supporting technical-document, а не частью required core.

Его роль:
- зафиксировать границы verification-layer как части технической карты системы;
- развести verification checks, process gates, lifecycle closure и tool implementation;
- не дублировать `README.md` как карту technical-layer;
- не дублировать `Artifact_Lifecycle.md` как source-of-truth matrix и pass-close contour;
- не дублировать `Platform_Contracts.md` как execution perimeter и supported tool perimeter;
- не дублировать `Pipeline/*` как process-canon и gate registry;
- не дублировать `Tools/*` как реализацию самих проверок.

## Чем verification-layer отличается от соседних документов
- `README.md` отвечает за карту technical-layer и required/supporting split.
- `Artifact_Lifecycle.md` отвечает за жизненный цикл артефактов, обязательные sync-loop и pass-close contour.
- `Platform_Contracts.md` отвечает за supported platform/tool perimeter и execution assumptions.
- `Pipeline/Phase_Gates.md` отвечает за gates и политику перехода между фазами.
- `Tools/*` отвечают за materialization и machine-execution конкретных checks.
- `Verification.md` отвечает только за границы verification-layer, классы проверок и разделение ownership между layer, process и tooling.

## Verification-layer в системе
Verification-layer находится на стыке technical-layer, planning-layer, process-layer и tools perimeter.

Его место в системе:
- читает system contracts из `Docs/Technical/*`, `Rules/*`, `Standards/*` и связанных active domains;
- использует process-canon из `Pipeline/*` как источник информации о том, где нужны gates, но не владеет самими gates;
- использует `Tools/*` как execution mechanism автоматических checks, но не владеет tool implementation;
- возвращает результат проверки в planning/fact contour через pass-close sync, `Logs/QualityLog.md` и согласование статусов.

Verification-layer не является отдельным source-of-truth доменом исполнения. Это boundary layer, который определяет, как checks contour соотносится с contracts, process и tools.

## Что относится к automatic checks
К automatic checks относятся machine-executable проверки, которые могут быть повторены без ручной интерпретации результата.

В текущем `BytePress` сюда относятся:
- `python3 Tools/bp_lint.py --repo .` как обязательный structural check active repo;
- deterministic tool checks внутри `Tools/*`, если они явно введены документным contract;
- shell-level повторяемые проверки, которые не требуют ручного governance-решения для интерпретации результата.

Automatic checks:
- могут быть gate input;
- могут быть частью pass-close contour;
- не заменяют procedural verification там, где нужен human judgment.

## Что относится к procedural checks
К procedural checks относятся проверки, требующие управляемого просмотра, сопоставления contracts и осмысленного решения человека или агента.

В текущем `BytePress` сюда относятся:
- governance-сверка `Roadmap`, `Backlog`, current `Plan` и фактического closure-state pass;
- audit на отсутствие hidden contradictions между active layer documents;
- review того, что direct references, ownership и boundaries не сломаны фактическим изменением;
- процедурная часть bootstrap validation, которая не сводится к одному structural lint run;
- PR-oriented review проверки перед публикацией результата.

Procedural checks:
- не обязаны превращаться в tool output;
- не подменяют собой process gates;
- могут использовать результаты automatic checks как вход, но не сводятся к ним.

## Что остаётся в `Pipeline` как gates
`Pipeline/*`, и в частности `Pipeline/Phase_Gates.md`, владеет:
- понятием gate между фазами;
- политикой ручного утверждения перехода;
- различием между завершённой фазой и утверждённой фазой.

Gate не равен verification result.

Это означает:
- успешный lint не открывает gate автоматически;
- выполненный procedural check не равен самому phase approval;
- verification даёт evidence для перехода, но само решение о переходе остаётся process-layer responsibility.

## Что остаётся в `Tools` как реализация
`Tools/*` владеет только реализацией machine-executable checks и materializers.

Для verification contour это означает:
- `Tools/bp_lint.py` остаётся текущим repo-native automatic check;
- будущие `bp_check` / `bp_verify` могут появиться как отдельный tooling pass, но не являются частью текущего boundary-pass;
- tool implementation не становится источником смысла verification-layer без синхронизации `Docs/Technical/*`.

Verification-layer задаёт границы и ownership, а не код инструментов.

## Что verification-layer не должен подменять
Verification-layer не должен:
- превращаться в новый process-canon;
- забирать у `Pipeline/*` ownership gates и phase approvals;
- забирать у `Artifact_Lifecycle.md` ownership source-of-truth matrix и sync-loop;
- забирать у `Platform_Contracts.md` ownership supported tool perimeter;
- забирать у `Tools/*` ownership actual check implementation;
- превращаться в planning-state или log registry.

## Минимальный target-state для будущего `bp_check / bp_verify`
Будущий tooling horizon допустим только как отдельный pass, но boundary target-state уже должен быть ясен.

Минимальный target-state verification contour:
- отдельный verification-layer чётко разводит automatic и procedural checks;
- machine checks имеют явную привязку к document contracts, а не живут как ad hoc scripts;
- governance-сверка и другие procedural checks не маскируются под process gates;
- possible future `bp_check / bp_verify` остаётся implementation-layer поверх уже зафиксированных boundaries;
- появление новых commands не меняет ownership: contracts живут в docs, gates в `Pipeline/*`, code в `Tools/*`.

## Отношение verification-layer к соседним контурам
### К `Plans/*`
`Plans/*` задаёт current stage/task/pass. Verification-layer проверяет согласованность результатов pass, но не владеет planning-state.

### К `Artifact_Lifecycle.md`
Lifecycle contract фиксирует, что должно быть синхронизировано и замкнуто. Verification-layer фиксирует, какие checks используются для подтверждения этого closure.

### К `Platform_Contracts.md`
Platform contract определяет, в какой среде check tooling считается поддерживаемым. Verification-layer определяет, как результаты этих checks интерпретируются в системе.

### К `Pipeline/*`
`Pipeline/*` остаётся owner process gates. Verification-layer поставляет check evidence, но не подменяет phase approval.

### К `Tools/*`
`Tools/*` исполняют machine checks. Verification-layer не описывает код реализации, а только boundary and ownership contract.

## Граница документа
`Docs/Technical/Verification.md` не является:
- новым tool design document;
- процессным реестром gates;
- checklist всех procedural действий агента;
- заменой `QualityLog`;
- roadmap будущего verification stage beyond boundary-pass.

Он остаётся каноническим boundary-document verification-layer текущего `BytePress`.

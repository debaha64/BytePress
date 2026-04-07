# Verification_Levels

ID: DOC-000001
Название: Verification Levels
Статус: Действует
Связи: `ROAD-000011`, `BACK-000064`, `PLAN-000052`, `Docs/Technical/Verification.md`
Источник: Следующий узкий pass этапа `ROAD-000011`
Дата_создания: 2026-04-07
Дата_изменения: 2026-04-07

## Назначение
`Docs/Technical/Verification_Levels.md` является каноническим singleton document, который фиксирует уровни verification-контура текущего `BytePress`.

Этот document отвечает на вопросы:
- какие уровни verification система различает;
- какая цель у каждого уровня;
- какие checks на каждом уровне automatic, а какие procedural;
- какой evidence нужен на каждом уровне;
- кто владеет результатом каждого уровня;
- где уровень влияет на pass-close contour;
- что должно лечь в будущий `bp_check`;
- что должно лечь в будущий `bp_verify`;
- что не должно автоматизироваться.

## Место документа в technical-layer
`Verification_Levels.md` является supporting technical-document verification-layer.

Его роль:
- детализировать уровни verification поверх общей contract map из `Verification.md`;
- удерживать target split будущих `bp_check / bp_verify` без реализации toolchain;
- не дублировать `Verification.md` как общую карту inputs/outputs/evidence/ownership;
- не дублировать `Pipeline/Phase_Gates.md` как gate policy;
- не дублировать `Artifact_Lifecycle.md` как sync matrix и closure-loop;
- не дублировать `Platform_Contracts.md` как supported tool perimeter;
- не дублировать `Tools/*` как implementation будущих commands.

## Чем document отличается от соседних contracts
- `Verification.md` задаёт общую contract map verification-layer.
- `Verification_Levels.md` раскладывает verification contour по уровням и target automation split.
- `Artifact_Lifecycle.md` задаёт, что должно быть синхронизировано перед closure, но не делит verification на уровни.
- `Platform_Contracts.md` задаёт supported tool perimeter, но не определяет verification levels.
- `Pipeline/Phase_Gates.md` задаёт gate policy, но не описывает verification evidence ladder.

## Уровни verification-контура
### Level 1. Structural Readiness
Цель:
- подтвердить, что active repository structurally пригоден к дальнейшей проверке и pass work не сломал базовые contracts.

Тип checks:
- automatic.

Текущие checks:
- `git diff --check`;
- `python3 Tools/bp_lint.py --repo .`.

Evidence:
- чистый diff-check;
- pass/fail output repo lint.

Owner результата:
- pass owner интерпретирует итог;
- `Tools/*` владеет только исполнением automatic checks.

Влияние на pass-close contour:
- обязателен после каждого локального commit;
- обязателен перед финальным commit и перед `push`;
- fail на этом уровне блокирует дальнейший локальный close pass.

Target automation:
- должен входить в будущий `bp_check`.

### Level 2. Contract Consistency
Цель:
- подтвердить, что изменённые contracts и direct references остаются согласованными и deterministic parts могут быть перепроверены машинно.

Тип checks:
- automatic, где contract допускает deterministic validation;
- procedural, где нужен осмысленный review wording и ownership.

Текущие checks:
- automatic: существующие deterministic repo checks, если они прямо введены в `Tools/*`;
- procedural: audit на отсутствие противоречий между `Verification.md`, `Verification_Levels.md`, `Artifact_Lifecycle.md`, `Platform_Contracts.md` и реально затронутыми active docs.

Evidence:
- automatic outputs конкретных checks;
- явное подтверждение отсутствия contradictions в итоге pass.

Owner результата:
- pass owner.

Влияние на pass-close contour:
- уровень подтверждает, что active documents можно считать согласованными после изменения;
- fail на этом уровне не даёт закрыть backlog-задачу даже при успешном structural lint.

Target automation:
- deterministic часть должна входить в будущий `bp_check`;
- procedural часть может собираться будущим `bp_verify` как evidence package, но не должна полностью автоматизироваться.

### Level 3. Pass Closure Verification
Цель:
- подтвердить, что текущий pass завершён в planning-contour и verification evidence достаточно для локального closure.

Тип checks:
- procedural с возможным использованием automatic inputs.

Текущие checks:
- governance-сверка backlog-задачи;
- проверка её секции `Активные/Завершённые`;
- проверка индекса `Backlog.md`;
- проверка статуса и `Связанные_backlog` у текущего `ROAD-*` в `Roadmap.md`;
- проверка статуса current `Plan`.

Evidence:
- явная governance-сверка в user-facing report;
- согласованное состояние `Roadmap`, `Backlog` и current `Plan`;
- при необходимости запись в `Logs/QualityLog.md`.

Owner результата:
- pass owner.

Влияние на pass-close contour:
- это последний verification уровень перед локальным признанием pass завершённым;
- без него pass нельзя переводить в финальные статусы и публиковать.

Target automation:
- future `bp_verify` может собирать checklist/evidence scaffold для этого уровня;
- окончательная интерпретация должна оставаться procedural.

### Level 4. Gate Readiness Handoff
Цель:
- передать verification evidence в process-layer как возможный input для phase approval, не подменяя сам gate.

Тип checks:
- procedural.

Текущие checks:
- review того, что evidence levels 1-3 complete;
- review того, что verification result действительно может быть использован как gate input.

Evidence:
- aggregated verification result;
- ссылка на пройденные automatic checks;
- подтверждённый pass-close state.

Owner результата:
- process-layer approval owner по правилам `Pipeline/*`.

Влияние на pass-close contour:
- уровень сам не закрывает pass и не является automatic approval;
- он только оформляет handoff между verification contour и process gates.

Target automation:
- не должен становиться частью `bp_check`;
- future `bp_verify` может только подготавливать handoff package, но не принимать gate decision.

## Target contract для будущего `bp_check`
`bp_check` должен оставаться инструментом automatic verification.

В его target contract должны входить:
- structural readiness checks уровня 1;
- deterministic contract checks уровня 2;
- machine-readable exit status;
- явное разделение пройденных и проваленных automatic checks;
- отсутствие претензии на phase approval, pass approval или procedural interpretation.

`bp_check` не должен:
- закрывать backlog-задачу;
- переводить `Plan` или `Roadmap` в финальные статусы;
- принимать gate decision;
- подменять review wording и semantic audit.

## Target contract для будущего `bp_verify`
`bp_verify` должен оставаться verification-orchestration tool поверх уже утверждённых contracts.

В его target contract должны входить:
- сбор automatic evidence из `bp_check` и других deterministic checks;
- scaffold для procedural verification levels 2-4;
- явный отчёт о missing evidence;
- handoff package для pass-close contour и, при необходимости, gate readiness.

`bp_verify` не должен:
- подменять человека или агента в интерпретации procedural результата;
- автоматически утверждать phase transition;
- становиться новым source of truth вне `Plans/*`, `Docs/*` и `Logs/*`;
- скрывать, какие части verification остались ручными.

## Что не должно автоматизироваться
- phase approval и любые process gates;
- semantic review качества текста contract, если он не выражен deterministic rule;
- решение о том, достаточно ли evidence для закрытия конкретного pass;
- интерпретация residual contradictions, требующая инженерного суждения;
- принятие решения о переводе stage/task/pass в финальные статусы.

## Отношение уровней verification к соседним контурам
### К `Verification.md`
`Verification.md` удерживает общую карту verification-layer. `Verification_Levels.md` раскладывает эту карту по operational levels и target automation split.

### К `Artifact_Lifecycle.md`
Lifecycle contract задаёт, какие sync-loop обязательны. Verification levels задают, на каких уровнях и каким evidence эти loop подтверждаются.

### К `Pipeline/Phase_Gates.md`
Gate policy остаётся в `Pipeline/*`. Verification levels только показывают, где verification result превращается в gate input.

### К `Tools/*`
`Tools/*` не получают реализации в этом pass. Document фиксирует только target contract будущих `bp_check / bp_verify`.

## Граница документа
`Verification_Levels.md` не является:
- implementation spec новых commands;
- roadmap для `ROAD-000012`;
- gate policy;
- checklist каждого возможного review case.

Он остаётся каноническим документом уровней verification-контура и target automation split текущего `BytePress`.

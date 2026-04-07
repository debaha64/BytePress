# Verification_Evidence

## Назначение
`Docs/Technical/Verification_Evidence.md` фиксирует contract verification evidence текущего `BytePress`.

Этот document отвечает на вопросы:
- какие виды evidence допустимы для verification-layer;
- какие evidence обязательны и какие опциональны (в зависимости от класса checks);
- где evidence хранится и как связывается с pass-close contour;
- что считается insufficient evidence;
- что не должно считаться evidence.

## Место документа в verification-layer
`Verification_Evidence.md` является supporting technical-document verification-layer.

Его роль:
- описывать evidence, а не сами checks;
- описывать storage и linkage evidence к `Plans/*` и `Logs/*`;
- не дублировать `Verification.md` как contract map;
- не дублировать `Verification_Levels.md` как уровни verification и target split;
- не дублировать `Artifact_Lifecycle.md` как lifecycle/sync matrix и closure-loop;
- не дублировать `Pipeline/Phase_Gates.md` как gate policy;
- не дублировать `Tools/*` как implementation checks.

## Термины
- Evidence: артефакт или факт, который можно перепроверить и который подтверждает выполнение проверки или её результат.
- Evidence package: минимальный связный набор evidence, достаточный для локального pass-close и для gate handoff (если требуется).
- Storage: домен, где evidence живёт как source of truth (или как допустимая ссылка).

## Классы evidence
### EVC-001 — Tool output evidence
Что это:
- stdout/stderr, exit code или текстовый итог machine-executable check.

Примеры:
- результат `python3 Tools/bp_lint.py --repo .`.

Где хранится:
- как summary в current `Plan` (и/или в user-facing отчёте);
- при необходимости как факт проверки в `Logs/QualityLog.md`.

### EVC-002 — Repo state evidence
Что это:
- evidence, отражающее состояние Git-дерева после изменения.

Примеры:
- чистый `git diff --check`;
- перечень изменённых файлов;
- commit SHAs текущего pass.

Где хранится:
- в Git history (commits);
- summary в current `Plan` и в user-facing отчёте.

### EVC-003 — Planning state evidence
Что это:
- evidence, подтверждающее согласованность stage/task/pass state.

Примеры:
- status текущей backlog-задачи и её секция `Активные/Завершённые`;
- индекс `Backlog.md`;
- статус `ROAD-*` и `Связанные_backlog` в `Roadmap.md`;
- статус current `Plan`.

Где хранится:
- в `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`.

### EVC-004 — Fact log evidence
Что это:
- доказательство как факт, записанный в log-layer.

Примеры:
- запись о выполненной проверке в `Logs/QualityLog.md`;
- запись о содержательном изменении в `Logs/ChangeLog.md`.

Где хранится:
- в `Logs/*` как каноническом fact-layer.

### EVC-005 — Review and delivery evidence
Что это:
- evidence delivery contour, которое подтверждает, что результат был опубликован и прошёл review perimeter.

Примеры:
- `git push` результата;
- ссылка на PR и его метаданные.

Где хранится:
- в Git/GitHub history как внешняя reference;
- summary должен быть отражён в user-facing отчёте.

### EVC-006 — Gate handoff evidence
Что это:
- evidence package, подготовленный как input для gate, без подмены gate approval.

Примеры:
- компактное описание того, какие levels пройдены, с ссылками на EVC-001..EVC-005.

Где хранится:
- в current `Plan` и/или в PR (как handoff note), если gate approval требует.

## Обязательность evidence по классам checks
### Automatic checks (structural и deterministic)
Mandatory evidence:
- EVC-001 (tool output summary) и EVC-002 (repo state: `diff --check` / commits).

Optional evidence:
- EVC-004 (QualityLog entry), если pass приводит к содержательному изменению и факт проверки должен жить как history.

### Procedural checks (governance и semantic audit)
Mandatory evidence:
- EVC-003 (planning state evidence) как явная governance-сверка;
- EVC-002 (repo state evidence) как контекст того, что именно проверялось.

Optional evidence:
- EVC-004 (QualityLog entry), если verification должен быть зафиксирован как факт;
- EVC-005 (PR link), если delivery contour является частью acceptance perimeter.

### Gate input (handoff)
Mandatory evidence:
- EVC-006 (handoff package) как связка уже собранных evidence.

Not evidence:
- gate approval itself как substitute для verification evidence.

## Где evidence хранится (source-of-truth)
Правило: evidence хранится там, где система владеет соответствующим типом состояния.

Канонические storage точки:
- `Plans/*`:
  - current `Plan` хранит summary evidence package текущего pass;
  - `Backlog` и `Roadmap` хранят planning-state evidence.
- `Logs/*`:
  - `Logs/QualityLog.md` хранит факты проверки;
  - `Logs/ChangeLog.md` хранит факты изменения.
- `Tools/*`:
  - владеет только implementation checks, но не evidence storage как source of truth.
- внешняя delivery поверхность (PR):
  - допускается как reference, но не должна быть единственным storage для обязательного evidence.

## Как evidence связывается с pass-close contour
Evidence package для pass-close должен быть связан минимум так:
- ссылка на `BACK-*` и `PLAN-*` (planning identity);
- список изменённых артефактов (paths);
- фиксированный список выполненных automatic checks и их verdict;
- явная governance-сверка planning-state;
- если применимо, ссылка на log-entry о проверке.

Нормальная точка фиксации этого linkage:
- раздел `## Результат` current `Plan`;
- user-facing отчёт о pass (как delivery evidence).

## Insufficient evidence
Insufficient evidence считается:
- утверждение “проверка пройдена” без EVC-001/EVC-003;
- ссылка на память исполнителя без воспроизводимого check;
- “скриншот результата” вместо machine-executable output;
- raw output без связи с тем, какой contract он подтверждает;
- gate approval без предъявленного evidence package.

## Что не является evidence
- chat transcript и runtime notes как единственный носитель результата;
- “фаза утверждена” как substitute для verification evidence;
- наличие файла без подтверждения, что его содержание соответствует contract;
- произвольные одноразовые команды вне supported tool perimeter как каноническая проверка.

## Граница документа
`Verification_Evidence.md` не:
- описывает gate policy;
- описывает tool implementation;
- заменяет `Verification.md` и `Verification_Levels.md`;
- превращает evidence в обязательное хранение raw output в репозитории по умолчанию.

Он фиксирует только contract evidence: виды, обязательность, storage и linkage к pass-close contour.

## Связанные артефакты
- `Docs/Technical/Verification.md`
- `Docs/Technical/Verification_Levels.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-<NNNNNN>-<slug>.md` (current pass plan)
- `Logs/QualityLog.md` (если факт проверки фиксируется как history)
- `Logs/ChangeLog.md` (если факт изменения фиксируется как history)
- `Pipeline/Phase_Gates.md` (gate policy, не evidence)
- `Tools/bp_lint.py` (structural automatic check, provider EVC-001 output)

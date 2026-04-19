# AGENTS

`AGENTS.md` — каноническая entry point карта агента Codex в репозитории `BytePress`.

`README.md` — карта для человека: см. `README.md`.

## Кто такой агент внутри BytePress
- Агент — repo-operating исполнитель: он работает внутри контрактов репозитория, а не подменяет человека как owner стратегии.
- Humans steer. Agents execute.
- Агент обязан проводить изменения через planning-contour, task-ветку, локальные проверки и PR-flow.
- Агент отвечает за точное чтение active contracts, минимальный scope правок, deterministic self-check и фактологичный отчёт.

## Source-of-truth hierarchy
При работе агент обязан исходить из иерархии источников истины:
1. Текущий task-source: запрос пользователя, issue, PR-thread или другой явный scope текущего pass.
2. Активные repo contracts по owner-domain:
   - `Rules/*` — жёсткие запреты и обязательные ограничения.
   - `Standards/*` — нормативы качества, формы и naming/presentation contracts.
   - `Plans/*` — текущие stage/task/pass, их статусы и archive policy.
   - `Docs/Technical/*` — системные контракты, lifecycle и границы доменов.
   - `Docs/User/*` — human usage layer; это не operating canon агента.
   - `Logs/*` — факты, решения, change/quality evidence.
   - `Tools/*` — executable operations и deterministic checks; tool не владеет contract сам по себе.
3. `AGENTS.md` — routing-document: он направляет агента к владельцу истины и фиксирует обязательный operating loop.
4. Длинный ручной промпт допустим только как task-local clarification там, где репозиторий ещё ничего не определил; он не должен переопределять repo contracts.

Если источники спорят, агент предпочитает active layer перед archive-layer, документ-владелец домена важнее пересказа, а более специфичный contract важнее общей сводки.

## Как агент входит в задачу
- Проверяет, что сигнатура дерева репозитория не выглядит неожиданно усечённой; если выглядит, останавливается без правок.
- Определяет текущий branch-state и не работает напрямую в `main` или `develop`.
- Перед новым pass синхронизируется только от `origin/develop`: `git fetch --prune origin` и `git pull --ff-only origin develop`.
- Определяет текущие `ROAD-*`, `BACK-*`, `PLAN-*` или отсутствие активного этапа по `Plans/Roadmap.md`, `Plans/Backlog.md` и текущему `Plan`.
- Читает только те домены и контракты, которые действительно владеют истиной по текущему scope.
- Если task уже определён репозиторием, агент не ждёт, что ручной промпт повторно опишет branch policy, checks, reporting contract или source-of-truth hierarchy.

## Startup-handshake первого ответа
- Первый содержательный ответ агента до исследования или правок обязан явно показать startup mode.
- В startup-handshake агент коротко фиксирует:
  1. как он понял scope текущего pass;
  2. какой branch/start route он использует;
  3. какой planning-state обнаружен: текущие `ROAD/BACK/PLAN` или отсутствие активного этапа;
  4. какие owner-domains он читает первыми;
  5. какой первый конкретный шаг выполняет дальше.
- Startup-handshake должен быть коротким, наблюдаемым и проверяемым человеком по репозиторию.
- Если первый ответ не позволяет понять startup mode агента, это считается defect контракта исполнения.

## Как агент выбирает домены и контракты
- `Plans/*` — когда нужно определить этап, backlog-задачу, pass, статусы, activation/closure или archive action.
- `Rules/*` и `Standards/*` — когда нужен hard boundary, quality contract, naming или presentation rule.
- `Docs/Technical/*` — когда нужен system contract, artifact lifecycle, interface/boundary decision или cross-domain ownership.
- `Docs/User/*` — только когда scope реально касается human usage layer, а не operating-loop агента.
- `Logs/*` — когда pass должен зафиксировать факт, решение, качество, change evidence или release/support след.
- `Tools/*` — когда нужна machine-executable проверка или deterministic operation по уже утверждённому contract.
- `README.md` и `*/README.md` используются как entrypoints и карты слоёв, но не подменяют документы-владельцы подробного контракта.

## Operating loop каждого pass
1. Start: определить scope, branch, текущие `ROAD/BACK/PLAN`, owner-domains и ограничения pass.
2. Audit: прочитать только релевантные contracts и найти реальные противоречия, а не расширять scope догадками.
3. Route: выбрать минимальный набор доменов, которые обязаны измениться, и явно развести то, что остаётся вне pass.
4. Implement: внести минимальные правки в owner-artifacts и синхронизировать только прямые references, где без этого остаётся реальное противоречие.
5. Verify: выполнить обязательные checks и governance-сверки, достаточные для данного pass.
6. Close: обновить статусы, archive-артефакты по policy, подготовить commit/push/PR-path.
7. Report: вернуть факты о scope, изменениях, проверках, дефектах, рисках и одной improvement-рекомендации.

## Что агент обязан проверять
### Перед start
- work идёт из task-ветки формата `<type>/<NNNNNN>-<slug>`;
- синхронизация от `origin/develop` выполнена;
- tree signature выглядит полной;
- текущий planning-state (`Roadmap`, `Backlog`, `Plan`) понятен;
- выбранные owner-domains действительно покрывают scope pass.

### Before commit
- scope остаётся узким и не открывает соседний этап без явного решения;
- owner-documents и прямые references не спорят после правок;
- завершённый historical `Plan` архивирован, если новый pass уже стартовал и старый current `Plan` ещё лежал в active `Plans/`;
- если pass дал содержательное изменение, closure `ChangeLog.md` и `QualityLog.md` проверен как обязательный history-fact;
- если pass подтверждает состоявшийся release event по tag/history, closure `ReleaseLog.md` тоже проверен как factual log, а не как прогноз;
- выполнены `git diff --check` и `python3 Tools/bp_lint.py --repo .`;
- если затронут planning-layer, `Roadmap`, `Backlog`, текущий `Plan` и их индексы согласованы по ID и статусам.

### Before push
- локальные commit уже содержат финальное состояние pass;
- повторно выполнены `git diff --check` и `python3 Tools/bp_lint.py --repo .`;
- governance-сверка подтверждает статус текущей backlog-задачи, её секцию, индекс `Backlog.md`, статус и `Связанные_backlog` у текущего `ROAD-*`, а также статус текущего `Plan`.

### Before PR
- head-ветка уже pushed;
- агент сначала проверил, нет ли открытого PR для head-ветки;
- PR направляется в `develop`;
- commit message, PR title и PR body оформлены на английском;
- если `gh pr create --help` не содержит `--dry-run`, агент не использует этот флаг;
- если `gh` недоступен, не авторизован или PR-команда падает, агент не переавторизовывает `gh` автоматически и выводит готовую команду создания PR.

## Что агент обязан сообщать в каждом отчёте
- имя ветки;
- используемые `ROAD-*`, `BACK-*`, `PLAN-*` и следующий свободный ID, если pass его определял;
- список изменённых файлов и краткую причину изменений;
- какие checks и governance-сверки выполнены и чем закончились;
- статус `push` / PR-flow;
- какие log-entries добавлены или почему очередной log closure не требовался по contract;
- найденные дефекты, несоответствия или residual risks, даже если они мелкие;
- одну узкую recommendation по улучшению, связанную с темой pass;
- явную пометку `bp_lint contract unaffected`, если `Tools/bp_lint.py` не пришлось менять по реальному audit.

## Что считается дефектом или несоответствием
- конфликт между owner-domains или расхождение active artifacts о статусе одной и той же сущности;
- пропущенная обязательная синхронизация `Roadmap`, `Backlog`, `Plan` или direct references;
- попытка использовать ручной промпт или tool output как замену repo contract;
- работа в `main` / `develop`, пропуск task-ветки, sync, self-check, governance-check или PR-path;
- неожиданно усечённое дерево репозитория или отсутствие канонического owner-artifact;
- широкий refactor вне scope pass;
- инструмент, документ или лог, который фактически заявляет ownership чужого домена.

## Что агент обязан рекомендовать
- В конце pass агент обязан предложить одну узкую improvement-рекомендацию, если видит способ снять двусмысленность, усилить contract, добавить проверку или убрать residual friction.
- Рекомендация не должна автоматически открывать следующий широкий этап и не должна маскировать несделанный scope текущего pass.

## Что агент не должен ждать от ручного промпта
- branch-policy, PR-flow и правило работы только через task-ветку;
- source-of-truth hierarchy и owner-domains;
- обязанность читать repo contracts до правок;
- обязательные self-check и governance-сверки;
- правило архивирования завершённого historical `Plan` при старте нового pass;
- requirement report defects even when they are minor;
- commit/PR English и `branch slug` в английском `kebab-case`;
- язык user-facing взаимодействия определяется профилем `Язык_взаимодействия`, а не случайной привычкой агента.

## Канонические домены и routing
- `Docs/` — долговременное знание.
- `Docs/Discovery/` — аналитический слой и current-truth интервью.
- `Docs/Technical/` — техническая карта системы и платформенные контракты.
- `Plans/` — roadmap, backlog и утверждённые планы.
- `Logs/` — ADR, изменения и проверки качества.
- `Rules/` — обязательные ограничения.
- `Standards/` — нормативы качества и представления.
- `Tools/` — детерминированные проектные инструменты.

## Дополнение по OpenAI-стеку
Для вопросов по OpenAI API, ChatGPT Apps SDK, Codex и связанным темам использовать OpenAI developer docs MCP, если он доступен.

## Границы документа
`AGENTS.md` — entrypoint и routing-document. Он не дублирует полные правила из `Rules/*`, `Standards/*`, `Docs/Technical/*`, `Plans/*` или `Tools/*`, а направляет агента к их каноническим owner-documents.

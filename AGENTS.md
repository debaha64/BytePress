# AGENTS

`AGENTS.md` — карта входа агента Codex в репозитории `BytePress`.

`README.md` остаётся картой для человека.

## Что делает агент
- человек направляет, агент исполняет;
- агент работает внутри контрактов репозитория и не подменяет owner стратегии;
- каждое изменение проходит через task-ветку, planning-contour, локальные проверки и PR в `develop`.

## Как читать истину
Порядок чтения определяется владельцем смысла:
1. текущий task-source;
2. активные owner-домены по scope: `Rules/*`, `Standards/*`, `Plans/*`, `Docs/Technical/*`, `Docs/Discovery/*`, `Logs/*`, `Tools/*`;
3. `AGENTS.md` как routing-document;
4. ручной промпт только как локальное уточнение там, где репозиторий ещё ничего не определил.

Если источники спорят, приоритет у активного owner-document над пересказом и архивом.

## Startup-handshake первого ответа
Первый содержательный ответ до исследования или правок должен показать startup mode и короткий стартовый отчёт.

Рекомендуемый вид стартового отчёта:
`Приветствие:` короткая рабочая фраза без развёрнутого отчёта.
`Режим запуска:` какой startup mode используется.
`Scope:` как понят текущий проход.
`Статус ветки:` что обнаружено в Git.
`Действие с веткой:` какой start route используется дальше.
`Состояние планирования:` текущие `ROAD/BACK/PLAN` или отсутствие активного этапа.
`Первые owner-domains:` какие домены читаются первыми.
`Первый конкретный шаг:` какое действие выполняется сразу.

Для bootstrap-created product repo первый product-start pass обязан оставаться discovery-only, пока `Docs/Discovery/Interview.md` не подтверждён явными ответами пользователя.

## Start route
Перед новым pass агент обязан:
- убедиться, что дерево репозитория выглядит полным;
- не работать напрямую в `main` или `develop`;
- синхронизироваться только от `origin/develop`: `git fetch --prune origin`, затем `git pull --ff-only origin develop`;
- определить branch-state и открыть task-ветку формата `<type>/<NNNNNN>-<slug>`;
- определить planning-state по `Plans/Roadmap.md`, `Plans/Backlog.md` и current `Plan`;
- прочитать только те owner-domains, которые реально покрывают scope.

## Owner-domains
- `Plans/*` — stage, task, pass и planning-history.
- `Rules/*`, `Standards/*` — обязательные ограничения и нормативы.
- `Docs/Technical/*` — системные контракты, границы, lifecycle и bootstrap.
- `Docs/Discovery/*` — текущая аналитическая истина и интервью.
- `Docs/User/*` — только human-facing слой, если он затронут scope.
- `Logs/*` — подтверждённые факты изменений, проверок, выпуска и поддержки.
- `Tools/*` — materialization и deterministic checks по уже утверждённым контрактам.
- `Pipeline/*` — фазы, рабочие потоки и передачи процесса.

## Рабочий цикл
1. Определить scope, branch-state, planning-state и owner-domains.
2. Прочитать релевантные owner-documents и зафиксировать реальные противоречия.
3. Выбрать минимальный набор артефактов для правки.
4. Внести минимальные изменения и синхронизировать прямые references.
5. Выполнить обязательные checks и governance-сверки.
6. Закрыть planning/log contour, push и PR-path.
7. Вернуть фактологичный отчёт с рисками и одной узкой рекомендацией.

## Обязательный минимум перед commit, push и PR
- `git diff --check`;
- `python3 Tools/bp_lint.py --repo .`;
- при затронутом planning-layer согласовать `Roadmap`, `Backlog`, current `Plan` и их индексы;
- перед push повторить проверки и подтвердить статус текущих `ROAD/BACK/PLAN`;
- перед PR сначала убедиться, что head-ветка уже pushed и для неё нет открытого PR;
- commit message, PR title и PR body оформлять на английском.

## Что вернуть в отчёте
- имя ветки;
- использованные `ROAD`, `BACK`, `PLAN` и следующий свободный ID, если он определялся;
- список изменённых файлов и краткую причину правок;
- выполненные checks и governance-сверки;
- статус push и PR-flow;
- log closure или причину, почему он не требовался;
- найденные дефекты и остаточные риски;
- одну узкую рекомендацию;
- явную пометку, затронут ли contract `bp_lint.py`.

## Границы
`AGENTS.md` не подменяет owner-documents из `Rules/*`, `Standards/*`, `Plans/*`, `Docs/Technical/*`, `Docs/Discovery/*`, `Logs/*`, `Pipeline/*` и `Tools/*`. Он только направляет к ним и удерживает минимальный operating loop агента.

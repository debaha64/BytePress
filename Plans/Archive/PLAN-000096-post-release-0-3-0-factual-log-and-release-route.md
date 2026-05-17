# PLAN-000096 — Фактический выпуск BytePress 0.3.0 и post-release маршрут

ID: PLAN-000096
Название: Фактический выпуск BytePress 0.3.0 и post-release маршрут
Статус: Завершено
Связи: ROAD-000042, BACK-000107, CHG-000108, QL-000103, RL-000009
Источник: Запрос владельца от 2026-05-18
Дата_создания: 2026-05-18
Дата_изменения: 2026-05-18
Основание: Владелец запросил узкий post-release проход после выпуска BytePress `0.3.0`: зафиксировать фактический внешний выпуск, синхронизировать плановый и журнальный контур и уточнить release/post-release маршрут после squash merge.
Связанные_требования:
Связанные_backlog: BACK-000107
Связанные_ADR: нет

## Текущая истина
- `PR #108` — Release BytePress `0.3.0`, принят в `main`.
- Commit выпуска в `main`: `56767aaa8208ebfb125afd00ac0b6d57e0fa0a98`.
- Tag `0.3.0` указывает на `56767aaa8208ebfb125afd00ac0b6d57e0fa0a98`.
- `git cat-file -t 0.3.0` вернул `commit`, поэтому tag фиксируется как фактическая ссылка на commit без утверждения, что tag annotated.
- `PR #109` — Sync develop with main after `0.3.0` release, принят в `develop`.
- `origin/main` и `origin/develop` совпадают по дереву.
- `origin/main` и `origin/develop` не находятся в ancestor-отношении ни в одну сторону после squash/post-release sync.
- `RL-000008` остаётся записью о готовности выпуска, а factual external release фиксируется отдельно в `RL-000009`.
- Product bootstrap, `Tools/bp_bootstrap.py` и данные тестовых продуктов не входят в область прохода.

## Шаги
1. Синхронизироваться от `origin/develop` и открыть рабочую ветку `docs/000096-post-release-0-3-0-factual-log-and-release-route`.
   - DoD: проход выполняется не в `develop` и не в `main`.
2. Подтвердить Git-факты выпуска и post-release sync.
   - DoD: commit, tag, деревья и ancestry-отношение проверены локальными Git-командами.
3. Открыть и закрыть `ROAD-000042`, `BACK-000107` и `PLAN-000096`.
   - DoD: активных задач после закрытия прохода нет.
4. Зафиксировать `RL-000009`, `CHG-000108` и `QL-000103`.
   - DoD: factual release event отделён от release-readiness `RL-000008`.
5. Уточнить release/post-release маршрут.
   - DoD: договор описывает release PR в `main`, tag после merge в `main`, sync `develop` после выпуска, допустимый sync через отдельный PR при запрете force-push и допустимое отличие истории после squash merge.
6. Выполнить обязательные проверки и подготовить PR в `develop` через `gh`.
   - DoD: `git diff --check` и `python3 Tools/bp_lint.py --repo .` пройдены, ветка отправлена один раз, PR создан через `gh`.

## Риски
- Если проект захочет требовать ancestry между `main` и `develop`, это будет отдельное решение о merge strategy, а не следствие текущего post-release договора.
- Squash merge может сохранять одинаковое дерево при разной истории; такой результат не считается дефектом в текущем договоре.
- Фактический release tag `0.3.0` не называется annotated, потому что локальная проверка подтвердила тип `commit`.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000042.md`
- `Plans/Archive/PLAN-000096-post-release-0-3-0-factual-log-and-release-route.md`
- `Logs/ReleaseLog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `Rules/Git.md`
- `Pipeline/Workflows.md`
- `Docs/Technical/Platform_Contracts.md`
- `Setup_Guide.md`

## DoD
Фактический внешний выпуск `0.3.0` отражён в `RL-000009`, плановый и журнальный контур закрыт, release/post-release маршрут уточнён без нового ADR и без изменения product bootstrap, обязательные проверки пройдены, PR подготовлен через `gh`.

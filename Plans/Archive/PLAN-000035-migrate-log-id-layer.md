# PLAN-000035 — Migrate log ID layer

ID: PLAN-000035
Название: Привести `Logs/*` и ссылочный слой журналов к unified `ID scheme`
Статус: Завершено
Связи: BACK-000047
Источник: Narrow log-layer migration pass inside `ROAD-000009`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: Planning-contour уже завершён, а unified `ID scheme` для репозитория утверждена, но log-layer остаётся не полностью согласованным: `ADRlog`, `ChangeLog` и `QualityLog` уже несут serial entry IDs, тогда как `ReleaseLog` остаётся на старом коротком `RL-*` pattern без доведения до общего contract. Нужен отдельный pass, который приведёт `Logs/*` к уже принятой модели без redesign других доменов.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000047
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать scope log-layer pass внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для migration `ID` и ссылочного слоя `Logs/*`.
   - DoD: `BACK-000047` и `PLAN-000035` описывают только log-layer migration без открытия других доменов.
2. Определить и применить минимальную migration model для `Logs/*`.
   - Описание: Оставить journal files singleton-документами, а log entries привести к serial `ID` там, где это уже вытекает из принятого contract.
   - DoD: log entries не спорят между собой по формату `ID`, а singleton log-files не сериализуются искусственно.
3. Синхронизировать реально затронутые ссылки и active references.
   - Описание: Обновить только те path/reference места, которые реально ломаются или становятся противоречивыми после migration log-layer.
   - DoD: active-layer не содержит broken или устаревших ссылок на log IDs и log files.
4. Обновить минимально необходимые contracts.
   - Описание: Уточнить `Standards/Naming.md` и при необходимости связанные active docs только там, где log contract был недостаточно явным.
   - DoD: naming/planning-facing слой описывает фактически реализованную log model без redesign других доменов.
5. Подтвердить границы contract checks.
   - Описание: Оценить, требует ли migrated log-layer обновления `bp_lint.py`, и менять его только при доказанной необходимости.
   - DoD: `bp_lint.py` синхронизирован только если реально нужен новый structural check, либо зафиксирован вывод `bp_lint contract unaffected`.

## Ограничения
- без migration `ID` для `Rules`, `Standards`, `Templates`, `Schemas`, `Roles`, `Profiles`, `Docs/*`, `Pipeline/*` и остальных доменов;
- без изменения active/archive layout для `Plans`;
- без изменения backlog archive layout;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`;
- без создания новой модели `Logs`, если текущий contract уже позволяет минимальную migration.

## Риски
- если log entries не довести до единого serial pattern, unified `ID scheme` останется частично декларативной и не исполненной на active log-layer;
- если сериализовать сами log-files вместо log entries, pass выйдет за пределы принятого singleton contract;
- если не синхронизировать реально затронутые references, репозиторий оставит сломанные или двусмысленные ссылки на migrated log IDs.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/Archive/PLAN-000035-migrate-log-id-layer.md`
- `Logs/*`
- `Standards/Naming.md`
- `Standards/Planning.md`
- `Plans/README.md`

## DoD
- создана одна узкая backlog-задача только для migration `ID` и ссылочного слоя `Logs/*`.
- создан новый текущий `Plan` только под этот pass.
- `Logs/*` приведены к unified `ID scheme` в реально необходимом объёме.
- все реально затронутые ссылки на log-layer синхронизированы.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Фактический результат
- `BACK-000047` и `PLAN-000035` зафиксировали только узкий pass по migration log-layer без открытия других доменов.
- `Logs/QualityLog.md` получил явные `ID:` для всех serial quality entries, а `Logs/ReleaseLog.md` переведён на шестизначный `RL-<NNNNNN>` contract с явными внутренними `ID`.
- singleton log-files остались singleton-артефактами: migration затронула только serial entry layer и не вводила serial filenames для `Logs/*`.
- `Standards/Naming.md` и `Logs/README.md` синхронизированы с фактически реализованной log model и правилом ссылок на singleton log-files и их serial entries.
- `bp_lint.py` не менялся, потому что structural contract репозитория и обязательный file set log-layer не изменились; `bp_lint contract unaffected`.

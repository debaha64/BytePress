# PLAN-000033 — Archive backlog history layer

ID: PLAN-000033
Название: Вывести historical backlog прошлых этапов в archive layer
Статус: В_работе
Связи: BACK-000045
Источник: Narrow backlog archive pass inside `ROAD-000009`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: После migration plan-files planning-contour всё ещё спорит с целевой моделью backlog-layer: historical backlog прошлых этапов остаётся в активном `Plans/Backlog.md`, хотя active backlog уже должен хранить только текущий этап. Нужен отдельный pass, который введёт archive layout для backlog history-layer, выведет backlog прошлых этапов из active layer и не затронет остальные домены.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000045
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать текущий scope внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для archive migration historical backlog.
   - DoD: `BACK-000045` и `PLAN-000033` описывают только backlog history-layer и не открывают migration других доменов.
2. Ввести archive layout для backlog history-layer.
   - Описание: Создать `Plans/Archive/Backlog/` и вывести backlog прошлых этапов из активного `Plans/Backlog.md` в stage archive files.
   - DoD: historical backlog прошлых этапов больше не находится в active `Plans/Backlog.md`, а лежит в `Plans/Archive/Backlog/`.
3. Оставить в active backlog только текущий этап.
   - Описание: Пересобрать `Plans/Backlog.md` так, чтобы active file содержал только `ROAD-000009`, его индекс и при необходимости короткую навигацию к archive backlog.
   - DoD: активный `Backlog.md` не смешивает текущий этап с historical backlog и не превращается в index всей истории.
4. Синхронизировать минимально необходимые contracts.
   - Описание: Обновить `Standards/Planning.md`, `Plans/README.md` и `Standards/Naming.md` только там, где это нужно для уже реализованного backlog archive-layer.
   - DoD: contract planning-layer описывает фактически реализованное active/archive состояние backlog без открытия нового redesign.
5. Подтвердить границы contract checks.
   - Описание: Оценить, требует ли backlog archive-layer обновления `bp_lint.py`, и внести только минимально необходимое изменение при доказанной необходимости.
   - DoD: `bp_lint.py` синхронизирован только там, где это действительно нужно для нового backlog archive layout, либо зафиксирован вывод `bp_lint contract unaffected`.

## Ограничения
- без migration `ID` для logs, rules, standards, templates, schemas и остальных доменов;
- без изменения plan archive layout;
- без удаления `Runtime/Plan.md`;
- без широкого переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`;
- без больших structural moves вне backlog history-layer и минимально необходимых ссылок.

## Риски
- если historical backlog останется в активном `Plans/Backlog.md`, active layer продолжит спорить с уже принятым planning-contract;
- если stage archive files потеряют порядок или traceability, backlog history перестанет быть проверяемой;
- если contract documents не синхронизировать, репозиторий снова будет одновременно утверждать две разные модели backlog-layer.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Roadmap.md`
- `Plans/PLAN-000033-archive-backlog-history-layer.md`
- `Plans/Archive/Backlog/*`
- `Standards/Planning.md`
- `Plans/README.md`
- `Standards/Naming.md`

## DoD
- создана одна узкая backlog-задача только для archive migration historical backlog.
- создан новый текущий `Plan` только под этот pass.
- historical backlog прошлых этапов migrated в `Plans/Archive/Backlog/`.
- в активном `Plans/Backlog.md` остался только текущий этап `ROAD-000009`.
- `python3 Tools/bp_lint.py --repo .` проходит.

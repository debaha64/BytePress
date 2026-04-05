# PLAN-000029 — Activate ROAD-000009 operating model pass

ID: PLAN-000029
Название: Активировать первый governance-pass операционной модели ROAD-000009
Статус: Завершено
Связи: BACK-000041
Источник: First governance-pass of the new BytePress operating model
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: После завершения `ROAD-000008` следующий этап должен стартовать не через `Docs/User/*` или большой technical rewrite, а через короткий governance-pass, который закрепит новую операционную модель `BytePress`: `stage / task / pass`, ownership состояния, lifecycle `Plan`, неканоничность `Runtime/Plan.md` и hard-close contour задачи.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000041
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать `ROAD-000009` как новый текущий этап.
   - Описание: Обновить `Roadmap` и `Backlog` так, чтобы текущий стратегический горизонт начинался с operating model pass, а не с foundation/user layer.
   - DoD: `ROAD-000009` имеет новый смысл, статус `В_работе` и реальную связанную backlog-задачу `BACK-000041`.
2. Зафиксировать узкий scope первого governance-pass.
   - Описание: Создать отдельную backlog-задачу и текущий plan-file только для фиксации терминологии, ownership состояния, lifecycle `Plan`, правила для `Runtime/Plan.md` и hard-close contour.
   - DoD: `BACK-000041` и `PLAN-000029` описывают только этот pass без ID migration, без массового архива и без переписывания `AGENTS.md`.
3. Синхронизировать planning-contract на минимально необходимом уровне.
   - Описание: Обновить `Standards/Planning.md`, `Plans/README.md` и при необходимости терминологический слой без расширения scope на весь technical layer.
   - DoD: contract `этап / задача / проход`, ownership состояния и lifecycle `Plan` зафиксированы в каноне.
4. Подтвердить границы изменения для tooling.
   - Описание: Оценить, требует ли новый contract изменения `bp_lint.py`, и менять инструмент только при доказанной необходимости.
   - DoD: зафиксирован явный вывод `bp_lint contract unaffected` либо внесено минимально необходимое изменение.

## Ограничения
- без полной migration `ID`;
- без массового переименования plan-files;
- без физического переноса historical `Plan` в архив;
- без переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`;
- без удаления historical layer сверх минимально нужной синхронизации.

## Риски
- смешение `stage`, `task` и `pass` сохранит двусмысленность ownership и снова размоет planning-contract;
- преждевременное превращение pass в большой technical rewrite выведет работу за согласованный scope;
- некорректное закрытие backlog-задачи без сверки `Roadmap`, `Backlog` и `Plan` оставит governance-контур несогласованным.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/PLAN-000029-activate-road-000009-operating-model-pass.md`
- `Standards/Planning.md`
- `Plans/README.md`
- `Docs/Terms/TERM-000007-roadmap.md`
- `Docs/Terms/TERM-000008-backlog.md`
- `Docs/Terms/TERM-000009-plan.md`

## DoD
- `ROAD-000009` активирован как текущий этап в новом смысле.
- `ROAD-000010` переведён на новый технический смысл, а дальний горизонт согласован без избыточной детализации.
- в активном `Backlog` отражены только задачи текущего этапа, а текущий pass оформлен как `BACK-000041`.
- `Plan` описывает только один pass и не владеет глобальным статусом этапа или backlog.
- `Runtime/Plan.md` явно выведен из канона как неисточник истины.
- hard-close contour задачи зафиксирован на контрактном уровне.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Фактический результат
- `ROAD-000009` активирован как первый governance-pass новой operating model `BytePress`, а `ROAD-000010` переопределён как следующий technical-layer stage.
- `BACK-000041` зафиксировал узкий pass только на терминологию, ownership состояния, lifecycle `Plan`, неканоничность `Runtime/Plan.md` и hard-close contour задачи.
- `Standards/Planning.md`, `Plans/README.md` и связанные planning-terms синхронизированы минимально необходимым объёмом.
- `bp_lint.py` не менялся, потому что новый pass меняет contract смыслов и ownership, но не обязательный набор путей, шаблонов или файловых проверок; `bp_lint contract unaffected`.

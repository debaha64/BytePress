# PLAN-000030 — Align roadmap and planning transition

ID: PLAN-000030
Название: Снять противоречия между planning-каноном и переходным состоянием репозитория
Статус: Завершено
Связи: BACK-000042
Источник: Corrective pass after merge of `docs/000034-activate-road-000009-operating-model`
Дата_создания: 2026-04-06
Дата_изменения: 2026-04-06
Основание: После первого governance-pass `ROAD-000009` новый planning-канон уже зафиксирован, но `Roadmap`, `Backlog`, `Plans/README.md`, `Standards/Planning.md` и `Standards/Naming.md` ещё создают видимость, будто целевое устройство уже полностью материализовано в дереве. Нужен короткий corrective pass, который разведёт целевую модель и переходное legacy-состояние без migration `ID`, без переименования historical `BP-*` plan-files и без физического вывода historical backlog-записей в архив.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000042
Связанные_ADR:
- отсутствуют

## Шаги
1. Довести `Roadmap` до утверждённого горизонта `ROAD-000009`–`ROAD-000014`.
   - Описание: Обновить формулировки этапов так, чтобы `ROAD-000009` и следующие этапы полностью соответствовали уже утверждённому новому стратегическому горизонту.
   - DoD: `ROAD-000009`–`ROAD-000014` согласованы с принятым каноном и не распадаются на мелкие шаги.
2. Зафиксировать corrective task и текущий pass внутри `ROAD-000009`.
   - Описание: Добавить одну реальную backlog-задачу и один новый текущий `Plan` только для устранения противоречий planning-transition.
   - DoD: `BACK-000042` и `PLAN-000030` описывают только этот corrective pass и не открывают migration historical layer.
3. Развести целевую модель и transitional state в planning-contract.
   - Описание: Обновить `Standards/Planning.md`, `Plans/README.md` и `Standards/Naming.md`, не меняя сам legacy-слой физически.
   - DoD: целевая модель, transitional policy и legacy-исключения явно разделены и больше не противоречат текущему дереву.
4. Подтвердить границы contract changes для tooling.
   - Описание: Оценить, нужно ли менять `bp_lint.py`, и менять его только при реальном изменении проверочного контракта.
   - DoD: зафиксирован вывод `bp_lint contract unaffected` либо внесено минимально необходимое изменение.

## Ограничения
- без migration `ID`;
- без переименования historical `BP-*` plan-files;
- без физического переноса historical `Plan` в `Plans/Archive/`;
- без физического вывода historical backlog-задач из `Plans/Backlog.md`;
- без удаления `Runtime/Plan.md`;
- без переписывания `Docs/Technical/*`, `AGENTS.md` и `Docs/User/*`.

## Риски
- если не развести target-state и transitional state явно, planning-contract продолжит спорить с фактическим деревом и будет вводить в заблуждение следующий pass;
- преждевременная migration historical layer выведет corrective pass за согласованный scope;
- если текущий `Plan` не использовать по целевому filename-contract, противоречие между target naming model и текущей практикой останется открытым.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000030-align-roadmap-and-planning-transition.md`
- `Standards/Planning.md`
- `Plans/README.md`
- `Standards/Naming.md`

## DoD
- `ROAD-000009`–`ROAD-000014` полностью согласованы с утверждённым горизонтом.
- `ROAD-000009` остаётся текущим активным этапом.
- создана одна узкая corrective backlog-задача `BACK-000042`.
- создан новый текущий `Plan` только под corrective pass.
- целевая модель и transitional policy явно разведены.
- `Runtime/Plan.md` описан как legacy/non-canonical artifact.
- `python3 Tools/bp_lint.py --repo .` проходит.

## Фактический результат
- `Roadmap` доведён до утверждённого горизонта: `ROAD-000011` теперь означает verification contour, `ROAD-000012` — agent entry point and user layer, `ROAD-000013` — product repo replication and baseline `0.2.0`, `ROAD-000014` — integration layer and future extensions.
- `BACK-000042` и `PLAN-000030` зафиксировали только corrective pass на выравнивание planning-transition без migration historical layer.
- `Standards/Planning.md`, `Plans/README.md` и `Standards/Naming.md` теперь явно разводят целевой active layer и текущее legacy/transitional состояние дерева.
- `bp_lint.py` не менялся, потому что pass не меняет обязательный набор путей или файловых структур, а только уточняет planning-contract и transitional policy; `bp_lint contract unaffected`.

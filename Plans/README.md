# Plans

`Plans/` хранит roadmap, backlog, текущий canonical `Plan` и historical planning-layer.

## Состав
- `Roadmap.md` — дорожная карта крупных этапов уровня системы.
- `Backlog.md` — файл planning-backlog, в котором целевой active layer принадлежит текущему этапу.
- `Plans/PLAN-<NNNNNN>-<slug>.md` — целевой канонический формат имени plan-file для одного pass.
- `Plans/Archive/` — целевой архив завершённых `Plan` после управляемой архивации.
- `Plans/BP-*.md` — historical legacy `Plan`, которые остаются в каталоге до отдельной migration-задачи.

## Контракт именования
- числовая часть ID содержит 6 знаков;
- типовой префикс сущности сохраняется;
- `slug` оформляется в `kebab-case`;
- имя файла не дублирует родительский каталог;
- целевой типовой префикс текущего `Plan` — `PLAN`.
- repo-wide classes `serial / hybrid / singleton` и migration-order определяются в `Standards/Naming.md`.

## Целевая модель
Активный слой `Plans/` использует один текущий `Plan` в целевом filename-contract `Plans/PLAN-<NNNNNN>-<slug>.md`.

Текущий `Plan` описывает только один pass и не владеет глобальным статусом этапа или backlog.

В активном слое должен существовать только один текущий `Plan`; завершённые `Plan` должны переходить в `Plans/Archive/` отдельным управляемым lifecycle, без смешения с текущим pass.

Целевой active `Backlog` хранит задачи только текущего этапа, а статусы этапов принадлежат `Roadmap.md`.

## Переходное состояние
До отдельной migration-задачи репозиторий остаётся в transitional state:
- historical `BP-*` plan-files ещё физически лежат в `Plans/`;
- historical backlog-записи прошлых этапов ещё физически лежат в `Plans/Backlog.md`;
- `Runtime/Plan.md` ещё физически существует как legacy runtime draft.

Это legacy/transitional layer, а не канонический active planning-layer.

## Правило
`Runtime/Plan.md` не считается источником истины для плана, не является каноническим `Plan` и до отдельного pass остаётся только legacy-артефактом runtime-layer.

Целевая модель `Backlog.md` хранит только задачи текущего этапа; дальний горизонт и статусы этапов принадлежат `Roadmap.md`.

`Roadmap.md` не дублирует backlog и не перечисляет каждый документный или контрактный проход.

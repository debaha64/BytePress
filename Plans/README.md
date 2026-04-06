# Plans

`Plans/` хранит roadmap, активный backlog текущего этапа, текущий canonical `Plan` и historical planning-layer.

## Состав
- `Roadmap.md` — дорожная карта крупных этапов уровня системы.
- `Backlog.md` — active planning-backlog, который хранит только текущий этап.
- `Plans/PLAN-<NNNNNN>-<slug>.md` — целевой канонический формат имени plan-file для одного pass.
- `Plans/Archive/PLAN-<NNNNNN>-<slug>.md` — реализованный архив завершённых `Plan`.
- `Plans/Archive/Backlog/ROAD-<NNNNNN>.md` — реализованный архив backlog прошлых завершённых этапов.

## Контракт именования
- числовая часть ID содержит 6 знаков;
- типовой префикс сущности сохраняется;
- `slug` оформляется в `kebab-case`;
- имя файла не дублирует родительский каталог;
- целевой типовой префикс текущего `Plan` — `PLAN`.
- repo-wide classes `serial / hybrid / singleton` и migration-order определяются в `Standards/Naming.md`.

## Реализованный plan-layer
Активный слой `Plans/` использует один текущий `Plan` в filename-contract `Plans/PLAN-<NNNNNN>-<slug>.md`.

Текущий `Plan` описывает только один pass и не владеет глобальным статусом этапа или backlog.

В активном слое существует только один текущий `Plan`; завершённые `Plan` хранятся в `Plans/Archive/` и не смешиваются с текущим pass.

Активный `Backlog.md` хранит задачи только текущего этапа, а historical backlog прошлых этапов вынесен в `Plans/Archive/Backlog/`.

Статусы этапов и дальний горизонт принадлежат `Roadmap.md`.

## Реализованное состояние
Historical `Plan` больше не остаются в active `Plans/`: они migrated в `Plans/Archive/`.

Historical backlog прошлых этапов больше не остаётся в active `Plans/Backlog.md`: он migrated в `Plans/Archive/Backlog/`.

Planning-contour в рабочем дереве больше не использует отдельный runtime plan artifact.

## Правило
`Runtime/` остаётся только временным рабочим контекстом и не подменяет канонический `Plan`.

`Backlog.md` хранит только задачи текущего этапа; historical backlog хранится в `Plans/Archive/Backlog/`, а дальний горизонт и статусы этапов принадлежат `Roadmap.md`.

`Roadmap.md` не дублирует backlog и не перечисляет каждый документный или контрактный проход.

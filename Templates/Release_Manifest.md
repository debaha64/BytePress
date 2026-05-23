# Release Manifest Template

<!-- ID: TPL-000020 -->

ID: RELEASE-MANIFEST-<version>
Версия: <version>
Статус: Черновик | Проверено | Заменено
Дата_создания: <YYYY-MM-DD>
Дата_изменения: <YYYY-MM-DD>

## Плановый контур
- ROAD: `<ROAD-*>`
- BACK: `<BACK-*>`
- PLAN: `<PLAN-*>`

## Журнальный контур
- ReleaseLog: `<RL-*>`
- ChangeLog: `<CHG-*>`
- QualityLog: `<QL-*>`

## Источник архивных файлов
- Backlog: `<Plans/Archive/Backlog/ROAD-*.md>`
- Plan: `<Plans/Archive/Plans/PLAN-*.md>`

## Состав zip
- `MANIFEST.md`
- `Backlog/<ROAD-файл>`
- `Plans/<PLAN-файл>`

## Проверки
- Создание: `<команда или способ создания zip>`
- Целостность: `python3 -m zipfile -t <path>`
- Состав: `<команда или способ сверки namelist>`

## Границы
Zip содержит только manifest, архивный backlog и архивный plan релиза. Zip не является текущим источником истины и не заменяет `Logs/ReleaseLog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, tag или текущие owner-documents.

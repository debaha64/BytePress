# PLAN-000116 — Исправление release archive zip

ID: PLAN-000116
Название: Исправление release archive zip
Статус: Завершено
Связи: ROAD-000047, BACK-000128, CHG-000128, QL-000123
Источник: Запрос владельца от 2026-05-24
Дата_создания: 2026-05-24
Дата_изменения: 2026-05-24
Основание: Владелец подтвердил дефект `BACK-000127`: zip-пакеты `0.1.0`, `0.2.0` и `0.3.0` были созданы как полный source tree соответствующих tag. Требуемый release archive должен хранить только `MANIFEST.md`, архивный backlog и архивный plan релиза.
Связанные_требования:
- Удалить ошибочные zip-пакеты полного source tree и внешние каталоги release manifest.
- Создать `Plans/Archive/Releases/0.1.0.zip`, `Plans/Archive/Releases/0.2.0.zip`, `Plans/Archive/Releases/0.3.0.zip`.
- Каждый zip должен содержать только `MANIFEST.md`, `Backlog/<ROAD-файл>` и `Plans/<PLAN-файл>`.
- Перенести manifest template в `Templates/Release_Manifest.md`.
- Не переписывать историю Git.
- Не менять `Logs/ReleaseLog.md`, `bp_lint.py`, `bp_check.py` и product bootstrap.
- Не начинать `ROAD-000048`.
Связанные_backlog:
- BACK-000128
Связанные_ADR:
- ADR-000028 не создан
Артефакты:
- `Plans/Archive/Releases/0.1.0.zip`
- `Plans/Archive/Releases/0.2.0.zip`
- `Plans/Archive/Releases/0.3.0.zip`
- `Plans/Archive/Releases/README.md`
- `Templates/Release_Manifest.md`
- `Templates/README.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000047.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
Риски:
- Zip-пакеты являются историческим archive package и не заменяют текущие owner-documents, журналы или tag.
- Повторное изменение состава release archive после исправления требует отдельного прохода и явной проверки состава.
Определение_готовности:
- Ошибочные каталоги `Plans/Archive/Releases/0.1.0/`, `Plans/Archive/Releases/0.2.0/`, `Plans/Archive/Releases/0.3.0/` и `Plans/Archive/Releases/MANIFEST_TEMPLATE.md` удалены.
- Новые zip находятся в корне `Plans/Archive/Releases/`.
- `0.1.0.zip` содержит только `MANIFEST.md`, `Backlog/ROAD-000015.md`, `Plans/PLAN-000067-release-readiness-and-log-closure.md`.
- `0.2.0.zip` содержит только `MANIFEST.md`, `Backlog/ROAD-000016.md`, `Plans/PLAN-000068-sync-develop-after-release-0.2.0.md`.
- `0.3.0.zip` содержит только `MANIFEST.md`, `Backlog/ROAD-000042.md`, `Plans/PLAN-000096-post-release-0-3-0-factual-log-and-release-route.md`.
- Проверки zip и проверки репозитория пройдены.
- `ROAD-000047` остаётся `Завершено`, `ROAD-000048` не начат.

## Шаги
1. Удалить дефектные release package.
   - Описание: Удалить каталоги версий внутри `Plans/Archive/Releases/` и старый `MANIFEST_TEMPLATE.md`.
   - Определение_готовности: В release archive нет внешних manifest-каталогов и zip полного source tree.
2. Создать исправленные zip.
   - Описание: Сформировать zip из `MANIFEST.md`, архивного backlog и архивного plan каждого релиза.
   - Определение_готовности: Каждый zip содержит ровно три файла и не содержит source tree BytePress.
3. Перенести manifest template.
   - Описание: Добавить `Templates/Release_Manifest.md` и обновить `Templates/README.md`.
   - Определение_готовности: Шаблон находится в домене `Templates`, а release archive хранит только zip и README.
4. Закрыть плановый и журнальный контур.
   - Описание: Добавить `BACK-000128`, `PLAN-000116`, `CHG-000128`, `QL-000123` и подтвердить исправленное закрытие `ROAD-000047`.
   - Определение_готовности: `ROAD-000047` остаётся `Завершено`, `ROAD-000048` не начат.
5. Выполнить проверки и подготовить PR.
   - Описание: Выполнить обязательные проверки, сделать commit, отправить ветку и создать PR в `develop` через `gh`.
   - Определение_готовности: Проверки пройдены, ветка отправлена, PR создан.

## Итог
`BACK-000128` и `PLAN-000116` завершены. Дефект `BACK-000127` исправлен без переписывания истории Git: zip полного source tree удалены, новые release archive zip содержат только `MANIFEST.md`, архивный backlog и архивный plan релиза. `Templates/Release_Manifest.md` добавлен как доменный шаблон manifest. `ROAD-000047` остаётся `Завершено`, `ROAD-000048` не начат.

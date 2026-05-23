# PLAN-000112 — Архивный контур Plans

ID: PLAN-000112
Название: Архивный контур Plans
Статус: В_работе
Связи: ROAD-000047, BACK-000124
Источник: Запрос владельца от 2026-05-23
Дата_создания: 2026-05-23
Дата_изменения: 2026-05-23
Основание: Владелец запросил открыть `ROAD-000047` и выполнить `BACK-000124`: отделить архив завершённых планов от архива этапов, создать release archive и подготовить post-release очистку без zip-архивов.
Связанные_требования:
- Создать `Plans/Archive/Plans/`.
- Перенести завершённые `PLAN-*.md` из `Plans/Archive/` в `Plans/Archive/Plans/`.
- Создать `Plans/Archive/Releases/`.
- Добавить `Plans/Archive/Releases/README.md`.
- Описать назначение release archive и manifest.
- Обновить ссылки на архивные планы.
- Обновить владельцев смысла архивного контура.
- Оставить zip-архивацию следующим шагом внутри `ROAD-000047`, если для неё нужен отдельный manifest-договор.
- Не создавать zip-архивы.
- Не удалять журналы, правила, схемы, шаблоны и текущие owner-documents.
- Не менять product bootstrap.
- Не менять `bp_lint.py`.
- Не расширять `bp_check.py`, кроме минимальной синхронизации путей, если перенос планов ломает проверку.
- Не начинать `ROAD-000048`.
Связанные_backlog:
- BACK-000124
Связанные_ADR:
- ADR-000028 не создан
Артефакты:
- `Plans/README.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000047.md`
- `Plans/Archive/Plans/`
- `Plans/Archive/Releases/README.md`
- `Docs/Technical/Verification.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Pipeline/Workflows.md`
- `Tools/README.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
Риски:
- Массовый перенос архивных планов требует синхронизации прямых ссылок, иначе уровень `check` зафиксирует разрыв Markdown-ссылок.
Определение_готовности:
- Архив завершённых планов живёт в `Plans/Archive/Plans/`.
- Архив завершённых этапов остаётся в `Plans/Archive/Backlog/`.
- Release archive создан в `Plans/Archive/Releases/` и описывает manifest без zip-файлов.
- Прямые ссылки на архивные планы синхронизированы.
- `ROAD-000047`, `BACK-000124` и `PLAN-000112` согласованы.
- `ROAD-000048` не начат.
- Выполнены `git diff --check`, `python3 Tools/bp_lint.py --repo .`, `python3 Tools/bp_check.py --repo .` и `python3 Tools/bp_check.py --repo . --format json`.

## Шаги
1. Открыть плановый контур.
   - Описание: Перевести `ROAD-000047` в работу, завести `BACK-000124` и создать `PLAN-000112`.
   - Определение_готовности: `Plans/Roadmap.md`, `Plans/Backlog.md` и `PLAN-000112` согласованы.
2. Разделить архивы Plans.
   - Описание: Создать `Plans/Archive/Plans/`, перенести туда завершённые `PLAN-*.md` и обновить прямые ссылки.
   - Определение_готовности: В `Plans/Archive/` не остаётся завершённых `PLAN-*.md` на верхнем уровне, а локальные Markdown-ссылки указывают на новый путь.
3. Создать release archive.
   - Описание: Создать `Plans/Archive/Releases/README.md` и закрепить назначение release archive и manifest без zip-файлов.
   - Определение_готовности: Release archive описан как будущий проверяемый контур release package, а zip-архивация оставлена следующим шагом внутри `ROAD-000047`.
4. Синхронизировать владельцев смысла.
   - Описание: Обновить плановый, проверочный, процессный и инструментальный контуры только в части нового архивного пути.
   - Определение_готовности: `Plans/README.md`, `Docs/Technical/Verification.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Pipeline/Workflows.md` и `Tools/README.md` не спорят о структуре архива.
5. Закрыть проход.
   - Описание: Добавить `CHG-000124` и `QL-000119`, выполнить проверки и архивировать `PLAN-000112`.
   - Определение_готовности: Журналы содержат факты, проверки пройдены, `BACK-000124` и `PLAN-000112` завершены, `ROAD-000047` остаётся `В_работе`.

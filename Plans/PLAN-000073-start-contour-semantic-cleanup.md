# PLAN-000073 — Start contour semantic cleanup

ID: PLAN-000073
Название: Start contour semantic cleanup
Статус: В_работе
Связи: BACK-000085
Источник: Corrective pass after repeated `Minesweeper` field test
Дата_создания: 2026-04-24
Дата_изменения: 2026-04-24
Основание: Повторный аудит стартового контура после полевого теста подтвердил остаточные смысловые разрывы между термином `Каркас репозитория`, матрицей начального развёртывания, продуктовым `Base_Terms.md`, `AGENTS.md`, стартовым отчётом агента, интервью, картой жизненного цикла и фактическим bootstrap-result.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000085
Связанные_ADR:
- отсутствуют

## Шаги
1. Переоткрыть corrective planning-contour и зафиксировать owner-scope прохода.
   - DoD: `ROAD-000020`, `BACK-000085` и текущий `PLAN-000073` согласованы в active planning-layer.
2. Снять противоречия между термином `Каркас репозитория`, матрицей начального развёртывания, bootstrap-contract и фактическим `bp_bootstrap.py`.
   - DoD: default scaffold, будущие product-side расширения и BytePress-only domains разведены одинаково в терминологии, technical docs и bootstrap result.
3. Ввести минимальный стартовый пакет терминов и синхронизировать agent/discovery lifecycle раннего product-start.
   - DoD: generated product repo получает `Docs/Terms/Base_Terms.md` с реальным минимальным набором терминов, а `AGENTS.md`, стартовый отчёт, интервью и lifecycle/handoff map согласованы между owner-documents и tooling.
4. Обновить tooling и checks под исправленный контракт.
   - DoD: `bp_bootstrap.py`, generated repo templates и `bp_lint.py` materialize и проверяют только согласованный стартовый контур.
5. Подтвердить результат проверками и закрыть corrective pass.
   - DoD: repo lint, bootstrap smoke, generated repo lint, product-side smoke checks и branch-gate checks не подтверждают residual contradiction в scope pass.

## Ограничения
- не продолжать `Minesweeper`;
- не вводить optional bootstrap profiles;
- не копировать весь `BytePress` в generated product repo;
- не разворачивать новую тяжёлую process-subsystem вместо точечной корректировки owner-documents и checks;
- не расширять языковую чистку за пределы затронутых артефактов.

## Артефакты
- `AGENTS.md`
- `Docs/Discovery/*`
- `Docs/Terms/*`
- `Docs/Technical/*`
- `Pipeline/*`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000073-start-contour-semantic-cleanup.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- термин `Каркас репозитория` больше не спорит с матрицей bootstrap и generated result;
- generated product repo получает минимальный стартовый пакет терминов в `Docs/Terms/Base_Terms.md`;
- `AGENTS.md` остаётся короткой картой входа, а стартовый отчёт агента оформлен как короткий блок с приветствием и семью полями;
- owner протокола интервью один, остальные места сведены к ссылкам или кратким выдержкам;
- `Pipeline/*` содержит компактную карту жизненного цикла и передач без новой подсистемы;
- bootstrap, generated repo, docs и lint ведут себя одинаково в раннем product-start contour.

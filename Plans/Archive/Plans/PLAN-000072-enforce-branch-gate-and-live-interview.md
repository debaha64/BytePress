# PLAN-000072 — Enforce branch gate and live interview discipline

ID: PLAN-000072
Название: Enforce branch gate and live interview discipline
Статус: Завершено
Связи: BACK-000084
Источник: Corrective pass after blind field test of generated product repo
Дата_создания: 2026-04-22
Дата_изменения: 2026-04-22
Основание: Blind field test свежего generated product repo подтвердил два live-defect раннего product-start contour: первый writable action всё ещё мог происходить в `develop` без task-ветки, а живое интервью первого product-start pass не удерживало нумерованный и lettered/recommended format при узком delta-интервью.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000084
Связанные_ADR:
- отсутствуют

## Шаги
1. Переоткрыть corrective stage и зафиксировать новый planning pass.
   - DoD: `ROAD-000019`, `BACK-000084` и текущий `PLAN-000072` согласованы в active planning-layer.
2. Довести branch gate generated product repo до реального early product-start execution discipline.
   - DoD: generated repo требует task-ветку до любых writable changes, включая `Docs/Discovery/*`, `Plans/*` и `Logs/*`, а startup-handshake явно сообщает branch status и branch action.
3. Довести live interview contract до жёсткого structured format.
   - DoD: full interview и допустимый delta-интервью одинаково требуют нумерованные вопросы, буквенные варианты там, где выбор ограничен, и рекомендуемый вариант там, где это уместно.
4. Синхронизировать branch/interview rules между core contracts, generated repo, bootstrap и lint.
   - DoD: `AGENTS.md`, discovery docs, bootstrap/validation contracts, lifecycle и tooling не спорят друг с другом.
5. Подтвердить corrective result фактическим smoke bootstrap и закрыть pass.
   - DoD: repo lint, generated repo lint, smoke bootstrap, branch-gate smoke и delta-interview smoke подтверждают отсутствие residual ambiguity.

## Ограничения
- не открывать новый release contour;
- не смешивать corrective scope с разработкой `Minesweeper`;
- не вводить декоративную telemetry или новый tool family;
- не расширять generated product repo beyond минимально нужных contract sync.

## Артефакты
- `AGENTS.md`
- `Setup_Guide.md`
- `Docs/Discovery/*`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000072-enforce-branch-gate-and-live-interview.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- первый writable action в generated product repo больше не допускается без task-ветки;
- branch gate распространяется и на discovery/planning/log closure;
- startup-handshake и live branch discipline согласованы end-to-end;
- live interview contract удерживает lettered/recommended format даже для delta-интервью;
- bootstrap, generated repo, docs и lint не спорят друг с другом;
- smoke bootstrap проходит без residual ambiguity.

## Результат
- `ROAD-000019`, `BACK-000084` и `PLAN-000072` открыты и затем закрыты в одном corrective pass; active `Backlog` снова очищен, а current `Plan` выведен в archive-layer без автоматической активации нового `ROAD-*`.
- Core `AGENTS.md`, `Docs/Discovery/*`, `Product_Bootstrap_Contract.md`, `Product_Bootstrap_Validation.md`, `Artifact_Lifecycle.md`, `Setup_Guide.md`, `bp_bootstrap.py` и `bp_lint.py` теперь одинаково удерживают branch gate generated product repo: до task-ветки запрещён любой writable action, включая discovery/planning/log closure, а startup-handshake обязан сообщать branch status и branch action.
- Bootstrap-generated `AGENTS.md`, `Setup_Guide.md`, `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` и initial `Plan` теперь требуют task-ветку до первого writable action и не допускают свободноформатный delta-интервью при наличии structured choice.
- Фактический smoke bootstrap во временный target path `/tmp/bytepress-branch-gate-dyeQlM/repo` подтвердил, что generated repo структурно валиден после bootstrap, затем отклоняется lint'ом на ветке `develop`, проходит lint на task-ветке `feat/000001-confirm-current-truth`, а negative smoke свободноформатного delta-интервью падает с ошибкой `missing delta-interview format contract`.

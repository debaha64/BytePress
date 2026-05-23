# PLAN-000071 — Domain bootstrap strategy and interview gate

ID: PLAN-000071
Название: Domain bootstrap strategy and interview gate
Статус: Завершено
Связи: BACK-000083
Источник: Corrective pass after repeated `Minesweeper` field test
Дата_создания: 2026-04-21
Дата_изменения: 2026-04-21
Основание: Повторный полевой тест generated product repo на `Minesweeper` подтвердил системный разрыв раннего product-start contour: bootstrap replication matrix остаётся неполной на уровне top-level domains, незаполненный discovery всё ещё слишком легко трактуется как implicit approval для implementation, startup-handshake остаётся недостаточно управляемым в живом product-start behavior, а canonical failed-start reset/cleanup route не оформлен.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000083
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать planning activation для corrective stage.
   - DoD: `ROAD-000019`, `BACK-000083` и текущий `PLAN-000071` согласованы в active planning-layer.
2. Принять каноническую domain replication matrix для всех top-level доменов `BytePress`.
   - DoD: owner-documents явно классифицируют каждый top-level domain как `Default`, `Optional`, `Later product-pass` или `BytePress-only`.
3. Усилить hard first product-start gate и reset route в generated repo, bootstrap и lint.
   - DoD: без ответов пользователя generated repo остаётся в discovery-only contour, а failed product-start имеет canonical cleanup route.
4. Подтвердить corrective result фактическим smoke bootstrap.
   - DoD: temporary generated repo соответствует принятой matrix, проходит lint и не трактует незаполненный discovery как разрешение на implementation.
5. Закрыть stage в одном pass.
   - DoD: `Roadmap`, `Backlog`, archive actions, `ChangeLog`, `QualityLog`, `git diff --check`, repo lint, smoke bootstrap и PR-flow завершены без residual contradiction.

## Ограничения
- не открывать новый release contour;
- не смешивать corrective scope с предметной разработкой `Minesweeper`;
- не materialize top-level домены в generated product repo без явного решения по matrix;
- не вводить декоративную telemetry или новый toolchain сверх прямого contract gap.

## Артефакты
- `AGENTS.md`
- `README.md`
- `Setup_Guide.md`
- `Docs/Discovery/*`
- `Docs/Technical/README.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Domain_Matrix.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000071-domain-bootstrap-strategy-and-interview-gate.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- все top-level домены `BytePress` классифицированы без пропусков;
- bootstrap contract, generated repo, discovery docs и lint одинаково удерживают hard first product-start gate;
- canonical failed-start reset/cleanup route оформлен;
- smoke bootstrap проходит и подтверждает отсутствие residual ambiguity по раннему product-start contour.

## Результат
- `ROAD-000019`, `BACK-000083` и `PLAN-000071` закрыты в одном corrective pass; active `Backlog` очищен, а current `Plan` выведен в archive-layer без автоматической активации нового `ROAD-*`.
- `Docs/Technical/Product_Bootstrap_Domain_Matrix.md` принят как supporting owner-document для канонической классификации всех top-level доменов `BytePress`: `Docs`, `Plans`, `Logs`, `Runtime`, `Profiles`, `Adapters` materialize по default; `Pipeline`, `Rules`, `Standards`, `Schemas`, `Templates`, `Roles`, `Skills` отнесены к later product-pass; `Tools`, `Memory`, `MCP` закреплены как `BytePress-only`; optional profile не вводится.
- `AGENTS.md`, `Docs/Discovery/*`, `Docs/Technical/Product_Bootstrap_Contract.md`, `Docs/Technical/Product_Bootstrap_Validation.md`, `Docs/Technical/Artifact_Lifecycle.md`, `Tools/bp_bootstrap.py` и `Tools/bp_lint.py` теперь одинаково удерживают hard first product-start gate: bootstrap-created `Docs/Discovery/Interview.md` стартует в состоянии `Статус_текущей_истины: Не_подтверждена`, placeholders не считаются подтверждением current truth, а до ответов пользователя допускаются только `Docs/Discovery/*`, `Plans/*`, `Logs/*` и reset route.
- `Tools/bp_bootstrap.py` materialize `scripts/reset-product-start.sh`, а `Artifact_Lifecycle`, bootstrap contract и generated product `AGENTS.md` закрепляют canonical failed-start cleanup route без silent salvage tracked drift вне раннего discovery-only contour.
- Фактический smoke bootstrap во временный target path `/tmp/bytepress-domain-bootstrap-qTYUiZ/repo`, `python3 Tools/bp_lint.py --repo /tmp/bytepress-domain-bootstrap-qTYUiZ/repo`, `BYTEPRESS_ROOT=/home/dmin/code/BytePress scripts/integration-smoke.sh` и `scripts/reset-product-start.sh` подтвердили, что generated repo соответствует matrix, проходит lint и не трактует незаполненный discovery как разрешение на implementation.

# PLAN-000070 — Close product-start control gaps

ID: PLAN-000070
Название: Закрыть оставшиеся product-start control gaps
Статус: Завершено
Связи: BACK-000082
Источник: Corrective pass after `Minesweeper` field test
Дата_создания: 2026-04-20
Дата_изменения: 2026-04-20
Основание: Полевой тест generated product repo на `Minesweeper` подтвердил остаточные end-to-end gaps первого запуска: generated product `AGENTS.md` не требует наблюдаемый startup-handshake первого ответа, bootstrap interview не materialize исполнимый first-pass current-truth contract, core docs всё ещё создают двусмысленность discovery minimum относительно generated repo, а runtime artifact hygiene для `Runtime/Integration_Smoke_Report.json` не зафиксирована машинно и документно.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000082
Связанные_ADR:
- отсутствуют

## Шаги
1. Синхронизировать planning-layer для нового corrective pass.
   - DoD: `PLAN-000069` архивирован, `ROAD-000018` и `BACK-000082` активированы, текущий `Plan` оформлен как `PLAN-000070`.
2. Довести startup-handshake и interview contract до generated product repo.
   - DoD: product `AGENTS.md` требует наблюдаемый первый ответ с mode, scope, route, planning-state, owner-domains первого чтения и первым конкретным шагом, а generated `Docs/Discovery/Interview.md` materialize 8–10 исполнимых вопросов с буквенными вариантами там, где выбор ограничен.
3. Снять двусмысленность discovery minimum и runtime artifact hygiene.
   - DoD: core docs, bootstrap contract, validation contract, generated repo и lint одинаково трактуют early product-start discovery minimum и канон `Runtime/Integration_Smoke_Report.json`.
4. Подтвердить контур реальным bootstrap smoke.
   - DoD: временный generated product repo проходит `python3 Tools/bp_lint.py --repo <generated-product-repo>`, содержит discovery minimum и startup-handshake contract, а runtime artifact hygiene не спорит с baseline.

## Ограничения
- не открывать новый release contour;
- не расширять систему новыми широкими доменами без прямого contract gap;
- не превращать startup-handshake в telemetry layer;
- не смешивать corrective pass с предметной разработкой `Minesweeper`.

## Артефакты
- `AGENTS.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Discovery/*`
- `Skills/Interview.md`
- `Templates/Interview.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000070-close-product-start-control-gaps.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- startup-handshake доведён end-to-end до generated product repo;
- contract первого ответа агента в product repo стал явно наблюдаемым и проверяемым;
- interview contract реально исполним на первом product-start pass;
- discovery minimum больше не противоречит bootstrap и lint;
- runtime artifact hygiene определена и согласована;
- smoke bootstrap проходит;
- no residual contradiction между core contracts, bootstrap tool, generated repo и validation.

## Результат
- `PLAN-000069` выведен из active `Plans/` в archive-layer, а corrective stage `ROAD-000018` / `BACK-000082` активирован и закрыт в одном pass.
- Core `AGENTS.md` и generated product `AGENTS.md` теперь одинаково требуют observable startup-handshake первого ответа с mode, scope, route, planning-state, owner-domains первого чтения и первым конкретным шагом.
- `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md`, `Skills/Interview.md` и `Templates/Interview.md` синхронизированы вокруг current-truth ownership `Docs/Discovery/Interview.md` и first-pass interview из 8–10 ключевых вопросов с буквенными вариантами и рекомендуемыми ответами там, где это уместно.
- `Tools/bp_bootstrap.py` materialize generated repo с новым product `AGENTS.md`, 10-вопросным `Docs/Discovery/Interview.md`, runtime hygiene note и `.gitignore`, который удерживает `Runtime/Integration_Smoke_Report.json` вне baseline commit по умолчанию.
- `Tools/bp_lint.py` теперь проверяет startup-handshake contract, first interview contract и runtime artifact hygiene как в `BytePress`, так и в generated product repo.
- Фактический smoke bootstrap во временный target path, `python3 Tools/bp_lint.py --repo /tmp/bytepress-product-start-1okrN3/repo` и `BYTEPRESS_ROOT=/home/dmin/code/BytePress scripts/integration-smoke.sh` подтвердили отсутствие residual contradiction в corrective scope.

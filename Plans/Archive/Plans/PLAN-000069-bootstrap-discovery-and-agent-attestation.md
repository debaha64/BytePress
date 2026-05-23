# PLAN-000069 — Bootstrap discovery and agent attestation

ID: PLAN-000069
Название: Закрыть ранние control gaps bootstrap discovery и startup-handshake
Статус: Завершено
Связи: BACK-000081
Источник: Corrective pass after first field test of generated product repo
Дата_создания: 2026-04-19
Дата_изменения: 2026-04-19
Основание: Первый полевой запуск generated product repo подтвердил ранние control gaps: bootstrap не materialize minimal `Docs/Discovery/*`, product `AGENTS.md` не маршрутизировал discovery-layer явно, startup mode агента в `BytePress` был недостаточно наблюдаемым, а interview contract не фиксировал канонический формат вопросов и вариантов. Требуется узкий corrective pass без расширения release или integration contour.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000081
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать и закрыть узкий corrective stage.
   - Описание: оформить новый stage/task/pass, архивировать предыдущий completed current `Plan` и замкнуть planning-layer без открытия широкого roadmap-front.
   - DoD: `Roadmap`, `Backlog`, current `Plan` и archive-actions согласованы.
2. Синхронизировать bootstrap, validation и product agent contour.
   - Описание: добавить minimal `Docs/Discovery/*` в materialized product repo, включить discovery-layer в product `AGENTS.md` и согласовать contracts.
   - DoD: bootstrap-contract, validation-contract, generated `AGENTS.md` и `bp_lint.py` больше не спорят по этому minimum.
3. Сделать startup mode агента наблюдаемым и закрепить interview format.
   - Описание: добавить в `AGENTS.md` startup-handshake contract первого ответа и явно канонизировать interview format в skill/template/discovery-layer.
   - DoD: startup-handshake и interview format формализованы и проверяемы по active contracts.
4. Подтвердить corrective result фактическим bootstrap smoke.
   - Описание: materialize repo во временный target path, проверить новый discovery minimum и прогнать `python3 Tools/bp_lint.py --repo <generated-product-repo>`.
   - DoD: smoke bootstrap проходит и generated repo реально содержит `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md`.

## Ограничения
- без изменения release contour;
- без изменения integration contour beyond direct sync;
- без materialization новых доменов beyond direct contract gap;
- без превращения startup-handshake в новый тяжёлый layer.

## Артефакты
- `AGENTS.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Skills/Interview.md`
- `Templates/Interview.md`
- `Docs/Discovery/README.md`
- `Docs/Discovery/Interview.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000069-bootstrap-discovery-and-agent-attestation.md`
- `Plans/Archive/Plans/PLAN-000068-sync-develop-after-release-0.2.0.md`
- `Plans/Archive/Backlog/ROAD-000017.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- generated product repo materialize minimal `Docs/Discovery/*` contour;
- product `AGENTS.md` синхронизирован с discovery routing;
- startup-handshake агента стал явно наблюдаемым;
- interview format contract закреплён явно;
- `bp_lint.py` проверяет новый bootstrap minimum;
- smoke bootstrap проходит;
- bootstrap tool, docs и validation больше не имеют доказанного contradiction в этом scope.

## Результат
- Узкий corrective stage `ROAD-000017` активирован и закрыт в одном pass.
- `Tools/bp_bootstrap.py` теперь materialize `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md`, а generated `AGENTS.md` включает discovery-layer в source-of-truth hierarchy и task entry route.
- `AGENTS.md` самого `BytePress` получил observable startup-handshake contract первого ответа.
- `Skills/Interview.md`, `Templates/Interview.md` и active discovery-layer согласованно требуют нумерованные вопросы, буквенные варианты ответа там, где это уместно, и рекомендуемый вариант, если он есть.
- `Tools/bp_lint.py` расширен: он проверяет startup-handshake и interview contract в `BytePress`, а также discovery minimum и discovery routing в generated product repo.
- Smoke bootstrap и `python3 Tools/bp_lint.py --repo <generated-product-repo>` подтверждают отсутствие residual contradiction в corrective scope.

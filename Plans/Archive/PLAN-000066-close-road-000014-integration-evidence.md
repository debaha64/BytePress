# PLAN-000066 — Close ROAD-000014 integration evidence

ID: PLAN-000066
Название: Закрыть `ROAD-000014` через repo-native integration evidence handoff
Статус: Завершено
Связи: BACK-000078
Источник: Новый stage-closing pass этапа `ROAD-000014`
Дата_создания: 2026-04-13
Дата_изменения: 2026-04-13
Основание: После activation pass у `BytePress` уже есть controlled integration contour и minimal integration smoke route generated product repo, но residual gap остаётся в evidence handoff: smoke route даёт только pass/fail output и не materialize deterministic repo-native evidence/report artifact, который можно использовать как verification/validation basis без внешних подключений. Нужен один stage-closing pass, который усилит существующий smoke route, синхронизирует evidence contracts и при clean audit закроет `ROAD-000014`.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000078
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать stage-closing pass `ROAD-000014`.
   - Описание: Обновить `Roadmap` и `Backlog`, создать `BACK-000078` и `PLAN-000066`, а завершённый `PLAN-000065` вывести в archive-layer.
   - DoD: planning-layer согласован с новым closing-pass.
2. Оформить repo-native integration evidence handoff.
   - Описание: Усилить существующие `bp_integration_smoke.py` и `scripts/integration-smoke.sh`, чтобы generated product repo выпускал deterministic evidence/report artifact без открытия внешних подключений.
   - DoD: smoke route и evidence artifact согласованы с technical evidence contracts.
3. Синхронизировать evidence contracts и gate handoff boundary.
   - Описание: Точечно обновить `Interfaces.md`, `Platform_Contracts.md`, bootstrap/validation contracts, `Verification_Evidence.md`, `Validation_Evidence.md` и `Pipeline/Phase_Gates.md` без redesign evidence storage model.
   - DoD: active contracts не спорят о storage, linkage и роли integration evidence.
4. Выполнить bootstrap smoke и финальный audit.
   - Описание: Materialize generated product repo во временный target path, выполнить `bp_lint`, `integration-smoke` и evidence/report route.
   - DoD: generated repo проходит все checks, artifact создаётся, verdict согласован со smoke result.
5. Закрыть `ROAD-000014`, если residual gap не подтверждён.
   - Описание: Перевести `BACK-000078` и `PLAN-000066` в `Завершено`, закрыть `ROAD-000014` и вывести backlog этапа в archive-layer.
   - DoD: stage закрыт clean audit'ом без автоматической активации нового `ROAD-*`.

## Риски
- если evidence artifact начнёт выглядеть как новый отдельный layer, stage scope снова расползётся;
- если report route начнёт тянуть timestamps, network state или vendor-specific data, evidence перестанет быть deterministic;
- если contracts останутся несогласованными по storage, artifact будет существовать технически, но не станет валидным handoff basis.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/PLAN-000066-close-road-000014-integration-evidence.md`
- `Plans/Archive/PLAN-000065-activate-road-000014-integration-contour.md`
- `Plans/Archive/Backlog/ROAD-000014.md`
- `Docs/Technical/Interfaces.md`
- `Docs/Technical/Platform_Contracts.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Docs/Technical/Verification_Evidence.md`
- `Docs/Technical/Validation_Evidence.md`
- `Pipeline/Phase_Gates.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_integration_smoke.py`

## DoD
- создана одна новая backlog-задача и один новый current `Plan` для stage-closing pass `ROAD-000014`.
- repo-native integration evidence handoff оформлен как часть существующего controlled integration contour.
- generated product repo выполняет integration smoke route и выпускает deterministic evidence/report artifact без внешних подключений.
- evidence/report route согласован с `Verification_Evidence.md` и `Validation_Evidence.md`.
- при clean audit `ROAD-000014` переведён в `Завершено` и backlog этапа выведен в archive-layer.

## Результат
- Существующий `integration-smoke` route усилен до deterministic repo-native evidence handoff: `bp_integration_smoke.py` может materialize report artifact, а bootstrap-generated `scripts/integration-smoke.sh` пишет его в `Runtime/Integration_Smoke_Report.json`.
- `Interfaces.md`, `Platform_Contracts.md`, bootstrap/validation contracts, `Verification_Evidence.md`, `Validation_Evidence.md` и `Pipeline/Phase_Gates.md` согласованы с этим handoff без redesign evidence storage model и без открытия нового tool family.
- Реальный smoke bootstrap на отдельном target path подтвердил, что generated repo проходит `bp_lint`, integration smoke и выпускает report artifact с verdict, согласованным со smoke result.
- Финальный audit не подтвердил residual gap в scope `ROAD-000014`, поэтому `BACK-000078` и `ROAD-000014` закрыты, а backlog этапа выведен в `Plans/Archive/Backlog/ROAD-000014.md`.

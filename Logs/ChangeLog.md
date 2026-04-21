# ChangeLog

## Индекс
- CHG-000083 — Domain bootstrap matrix and early product-start gate synchronized
- CHG-000082 — Product-start corrective contour synchronized after first field test
- CHG-000081 — Bootstrap discovery minimum and agent startup attestation synchronized
- CHG-000080 — Post-release sync completed and factual `0.2.0` release logged
- CHG-000079 — Release workflow canon completed and missing history-facts closed for ROAD-000015
- CHG-000078 — Close ROAD-000014 integration evidence
- CHG-000077 — Activate ROAD-000014 integration contour
- CHG-000076 — Close ROAD-000013 product replication
- CHG-000075 — Close ROAD-000012 user entry
- CHG-000074 — Minimal user boundary
- CHG-000073 — Activate ROAD-000012 agent entry boundaries
- CHG-000072 — Audit and close ROAD-000011
- CHG-000071 — Define validation tooling boundary
- CHG-000070 — Define validation evidence contract
- CHG-000069 — Define validation levels
- CHG-000068 — Clarify validation contract map
- CHG-000067 — Define validation boundaries
- CHG-000066 — Define verification evidence contract
- CHG-000065 — Define verification tooling boundary
- CHG-000064 — Define verification levels
- CHG-000063 — Clarify verification contract map
- CHG-000062 — Activate ROAD-000011 verification boundaries
- CHG-000061 — Audit and close ROAD-000010
- CHG-000060 — Clarify product bootstrap validation
- CHG-000059 — Clarify product bootstrap contract
- CHG-000058 — Clarify technical platform contracts
- CHG-000057 — Clarify technical system invariants
- CHG-000056 — Clarify technical interfaces core
- CHG-000055 — Clarify technical artifact lifecycle
- CHG-000054 — Clarify technical model core
- CHG-000053 — Clarify technical architecture core
- CHG-000052 — Clarify technical contract map
- CHG-000051 — Activate ROAD-000010 technical boundaries
- CHG-000050 — Audit and close ROAD-000009
- CHG-000049 — Migrate remaining governance ID layer
- CHG-000048 — Migrate governance ID layer
- CHG-000047 — Migrate log ID layer
- CHG-000046 — Remove runtime plan legacy tail
- CHG-000045 — Archive backlog history layer
- CHG-000044 — Migrate plan history to archive
- CHG-000043 — Define unified ID scheme
- CHG-000042 — Align roadmap and planning transition
- CHG-000041 — Activate ROAD-000009 operating model pass
- CHG-000040 — ROAD-000008 governance state repaired and the stage closed consistently
- CHG-000039 — Requirements introduced as the next canonical artifact of ROAD-000008
- CHG-000038 — Research introduced as the next canonical artifact of ROAD-000008
- CHG-000037 — Discussion introduced as the first canonical artifact of ROAD-000008
- CHG-000036 — ROAD-000007 closed, ROAD-000008 activated, and discovery templates introduced
- CHG-000035 — Analytical, product, and planning contours aligned for ROAD-000007
- CHG-000034 — Pipeline, roadmap, and backlog governance aligned to the accepted stage model
- CHG-000033 — Domain participation contract clarified execution and extension domains
- CHG-000032 — Artifact lifecycle contract consolidated update order and reduced technical process noise
- CHG-000031 — Branch and PR process contract finalized and residual process noise removed
- CHG-000030 — Repo-wide active layer audit aligned maps, roles, skills and technical references
- CHG-000029 — Discovery layer, interview current truth and sync contract surfaced
- CHG-000028 — Delivery template, bootstrap, and lint contracts synchronized with product layer canon
- CHG-000027 — Product layer aligned with canonical templates and minimal document scope
- CHG-000026 — Release branch example aligned with canonical branch naming
- CHG-000025 — Release governance and README product value formalized before main preparation
- CHG-000024 — Planning truth aligned with logs truth for release preparation
- CHG-000023 — Orphan IDs removed from active plans and approval rule without new namespaces
- CHG-000022 — Semver operationalized for active BytePress documents at baseline 0.1.0
- CHG-000021 — Historical logs migrated to six-digit IDs and active references synced
- CHG-000020 — Active non-log ID layer переведён на 6-значный формат без переписывания historical logs
- CHG-000019 — Tool contract sync завершил приведение bootstrap и lint к текущим contracts
- CHG-000018 — Terms layer мигрирован на канонические filenames и 6-значные TERM ID
- CHG-000017 — Синхронизированы схемы, шаблоны, профили и language contract Git/PR
- CHG-000016 — Зафиксирована repo-wide policy фазной ID migration без запуска rewrite-pass
- CHG-000015 — Remaining plan layer приведён к каноническим именам и 6-значным plan ID
- CHG-000014 — Нормализован foundation-план BytePress и удалён legacy-дубль
- CHG-000013 — Зафиксирован контракт 6-значных ID, naming plan-file и модель профилей
- CHG-000012 — Зафиксированы branch lifecycle, целевой Auto-PR процесс и следующий плановый проход
- CHG-000011 — Добавлены корневые карты README.md и AGENTS.md и обновлены минимальные контракты агентной работы
- CHG-000010 — Подтверждён рабочий цикл agent push -> agent PR -> human approve -> human merge в GitHub
- CHG-000009 — Усилен bootstrap продукта и подтверждён тестовой генерацией
- CHG-000008 — Оформлен интеграционный каркас Adapters, Memory и MCP
- CHG-000007 — Замкнут исполнительный контур ролей, навыков и инструментов BytePress
- CHG-000006 — Усилен технический слой и контур правил BytePress
- CHG-000005 — Введён рабочий журнальный контур решений и изменений
- CHG-000004 — Заполнены короткие стандарты BytePress полезными практиками
- CHG-000003 — Заполнена базовая терминология BytePress и политика её изменений
- CHG-000002 — Уточнены схемы и шаблоны ключевых сущностей
- CHG-000001 — Создан первичный каркас BytePress v1

---

## CHG-000083 — Domain bootstrap matrix and early product-start gate synchronized
ID: CHG-000083
Дата: 2026-04-21
Тип_изменения: Документация
Источник: Corrective pass after repeated `Minesweeper` field test
Связи: PLAN-000071, BACK-000083, QL-000078
Дата_создания: 2026-04-21
Дата_изменения: 2026-04-21

### Описание
`Docs/Technical/Product_Bootstrap_Domain_Matrix.md` добавлен как канонический supporting document для классификации всех top-level доменов `BytePress` по replication matrix `Default / Later product-pass / BytePress-only` без optional profile. Одновременно core `AGENTS.md`, active discovery-layer, bootstrap/validation contracts, `Artifact_Lifecycle.md`, `Setup_Guide.md`, `Tools/bp_bootstrap.py` и `Tools/bp_lint.py` синхронизированы так, чтобы generated product repo оставался в discovery-only contour до ответов пользователя и получал canonical failed-start reset route `scripts/reset-product-start.sh`.

### Эффект
Ранний product-start contour generated repo стал управляемым end-to-end: bootstrap materialize только утверждённый subset доменов, незаполненный discovery больше не трактуется как implicit approval для implementation, а failed start имеет проверяемый cleanup route вместо silent salvage.

---

## CHG-000082 — Product-start corrective contour synchronized after first field test
ID: CHG-000082
Дата: 2026-04-20
Тип_изменения: Документация
Источник: Corrective pass after `Minesweeper` field test
Связи: PLAN-000070, BACK-000082, QL-000077
Дата_создания: 2026-04-20
Дата_изменения: 2026-04-20

### Описание
Core `AGENTS.md`, bootstrap/validation contracts, active discovery-layer, `Skills/Interview.md`, `Templates/Interview.md`, `Tools/bp_bootstrap.py` и `Tools/bp_lint.py` синхронизированы после полевого теста `Minesweeper`. Generated product repo теперь materialize observable startup-handshake contract первого ответа, 10-вопросный `Docs/Discovery/Interview.md` как owner current truth и `.gitignore`, который удерживает `Runtime/Integration_Smoke_Report.json` вне baseline commit по умолчанию.

### Эффект
Ранний product-start contour первого запуска generated repo стал наблюдаемым, проверяемым и согласованным end-to-end без открытия нового release contour или предметной разработки `Minesweeper`.

---


## CHG-000081 — Bootstrap discovery minimum and agent startup attestation synchronized
ID: CHG-000081
Дата: 2026-04-19
Тип_изменения: Документация
Источник: Corrective pass after first field test of generated product repo
Связи: PLAN-000069, BACK-000081, QL-000076
Дата_создания: 2026-04-19
Дата_изменения: 2026-04-19

### Описание
`AGENTS.md`, bootstrap/validation contracts, `Skills/Interview.md`, `Templates/Interview.md`, active discovery-layer и tooling синхронизированы после первого полевого запуска generated product repo. Bootstrap теперь materialize minimal `Docs/Discovery/README.md` и `Docs/Discovery/Interview.md`, generated product `AGENTS.md` маршрутизирует discovery-layer явно, а startup mode агента в `BytePress` фиксируется через observable startup-handshake первого ответа.

### Эффект
Ранние control gaps первого bootstrap-run закрыты без изменения release contour, integration contour или открытия нового широкого roadmap-stage.

---

## CHG-000080 — Post-release sync completed and factual `0.2.0` release logged
ID: CHG-000080
Дата: 2026-04-15
Тип_изменения: Документация
Источник: Post-release sync pass after merged `0.2.0`
Связи: PLAN-000068, BACK-000080, QL-000075, RL-000007
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
После подтверждённого merge `PR #77` и annotated tag `0.2.0` выполнен минимальный post-release sync-pass в `develop`: local/remote release-ветка снята из operational contour, `ReleaseLog.md` получил factual запись `RL-000007`, а planning-layer зафиксировал отдельный operational stage `ROAD-000016` только для этого closure. Сравнение `origin/main` и `origin/develop` не подтвердило release-only tree fixes для back-sync, поэтому sync-pass не вносил новых product-development changes beyond factual release logging и minimal planning/log closure.

### Эффект
Post-release contour `0.2.0` закрыт в `develop` как history-fact без открытия нового широкого roadmap-stage.

---

## CHG-000079 — Release workflow canon completed and missing history-facts closed for ROAD-000015
ID: CHG-000079
Дата: 2026-04-15
Тип_изменения: Документация
Источник: Corrective closure pass for `ROAD-000015`
Связи: PLAN-000067, BACK-000079, QL-000074
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Setup_Guide.md`, `Standards/Release.md`, `Artifact_Lifecycle.md`, evidence contracts и `Pipeline/Phase_Gates.md` теперь согласованно фиксируют полный release workflow `release/* -> main -> tag -> cleanup -> develop sync -> factual release logging` без подмены release event gate approval или прогнозом. Одновременно `ChangeLog.md` и `QualityLog.md` дозаполнены начиная с первого реально незалогированного pass после `CHG-000040` / `QL-000035`, а `ReleaseLog.md` получил factual запись `RL-000006` о release event `0.1.0`, подтверждённом annotated tag `0.1.0` на commit `92891482e9bc88940069700ba93890fb317b5cab`.

### Эффект
Release-readiness и journaling contour больше не имеют доказанного active-layer gap для подготовки `0.2.0`, а `ROAD-000015` закрыт без открытия нового roadmap-stage.

---

## CHG-000078 — Close ROAD-000014 integration evidence
ID: CHG-000078
Дата: 2026-04-13
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000066
Связи: PLAN-000066, BACK-000078, QL-000073
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
Существующий `integration-smoke` route усилен до deterministic repo-native evidence handoff: `bp_integration_smoke.py` может materialize report artifact, а bootstrap-generated `scripts/integration-smoke.sh` пишет его в `Runtime/Integration_Smoke_Report.json`. `Interfaces.md`, `Platform_Contracts.md`, bootstrap/validation contracts, `Verification_Evidence.md`, `Validation_Evidence.md` и `Pipeline/Phase_Gates.md` согласованы с этим handoff без redesign evidence storage model и без открытия нового tool family.

### Эффект
History-fact stage-closing pass `ROAD-000014` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000077 — Activate ROAD-000014 integration contour
ID: CHG-000077
Дата: 2026-04-13
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000065
Связи: PLAN-000065, BACK-000077, QL-000072
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`ROAD-000014` активирован и оставлен в статусе `В_работе` как текущий stage. `Docs/Technical/*`, `MCP/*`, `Adapters/*` и `Tools/README.md` теперь согласованно фиксируют controlled integration contour, границы `Adapters/*` и `MCP/*`, product-side handoff через `scripts/*` и отсутствие реальных внешних подключений в active scope.

### Эффект
History-fact activation pass `ROAD-000014` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000076 — Close ROAD-000013 product replication
ID: CHG-000076
Дата: 2026-04-13
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000064
Связи: PLAN-000064, BACK-000076, QL-000071
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`bp_bootstrap.py` больше не materialize лишь minimal skeleton: generated repo получает `README.md`, `AGENTS.md`, `Setup_Guide.md`, полный минимальный `Docs/User/*` contour, adapter policy/registry, executable scripts и initial current stage/task/pass. `bp_lint.py` расширен до structural contract first-usable replicated repo и подтверждает не только product skeleton, но и human/agent entry contour, `.gitignore` для `.codex`, executable scripts и initial planning state.

### Эффект
History-fact stage-closing pass `ROAD-000013` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000075 — Close ROAD-000012 user entry
ID: CHG-000075
Дата: 2026-04-11
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000063
Связи: PLAN-000063, BACK-000075, QL-000070
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Pass_Request.md` добавлен как минимальный user-facing contract для формулирования pass человеком через repo contracts без дублирования agent operating loop. Direct contradiction в `Docs/User/*` вокруг запуска `bp_lint.py` из корня репозитория исправлен: user-layer теперь ссылается на `python3 Tools/bp_lint.py --repo .` именно как на команду из корня репозитория.

### Эффект
History-fact closure-pass `ROAD-000012` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000074 — Minimal user boundary
ID: CHG-000074
Дата: 2026-04-11
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000062
Связи: PLAN-000062, BACK-000074, QL-000069
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`ROAD-000012` остался активным, а `ROAD-000013` не активирован. `PLAN-000061` выведен в archive-layer, `PLAN-000062` оформлен как новый current `Plan`.

### Эффект
History-fact pass минимального user-layer добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000073 — Activate ROAD-000012 agent entry boundaries
ID: CHG-000073
Дата: 2026-04-11
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000061
Связи: PLAN-000061, BACK-000073, QL-000068
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`ROAD-000012` активирован без автоматической активации `ROAD-000013`. `Plans/Backlog.md` переведён на `ROAD-000012` и содержит одну завершённую задачу `BACK-000073` этого узкого pass.

### Эффект
History-fact activation pass `ROAD-000012` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000072 — Audit and close ROAD-000011
ID: CHG-000072
Дата: 2026-04-11
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000060
Связи: PLAN-000060, BACK-000072, QL-000067
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
Audit active verification/validation contour не подтвердил реального residual gap: verification, validation, evidence, tooling support и gates разведены без доказанного active-layer contradiction. `ROAD-000011` переведён в `Завершено` без candidate tail и без автоматической активации `ROAD-000012`.

### Эффект
History-fact audit-pass `ROAD-000011` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000071 — Define validation tooling boundary
ID: CHG-000071
Дата: 2026-04-11
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000059
Связи: PLAN-000059, BACK-000071, QL-000066
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
Planning-contour согласован: `BACK-000071` находится в завершённой секции и индексе `Backlog.md`, `ROAD-000011` остаётся в `В_работе`, current `Plan` оформлен как `PLAN-000059`. `Tools/README.md` пересобран как boundary-document verification + validation tooling contour с явным разделением роли `bp_lint`, target role будущих `bp_check / bp_verify`, допустимого future validation tooling и procedural validation.

### Эффект
History-fact pass validation tooling boundary добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000070 — Define validation evidence contract
ID: CHG-000070
Дата: 2026-04-11
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000058
Связи: PLAN-000058, BACK-000070, QL-000065
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Validation_Evidence.md` создан как singleton contract validation evidence: classes, mandatory / optional expectations, storage, sufficient / insufficient criteria и relation к validation levels и pass-close contour. `Docs/Technical/Validation.md` минимально синхронизирован, чтобы явно ссылаться на `Validation_Evidence.md` как отдельный evidence-contract validation-layer.

### Эффект
History-fact pass validation evidence добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000069 — Define validation levels
ID: CHG-000069
Дата: 2026-04-08
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000057
Связи: PLAN-000057, BACK-000069, QL-000064
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Validation_Levels.md` создан как singleton contract уровней validation-контура: уровни, цели, required inputs, expected outputs и relation к evidence package и pass-close contour. `Docs/Technical/Validation.md` минимально синхронизирован ссылкой на отдельный levels-document.

### Эффект
History-fact pass validation levels добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000068 — Clarify validation contract map
ID: CHG-000068
Дата: 2026-04-08
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000056
Связи: PLAN-000056, BACK-000068, QL-000063
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Validation.md` пересобран из boundary-doc в contract map validation-layer: document теперь явно фиксирует validation inputs, outputs, verdict classes, ownership интерпретации, отношение к evidence package и место в pass-close contour. `Docs/Technical/Verification.md` минимально синхронизирован, чтобы развести verification contract map и validation contract map.

### Эффект
History-fact pass validation contract map добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000067 — Define validation boundaries
ID: CHG-000067
Дата: 2026-04-08
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000055
Связи: PLAN-000055, BACK-000067, QL-000062
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Validation.md` создан как singleton boundary-document validation-layer: назначение validation, отличия от verification, inputs/outputs, evidence usage, ownership результата и связь с pass-close contour и phase gates. `Docs/Technical/Verification.md` минимально синхронизирован, чтобы явно развести verification contract и validation outcome confirmation.

### Эффект
History-fact pass validation boundaries добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000066 — Define verification evidence contract
ID: CHG-000066
Дата: 2026-04-08
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000054
Связи: PLAN-000054, BACK-000066, QL-000061
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Verification_Evidence.md` создан как singleton contract verification evidence: evidence classes, обязательность, storage и linkage к pass-close contour. `Docs/Technical/Verification.md` и `Docs/Technical/Verification_Levels.md` минимально синхронизированы ссылками на evidence contract.

### Эффект
History-fact pass verification evidence добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000065 — Define verification tooling boundary
ID: CHG-000065
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000053
Связи: PLAN-000053, BACK-000065, QL-000060
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Tools/README.md` пересобран как boundary-document tooling verification contour с явным разделением ролей `bp_lint`, будущего `bp_check`, будущего `bp_verify` и procedural verification. `Docs/Technical/Verification_Levels.md` минимально синхронизирован ссылкой на tooling boundary.

### Эффект
History-fact pass verification tooling boundary добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000064 — Define verification levels
ID: CHG-000064
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000052
Связи: PLAN-000052, BACK-000064, QL-000059
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Verification_Levels.md` создан как supporting technical document уровней verification-контура и target split будущих `bp_check / bp_verify`. `Docs/Technical/Verification.md` минимально синхронизирован ссылкой на level-specific document, а `Docs/Technical/README.md` обновлён в карте supporting documents.

### Эффект
History-fact pass verification levels добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000063 — Clarify verification contract map
ID: CHG-000063
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000051
Связи: PLAN-000051, BACK-000063, QL-000058
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Verification.md` пересобран из boundary-document в contract map verification-layer с явными классами checks, inputs, outputs, evidence forms и ownership интерпретации результата. Automatic checks, procedural checks и process gates разведены без переноса gate policy в `Pipeline/*` или tooling implementation в `Docs/Technical/*`.

### Эффект
History-fact pass verification contract map добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000062 — Activate ROAD-000011 verification boundaries
ID: CHG-000062
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000050
Связи: PLAN-000050, BACK-000062, QL-000057
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Verification.md` создан как канонический boundary-document verification-layer и фиксирует границы между automatic checks, procedural checks, process gates и tool implementation. `Docs/Technical/README.md` минимально синхронизирован: `Verification.md` добавлен в supporting technical-documents и в карту слоя.

### Эффект
History-fact activation pass `ROAD-000011` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000061 — Audit and close ROAD-000010
ID: CHG-000061
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000049
Связи: PLAN-000049, BACK-000061, QL-000056
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
Финальный audit active technical layer не подтвердил реального residual gap: required core и supporting technical contracts согласованы между собой и с planning/process/bootstrap perimeter. `ROAD-000010` переведён в `Завершено` без candidate tail и без автоматической активации `ROAD-000011`.

### Эффект
History-fact audit-pass `ROAD-000010` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000060 — Clarify product bootstrap validation
ID: CHG-000060
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000048
Связи: PLAN-000048, BACK-000060, QL-000055
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Product_Bootstrap_Validation.md` пересобран как канонический validation-contract bootstrap-result текущего `BytePress`: document теперь явно фиксирует validation-scope, acceptance criteria, automatic/procedural split и недопустимые validation-пропуски. Validation-layer явно разведен с bootstrap-contract: `Product_Bootstrap_Contract.md` владеет bootstrap obligations, а `Product_Bootstrap_Validation.md` владеет критериями и режимом проверки результата.

### Эффект
History-fact pass product bootstrap validation добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000059 — Clarify product bootstrap contract
ID: CHG-000059
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000047
Связи: PLAN-000047, BACK-000059, QL-000054
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Product_Bootstrap_Contract.md` пересобран как канонический bootstrap-contract текущего `BytePress`: теперь он явно фиксирует CLI contract, minimal product repo outcome, обязательные создаваемые артефакты, bootstrap boundaries, допустимые упрощения и недопустимые bootstrap-пропуски. Bootstrap-contract теперь прямо разводит contract obligations, platform assumptions, lifecycle rules и validation result: `Product_Bootstrap_Validation.md` остаётся evidence document, а не substitute для самого contract.

### Эффект
History-fact pass product bootstrap contract добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000058 — Clarify technical platform contracts
ID: CHG-000058
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000046
Связи: PLAN-000046, BACK-000058, QL-000053
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Platform_Contracts.md` пересобран как канонический platform-contract текущего `BytePress`: теперь он явно фиксирует supported execution environment, platform assumptions, supported tool perimeter, роли ключевых инструментов, допустимые режимы platform usage и недопустимые anti-patterns без смешения с architecture, model, lifecycle, interfaces, invariants или process-canon. `Docs/Technical/README.md` синхронизирован минимально: supporting role `Platform_Contracts.md` теперь описана как канонический platform/tool contract, а не как расплывчатый контекстный document.

### Эффект
History-fact pass technical platform contracts добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000057 — Clarify technical system invariants
ID: CHG-000057
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000045
Связи: PLAN-000045, BACK-000057, QL-000052
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/System_Invariants.md` пересобран как канонический invariant-contract текущего `BytePress`: в одном document теперь явно собраны repository/source-of-truth, planning, ownership, active/archive, traceability, process и tooling invariants, а также нарушения и их последствия. Для pass не потребовался отдельный шаблон: existing `Templates/Document.md` достаточен как общий singleton-document template, поэтому новый special template не вводился.

### Эффект
History-fact pass system invariants добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000056 — Clarify technical interfaces core
ID: CHG-000056
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000044
Связи: PLAN-000044, BACK-000056, QL-000051
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Interfaces.md` пересобран как канонический interface-contract текущего `BytePress`: в одном document теперь явно разведены внутренние и внешние интерфейсы, stable/service/derived classes, допустимые touchpoints и недопустимые обходы границ. `Interfaces.md` больше не выглядит как короткий legacy-list связей: отношение interface-layer к `Plans/*`, `Runtime/*`, `Logs/*` и `Pipeline/*` зафиксировано отдельно от архитектурной карты, ownership-модели и lifecycle-contract.

### Эффект
History-fact pass technical interfaces добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000055 — Clarify technical artifact lifecycle
ID: CHG-000055
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000043
Связи: PLAN-000043, BACK-000055, QL-000050
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Artifact_Lifecycle.md` пересобран как канонический lifecycle-contract текущего `BytePress`: в одном document теперь явно разведены артефактные группы, источники истины, обязательные sync-loop, допустимые переходы между active, archive, runtime и log слоями и недопустимые lifecycle-пропуски. `Artifact_Lifecycle.md` больше не выглядит как короткий sync-note: closure-loop перед завершением pass, допустимые layer transitions и границы между lifecycle-layer, architecture-layer, model-layer и process-layer зафиксированы явно.

### Эффект
History-fact pass artifact lifecycle добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000054 — Clarify technical model core
ID: CHG-000054
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000042
Связи: PLAN-000042, BACK-000054, QL-000049
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Model.md` пересобран как каноническая модель текущего `BytePress`: в одном document теперь явно разведены ключевые сущности системы, ownership состояния, основные связи и недопустимые смешения ответственности. `Model.md` больше не смешивает profile policy, naming migration и historical state с моделью сущностей; границы между model-layer, architecture-layer, lifecycle-layer и process-layer зафиксированы явно.

### Эффект
History-fact pass technical model добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000053 — Clarify technical architecture core
ID: CHG-000053
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000041
Связи: PLAN-000041, BACK-000053, QL-000048
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/Architecture.md` пересобран как каноническая архитектурная карта текущего `BytePress`: в одном document теперь явно разведены domain map, layer map, границы ответственности, допустимые направления связей и недопустимые подмены. Архитектурная граница между `Docs/Technical/*` и `Pipeline/*` зафиксирована без дублирования process-canon: `Architecture.md` описывает место process-layer в системе, но не повторяет фазы, gates и process IO.

### Эффект
History-fact pass technical architecture добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000052 — Clarify technical contract map
ID: CHG-000052
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000040
Связи: PLAN-000040, BACK-000052, QL-000047
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Docs/Technical/README.md` теперь явно делит current technical-documents на required core и supporting layer и фиксирует роль каждого документа в слое. `Docs/Technical/Pipeline.md` возвращён к supporting technical view: из active layer убран дублирующий process-canon, а приоритет `Pipeline/*` как process-domain закреплён явно.

### Эффект
History-fact pass technical contract map добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000051 — Activate ROAD-000010 technical boundaries
ID: CHG-000051
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000039
Связи: PLAN-000039, BACK-000051, QL-000046
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`ROAD-000010` активирован как текущий этап без переоткрытия `ROAD-000009`. `Docs/Technical/README.md` зафиксировал назначение technical-layer, его включения, исключения, отношение к `Pipeline/*`, `Plans/*`, `Runtime/*` и `Logs/*`, а также минимальный required состав слоя.

### Эффект
History-fact activation pass `ROAD-000010` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000050 — Audit and close ROAD-000009
ID: CHG-000050
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000038
Связи: PLAN-000038, BACK-000050, QL-000045
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
Audit активного governance-layer и planning-contour не подтвердил реального residual gap: candidate про hard-close contour не опирался на активное рассогласование и снят как неподтверждённый. `ROAD-000009` переведён в `Завершено`; `ROAD-000010` не активирован автоматически и остаётся следующим черновым горизонтом без новой backlog-задачи.

### Эффект
History-fact audit-pass `ROAD-000009` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000049 — Migrate remaining governance ID layer
ID: CHG-000049
Дата: 2026-04-07
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000037
Связи: PLAN-000037, BACK-000049, QL-000044
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Profiles/*` доведены до implemented hybrid contract без migration semantic filenames: внутренние `PROF-*` сохранены, а ссылочные списки `Активные_*` и `Резервные_*` нормализованы на canonical `ID`. `Docs/Terms/*` не потребовал file migration: `TERM-*` уже соответствовали serial contract, а singleton support-files внутри домена явно разведены с term-card layer.

### Эффект
History-fact pass remaining governance IDs добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000048 — Migrate governance ID layer
ID: CHG-000048
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000036
Связи: PLAN-000036, BACK-000048, QL-000043
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`BACK-000048` и `PLAN-000036` зафиксировали только узкий pass по active governance/supporting domains без открытия других доменов. `Rules/*` подтвердили singleton contract без filename-migration; `Standards/Naming.md`, `Standards/Quality.md` и `Standards/Traceability.md` доведены до явных `STD-*`.

### Эффект
History-fact pass governance ID layer добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000047 — Migrate log ID layer
ID: CHG-000047
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000035
Связи: PLAN-000035, BACK-000047, QL-000042
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`BACK-000047` и `PLAN-000035` зафиксировали только узкий pass по migration log-layer без открытия других доменов. `Logs/QualityLog.md` получил явные `ID:` для всех serial quality entries, а `Logs/ReleaseLog.md` переведён на шестизначный `RL-<NNNNNN>` contract с явными внутренними `ID`.

### Эффект
History-fact pass log ID layer добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000046 — Remove runtime plan legacy tail
ID: CHG-000046
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000034
Связи: PLAN-000034, BACK-000046, QL-000041
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`BACK-000046` и `PLAN-000034` зафиксировали только cleanup-pass по legacy runtime tail planning-контура. `Runtime/Plan.md` удалён из рабочего дерева, а `Tools/bp_bootstrap.py` больше не материализует этот legacy artifact.

### Эффект
History-fact pass runtime plan cleanup добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000045 — Archive backlog history layer
ID: CHG-000045
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000033
Связи: PLAN-000033, BACK-000045, QL-000040
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`BACK-000045` и `PLAN-000033` зафиксировали только pass на archive migration historical backlog прошлых этапов. Historical backlog `ROAD-000001`–`ROAD-000008` выведен в `Plans/Archive/Backlog/ROAD-<NNNNNN>.md` с сохранением `BACK-ID`, порядка и связи с соответствующим `ROAD-*`.

### Эффект
History-fact pass backlog archive migration добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000044 — Migrate plan history to archive
ID: CHG-000044
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000032
Связи: PLAN-000032, BACK-000044, QL-000039
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`BACK-000044` и `PLAN-000032` зафиксировали только pass на migration plan-files и archive policy. Historical `BP-*` и завершённые `PLAN-*` перемещены в `Plans/Archive/` и приведены к `PLAN-*` filename-contract.

### Эффект
History-fact pass plan archive migration добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000043 — Define unified ID scheme
ID: CHG-000043
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000031
Связи: PLAN-000031, BACK-000043, QL-000038
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`BACK-000043` и `PLAN-000031` зафиксировали только pass на unified `ID scheme` без запуска migration. `Standards/Naming.md` зафиксировал target `ID scheme` для serial / hybrid / singleton domains, правила filename и внутренних ссылок, а также future migration-order по доменам.

### Эффект
History-fact pass unified ID scheme добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000042 — Align roadmap and planning transition
ID: CHG-000042
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000030
Связи: PLAN-000030, BACK-000042, QL-000037
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`Roadmap` доведён до утверждённого горизонта: `ROAD-000011` теперь означает verification contour, `ROAD-000012` — agent entry point and user layer, `ROAD-000013` — product repo replication and baseline `0.2.0`, `ROAD-000014` — integration layer and future extensions. `BACK-000042` и `PLAN-000030` зафиксировали только corrective pass на выравнивание planning-transition без migration historical layer.

### Эффект
History-fact corrective pass planning transition добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000041 — Activate ROAD-000009 operating model pass
ID: CHG-000041
Дата: 2026-04-06
Тип_изменения: Документация
Источник: Archive backfill from PLAN-000029
Связи: PLAN-000029, BACK-000041, QL-000036
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15

### Описание
`ROAD-000009` активирован как первый governance-pass новой operating model `BytePress`, а `ROAD-000010` переопределён как следующий technical-layer stage. `BACK-000041` зафиксировал узкий pass только на терминологию, ownership состояния, lifecycle `Plan`, неканоничность `Runtime/Plan.md` и hard-close contour задачи.

### Эффект
History-fact activation pass `ROAD-000009` добавлен в `ChangeLog` без подмены planning-layer журналом.

---

## CHG-000040 — ROAD-000008 governance state repaired and the stage closed consistently
ID: CHG-000040
Дата: 2026-04-02
Тип_изменения: Документация
Источник: Short governance repair pass after Requirements introduction
Связи: PLAN-000028, BACK-000040, QL-000035
Дата_создания: 2026-04-02
Дата_изменения: 2026-04-02

### Описание
Остаточный candidate-level хвост этапа `ROAD-000008` переведён в реальную backlog-задачу `BACK-000040`, после чего `Docs/Technical/Pipeline.md`, `Plans/Roadmap.md` и `Plans/Backlog.md` синхронизированы под правило, что этап roadmap со статусом `В_работе` не может оставаться без активной backlog-задачи. По результату pass `BACK-000040`, `PLAN-000028` и сам `ROAD-000008` закрыты как завершённые без рассогласования между статусом этапа, составом `Связанные_backlog`, индексом backlog и положением задачи в секции `Завершённые`. `bp_lint.py` и `ADRlog` не менялись, потому что обязательный contract путей, шаблонов и доменов не изменился и новый устойчивый архитектурный выбор не появился.

### Эффект
`ROAD-000008` больше не остаётся активным без реальной задачи и больше не держит переход `Discussion -> Research -> Requirements -> Roadmap` только как кандидат: этап закрыт, а governance-контур согласован перед переходом к следующим roadmap-stage задачам.

---

## CHG-000039 — Requirements introduced as the next canonical artifact of ROAD-000008
ID: CHG-000039
Дата: 2026-04-01
Тип_изменения: Документация
Источник: Requirements artifact pass after Research introduction
Связи: PLAN-000027, BACK-000039, QL-000034
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01

### Описание
`Docs/Discovery/Requirements.md` введён как следующий реальный discovery-артефакт этапа `ROAD-000008` на основе уже существующего `Templates/Requirements.md`. `Docs/Discovery/README.md` обновлён под фактический состав discovery-layer, `BACK-000038` окончательно закрыт как pass по `Research`, а `Plans/Roadmap.md` и `Plans/Backlog.md` синхронизированы так, чтобы `Requirements` считался уже введённым артефактом текущего этапа без двусмысленного контейнера backlog. `Tools/bp_lint.py` минимально расширен и теперь требует `Docs/Discovery/Requirements.md` как обязательный discovery-артефакт BytePress repo. Новый `ADR` не создавался, потому что проход исполнил уже утверждённый порядок `место -> шаблон -> артефакт` без нового устойчивого архитектурного решения.

### Эффект
`ROAD-000008` получил третий канонический discovery-документ, а planning-контур и lint-contract теперь согласованно учитывают `Requirements` как реальный артефакт текущего этапа.

---

## CHG-000038 — Research introduced as the next canonical artifact of ROAD-000008
ID: CHG-000038
Дата: 2026-04-01
Тип_изменения: Документация
Источник: Research artifact pass after Discussion introduction
Связи: PLAN-000026, BACK-000038, QL-000033
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01

### Описание
`Docs/Discovery/Research.md` введён как следующий реальный discovery-артефакт этапа `ROAD-000008` на основе уже существующего `Templates/Research.md`. `Docs/Discovery/README.md` обновлён под фактический состав discovery-layer, а `Plans/Roadmap.md` и `Plans/Backlog.md` синхронизированы так, чтобы `Research` считался уже введённым артефактом текущего этапа, а `Requirements` оставались следующими задачами без преждевременного ввода. `Tools/bp_lint.py` минимально расширен и теперь требует `Docs/Discovery/Research.md` как обязательный discovery-артефакт BytePress repo. Новый `ADR` не создавался, потому что проход исполнил уже утверждённый порядок `место -> шаблон -> артефакт` без нового устойчивого архитектурного решения.

### Эффект
`ROAD-000008` получил следующий реальный discovery-документ после `Discussion`, а planning-контур и lint-contract теперь согласованно учитывают `Research` как канонический артефакт текущего этапа.

---

## CHG-000037 — Discussion introduced as the first canonical artifact of ROAD-000008
ID: CHG-000037
Дата: 2026-04-01
Тип_изменения: Документация
Источник: First real ROAD-000008 pass after discovery template bootstrap
Связи: PLAN-000025, BACK-000038, QL-000032
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01

### Описание
`Docs/Discovery/Discussion.md` введён как первый реальный рабочий артефакт этапа `ROAD-000008` на основе уже существующего `Templates/Discussion.md`. `Docs/Discovery/README.md` обновлён под фактический discovery-layer, а `Plans/Roadmap.md` и `Plans/Backlog.md` синхронизированы так, чтобы `Discussion` считался уже введённым артефактом текущего этапа, а `Research` и `Requirements` оставались следующими задачами без преждевременного ввода. `Tools/bp_lint.py` минимально расширен и теперь требует `Docs/Discovery/Discussion.md` как обязательный discovery-артефакт BytePress repo. Новый `ADR` не создавался, потому что проход исполнил уже утверждённый порядок `место -> шаблон -> артефакт` без нового устойчивого архитектурного решения.

### Эффект
`ROAD-000008` получил первый реальный discovery-документ, а planning-контур и lint-contract теперь согласованно учитывают `Discussion` как канонический артефакт текущего этапа.

---

## CHG-000036 — ROAD-000007 closed, ROAD-000008 activated, and discovery templates introduced
ID: CHG-000036
Дата: 2026-04-01
Тип_изменения: Контракт
Источник: Transition pass from governance stage to research-and-requirements stage
Связи: PLAN-000024, BACK-000037, QL-000031
Дата_создания: 2026-04-01
Дата_изменения: 2026-04-01

### Описание
`Plans/Roadmap.md` и `Plans/Backlog.md` синхронизированы для перехода между этапами: `ROAD-000007` закрыт как завершённый governance-stage, а `ROAD-000008` активирован как текущий этап `Research and Requirements`. `BACK-000037` использован как стартовый pass этого этапа и после завершения перенесён в правильную секцию backlog без нарушения индексного канона. `Docs/Technical/Pipeline.md` закрепил место `Discussion`, `Research` и `Requirements` в конвейере и явное правило ввода новых типов артефактов по цепочке `место -> шаблон -> артефакт`. В `Templates/` добавлены канонические шаблоны `Discussion.md`, `Research.md`, `Requirements.md`, а `Tools/bp_lint.py` расширен ровно на требование этих новых обязательных template-файлов.

### Эффект
Governance-переход между `ROAD-000007` и `ROAD-000008` больше не содержит хвостов по статусам и секциям backlog, а discovery-stage получил каноническое место в `Pipeline` и обязательный template contract без преждевременного ввода рабочих discovery-документов.

---

## CHG-000035 — Analytical, product, and planning contours aligned for ROAD-000007
ID: CHG-000035
Дата: 2026-03-31
Тип_изменения: Документация
Источник: Planning alignment pass after pipeline governance rewrite
Связи: PLAN-000023, BACK-000036, QL-000030
Дата_создания: 2026-03-31
Дата_изменения: 2026-03-31

### Описание
`Docs/Discovery/Interview.md` минимально уточнён и теперь прямо фиксирует, что `Backlog` является производным от `Roadmap`, а `Plan` порождается из backlog-задачи. `Docs/Product/JTBD.md` и `Docs/Product/PRD.md` проверены и не потребовали изменений, потому что их текущая продуктовая рамка не противоречит current-truth интервью и текущему roadmap. В planning-layer исправлена синхронизация этапа `ROAD-000007`: `BACK-000032` убран из секции `Активные`, `Plans/Roadmap.md` теперь ссылается на фактический набор backlog-задач этапа, а текущий pass закреплён отдельным `PLAN-000023`. `ADRlog` и `bp_lint.py` не менялись, потому что новый архитектурный contract и обязательный lint contract в этом проходе не изменились.

### Эффект
Current-truth интервью, продуктовая рамка и planning-контур `ROAD-000007` больше не расходятся по роли backlog, статусам задач и связям текущего этапа.

---

## CHG-000034 — Pipeline, roadmap, and backlog governance aligned to the accepted stage model
ID: CHG-000034
Дата: 2026-03-31
Тип_изменения: Контракт
Источник: Pipeline governance pass after domain participation contract
Связи: PLAN-000022, BACK-000032, QL-000029
Дата_создания: 2026-03-31
Дата_изменения: 2026-03-31

### Описание
`Docs/Technical/Pipeline.md` приведён к полному канону фаз и теперь явно фиксирует правило `Roadmap -> Backlog -> Plan`, а также запрет на произвольное пополнение backlog вне этапов roadmap. `Plans/Roadmap.md` переписан как непрерывный дальний путь `ROAD-000001`...`ROAD-000014` без разрыва `ROAD-ID`, с крупноэтапным уровнем и новым текущим этапом `ROAD-000007`. `Plans/Backlog.md` перестроен как производный слой roadmap: карточки сгруппированы по `ROAD-*`, внутри этапов используются секции `Активные` и `Завершённые`, последние записи выровнены по порядку, для `ROAD-000007` заведены реальные текущие задачи, а для будущих этапов оставлены только кандидаты задач без `BACK-ID`. `ADRlog` и `bp_lint.py` не менялись, потому что новый архитектурный contract и обязательные пути репозитория в этом pass не изменились.

### Эффект
Governance-контур `Pipeline`, `Roadmap` и `Backlog` снова согласован: roadmap задаёт непрерывный дальний путь, backlog строго порождается из этапов roadmap, а текущий этап `ROAD-000007` получил реальные активные задачи вместо разрозненного process-noise.

---

## CHG-000033 — Domain participation contract clarified execution and extension domains
ID: CHG-000033
Дата: 2026-03-29
Тип_изменения: Документация
Источник: Domain participation pass after artifact lifecycle contract
Связи: PLAN-000021, BACK-000031, QL-000028
Дата_создания: 2026-03-29
Дата_изменения: 2026-03-29

### Описание
Уточнён participation contract доменов `Runtime/`, `Pipeline/`, `Adapters/`, `Memory/` и `MCP/` в общей технической модели и в локальных README этих доменов. `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/Artifact_Lifecycle.md` и `Docs/Technical/README.md` теперь согласованно фиксируют назначение доменов, их статус `0.1.0`, участие в lifecycle, признак источника истины и границы подмены. `Pipeline/README.md`, `Runtime/README.md`, `Adapters/README.md`, `Memory/README.md` и `MCP/README.md` приведены к тому же краткому контракту. `README.md`, `bp_lint.py` и `ADRlog` не менялись, потому что корневая карта, обязательный contract и архитектурные решения не потребовали расширения.

### Эффект
Исполнительные и расширяющие домены BytePress больше не описаны разрозненно: роль `Runtime/`, `Pipeline/`, `Adapters/`, `Memory/` и `MCP/` в системе и lifecycle читается одинаково в общей technical model и в локальных domain maps.

---

## CHG-000032 — Artifact lifecycle contract consolidated update order and reduced technical process noise
ID: CHG-000032
Дата: 2026-03-29
Тип_изменения: Контракт
Источник: Artifact lifecycle pass after branch/PR process cleanup
Связи: PLAN-000020, BACK-000030, QL-000027
Дата_создания: 2026-03-29
Дата_изменения: 2026-03-29

### Описание
Добавлен `Docs/Technical/Artifact_Lifecycle.md` как короткий канонический technical-contract жизненного цикла артефактов, их источников истины и обязательного порядка синхронизации после типов изменений. `Docs/Technical/Pipeline.md` сокращён до краткой роли конвейера и ссылки на новую точку детализации, а `Docs/Technical/README.md` и `Docs/README.md` синхронизированы с новым technical artifact. `bp_lint.py` минимально расширен и теперь требует `Docs/Technical/Artifact_Lifecycle.md` в репозитории `BytePress`; `ADRlog` не менялся, так как новый устойчивый architectural decision в этом проходе не появился.

### Эффект
Lifecycle-порядок артефактов больше не размазан между discovery, pipeline, roadmap, plans и logs: у `BytePress` теперь есть одна короткая technical-contract точка, а lint гарантирует её наличие в активном слое.

---

## CHG-000031 — Branch and PR process contract finalized and residual process noise removed
ID: CHG-000031
Дата: 2026-03-28
Тип_изменения: Документация
Источник: Branch/PR process cleanup pass after repo-wide active layer audit
Связи: PLAN-000019, BACK-000027, QL-000026
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Завершён process-contract для task-branch, local commits, self-check, final push, проверки существующего PR и создания PR в `develop`. `AGENTS.md`, `Setup_Guide.md` и `Docs/Technical/Platform_Contracts.md` синхронизированы по правилу не использовать `--dry-run`, если текущий `gh` его не поддерживает, и по fallback без автоматической переавторизации `gh` при ошибке команды PR. `Plans/README.md` очищен от устаревшей привязки к раннему диапазону plan-files, а в `Roles/Developer.md`, `Roles/QA.md` и `Roles/Release.md` заменены остаточные ссылки `Plans/PLAN-*.md` на `Plans/BP-*.md`. `bp_lint.py` и `ADRlog` не менялись, так как обязательный contract и архитектурные решения в этом проходе не изменились.

### Эффект
Process-facing слой BytePress теперь описывает один и тот же практический branch/PR workflow без двусмысленностей по моменту `push`, созданию PR, `gh` fallback и повторному использованию head-ветки после merge.

---

## CHG-000030 — Repo-wide active layer audit aligned maps, roles, skills and technical references
ID: CHG-000030
Дата: 2026-03-28
Тип_изменения: Документация
Источник: Repo-wide audit pass after product, discovery and sync-contract canon alignment
Связи: PLAN-000018, BACK-000019, QL-000025
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Проведён repo-wide аудит активного слоя `BytePress` после отдельных проходов по product-layer, discovery-layer и pipeline sync-contract. В `README.md`, `AGENTS.md` и `Tools/README.md` устранены устаревшие формулировки и закреплена текущая модель discovery-layer, крупноэтапного `Roadmap` и lint-checks. В `Docs/Technical/Product_Bootstrap_Validation.md` выровнена фактическая формулировка validation-контракта, в `Roles/Business_Analyst.md`, `Roles/System_Analyst.md`, `Roles/Architect.md`, `Skills/Interview.md` и `Skills/Planning.md` исправлены реальные рассогласования по `Docs/Discovery/`, current-truth интервью и каноническому виду `Plans/BP-*.md`. В `Plans/Archive/PLAN-000017-discovery-and-sync-contract.md` удалён дублирующийся артефакт `Logs/ADRlog.md`; `bp_lint.py` не менялся, потому что обязательный contract в этом audit-pass не изменился.

### Эффект
Активный слой BytePress снова согласован repo-wide: карты, validation-контракт, роли, навыки и активные планы используют один и тот же текущий канон product/discovery/pipeline без большого рефакторинга и без переписывания historical layer.

---

## CHG-000029 — Discovery layer, interview current truth and sync contract surfaced
ID: CHG-000029
Дата: 2026-03-28
Тип_изменения: Контракт
Источник: Discovery/sync-contract pass after delivery/bootstrap/lint alignment
Связи: PLAN-000017, BACK-000029, ADR-000017, QL-000024
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Добавлен новый аналитический слой `Docs/Discovery/` с `README.md` и каноническим `Interview.md`, а также создан `Templates/Interview.md` как минимальный шаблон current-truth интервью. `Plans/Roadmap.md` приведён к уровню крупных этапов системы, `Docs/Technical/Pipeline.md` дополнен минимальной sync-matrix обязательной проверки связанных артефактов, `Docs/README.md`, `Plans/README.md`, `Docs/Technical/Architecture.md`, `Docs/Technical/Model.md`, `Docs/Technical/README.md` и `Templates/README.md` синхронизированы с новой моделью. `bp_lint.py` расширен так, чтобы валидировать `Docs/Discovery/README.md`, `Docs/Discovery/Interview.md` и `Templates/Interview.md`. В `ADR-000017` зафиксированы discovery-domain, current-truth модель интервью и sync-contract pipeline.

### Эффект
Аналитический слой BytePress стал явной частью `Docs/`, интервью закреплено как текущая истина, roadmap перестал дублировать backlog мелкими проходами, а pipeline contract получил обязательные правила синхронизации после изменения ключевых артефактов.

---

## CHG-000028 — Delivery template, bootstrap, and lint contracts synchronized with product layer canon
ID: CHG-000028
Дата: 2026-03-28
Тип_изменения: Контракт
Источник: Delivery/bootstrap/lint sync pass after product-layer normalization
Связи: PLAN-000016, BACK-000028, QL-000023
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28

### Описание
Добавлен `Templates/Delivery.md`, а `Templates/README.md` и `Docs/Product/Delivery.md` приведены к новому минимальному шаблону поставки. `Docs/Technical/Product_Bootstrap_Contract.md` и `Docs/Technical/Product_Bootstrap_Validation.md` синхронизированы с каноническим продуктовым набором `Docs/Product/README.md`, `Docs/Product/JTBD.md`, `Docs/Product/PRD.md`, `Docs/Product/Delivery.md`. `bp_bootstrap.py` теперь материализует весь этот набор в product repo, а `bp_lint.py` требует `Templates/Delivery.md` в `BytePress` и проверяет наличие полного минимального `Docs/Product/*` слоя в bootstrap-продукте. Краткая синхронизация добавлена в `Tools/README.md`.

### Эффект
Шаблоны, bootstrap-documentation, генерация продукта и lint используют один и тот же минимальный contract продуктового слоя; bootstrap smoke-check подтверждает, что этот contract действительно материализуется и валидируется.

---

## CHG-000027 — Product layer aligned with canonical templates and minimal document scope
ID: CHG-000027
Дата: 2026-03-27
Тип_изменения: Документация
Источник: Product-layer normalization pass after accepted JTBD and PRD templates
Связи: PLAN-000015, BACK-000026, QL-000022
Дата_создания: 2026-03-27
Дата_изменения: 2026-03-27

### Описание
`Docs/Product/PRD.md` и `Docs/Product/JTBD.md` приведены к каноническим шаблонам с сохранением продуктового смысла и без смешения с внутренними техническими слоями. `Docs/Product/README.md` и `Docs/Product/Delivery.md` сокращены до минимального продуктового канона, а `Docs/Product/Implementation_Plan.md` и `Docs/Product/Profiles.md` удалены как дубли или документы вне продуктовой границы. Технические документы bootstrap перенесены в `Docs/Technical/Product_Bootstrap_Contract.md` и `Docs/Technical/Product_Bootstrap_Validation.md`, после чего прямые ссылки в активных `Plans/*` и текущих журналах синхронизированы.

### Эффект
Продуктовый слой BytePress больше не смешивает продуктовые требования с внутренними системными описаниями и содержит только канонический минимальный набор документов, а технический bootstrap knowledge живёт в профильном слое `Docs/Technical/`.

---

## CHG-000026 — Release branch example aligned with canonical branch naming
ID: CHG-000026
Дата: 2026-03-19
Тип_изменения: Документация
Источник: Release-readiness cleanup before recreating the 0.1.0 release branch
Связи: CHG-000025, QL-000021
Дата_создания: 2026-03-19
Дата_изменения: 2026-03-19

### Описание
В `Setup_Guide.md` пример release-ветки приведён к каноническому формату `<type>/<NNNNNN>-<slug>` и заменён с `release/0.1.0` на `release/000019-0.1.0-rc2` в командах создания, открытия PR и удаления ветки.

### Эффект
Практический release workflow больше не противоречит принятому branch naming contract перед пересозданием release branch `0.1.0`.

---

## CHG-000025 — Release governance and README product value formalized before main preparation
ID: CHG-000025
Дата: 2026-03-18
Тип_изменения: Документация
Источник: Release branch workflow formalization before main preparation
Связи: STD-000004, CHG-000024, QL-000020
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
В `README.md` кратко усилено описание ценности `BytePress` как системы, которая формирует устойчивый контекст вокруг продукта, удерживает агента в управляемом контуре и снижает недетерминированность в SDLC. В `AGENTS.md`, `Setup_Guide.md`, `Docs/Technical/Platform_Contracts.md` и `Standards/Release.md` зафиксирован release-branch workflow для `release/*` как временной стабилизационной ветки от `develop` с PR только в `main`, без feature-work и с возвратом release-only fixes в `develop` при необходимости.

### Эффект
Release governance и краткое product value message формализованы до подготовки первого выхода `BytePress` в `main`.

---

## CHG-000024 — Planning truth aligned with logs truth for release preparation
ID: CHG-000024
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Release-readiness alignment pass for planning truth
Связи: PLAN-000006, BACK-000017, BACK-000018
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
В `Plans/Backlog.md` статусы `BACK-000017` и `BACK-000018` выровнены до `Завершено`, чтобы planning truth соответствовал уже зафиксированным `PLAN-000006`, `CHG-000012` и `QL-000007` перед подготовкой release branch `0.1.0`.

### Эффект
Planning truth и logs truth больше не расходятся по закрытию branch lifecycle и Auto-PR preparation pass.

---

## CHG-000023 — Orphan IDs removed from active plans and approval rule without new namespaces
ID: CHG-000023
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Orphan ID cleanup after semver operationalization
Связи: PLAN-000014, BACK-000019
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
Из `Plans/Archive/PLAN-000001-foundation.md` и `Plans/Archive/PLAN-000002-seed-docs-and-standards.md` удалён orphan ID `BP-REQ-0001` без введения нового requirement namespace и без замены его новой сущностью требований. Из `Rules/Approval_Strictness.md` удалён orphan ID `PIPE-0001`; смысл зависимости от конвейерных фаз сохраняется в текстовом описании и проверке правила без нового pipeline namespace.

### Эффект
Активный non-log слой BytePress больше не содержит оставшихся orphan ID `BP-REQ-0001` и `PIPE-0001`; ссылки и смысл документов сохранены без расширения модели и без добавления новых registry-доменов.

---

## CHG-000022 — Semver operationalized for active BytePress documents at baseline 0.1.0
ID: CHG-000022
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Semver operationalization pass after historical log migration
Связи: PLAN-000013, BACK-000019
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
В `Standards/Naming.md` и `Docs/Technical/Platform_Contracts.md` зафиксирован current operational baseline `BytePress` как `0.1.0`, а активные non-log документы переведены с использования `v1` на semver-метку `0.1.0` там, где `v1` обозначал текущий baseline-состояние системы. Historical logs намеренно не переписывались.

### Эффект
Текущий operational contract `BytePress` теперь маркируется через semver, а не через размытое обозначение `v1`, что снимает двусмысленность между baseline системы и историческими фазами её развития.

---

## CHG-000021 — Historical logs migrated to six-digit IDs and active references synced
ID: CHG-000021
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Late-phase historical logs migration after active non-log ID normalization
Связи: PLAN-000012, BACK-000024, ADR-000015
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
`Logs/ADRlog.md`, `Logs/ChangeLog.md` и `Logs/QualityLog.md` приведены к 6-значному формату исторических `ADR`, `CHG` и `QL ID` без изменения смысла записей, порядка, дат и текста истории. Прямые ссылки на historical log IDs в `Plans/*`, `Docs/Technical/*`, `Docs/Product/*`, `Rules/*`, `Standards/*`, `Adapters/*`, `Tools/README.md` и `Plans/Backlog.md` синхронизированы с новым форматом. Однозначные ссылки на старые `BACK` и `ROAD` в самих historical logs также приведены к уже действующему 6-значному формату, а `BP-REQ-0001` и `PIPE-0001` оставлены без изменений.

### Эффект
Журнальный исторический слой больше не смешивает 4- и 6-значный формат идентификаторов, а активные non-log документы ссылаются на historical logs по одному каноническому виду ID.

---

## CHG-000020 — Active non-log ID layer переведён на 6-значный формат без переписывания historical logs
ID: CHG-000020
Дата: 2026-03-18
Тип_изменения: Контракт
Источник: Следующая фаза repo-wide migration после term и tool sync-проходов
Связи: PLAN-000011, BACK-000019, ADR-000015, ADR-000016
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
Активные non-log internal ID в `Plans/Backlog.md`, `Plans/Roadmap.md`, `Profiles/*`, `Rules/*`, `Standards/*`, `Roles/*`, `Skills/*`, `Adapters/*`, `Memory/Registry.md`, `MCP/Registry.md`, `Docs/Technical/*` и `Docs/Technical/Product_Bootstrap_Contract.md` приведены к 6-значному формату для `BACK`, `ROAD`, `PROF`, `RULE`, `STD`, `ROLE`, `SKILL`, `ADP`, `MEM` и `MCP`. Прямые ссылки на старые 4-значные active ID синхронизированы, создан `Plans/Archive/PLAN-000011-migrate-active-nonlog-ids.md`, а historical logs намеренно не переписывались.

### Эффект
Активный non-log слой BytePress перестал смешивать 4- и 6-значный формат внутренних ID; текущие рабочие связи по singleton- и registry-доменам согласованы с repo-wide naming migration policy без запуска historical log rewrite-pass.

---

## CHG-000019 — Tool contract sync завершил приведение bootstrap и lint к текущим contracts
ID: CHG-000019
Дата: 2026-03-18
Тип_изменения: Инструмент
Источник: Исполнение tool contract sync после naming/profile/language migration passes
Связи: PLAN-000010, BACK-000022, ADR-000015, ADR-000016
Дата_создания: 2026-03-18
Дата_изменения: 2026-03-18

### Описание
`bp_bootstrap.py` переведён на обязательные параметры `--name`, `--product-code`, `--brand-profile`, `--target`; bootstrap теперь валидирует brand profile в `BytePress`, использует текущую дату выполнения, создаёт `Profiles/Product.md`, initial plan file `Plans/<PRODUCT_CODE>-000001-product-initialization.md` и 6-значные ID. `bp_lint.py` минимально обновлён под новый product bootstrap output contract, а `Tools/README.md`, `Docs/Technical/Product_Bootstrap_Contract.md`, `Docs/Technical/Product_Bootstrap_Validation.md` и `Profiles/README.md` синхронизированы с фактическим поведением инструментов; позднее contract дополнительно расширен каноническим `Delivery` template и полным минимальным `Docs/Product/*` набором.

### Эффект
Инструментальный контур больше не расходится с принятыми naming/profile/language contracts: bootstrap и lint работают по одному минимальному product bootstrap contract без большого рефакторинга tools.

---

## CHG-000018 — Terms layer мигрирован на канонические filenames и 6-значные TERM ID
ID: CHG-000018
Дата: 2026-03-17
Тип_изменения: Документация
Источник: Исполнение term migration phase из repo-wide naming policy
Связи: PLAN-000009, BACK-000023, ADR-000015
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
`Docs/Terms/*` приведены к каноническим filenames `TERM-<NNNNNN>-<slug>.md`, внутренние `TERM ID` выровнены до `TERM-000001`...`TERM-000016`, `Base_Terms.md` и прямые term-ссылки в `Docs/Technical/Model.md`, `Plans/Archive/PLAN-000003-fill-technical-and-rules.md`, `Plans/Archive/PLAN-000004-fill-skills-and-tools.md`, `Standards/*`, `Rules/Terms_Governance.md` и `Logs/ADRlog.md` синхронизированы. `bp_normalize_terms.py` минимально обновлён под новый filename pattern, а `Docs/Terms/README.md` и `Plans/Backlog.md` приведены к фактическому состоянию migration-pass.

### Эффект
Term layer перестал смешивать legacy filenames и 4-значные `TERM ID`; индекс словаря и прямые ссылки по репозиторию теперь согласованы с принятым naming contract без запуска migration для `Schemas/*`, `Templates/*`, `Profiles/*`, semver и historical logs.

---

## CHG-000017 — Синхронизированы схемы, шаблоны, профили и language contract Git/PR
ID: CHG-000017
Дата: 2026-03-17
Тип_изменения: Контракт
Источник: Первый migration-pass после фиксации repo-wide policy
Связи: ADR-000016, PLAN-000008, BACK-000021, BACK-000022, BACK-000025
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
`Schemas/*` и `Templates/*` переведены на 6-значную числовую часть `ID`, `Schemas/README.md` и `Templates/README.md` синхронизированы с новым контрактом, а `profile.schema.json` и `Templates/Profile.md` расширены полями `Тип_профиля`, `Код_продукта` и `Язык_взаимодействия`. `Profiles/README.md`, `Profiles/Default.md` и `Profiles/Speculorg.md` приведены к актуальной модели brand profiles с semantic filename и 6-значными внутренними `PROF ID`. В `AGENTS.md`, `Docs/Technical/Platform_Contracts.md` и `Standards/Documentation.md` зафиксировано правило английского языка для commit/PR artifacts и `branch slug`. Создан `Plans/Archive/PLAN-000008-schemas-templates-profiles-and-language-sync.md`.

### Эффект
Первый repo-wide migration-pass замкнул контракт между схемами, шаблонами, профилями и Git/PR-языком без запуска миграции `Terms/*`, `Tools/*`, semver и historical logs.

---

## CHG-000016 — Зафиксирована repo-wide policy фазной ID migration без запуска rewrite-pass
ID: CHG-000016
Дата: 2026-03-17
Тип_изменения: Контракт
Источник: Policy-проход после нормализации current plan layer
Связи: ADR-000015, PLAN-000007, BACK-000021, BACK-000022, BACK-000023, BACK-000024
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Уточнены `Standards/Naming.md`, `Docs/Technical/Model.md`, `Docs/Terms/README.md`, `Profiles/README.md` и `Plans/Backlog.md`: зафиксирована repo-wide policy фазной миграции ID и правил filename по доменам, различены serial-, hybrid- и singleton-домены, зафиксирован целевой контракт для `Docs/Terms/*`, подтверждено semantic-filename правило для brand profiles в `BytePress`, а historical logs вынесены в отдельную позднюю фазу миграции. Создан `Plans/Archive/PLAN-000007-id-migration-policy-and-phase-plan.md` как план policy-прохода без запуска самой миграции.

### Эффект
Репозиторий получил явный phase plan для remaining ID migration: новые артефакты создаются только по новому контракту, а legacy-слои переходят на него управляемыми отдельными проходами.

---

## CHG-000015 — Remaining plan layer приведён к каноническим именам и 6-значным plan ID
ID: CHG-000015
Дата: 2026-03-17
Тип_изменения: Документация
Источник: Исполнение принятого naming contract для remaining plan layer
Связи: ADR-000014, PLAN-000002, PLAN-000003, PLAN-000004, PLAN-000005, PLAN-000006, BACK-000021, BACK-000022
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Remaining plan-files приведены к каноническим именам `Plans/Archive/PLAN-000002-seed-docs-and-standards.md`, `Plans/Archive/PLAN-000003-fill-technical-and-rules.md`, `Plans/Archive/PLAN-000004-fill-skills-and-tools.md`, `Plans/Archive/PLAN-000005-adapters-memory-mcp-and-bootstrap.md` и `Plans/Archive/PLAN-000006-branch-lifecycle-auto-pr-and-audit-preparation.md`. Их внутренние `ID` выровнены до `PLAN-000002`...`PLAN-000006`, прямые ссылки в `Plans/Roadmap.md`, `Plans/Backlog.md`, `Logs/ADRlog.md`, `Logs/ChangeLog.md`, `Logs/QualityLog.md`, `Docs/Technical/Product_Bootstrap_Validation.md` и минимально в `Tools/bp_lint.py` обновлены под новый канон. `PLAN-000006` переведён в `Завершено` по фактически закрытому DoD.

### Эффект
Весь текущий plan layer BytePress теперь использует один naming contract и 6-значные plan ID без смешения 4- и 6-значного формата в актуальных плановых артефактах.

---

## CHG-000014 — Нормализован foundation-план BytePress и удалён legacy-дубль
ID: CHG-000014
Дата: 2026-03-17
Тип_изменения: Документация
Источник: Исполнение принятого naming contract для слоя `Plans/`
Связи: ADR-000014, PLAN-000001, BACK-000020
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Foundation-план BytePress приведён к каноническому имени `Plans/Archive/PLAN-000001-foundation.md`, его внутренний `ID` выровнен до `PLAN-000001`, статус приведён к фактическому состоянию `Завершено`, legacy-дубль `Plans/Plan_BP-0001_BytePress_V1.md` удалён, а `Plans/README.md` и продуктовый слой перепривязаны к актуальному plan-layer без отдельного дубля плана. Прямые ссылки в `Roadmap`, `Backlog` и связанных журнальных записях обновлены на новый `ID`.

### Эффект
В слое `Plans/` устранён параллельный канон для foundation-плана BytePress: остался один актуальный файл, один актуальный `ID` и одна рабочая точка ссылок для связанных документов.

---

## CHG-000013 — Зафиксирован контракт 6-значных ID, naming plan-file и модель профилей
ID: CHG-000013
Дата: 2026-03-17
Тип_изменения: Контракт
Источник: Контрактный проход перед нормализацией legacy-слоя `Plans/*`
Связи: ADR-000014, BACK-000019, BACK-000020, BACK-000021, BACK-000022
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17

### Описание
Уточнены `Standards/Naming.md`, `Docs/Technical/Model.md`, `Profiles/README.md`, `Plans/README.md` и `Plans/Backlog.md`: зафиксированы 6-значная числовая часть ID, каноническое имя plan-file `Plans/<PRODUCT_CODE>-<NNNNNN>-<slug>.md`, правила `PRODUCT_CODE`, граница `brand profile` / `product profile` и статус текущего слоя `Plans/*` как legacy до отдельного PR нормализации. В backlog добавлены отдельные задачи на нормализацию `Plans/*` и последующее приведение `Schemas/*`, `Templates/*` и `Tools/*` к новому контракту.

### Эффект
Система получила явный контракт именования и профилей до переименования legacy-планов, что снимает двусмысленность для следующих проходов и разделяет текущий контрактный шаг от будущей миграции исторического слоя.

---

## CHG-000012 — Зафиксированы branch lifecycle, целевой Auto-PR процесс и следующий плановый проход
ID: CHG-000012
Дата: 2026-03-14
Тип_изменения: Процесс
Источник: Уточнение управляемого Git/PR-контура BytePress
Связи: ADR-000013, PLAN-000006, BACK-000017, BACK-000018, BACK-000019
Дата_создания: 2026-03-14
Дата_изменения: 2026-03-14

### Описание
Уточнены `AGENTS.md`, `Docs/Technical/Platform_Contracts.md` и `Setup_Guide.md`: зафиксирован полный жизненный цикл ветки, целевой порядок Auto-PR после `push`, правило закрытия head-ветки после merge и минимальная подготовка `gh`. В `Backlog` и новом `Plan` добавлен следующий проход под branch lifecycle, Auto-PR process и подготовку к большому аудиту.

### Эффект
Процесс веток и PR стал управляемым и навигационно закреплённым, а следующий шаг по развитию локального агентного контура вынесен в плановый контур без запуска большого рефакторинга.

---

## CHG-000011 — Добавлены корневые карты README.md и AGENTS.md и обновлены минимальные контракты агентной работы
ID: CHG-000011
Дата: 2026-03-14
Тип_изменения: Документация
Источник: Синхронизация канона BytePress с фактической агентной работой
Связи: ADR-000010, ADR-000012
Дата_создания: 2026-03-14
Дата_изменения: 2026-03-14

### Описание
Добавлен корневой `AGENTS.md` как карта для агента, обновлён корневой `README.md` как карта для человека, минимально уточнены `Standards/Naming.md` и `Docs/Technical/Platform_Contracts.md` для фиксации веточного и PR-контура.

### Эффект
Навигация для человека и агента разведена, а минимальный канон текущего рабочего режима зафиксирован в постоянных артефактах.

---

## CHG-000010 — Подтверждён рабочий цикл agent push -> agent PR -> human approve -> human merge в GitHub
ID: CHG-000010
Дата: 2026-03-14
Тип_изменения: Процесс
Источник: Публикация BytePress в GitHub и фактические эпизоды агентной работы
Связи: ADR-000010, ADR-000011, ADR-000012
Дата_создания: 2026-03-14
Дата_изменения: 2026-03-14

### Описание
Подтверждён рабочий контур: агент работает в task-ветке, выполняет `push`, готовит PR, человек утверждает направление и выполняет merge в `develop`/`main`.

### Эффект
GitHub-процесс BytePress стал явным и воспроизводимым для следующих проходов агентной работы.

---

## CHG-000009 — Усилен bootstrap продукта и подтверждён тестовой генерацией
ID: CHG-000009
Дата: 2026-03-10
Тип_изменения: Инструмент
Источник: PLAN-000005
Связи: BACK-000016, ADR-000009, ROAD-000007
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
`bp_bootstrap.py` усилен до продуктового полезного минимума: теперь он создаёт не только папки, но и минимальные документы, журналы, один стартовый `Plan`, один стартовый backlog-элемент и управляемые скрипты продукта. Выполнена отдельная тестовая генерация каркаса `Speculorg.Terminal`.

### Эффект
Bootstrap продукта перестал быть декларативной заготовкой и стал подтверждённой функцией `BytePress v1`.

---

## CHG-000008 — Оформлен интеграционный каркас Adapters, Memory и MCP
ID: CHG-000008
Дата: 2026-03-10
Тип_изменения: Архитектура
Источник: PLAN-000005
Связи: BACK-000013, BACK-000014, BACK-000015, ADR-000008, ROAD-000007
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Домены `Adapters/`, `Memory/` и `MCP/` переведены из пустых заготовок в согласованный каркас: добавлены политика, реестры, интерфейсы и явные границы применения.

### Эффект
`BytePress` получил управляемый интеграционный контур расширения без внедрения лишней сложности в ядро знания.


---

## CHG-000007 — Замкнут исполнительный контур ролей, навыков и инструментов BytePress
ID: CHG-000007
Дата: 2026-03-10
Тип_изменения: Исполнение
Источник: PLAN-000004
Связи: BACK-000011, BACK-000012, ADR-000007, ROAD-000003, ROAD-000006
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Библиотека навыков BytePress усилена до полного набора фаз золотого пути, добавлены `Implementation` и `Quality`, существующие навыки приведены к единому формату. Инструменты `bp_bootstrap.py` и `bp_normalize_terms.py` переведены из заглушек в полезный минимум `v1`, а `bp_lint.py` согласован с исполнительным контуром. Роли и профили обновлены под актуальные навыки и стандарты.

### Эффект
BytePress получил рабочий исполнительный контур: роли, навыки, инструменты и профиль теперь поддерживают один и тот же порядок работы и перестали расходиться между собой.

---

## CHG-000006 — Усилен технический слой и контур правил BytePress
ID: CHG-000006
Дата: 2026-03-10
Тип_изменения: Архитектура
Источник: PLAN-000003
Связи: BACK-000009, BACK-000010, ADR-000005, ADR-000006
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
`Docs/Technical/*` заполнены до уровня рабочего технического контура `v1`, а `Rules/` дополнен правилами о доменных границах, планах, журналах и порядке массового наполнения.

### Эффект
BytePress получил не только каркас, но и явное техническое объяснение своего устройства и достаточный набор обязательных ограничений для системной работы.

---

## CHG-000005 — Введён рабочий журнальный контур решений и изменений
ID: CHG-000005
Дата: 2026-03-10
Тип_изменения: Процесс
Источник: PLAN-000002
Связи: BACK-000008, ADR-000002, ADR-000003, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
В `ADRlog` и `ChangeLog` добавлены пропущенные записи по уже принятым архитектурным решениям и значимым изменениям. Плановый и журнальный контуры приведены к рабочему режиму.

### Эффект
Журналы перестали быть пустой формальностью и стали системным контуром фиксации решений и значимых изменений.

---

## CHG-000004 — Заполнены короткие стандарты BytePress полезными практиками
ID: CHG-000004
Дата: 2026-03-10
Тип_изменения: Стандарт
Источник: PLAN-000002
Связи: BACK-000007, ADR-000003, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Стандарты `Documentation`, `Terminology`, `Planning`, `Coding` и `Release` усилены только теми практиками из Speculorg, которые полезны на текущем этапе.

### Эффект
BytePress получил рабочие короткие нормативы вместо пустых или слишком абстрактных заготовок.

---

## CHG-000003 — Заполнена базовая терминология BytePress и политика её изменений
ID: CHG-000003
Дата: 2026-03-10
Тип_изменения: Документация
Источник: PLAN-000002
Связи: BACK-000006, ADR-000002, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Созданы отдельные карточки базовых терминов BytePress, индекс словаря и политика изменения терминов.

### Эффект
Терминологическая база стала управляемой: определения вынесены в отдельные сущности, а ввод новых терминов теперь подчинён явной процедуре.

---

## CHG-000002 — Уточнены схемы и шаблоны ключевых сущностей
ID: CHG-000002
Дата: 2026-03-10
Тип_изменения: Стандарт
Источник: PLAN-000001
Связи: BACK-000004, ADR-000004
Дата_создания: 2026-03-10
Дата_изменения: 2026-03-10

### Описание
Уточнены `Schemas/` и `Templates/` для `Term`, `Roadmap`, `Backlog`, `Plan`, `ADRlog`, `ChangeLog`, `Profile`, `Role`, `Rule`, `Standard`.

### Эффект
Контракты данных стали пригодны для системного заполнения документов и дальнейшей автоматической проверки.

---

## CHG-000001 — Создан первичный каркас BytePress v1
ID: CHG-000001
Дата: 2026-03-09
Тип_изменения: Структура
Источник: PLAN-000001
Связи: ADR-000001, BACK-000003
Дата_создания: 2026-03-09
Дата_изменения: 2026-03-10

### Описание
Создан первичный каркас `BytePress v1` с доменным корнем, базовыми документами, журналами, профилями, ролями, правилами и стандартами.

### Эффект
Появилась переносимая основа системы, пригодная для дальнейшего уточнения контрактов данных.

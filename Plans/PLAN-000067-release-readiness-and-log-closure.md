# PLAN-000067 — Release readiness and log closure

ID: PLAN-000067
Название: Закрыть `ROAD-000015` и собрать канонический release/journaling closure contour
Статус: Завершено
Связи: BACK-000079
Источник: Новый stage-closing corrective pass этапа `ROAD-000015`
Дата_создания: 2026-04-15
Дата_изменения: 2026-04-15
Основание: После закрытия `ROAD-000014` active contracts всё ещё держат release/journaling gaps: release workflow до `main` описан неполно, `ReleaseLog.md` не содержит factual записи о подтверждённом tag/history event `0.1.0`, а `ChangeLog.md` и `QualityLog.md` обрываются до ряда уже завершённых pass. Нужен один узкий corrective stage, который зафиксирует полный release workflow, дозаполнит history-facts и при clean audit закроет `ROAD-000015` без открытия нового roadmap-stage.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000079
Связанные_ADR:
- отсутствуют

## Шаги
1. Активировать и сразу ограничить corrective stage `ROAD-000015`.
   - Описание: Обновить `Roadmap` и `Backlog`, создать одну backlog-задачу `BACK-000079` и один current `Plan`, а завершённый `PLAN-000066` вывести в archive-layer.
   - DoD: planning-layer согласован для одного corrective pass без открытия нового `ROAD-*`.
2. Довести release workflow до полного канона.
   - Описание: Уточнить `Setup_Guide.md`, `Standards/Release.md`, `Artifact_Lifecycle.md`, evidence contracts и `Pipeline/Phase_Gates.md`, чтобы release path явно покрывал release branch creation, final validation, PR в `main`, tag creation/push, cleanup release branch, sync `develop` и factual release logging path.
   - DoD: repo contracts больше не спорят о полном release workflow до `main`.
3. Дозаполнить factual journal closure.
   - Описание: Добавить пропущенные `ChangeLog` и `QualityLog` записи начиная с первого реально незалогированного pass после `CHG-000040` / `QL-000035`, а также factual `ReleaseLog` запись о `0.1.0`, если она подтверждена tag/history.
   - DoD: log-layer не содержит доказанных пропусков по scope corrective stage.
4. Провести финальный audit и закрыть stage.
   - Описание: Проверить release-readiness, journaling closure, planning sync и отсутствие residual blocker для подготовки `0.2.0`; затем закрыть `ROAD-000015` и вывести backlog этапа в archive-layer.
   - DoD: `ROAD-000015` закрыт clean audit'ом и не активирует новый roadmap-stage автоматически.

## Ограничения
- без release branch `0.2.0` внутри этого pass;
- без merge в `main` и без фактического релиза `0.2.0`;
- без правок `Tools/*`, если audit не докажет прямой structural gap;
- без правок product bootstrap, integration contour и generated product repo contracts вне доказанной связи с release/journaling gap;
- без новых `ADR`, если audit не докажет новый устойчивый архитектурный выбор.

## Риски
- если release workflow останется неполным, подготовка `0.2.0` снова будет опираться на неявные шаги и личную память;
- если history-fact журналы останутся с пропусками, release-readiness audit снова будет неполным даже при согласованном planning-layer;
- если `ReleaseLog.md` начнёт хранить прогнозы вместо factual events, release contour снова смешает candidate state и history-fact.

## Артефакты
- `AGENTS.md`
- `Setup_Guide.md`
- `Standards/Release.md`
- `Logs/README.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `Logs/ReleaseLog.md`
- `Docs/Technical/Artifact_Lifecycle.md`
- `Docs/Technical/Verification_Evidence.md`
- `Docs/Technical/Validation_Evidence.md`
- `Pipeline/Phase_Gates.md`
- `Plans/README.md`
- `Docs/User/Pass_Request.md`
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000015.md`

## DoD
- создана одна новая backlog-задача и один новый current `Plan` для corrective stage `ROAD-000015`.
- `ROAD-000015` активирован и закрыт в пределах этого же pass.
- release workflow до `main` явно покрывает release branch creation, final validation, PR в `main`, tag creation/push, cleanup release branch, sync `develop` и factual release logging path.
- `ChangeLog.md` и `QualityLog.md` больше не имеют доказанных пропусков по завершённым pass, начиная с первого реально незалогированного прохода.
- `ReleaseLog.md` содержит factual запись о `0.1.0` на основании подтверждённого tag/history.
- `AGENTS.md` и соседние owner-contracts явно не позволяют пропускать log closure в содержательном pass.
- `python3 Tools/bp_lint.py --repo .` проходит без изменения `Tools/*`.
- после финального audit не остаётся доказанного release-blocker для подготовки `0.2.0`.

## Результат
- `ROAD-000015` активирован и закрыт в одном corrective pass без открытия нового roadmap-stage.
- `Setup_Guide.md`, `Standards/Release.md`, `Artifact_Lifecycle.md`, evidence contracts и `Phase_Gates.md` теперь согласованно фиксируют полный release workflow до `main`, включая post-release factual logging path.
- `ChangeLog.md` и `QualityLog.md` дозаполнены для завершённых pass, начиная с первого реально незалогированного прохода после `CHG-000040` / `QL-000035`.
- `ReleaseLog.md` получил factual запись `RL-000006` о release event `0.1.0`, подтверждённом annotated tag `0.1.0` на commit `92891482e9bc88940069700ba93890fb317b5cab`.
- `bp_lint.py` не менялся, потому что audit не подтвердил прямого structural gap; `bp_lint contract unaffected`.

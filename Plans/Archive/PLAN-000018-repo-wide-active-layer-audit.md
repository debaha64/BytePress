# PLAN-000018 — Repo-wide active layer audit

ID: PLAN-000018
Название: Провести repo-wide аудит активного слоя BytePress
Статус: Завершено
Связи: BACK-000019, CHG-000030, QL-000025
Источник: Audit-pass после введения product-layer canon, discovery-layer canon и artifact sync-contract
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28
Основание: После отдельных проходов по product-layer, discovery-layer и sync-contract нужно проверить, что активный слой `BytePress` согласован не только локально в каждом домене, но и repo-wide: карты, technical docs, роли, навыки, tools docs и активные планы должны отражать текущий канон без скрытых устаревших формулировок.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000019
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур audit-pass.
   - Описание: Обновить `BACK-000019` под фактический смысл текущего repo-wide аудита и создать отдельный plan-file.
   - DoD: `BACK-000019` переведён в `В_работе`, а `Plans/Archive/PLAN-000018-repo-wide-active-layer-audit.md` фиксирует scope и ограничения прохода.
2. Проверить и минимально выровнять карты и technical docs.
   - Описание: Аудировать root maps, layer README и `Docs/Technical/*` только в части реальных рассогласований с product/discovery/sync-contract canon.
   - DoD: карты системы и technical docs не содержат устаревшей модели product/discovery/roadmap/pipeline.
3. Проверить роли, навыки и активные планы.
   - Описание: Аудировать `Roles/*`, `Skills/*` и активные `Plans/BP-*` на устаревшие прямые ссылки и формулировки, которые теперь вводят в заблуждение.
   - DoD: исправлены только реальные содержательные рассогласования активного слоя без переписывания истории и без большого рефакторинга.
4. Зафиксировать audit-pass в плановом и журнальном контуре.
   - Описание: Закрыть plan/backlog, обновить `ChangeLog` и `QualityLog`, а `ADR` создавать только при появлении нового устойчивого решения.
   - DoD: `python3 Tools/bp_lint.py --repo .` проходит, `BACK-000019` отражает фактический результат audit-pass, historical layer не переписывается.

## Риски
- попытка превратить audit-pass в большой rewrite выведет задачу за пределы согласованного scope;
- переписывание historical logs или process-docs смешает активный audit с историческим слоем;
- необоснованное изменение `bp_lint.py` создаст лишний contract drift вместо фиксации реальной необходимости.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Archive/PLAN-000018-repo-wide-active-layer-audit.md`
- `README.md`
- `AGENTS.md`
- `Tools/README.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Roles/Business_Analyst.md`
- `Roles/System_Analyst.md`
- `Roles/Architect.md`
- `Skills/Interview.md`
- `Skills/Planning.md`
- `Plans/Archive/PLAN-000017-discovery-and-sync-contract.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`

## DoD
- `BACK-000019` отражает актуальный смысл repo-wide audit-pass.
- root maps и layer maps согласованы с текущим каноном product/discovery/pipeline.
- `Docs/Technical/*`, `Roles/*`, `Skills/*` и активные `Plans/BP-*` проверены и минимально выровнены только там, где это реально нужно.
- historical layer, release governance и process-docs не переписываются.
- `bp_lint.py` меняется только если audit доказывает изменение обязательного contract; иначе фиксируется `bp_lint contract unaffected`.
- `ChangeLog` и `QualityLog` фиксируют факты audit-pass.

## Фактический результат
- Обновлены `README.md`, `AGENTS.md` и `Tools/README.md`, чтобы root maps и tool map отражали discovery-layer, крупноэтапный `Roadmap` и текущий lint contract.
- В `Docs/Technical/Product_Bootstrap_Validation.md` выровнена фактическая формулировка о синхронизации bootstrap validation с минимальным product-layer canon.
- В `Roles/*` и `Skills/*` исправлены только реальные рассогласования: discovery добавлен в допустимые артефакты аналитиков, `Plans/PLAN-*.md` заменён на `Plans/BP-*.md`, а `Interview` и `Planning` привязаны к current-truth интервью и roadmap уровня крупных этапов.
- В `Plans/Archive/PLAN-000017-discovery-and-sync-contract.md` удалён дублирующийся артефакт `Logs/ADRlog.md`.
- `bp_lint.py` не менялся, потому что audit-pass не изменил обязательный contract путей, шаблонов или доменов.

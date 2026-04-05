# PLAN-000009 — Migrate terms layer

ID: PLAN-000009
Название: Перевести Docs/Terms на канонический filename contract и 6-значные TERM ID
Статус: Завершено
Связи: BACK-000023, BACK-000022, CHG-000018
Источник: Следующая фаза после фиксации repo-wide migration policy для serial-domain `Docs/Terms/`
Дата_создания: 2026-03-17
Дата_изменения: 2026-03-17
Основание: После фиксации policy и sync-прохода по схемам и шаблонам нужно привести `Docs/Terms/*` к каноническим filenames и 6-значным внутренним `TERM ID`, не затрагивая `Schemas/*`, `Templates/*`, `Profiles/*`, semver и historical logs.
Связанные_требования:
- TERM-000001
- TERM-000015
- TERM-000016
Связанные_backlog:
- BACK-000023
- BACK-000022
Связанные_ADR:
- ADR-000015

## Шаги
1. Привести term-card files к каноническому filename format.
   - DoD: все term-files используют `Docs/Terms/TERM-<NNNNNN>-<slug>.md`.
2. Привести внутренние `TERM ID` и прямые ссылки к 6-значному формату.
   - DoD: `TERM-000001`...`TERM-000016` согласованы внутри term-card files, `Base_Terms.md` и прямых ссылок по репозиторию.
3. Минимально синхронизировать `bp_normalize_terms.py`.
   - DoD: инструмент принимает новый filename pattern и корректно пересобирает `Base_Terms.md`.
4. Зафиксировать факт migration-pass в плановом и журнальном контурах.
   - DoD: `Plans/Backlog.md`, `Logs/ChangeLog.md` и `Logs/QualityLog.md` отражают только факты этого прохода.

## Риски
- частичное обновление term-ссылок оставит репозиторий в смешанном 4- и 6-значном состоянии;
- неверный filename pattern в `bp_normalize_terms.py` сломает пересборку `Base_Terms.md`;
- выход за scope затронет schema/template/profile и historical-log слои раньше их очереди.

## Артефакты
- `Docs/Terms/README.md`
- `Docs/Terms/Base_Terms.md`
- `Docs/Terms/Term_Change_Policy.md`
- `Docs/Terms/TERM-*.md`
- `Docs/Technical/Model.md`
- `Plans/BP-000003-fill-technical-and-rules.md`
- `Plans/BP-000004-fill-skills-and-tools.md`
- `Plans/Backlog.md`
- `Plans/BP-000009-migrate-terms-layer.md`
- `Logs/ADRlog.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `Tools/bp_normalize_terms.py`

## DoD
Term layer мигрирован к каноническим filenames и 6-значным `TERM ID`, `Base_Terms.md` и прямые ссылки синхронизированы, а `bp_normalize_terms.py` продолжает корректно пересобирать индекс без выхода за scope текущего прохода.

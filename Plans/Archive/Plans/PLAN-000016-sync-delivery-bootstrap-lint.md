# PLAN-000016 — Sync delivery bootstrap lint

ID: PLAN-000016
Название: Синхронизировать Delivery template, bootstrap и lint с каноном продуктового слоя
Статус: Завершено
Связи: BACK-000028, CHG-000028
Источник: Delivery/bootstrap/lint sync pass после нормализации продуктового слоя
Дата_создания: 2026-03-28
Дата_изменения: 2026-03-28
Основание: После приведения `Docs/Product/` к минимальному канону шаблон `Delivery` отсутствует, `bp_bootstrap.py` не материализует полный продуктовый набор, а `bp_lint.py` не валидирует новый contract. Нужен короткий синхронизирующий проход без выхода в большой рефакторинг.
Связанные_требования:
- отсутствуют
Связанные_backlog:
- BACK-000028
Связанные_ADR:
- отсутствуют

## Шаги
1. Зафиксировать управляемый контур прохода.
   - Описание: Добавить текущий backlog-item и отдельный plan-file для синхронизации `Delivery`, bootstrap и lint.
   - DoD: `Plans/Backlog.md` содержит `BACK-000028`, а `Plans/Archive/Plans/PLAN-000016-sync-delivery-bootstrap-lint.md` фиксирует scope и ограничения текущего прохода.
2. Добавить канонический шаблон `Delivery` и выровнять продуктовый документ.
   - Описание: Создать `Templates/Delivery.md`, обновить `Templates/README.md` и привести `Docs/Product/Delivery.md` к новому минимальному шаблону без технической реализации.
   - DoD: `Templates/Delivery.md` существует, `Templates/README.md` перечисляет три продуктовых шаблона, а `Docs/Product/Delivery.md` следует каноническим разделам.
3. Синхронизировать bootstrap-documentation и инструментальный контракт.
   - Описание: Обновить `Docs/Technical/Product_Bootstrap_Contract.md`, `Docs/Technical/Product_Bootstrap_Validation.md`, `Tools/bp_bootstrap.py` и `Tools/bp_lint.py` под единый минимальный продуктовый слой.
   - DoD: bootstrap создаёт `Docs/Product/README.md`, `Docs/Product/JTBD.md`, `Docs/Product/PRD.md`, `Docs/Product/Delivery.md`, а lint валидирует новый template и product bootstrap contract.
4. Проверить фактическую материализацию контракта и закрыть проход.
   - Описание: Выполнить bootstrap smoke-check во временном каталоге, прогнать lint по сгенерированному продукту и зафиксировать факты в журналах.
   - DoD: `python3 Tools/bp_lint.py --repo .` проходит, bootstrap smoke-check проходит, а `Backlog`, `Plan`, `ChangeLog` и `QualityLog` переведены в финальное состояние.

## Риски
- частичная синхронизация `Delivery` шаблона и bootstrap оставит расхождение между шаблонами, документацией и генерацией;
- обновление только `bp_bootstrap.py` без `bp_lint.py` оставит невалидируемый contract;
- лишний выход в `Rules/*`, `Standards/*`, `Schemas/*` или process-docs выведет проход за утверждённый scope.

## Артефакты
- `Plans/Backlog.md`
- `Plans/Archive/Plans/PLAN-000016-sync-delivery-bootstrap-lint.md`
- `Templates/Delivery.md`
- `Templates/README.md`
- `Docs/Product/Delivery.md`
- `Docs/Technical/Product_Bootstrap_Contract.md`
- `Docs/Technical/Product_Bootstrap_Validation.md`
- `Tools/bp_bootstrap.py`
- `Tools/bp_lint.py`
- `Tools/README.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `/tmp/bytepress-delivery-bJeblG`

## DoD
- `Templates/Delivery.md` существует и отражён в `Templates/README.md`.
- `Docs/Product/Delivery.md` приведён к каноническому шаблону.
- `Docs/Technical/Product_Bootstrap_Contract.md` и `Docs/Technical/Product_Bootstrap_Validation.md` синхронизированы с новым продуктовым слоем.
- `bp_bootstrap.py` и `bp_lint.py` синхронизированы с единым product-layer contract.
- scope ограничен `Templates/*`, `Docs/Product/Delivery.md`, `Docs/Technical/Product_Bootstrap_*`, `Tools/bp_bootstrap.py`, `Tools/bp_lint.py`, связанными README и журналами; `Rules/*`, `Standards/*`, `Schemas/*` и process-docs не меняются, кроме обязательной синхронизации прямых ссылок.

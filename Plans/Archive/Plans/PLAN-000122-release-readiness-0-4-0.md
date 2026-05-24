# PLAN-000122 — Финальная предрелизная консолидация BytePress 0.4.0

ID: PLAN-000122
Название: Финальная предрелизная консолидация BytePress 0.4.0
Статус: Завершено
Связи: ROAD-000050, BACK-000132, CHG-000134, QL-000129, RL-000010
Источник: Запрос владельца от 2026-05-24
Дата_создания: 2026-05-24
Дата_изменения: 2026-05-24
Основание: `ROAD-000050` является последним этапом горизонта `0.4.0`; перед внешним выпуском требуется финальная предрелизная консолидация без release PR в `main` и без tag.
Связанные_требования:
Связанные_backlog: BACK-000132
Связанные_ADR:

## Цель
- проверить готовность BytePress `0.4.0` к выпуску;
- закрыть накопленные предрелизные дефекты;
- не начинать сам release в `main`;
- не создавать tag;
- подготовить release-readiness результат.

## Артефакты
- `Plans/Roadmap.md`
- `Plans/Backlog.md`
- `Plans/Archive/Backlog/ROAD-000050.md`
- `Plans/Archive/Plans/PLAN-000122-release-readiness-0-4-0.md`
- `Logs/ChangeLog.md`
- `Logs/QualityLog.md`
- `Logs/ReleaseLog.md`
- `Tools/bp_bootstrap.py`

## Шаги
1. Синхронизировать рабочую ветку и открыть `ROAD-000050`.
   - Определение_готовности: проход выполняется не в `develop` и не в `main`, а `ROAD-000050` открыт как последний этап горизонта `0.4.0`.
2. Проверить плановый контур, журналы, карты, активные документы, шаблоны, схемы и инструменты.
   - Определение_готовности: реальные предрелизные дефекты исправлены, исторические факты не переписаны ради старой лексики.
3. Проверить release archive и generated product.
   - Определение_готовности: zip-пакеты проходят проверку, временный generated product не получает удалённые домены и использует `Tools/*` как служебный вход.
4. Закрыть плановый и журнальный контур готовности.
   - Определение_готовности: `BACK-000132`, `PLAN-000122` и `ROAD-000050` завершены; `CHG-000134`, `QL-000129` и readiness-запись `RL-000010` добавлены.
5. Подготовить PR в `develop`.
   - Определение_готовности: обязательные проверки пройдены, ветка отправлена, PR создан через `gh`; release PR в `main` и tag не созданы.

## Проверки
- `git diff --check`
- `python3 Tools/bp_lint.py --repo .`
- `python3 Tools/bp_check.py --repo .`
- `python3 Tools/bp_check.py --repo . --format json`
- `python3 -m py_compile Tools/bp_lint.py Tools/bp_check.py Tools/bp_check_contract.py`
- `python3 -m py_compile Tools/bp_bootstrap.py`
- `python3 -m zipfile -t Plans/Archive/Releases/0.1.0.zip`
- `python3 -m zipfile -t Plans/Archive/Releases/0.2.0.zip`
- `python3 -m zipfile -t Plans/Archive/Releases/0.3.0.zip`
- минимальная bootstrap-проверка временного продукта `/tmp/bytepress-plan-000122-product` с последующим удалением каталога.

## Результат
`BACK-000132`, `PLAN-000122` и `ROAD-000050` завершены. Готовность выпуска `0.4.0` зафиксирована в `RL-000010` как release-readiness, а не как факт внешнего выпуска. Исправлен generated wording в `Tools/bp_bootstrap.py`: стартовый план создаваемого продукта использует `Определение_готовности` вместо `DoD`. `ADR-000028` не создан, потому что новое архитектурное решение не принималось.

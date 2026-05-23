# PLAN-000082 — Product pipeline control and retired domain cleanup

ID: PLAN-000082
Название: Product pipeline control and retired domain cleanup
Статус: Завершено
Связи: ROAD-000029, BACK-000094, ADR-000023, CHG-000094, QL-000089
Источник: Запрос владельца от 2026-04-29
Дата_создания: 2026-04-29
Дата_изменения: 2026-04-29
Основание: Новый полевой тест `Minesweeper` показал, что product skeleton работает, но agent route всё ещё допускал догадки в интервью, самовольный выбор GUI-стека, слабый local Pipeline, PR-маршрут не через `gh`, один общий коммит и неполное удаление legacy domains.
Связанные_требования:
- AGENTS.md
- Pipeline/Workflows.md
- Rules/Dependency_Selection.md
- Rules/PR_Route_Uses_GH.md
- Rules/Semantic_Commits.md
Связанные_backlog:
- BACK-000094
Связанные_ADR:
- ADR-000023
Артефакты:
- AGENTS.md
- README.md
- Pipeline/*
- Rules/*
- Docs/Discovery/*
- Docs/Technical/*
- Tools/bp_bootstrap.py
- Tools/bp_lint.py
- Tools/bp_integration_smoke.py
- Plans/*
- Logs/*
Риски:
- Исторические записи всё ещё содержат ссылки на удалённые домены как факты прошлого.
- `scripts/*` в generated product skeleton оставлены как transition wrappers с явным сроком удаления, а не удалены сразу.
DoD:
- Generated product Pipeline описывает основной путь, workflows, gates, уровни проверок, журнальное закрытие и PR через `gh`.
- Generated `AGENTS.md` направляет в generated Pipeline и требует фазу, workflow и gate в первом ответе.
- Interview protocol запрещает подтверждать текущую истину догадками и отделяет гипотезы.
- Dependency rule запрещает самовольный выбор стека и фиксирует GUI-проверку отдельно.
- `bp_lint.py` больше не требует retired domains в `BytePress`.
- Проверки из запроса пройдены.

## Шаги
1. Открыть planning и ADR contour.
   - DoD: `ROAD/BACK/PLAN/ADR` согласованы.
2. Перенести процедуры и нормы.
   - DoD: смысл `Skills/*` живёт в `Pipeline/Workflows.md`, обязательные нормы `Standards/*` живут в `Rules/*`.
3. Удалить retired domains.
   - DoD: `Adapters/*`, `Memory/*`, `MCP/*`, `Runtime/*`, `Roles/*`, `Skills/*`, `Standards/*` отсутствуют в active layer.
4. Обновить tools и generated skeleton.
   - DoD: fresh/developed/negative checks проходят, generated product не получает retired domains.
5. Закрыть logs и проверки.
   - DoD: `ChangeLog`, `QualityLog`, planning archive и PR route согласованы.

## Результат
Широкий corrective pass завершил cleanup доменной модели и усилил product-start control без изменения `Minesweeper`.

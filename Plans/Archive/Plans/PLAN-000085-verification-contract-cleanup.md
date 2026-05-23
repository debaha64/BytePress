# PLAN-000085 — Verification contract reduction and language cleanup

ID: PLAN-000085
Название: Verification contract reduction and language cleanup
Статус: Завершено
Связи: ROAD-000032, BACK-000097, ADR-000025, CHG-000097, QL-000092
Источник: Запрос владельца от 2026-04-30
Дата_создания: 2026-04-30
Дата_изменения: 2026-04-30
Основание: После удаления преждевременных доменов проверочный контур сохраняет повторяющиеся technical documents и формулировки, которые нужно свести к одному владельцу без ослабления fresh/developed checks.
Связанные_требования:
- Docs/Technical/Verification.md
- бывшие Docs/Technical/Verification_Levels.md
- бывшие Docs/Technical/Verification_Evidence.md
- бывшие Docs/Technical/Validation.md
- бывшие Docs/Technical/Validation_Levels.md
- бывшие Docs/Technical/Validation_Evidence.md
- Pipeline/Workflows.md
- Tools/bp_lint.py
- Tools/bp_bootstrap.py
Связанные_backlog:
- BACK-000097
Связанные_ADR:
- ADR-000025
Артефакты:
- Docs/Technical/*
- Pipeline/Workflows.md
- Rules/README.md
- Tools/README.md
- Tools/bp_lint.py
- Tools/bp_bootstrap.py
- Plans/*
- Logs/*
Риски:
- Нельзя потерять уровни проверок, evidence contract и связь с `Pipeline/*`.
- Нельзя ослабить fresh/developed product checks.
- Исторические архивы и журналы не переписываются без необходимости.
DoD:
- Один technical document владеет проверочным договором.
- Дублирующие проверочные документы удалены или заменены только если нужен короткий указатель.
- Прямые ссылки синхронизированы.
- Tools и generated product wording не ссылаются на старые проверочные документы или удалённые домены.
- Обязательные проверки пройдены.

## Шаги
1. Ревизовать проверочные документы.
   - DoD: найдено фактическое дублирование и выбран владелец договора.
2. Сократить technical docs и прямые ссылки.
   - DoD: уровни проверок, evidence и связь с `Pipeline/*` сохранены.
3. Синхронизировать Pipeline, Rules и Tools.
   - DoD: active references и generated product wording соответствуют текущей модели.
4. Выполнить проверки и закрыть контур.
   - DoD: checks, logs, archive planning и PR route завершены.

## Результат
Проверочный договор сокращён до одного владельца `Docs/Technical/Verification.md`. Документы `Verification_Levels.md`, `Verification_Evidence.md`, `Validation.md`, `Validation_Levels.md` и `Validation_Evidence.md` удалены как дублирующие. `Docs/Technical/README.md`, `Pipeline/*`, `Rules/README.md`, `Tools/README.md`, `bp_lint.py` и `bp_bootstrap.py` синхронизированы. Fresh/developed product checks не ослаблены.

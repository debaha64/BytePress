# Запись изменений

Применение: [sops/record-change.md](../sops/record-change.md).

```text
RECORD_ID: CHANGE-000001
WPLAN_ID: <WPLAN-ID | none>
DATE: YYYY-MM-DD
SUMMARY: <краткий факт>
SOURCE_REF: <workspace-relative-path>#<anchor-or-lines>
```

- Факт/результат: {{summary}}
- Изменённые поверхности: {{paths}}
- Свидетельство: {{reference}}
- Непроверенные области: {{limits}}
- Следующий шаг: {{next}}

Источник и transport выбираются по [контракту свидетельств](../docs/technical/artifact-lifecycle.md#источники-свидетельств); placeholder заменяется существующим локальным источником факта.

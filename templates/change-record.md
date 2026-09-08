# Запись изменений

Применение: [sops/record-change.md](../sops/record-change.md).

```text
RECORD_ID: CHANGE-000001
WPLAN_ID: <WPLAN-ID | none>
DATE: YYYY-MM-DD
SUMMARY: <краткий факт>
SOURCE_REF: codexlog:.codex/<actual-log-file>#lines=<start>-<end>
```

- Факт/результат: {{summary}}
- Изменённые поверхности: {{paths}}
- Свидетельство: {{reference}}
- Непроверенные области: {{limits}}
- Следующий шаг: {{next}}

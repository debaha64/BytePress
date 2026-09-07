# Запись качества

Применение: [sops/record-quality.md](../sops/record-quality.md).

```text
RECORD_ID: QUALITY-000001
WPLAN_ID: <WPLAN-ID | none>
EVIDENCE_KIND: <canonical required evidence kind | not-applicable>
DATE: YYYY-MM-DD
SUMMARY: <краткий факт>
SOURCE_REF: codexlog:.codex/<actual-log-file>#lines=<start>-<end>
```

- Факт/результат: {{summary}}
- Изменённые поверхности: {{paths}}
- Свидетельство: {{reference}}
- Непроверенные области: {{limits}}
- Следующий шаг: {{next}}

- Класс изменения и прослеживаемость: {{S0/S1/S2; REQ/INV/SCN}}
- Verification: {{result/reference}}
- Validation: {{status/reference}}
- Product Acceptance: {{status/reference}}
- Release Authorization: {{status/reference}}
- GUI, если применим: {{визуальный результат либо ready-for-owner-check}}

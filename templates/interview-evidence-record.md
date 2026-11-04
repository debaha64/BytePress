# Свидетельство интервью

Применение: [sops/interview.md](../sops/interview.md).

```text
RECORD_TYPE: interview_evidence
RECORD_ID: IE-000001
WPLAN_ID: <WPLAN-ID>
SESSION_ID: SESSION-000001
LAYERS_COMPLETE: <только подтверждённые сохранённым ответом слои>
LAYERS_DEFERRED: none
STATUS: complete
SOURCE_KIND: owner_response
SOURCE_REF: <workspace-relative-path>#<anchor-or-lines>
```

## Поля перехода, если применимы

```text
EVIDENCE_CLASS: transition
PRODUCT_INPUT_REF: <workspace-relative-path>#<anchor-or-lines>
ROUTE_CHOICE_REF: <workspace-relative-path>#<anchor-or-lines>
```

Источник и способ ссылки выбираются по [контракту свидетельств](../docs/technical/artifact-lifecycle.md#источники-свидетельств); заполнитель заменяется существующим локальным источником факта.

Не копируйте все слои автоматически. SOURCE_REF указывает фактический ответ и подтверждает только его содержание; полный диалог обычному Workspace не требуется. Точная skill-квалификация использует отдельное испытательное свидетельство по SOP interview.

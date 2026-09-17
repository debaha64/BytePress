# Свидетельство интервью

Применение: [sops/interview.md](../sops/interview.md).

```text
RECORD_TYPE: interview_evidence
RECORD_ID: IE-000001
WPLAN_ID: <WPLAN-ID>
SESSION_ID: SESSION-000001
LAYERS_COMPLETE: product-frame,user-scenario,data-storage,technical-frame,verification-dod,next-transition
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

Источник и transport выбираются по [контракту свидетельств](../docs/technical/artifact-lifecycle.md#источники-свидетельств); placeholder заменяется существующим локальным источником факта.

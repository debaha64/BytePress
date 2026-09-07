# Записи решений OD-* и PA-*

Применение: [sops/record-decision.md](../sops/record-decision.md).

```text
RECORD_TYPE: owner_decision
RECORD_ID: OD-000001
WPLAN_ID: <WPLAN-ID>
SESSION_ID: SESSION-000001
DECISION_KIND: implementation | decommissioning_authorization | retirement_authorization | sot_transition | local_git_route
DECISION_VALUE: approved
EVIDENCE_REF: IE-000001
SOT_FROM: none
SOT_TO: none
ROUTE_REF: none | <WBACK-ID>
ALLOWED_ACTIONS: <exact allowed actions>
PREVIOUS_STATUS: none
STATUS: active
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>
```

```text
RECORD_TYPE: product_acceptance
RECORD_ID: PA-000001
WPLAN_ID: <WPLAN-ID>
DECISION_VALUE: accepted | rejected
SOURCE_KIND: owner_response
SOURCE_REF: codexlog:.codex/<actual-raw-file>.raw.log#lines=<start>-<end>
```

`PA-*` и Release Authorization имеют отдельные контракты; `decommissioning_authorization` и `retirement_authorization` — виды OD-*.

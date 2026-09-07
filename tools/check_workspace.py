#!/usr/bin/env python3
"""Generic read-only checker for one Project Workspace."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse


DISPOSABLE_DIR_NAMES = ("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache")
DISPOSABLE_SUFFIXES = (".pyc", ".pyo", ".tmp", ".temp", ".orig")
SERVICE_NAMES = (".agents", ".codex", ".git")
CORE_DIRECTORIES = (
    "docs", "logs", "research", "roles", "skills", "sops", "templates", "tests", "tools",
    "plans", "plans/active", "plans/completed",
)
CORE_FILES = (
    "AGENTS.md", "SYSTEM.md", "plans/roadmap.md", "plans/backlog.md",
    "research/00-index.md", "tools/project_profile.py",
)
SOT_FIELD = re.compile(r"^\s*SOT_MODE\s*[:=]\s*`?([^`\s]+)`?\s*\.?\s*$")
REPOSITORY_FIELD = re.compile(r"^\s*SOT_GITHUB_REPOSITORY\s*:\s*`?([^`\s]+)`?\s*$")
TRANSITION_FIELDS = (
    "SDLC_TRANSITION", "TRANSITION_STATE", "FROM_PHASE", "FROM_ROLE",
    "PHASE_COMPLETION", "EVIDENCE_KIND", "EVIDENCE_REFS", "TRANSITION_CHECKPOINT", "HANDOFF_REF",
    "TO_PHASE", "TO_ROLE", "FROM_ROLE_AUTHORITY", "TO_ROLE_AUTHORITY",
    "AUTHORITY_REF", "OWNER_GATE", "OWNER_GATE_STATUS", "OWNER_GATE_REF",
    "VERIFICATION_STATUS", "VERIFICATION_REF", "VALIDATION_STATUS", "VALIDATION_REF",
    "PRODUCT_ACCEPTANCE_STATUS", "PRODUCT_ACCEPTANCE_REF",
    "RELEASE_AUTHORIZATION_STATUS", "RELEASE_AUTHORIZATION_REF",
)
BASELINE_HEADER = "manifest\t1\tcomplete\t."


class UsageError(RuntimeError):
    pass


class ContractError(RuntimeError):
    pass


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def _raw_sorted(values):
    return sorted(values, key=lambda value: str(value).encode("utf-8"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _regular(path: Path, kind: str, label: str):
    try:
        info = path.lstat()
    except OSError as error:
        raise ContractError(f"{label} отсутствует или недоступен") from error
    expected = stat.S_ISDIR(info.st_mode) if kind == "d" else stat.S_ISREG(info.st_mode)
    if stat.S_ISLNK(info.st_mode) or not expected:
        raise ContractError(f"{label} имеет недопустимый тип")


def _workspace_root(value) -> Path:
    path = Path(value)
    _regular(path, "d", "Workspace root")
    return path.resolve(strict=True)


def _load_profile_module(workspace: Path):
    checker = workspace / "tools/check_workspace.py"
    if Path(__file__).is_symlink() or Path(__file__).resolve() != checker.resolve(strict=True):
        raise UsageError("checker origin должен быть exact Workspace tools/check_workspace.py")
    parser_path = workspace / "tools/project_profile.py"
    _regular(parser_path, "f", "co-located project_profile.py")
    try:
        parser_path.resolve(strict=True).relative_to(workspace)
    except (OSError, ValueError) as error:
        raise UsageError("project_profile.py выходит за Workspace") from error
    name = "_deployed_workspace_profile"
    spec = importlib.util.spec_from_file_location(name, parser_path)
    if spec is None or spec.loader is None:
        raise UsageError("project_profile.py нельзя загрузить")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    if Path(module.__file__).resolve() != parser_path.resolve(strict=True):
        raise UsageError("project_profile module origin mismatch")
    return module


def _discover_profile(workspace: Path, module):
    profiles = []
    folded = {}
    for path in workspace.iterdir():
        key = path.name.casefold()
        if key in folded and folded[key] != path.name:
            raise ContractError(f"Workspace root case collision: {folded[key]}, {path.name}")
        folded[key] = path.name
        if path.name.endswith(".profile"):
            profiles.append(path)
    if len(profiles) != 1:
        raise ContractError("Workspace root должен содержать ровно один *.profile")
    profile_path = profiles[0]
    _regular(profile_path, "f", "Project Profile")
    try:
        profile = module.parse_project_profile(profile_path.read_bytes(), profile_path.name)
    except module.ProjectProfileError as error:
        raise ContractError(str(error)) from error
    if workspace.name != f"WS_{profile.slug}":
        raise ContractError("Workspace basename не соответствует Profile Slug")
    product = workspace / profile.slug
    _regular(product, "d", "Product root/delivery boundary")
    if product.resolve(strict=True).parent != workspace:
        raise ContractError("Product root выходит за Workspace")
    return profile, profile_path, product


def _check_core(workspace: Path):
    for relative in CORE_DIRECTORIES:
        _regular(workspace / relative, "d", relative)
    for relative in CORE_FILES:
        _regular(workspace / relative, "f", relative)


def _active_ids(text: str, prefix: str):
    pattern = re.compile(rf"(?m)^.*\b({prefix}-\d{{6}})\b.*\bactive\b.*$")
    return set(pattern.findall(text))


def _field(text: str, label: str):
    match = re.search(rf"(?m)^{re.escape(label)}\s*:\s*`?([^`\s]+)`?\s*\.?\s*$", text)
    return match.group(1) if match else None


def _checkpoint_values(text: str, label: str):
    return re.findall(rf"(?m)^{re.escape(label)}\s*:\s*`?([^`\s]+)`?\s*\.?\s*$", text)


def _single_field(text: str, label: str) -> str:
    values = _checkpoint_values(text, label)
    if len(values) != 1:
        raise ContractError(f"transition field {label} должен встречаться ровно один раз")
    return values[0]


def _phase_role_projection(workspace: Path):
    text = (workspace / "docs/technical/sdlc.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5 or not re.fullmatch(r"`?\d{2}`?", cells[0]):
            continue
        phase = cells[2].strip("`")
        role = re.fullmatch(r"\[[^]]+\]\(\.\./\.\./(roles/[^)]+)\)", cells[4])
        if not re.fullmatch(r"[a-z][a-z-]*", phase) or not role:
            raise ContractError("invalid phase/role projection in docs/technical/sdlc.md")
        rows.append((phase, role.group(1)))
    if len(rows) != 21 or len({phase for phase, _role in rows}) != 21:
        raise ContractError("phase/role projection must contain exact 21 unique phases")
    for _phase, relative in rows:
        _regular(workspace / relative, "f", relative)
    return rows


def _phase_gate_projection(workspace: Path, phases):
    text = (workspace / "docs/technical/phase-gates.md").read_text(encoding="utf-8")
    rows = []
    pattern = re.compile(
        r"^\| `([a-z][a-z-]*)` \| `([a-z][a-z-]*)` \| `([a-z][a-z0-9-]*)` \| "
        r"`(none|owner-open|owner-decision)` \| "
        r"`(none|implementation|product_acceptance|release_authorization|decommissioning_authorization|retirement_authorization)` \|$"
    )
    for line in text.splitlines():
        match = pattern.fullmatch(line)
        if match:
            rows.append(match.groups())
    expected_pairs = list(zip(phases, [*phases[1:], "retired"]))
    if [(source, target) for source, target, _evidence, _gate, _decision in rows] != expected_pairs:
        raise ContractError("phase gate projection must cover exact canonical transitions")
    if any(not evidence for _source, _target, evidence, _gate, _decision in rows):
        raise ContractError("phase gate evidence kind missing")
    if any(
        (gate == "owner-decision") != (decision != "none")
        for _source, _target, _evidence, gate, decision in rows
    ):
        raise ContractError("phase gate policy and required owner decision kind mismatch")
    return {
        (source, target): {
            "evidence_kind": evidence,
            "gate_policy": gate,
            "decision_kind": decision,
        }
        for source, target, evidence, gate, decision in rows
    }


def _checked_reference(
    workspace: Path, value: str, label: str, *, decision=False, marker=None,
    decision_value=None, decision_values=None,
):
    relative, separator, token = value.partition("#")
    if not separator or not token:
        raise ContractError(f"{label} должен быть exact path#token reference")
    pure = _declared_path(relative)
    candidate = workspace.joinpath(*pure.parts)
    _regular(candidate, "f", label)
    try:
        candidate.resolve(strict=True).relative_to(workspace)
    except (OSError, ValueError) as error:
        raise ContractError(f"{label} выходит за Workspace") from error
    if decision and pure != PurePosixPath("logs/decisions.md"):
        raise ContractError(f"{label} должен ссылаться на logs/decisions.md")
    if marker is not None and marker not in token:
        raise ContractError(f"{label} использует неверный decision kind")
    reference_text = candidate.read_text(encoding="utf-8")
    if token not in reference_text:
        raise ContractError(f"{label} token отсутствует: {value}")
    if decision_value is not None and not re.search(
        rf"(?m)^{re.escape(token)}:\s*{re.escape(decision_value)}\s*$", reference_text
    ):
        raise ContractError(f"{label} decision value mismatch")
    if decision_values is not None and not any(
        re.search(rf"(?m)^{re.escape(token)}:\s*{re.escape(item)}\s*$", reference_text)
        for item in decision_values
    ):
        raise ContractError(f"{label} decision value mismatch")
    return value


def _line_value(text: str, label: str) -> str:
    values = re.findall(rf"(?m)^{re.escape(label)}\s*:\s*(.+?)\s*$", text)
    if len(values) != 1:
        raise ContractError(f"WPLAN field {label} должен встречаться ровно один раз")
    return values[0].strip().strip("`")


def _machine_fields(text: str) -> dict[str, str]:
    fields = {}
    for key, value in re.findall(r"(?m)^([A-Z][A-Z0-9_]*)\s*:\s*(.+?)\s*$", text):
        if key in fields:
            raise ContractError(f"duplicate machine field in record: {key}")
        fields[key] = value.strip().strip("`")
    return fields


def _record_by_id(workspace: Path, record_id: str) -> dict[str, str]:
    if not re.fullmatch(r"(?:OD|PA)-\d{6}", record_id):
        raise ContractError(f"invalid decision record reference: {record_id}")
    text = (workspace / "logs/decisions.md").read_text(encoding="utf-8")
    matches = []
    for block in re.split(r"(?m)(?=^RECORD_TYPE:\s*)", text):
        if not block.startswith("RECORD_TYPE:"):
            continue
        if record_id not in re.findall(r"(?m)^RECORD_ID:\s*(\S+)\s*$", block):
            continue
        fields = _machine_fields(block)
        if fields.get("RECORD_ID") == record_id:
            matches.append(fields)
    if len(matches) != 1:
        raise ContractError(f"decision record must resolve exactly once: {record_id}")
    return matches[0]


def _owner_decision_refs(text: str) -> tuple[str, ...]:
    raw = _line_value(text, "OWNER_DECISION_REFS")
    if raw == "none":
        return ()
    values = tuple(raw.split(","))
    if not values or len(values) != len(set(values)) or any(not re.fullmatch(r"OD-\d{6}", value) for value in values):
        raise ContractError("OWNER_DECISION_REFS must contain unique OD identifiers")
    return values


def _owner_decision_record(
    workspace: Path, text: str, reference: str, decision_kind: str
) -> dict[str, str]:
    plan_id = _single_field(text, "WPLAN ID")
    plan_back = _single_field(text, "WBACK")
    if reference not in _owner_decision_refs(text):
        raise ContractError("owner decision must be projected by OWNER_DECISION_REFS")
    record = _record_by_id(workspace, reference)
    expected = {
        "RECORD_TYPE": "owner_decision",
        "RECORD_ID": reference,
        "WPLAN_ID": plan_id,
        "DECISION_KIND": decision_kind,
        "DECISION_VALUE": "approved",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ContractError(f"required decision kind = {decision_kind}: {key} mismatch")
    if record.get("STATUS") not in {"active", "applied"}:
        raise ContractError(f"required decision kind = {decision_kind}: status is not active/applied")
    if record.get("ROUTE_REF") not in {"none", plan_back}:
        raise ContractError(f"required decision kind = {decision_kind}: route scope mismatch")
    return record


def _implementation_authority(workspace: Path, text: str, authority_ref: str) -> dict[str, str]:
    if _line_value(text, "ALLOWED_SURFACES") == "none":
        raise ContractError("implementation authority requires non-empty ALLOWED_SURFACES")
    record = _owner_decision_record(workspace, text, authority_ref, "implementation")
    if record.get("EVIDENCE_REF") != _line_value(text, "INTERVIEW_EVIDENCE_REF"):
        raise ContractError("AUTHORITY_REF EVIDENCE_REF mismatch")
    return record


def _reference_evidence_fields(workspace: Path, reference: str) -> dict[str, str]:
    relative, separator, token = reference.partition("#")
    _checked_reference(workspace, reference, "EVIDENCE_REFS")
    if not separator:
        raise ContractError("EVIDENCE_REFS must be exact path#token references")
    text = workspace.joinpath(*_declared_path(relative).parts).read_text(encoding="utf-8")
    matches = []
    token_pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(token)}(?![A-Za-z0-9_-])")
    for block in re.split(r"\n\s*\n", text):
        if token_pattern.search(block):
            matches.append(_machine_fields(block))
    if len(matches) != 1:
        raise ContractError(f"EVIDENCE_REFS token must resolve to one structured evidence block: {reference}")
    return matches[0]


def _product_acceptance_record(
    workspace: Path, reference: str, value: str, *, gate_plan_id: str | None = None
) -> dict[str, str]:
    if not re.fullmatch(r"PA-\d{6}", reference):
        raise ContractError(f"invalid product acceptance reference: {reference}")
    record = _record_by_id(workspace, reference)
    expected = {
        "RECORD_TYPE": "product_acceptance", "RECORD_ID": reference,
        "DECISION_VALUE": value,
    }
    for key, expected_value in expected.items():
        if record.get(key) != expected_value:
            raise ContractError(f"product acceptance {key} mismatch")
    if not re.fullmatch(r"WPLAN-\d{6}", record.get("WPLAN_ID", "")):
        raise ContractError("product acceptance WPLAN_ID invalid")
    # Provenance remains durable; only the owner gate requires its own WPLAN.
    if gate_plan_id is not None and record["WPLAN_ID"] != gate_plan_id:
        raise ContractError("product acceptance WPLAN_ID mismatch")
    return record


def _scoped_marker_reference(workspace: Path, reference: str, plan_id: str, marker: str, value: str):
    relative, separator, token = reference.partition("#")
    if relative != "logs/decisions.md" or not separator or marker not in token:
        raise ContractError(f"reference must use {marker} decision kind")
    text = (workspace / relative).read_text(encoding="utf-8")
    matches = []
    for block in re.split(r"\n\s*\n", text):
        fields = _machine_fields(block)
        if re.search(rf"(?m)^{re.escape(token)}:\s*{re.escape(value)}\s*$", block):
            matches.append(fields)
    if len(matches) != 1 or matches[0].get("WPLAN_ID") != plan_id:
        raise ContractError(f"{marker} decision scope/value mismatch")


_DECISION_GATE_MARKERS = {
    "implementation": "IMPLEMENTATION-AUTHORIZATION",
    "product_acceptance": "PRODUCT-ACCEPTANCE",
    "release_authorization": "RELEASE-AUTHORIZATION",
    "decommissioning_authorization": "DECOMMISSIONING-AUTHORIZATION",
    "retirement_authorization": "RETIREMENT-AUTHORIZATION",
}


def _required_owner_decision(
    workspace: Path, text: str, values: dict[str, str], required_kind: str,
    plan_id: str,
):
    gate = values["OWNER_GATE"]
    marker = _DECISION_GATE_MARKERS[required_kind]
    if not gate.startswith("GATE-OWNER-") or marker not in gate:
        raise ContractError(f"OWNER_GATE does not match required decision kind = {required_kind}")
    reference = values["OWNER_GATE_REF"]
    if required_kind in {
        "implementation", "decommissioning_authorization", "retirement_authorization",
    }:
        _owner_decision_record(workspace, text, reference, required_kind)
        if required_kind == "implementation" and reference != values["AUTHORITY_REF"]:
            raise ContractError("implementation decision gate requires current AUTHORITY_REF")
    elif required_kind == "product_acceptance":
        _product_acceptance_record(workspace, reference, "accepted", gate_plan_id=plan_id)
        if (
            values["PRODUCT_ACCEPTANCE_STATUS"] != "accepted"
            or values["PRODUCT_ACCEPTANCE_REF"] != reference
        ):
            raise ContractError("Product Acceptance gate/status projection mismatch")
    elif required_kind == "release_authorization":
        _scoped_marker_reference(workspace, reference, plan_id, "RELEASE_AUTHORIZATION", "authorized")
        if (
            values["RELEASE_AUTHORIZATION_STATUS"] != "authorized"
            or values["RELEASE_AUTHORIZATION_REF"] != reference
        ):
            raise ContractError("Release Authorization gate/status projection mismatch")
    else:
        raise ContractError(f"unsupported required decision kind: {required_kind}")


def _status_reference(workspace: Path, values: dict[str, str], prefix: str, inactive, active, plan_id: str):
    status = values[f"{prefix}_STATUS"]
    reference = values[f"{prefix}_REF"]
    if status in inactive:
        if reference != "none":
            raise ContractError(f"{prefix} {status} требует {prefix}_REF: none")
        return
    if status not in active or reference == "none":
        raise ContractError(f"invalid {prefix} status/reference")
    if prefix in {"VERIFICATION", "VALIDATION"}:
        _checked_reference(workspace, reference, f"{prefix}_REF")
    elif prefix == "PRODUCT_ACCEPTANCE":
        _product_acceptance_record(workspace, reference, status)
    elif prefix == "RELEASE_AUTHORIZATION":
        _scoped_marker_reference(workspace, reference, plan_id, "RELEASE_AUTHORIZATION", status)


def _check_sdlc_transition(workspace: Path):
    plans = _raw_sorted((workspace / "plans/active").glob("WPLAN-*.md"))
    if not plans:
        return "NOT_APPLICABLE"
    text = plans[0].read_text(encoding="utf-8")
    values = {field: _single_field(text, field) for field in TRANSITION_FIELDS}
    if values["SDLC_TRANSITION"] != "v1":
        raise ContractError("unsupported SDLC_TRANSITION")

    projection = _phase_role_projection(workspace)
    phases = [phase for phase, _role in projection]
    roles = dict(projection)
    source = values["FROM_PHASE"]
    target = values["TO_PHASE"]
    if source not in roles:
        raise ContractError("FROM_PHASE отсутствует в canonical SDLC")
    expected_target = phases[phases.index(source) + 1] if source != phases[-1] else "retired"
    if target != expected_target:
        raise ContractError("phase transition skips canonical next phase")
    gate_contract = _phase_gate_projection(workspace, phases)[(source, target)]
    gate_policy = gate_contract["gate_policy"]
    required_evidence_kind = gate_contract["evidence_kind"]
    required_decision_kind = gate_contract["decision_kind"]
    if values["FROM_ROLE"] != roles[source]:
        raise ContractError("FROM_ROLE не соответствует phase owner")
    expected_role = roles[target] if target in roles else "none"
    if values["TO_ROLE"] != expected_role:
        raise ContractError("TO_ROLE не соответствует next phase owner")

    plan_phase = _single_field(text, "Фаза SDLC")
    plan_id = _single_field(text, "WPLAN ID")
    plan_checkpoint = _single_field(text, "Текущая контрольная отметка")
    if values["TRANSITION_CHECKPOINT"] != plan_checkpoint:
        raise ContractError("transition checkpoint mismatch")
    _implementation_authority(workspace, text, values["AUTHORITY_REF"])
    if values["EVIDENCE_KIND"] != required_evidence_kind:
        raise ContractError("EVIDENCE_KIND does not match phase-gate required evidence kind")

    state = values["TRANSITION_STATE"]
    if state == "in-progress":
        expected = {
            "PHASE_COMPLETION": "pending", "EVIDENCE_REFS": "none", "HANDOFF_REF": "none",
            "FROM_ROLE_AUTHORITY": "active", "TO_ROLE_AUTHORITY": "withheld",
        }
        if plan_phase != source or any(values[key] != value for key, value in expected.items()):
            raise ContractError("in-progress transition grants premature completion/handoff/authority")
    elif state == "complete":
        if plan_phase != target or values["PHASE_COMPLETION"] != "complete":
            raise ContractError("completed transition phase mismatch")
        if values["EVIDENCE_REFS"] == "none":
            raise ContractError("completed phase requires evidence")
        references = values["EVIDENCE_REFS"].split(",")
        if not references or any(not value for value in references):
            raise ContractError("invalid EVIDENCE_REFS")
        for reference in references:
            fields = _reference_evidence_fields(workspace, reference)
            if fields.get("EVIDENCE_KIND") != required_evidence_kind:
                raise ContractError("EVIDENCE_REFS evidence kind mismatch")
            if fields.get("WPLAN_ID") != plan_id:
                raise ContractError("EVIDENCE_REFS WPLAN scope mismatch")
        if values["HANDOFF_REF"] == "none":
            raise ContractError("completed transition requires handoff")
        _checked_reference(workspace, values["HANDOFF_REF"], "HANDOFF_REF")
        if values["FROM_ROLE_AUTHORITY"] != "relinquished":
            raise ContractError("previous role retains write-authority after handoff")
        expected_authority = "granted" if target != "retired" else "not-applicable"
        if values["TO_ROLE_AUTHORITY"] != expected_authority:
            raise ContractError("next-role authority missing or premature")
    else:
        raise ContractError("TRANSITION_STATE must be in-progress or complete")

    gate_status = values["OWNER_GATE_STATUS"]
    if gate_policy == "owner-decision":
        marker = _DECISION_GATE_MARKERS[required_decision_kind]
        if not values["OWNER_GATE"].startswith("GATE-OWNER-") or marker not in values["OWNER_GATE"]:
            raise ContractError(
                f"OWNER_GATE does not match required decision kind = {required_decision_kind}"
            )
    if gate_status == "not-applicable":
        if values["OWNER_GATE"] != "none" or values["OWNER_GATE_REF"] != "none":
            raise ContractError("not-applicable owner gate must be empty")
    elif gate_status == "pending":
        if values["OWNER_GATE"] == "none" or values["OWNER_GATE_REF"] != "none":
            raise ContractError("pending owner gate cannot be auto-satisfied")
    elif gate_status == "satisfied":
        if values["OWNER_GATE"] == "none" or values["OWNER_GATE_REF"] == "none":
            raise ContractError("satisfied owner gate requires owner decision")
        if required_decision_kind == "none":
            raise ContractError("phase transition does not define a required owner decision kind")
        _required_owner_decision(
            workspace, text, values, required_decision_kind, plan_id
        )
        if values["OWNER_GATE_REF"] == values["VERIFICATION_REF"]:
            raise ContractError("Verification cannot satisfy owner gate")
    else:
        raise ContractError("invalid OWNER_GATE_STATUS")
    if gate_policy == "none" and gate_status != "not-applicable":
        raise ContractError("phase transition has unexpected owner gate")
    if gate_policy == "owner-open" and gate_status != "pending":
        raise ContractError("phase transition requires open owner gate")
    if gate_policy == "owner-decision":
        required = {"pending", "satisfied"} if state == "in-progress" else {"satisfied"}
        if gate_status not in required:
            raise ContractError("phase transition requires owner decision")

    _status_reference(workspace, values, "VERIFICATION", {"pending", "unverified"}, {"pass", "fail"}, plan_id)
    _status_reference(workspace, values, "VALIDATION", {"not-performed"}, {"pass", "fail"}, plan_id)
    _status_reference(workspace, values, "PRODUCT_ACCEPTANCE", {"not-performed"}, {"accepted", "rejected"}, plan_id)
    _status_reference(workspace, values, "RELEASE_AUTHORIZATION", {"not-performed"}, {"authorized", "denied"}, plan_id)
    active_refs = [
        values[name] for name in (
            "VERIFICATION_REF", "VALIDATION_REF", "PRODUCT_ACCEPTANCE_REF", "RELEASE_AUTHORIZATION_REF"
        ) if values[name] != "none"
    ]
    if len(active_refs) != len(set(active_refs)):
        raise ContractError("Verification/Validation/Product Acceptance/Release Authorization refs must be distinct")
    return {
        "state": state, "from": source, "to": target,
        "owner_gate": gate_status, "next_role_authority": values["TO_ROLE_AUTHORITY"],
    }


def _check_documentation_impact(workspace: Path):
    plans = _raw_sorted((workspace / "plans/active").glob("WPLAN-*.md"))
    if not plans:
        return "NOT_APPLICABLE"
    text = plans[0].read_text(encoding="utf-8")
    kind = _field(text, "Класс изменения")
    if kind not in {"S1", "S2"}:
        return "NOT_APPLICABLE"
    sections = re.findall(r"(?ms)^## Documentation Impact\s*\n(.*?)(?=^## |\Z)", text)
    if len(sections) != 1:
        raise ContractError("S1/S2 requires one Documentation Impact section")
    fields = {key: _line_value(sections[0], key) for key in ("Disposition", "Owners", "Reason")}
    if fields["Disposition"] not in {"affected", "not affected"}:
        raise ContractError("Documentation Impact disposition must be affected or not affected")
    for key, value in fields.items():
        if not value.strip() or value in {"none", "pending", "<reason>", "<owners>"}:
            raise ContractError(f"Documentation Impact {key} is empty or unresolved")
    owners = fields["Owners"].split(",")
    if len(set(owners)) != len(owners):
        raise ContractError("Documentation Impact owners must be unique")
    for raw in owners:
        path = _declared_path(raw.strip())
        if raw.strip().endswith("/**") or "<" in raw or ">" in raw:
            raise ContractError("Documentation Impact requires exact owner paths")
        # Paths can name an owner created/removed by this active migration;
        # the plan manifest and links checks own existence/actual delta.
    return fields


def _check_route(workspace: Path):
    roadmap = (workspace / "plans/roadmap.md").read_text(encoding="utf-8")
    backlog = (workspace / "plans/backlog.md").read_text(encoding="utf-8")
    road_ids = _active_ids(roadmap, "WROAD")
    if len(road_ids) != 1:
        raise ContractError(f"требуется один active WROAD, получено {len(road_ids)}")
    plans = _raw_sorted((workspace / "plans/active").glob("WPLAN-*.md"))
    if len(plans) > 1:
        raise ContractError(f"active WPLAN count > 1: {len(plans)}")
    declared_counts = re.findall(r"(?m)^active WPLAN count\s+(\d+)\s*$", backlog)
    if declared_counts != [str(len(plans))]:
        raise ContractError("active WPLAN count projection mismatch")
    nonexecuting = _checkpoint_values(backlog, "NON_EXECUTING_CHECKPOINT")
    current = _checkpoint_values(backlog, "CHECKPOINT")
    if not plans:
        if len(nonexecuting) != 1 or current:
            raise ContractError("нулевой active WPLAN требует одну non-executing checkpoint")
        return {"active_wplan_count": 0, "checkpoint": nonexecuting[0]}
    if nonexecuting or len(current) != 1:
        raise ContractError("active WPLAN требует одну executing checkpoint")
    path = plans[0]
    text = path.read_text(encoding="utf-8")
    plan_id = _field(text, "WPLAN ID")
    road_id = _field(text, "WROAD")
    back_id = _field(text, "WBACK")
    plan_checkpoint = _field(text, "Текущая контрольная отметка")
    if not plan_id or not path.name.startswith(plan_id + "-"):
        raise ContractError("active WPLAN filename/ID mismatch")
    if road_id not in road_ids:
        raise ContractError("active WPLAN WROAD mismatch")
    if back_id not in _active_ids(backlog, "WBACK"):
        raise ContractError("active WPLAN WBACK mismatch")
    if plan_checkpoint != current[0]:
        raise ContractError("active WPLAN checkpoint mismatch")
    return {"active_wplan_count": 1, "checkpoint": current[0], "wplan": plan_id}


def _declared_path(value: str) -> PurePosixPath:
    normalized = value[:-3] if value.endswith("/**") else value
    path = PurePosixPath(normalized)
    if (
        not normalized
        or path.is_absolute()
        or path == PurePosixPath(".")
        or ".." in path.parts
        or "\\" in normalized
        or any(character in normalized for character in "*?[]{}")
    ):
        raise ContractError(f"plan surface не является bounded Workspace path: {value}")
    return path


def _plan_surface_declarations(workspace: Path):
    plans = _raw_sorted((workspace / "plans/active").glob("WPLAN-*.md"))
    if not plans:
        return None
    text = plans[0].read_text(encoding="utf-8")
    declarations = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        heading = re.fullmatch(
            r"###\s+(?:Grouped\s+)?(CREATE|UPDATE|PRESERVE|REMOVE)(?:\s+[—-]\s+(\d+))?\s*",
            lines[index],
        )
        if not heading:
            index += 1
            continue
        action, declared_count = heading.groups()
        if action in declarations:
            raise ContractError(f"duplicate plan surface section: {action}")
        rows = []
        index += 1
        while index < len(lines) and not re.match(r"^#{1,3}\s+", lines[index]):
            row = re.match(r"^\d+\.\s+`([^`]+)`(?:\s+[—-]\s+`([^`]+)`)?", lines[index])
            if row:
                raw, contract = row.groups()
                rows.append({
                    "path": _declared_path(raw),
                    "tree": raw.endswith("/**"),
                    "contract": contract,
                    "raw": raw,
                })
            index += 1
        if declared_count is not None and len(rows) != int(declared_count):
            raise ContractError(f"{action} declared count mismatch")
        if len({(row["path"], row["tree"]) for row in rows}) != len(rows):
            raise ContractError(f"duplicate path in {action}")
        declarations[action] = rows
    flattened = [
        (action, row["path"])
        for action, rows in declarations.items()
        for row in rows
    ]
    for position, (left_action, left) in enumerate(flattened):
        for right_action, right in flattened[position + 1:]:
            if left_action == right_action:
                continue
            if left == right or left in right.parents or right in left.parents:
                raise ContractError(
                    f"plan surfaces overlap: {left_action} {left}; {right_action} {right}"
                )
    return declarations


def _check_plan_surfaces(workspace: Path):
    declarations = _plan_surface_declarations(workspace)
    if declarations is None:
        return "NOT_APPLICABLE"
    if not declarations:
        return "UNDECLARED"
    return {action: len(rows) for action, rows in declarations.items()}


def _delta_excluded(relative: PurePosixPath) -> bool:
    if relative.parts and relative.parts[0] in {*SERVICE_NAMES, "temp"}:
        return True
    if any(part in DISPOSABLE_DIR_NAMES for part in relative.parts):
        return True
    name = relative.parts[-1] if relative.parts else ""
    return name.endswith(DISPOSABLE_SUFFIXES) or name.endswith(":Zone.Identifier")


def _filesystem_manifest(workspace: Path):
    result = {}
    for current, directories, files in os.walk(workspace, topdown=True, followlinks=False):
        base = Path(current)
        relative_base = base.relative_to(workspace)
        kept = []
        for name in directories:
            path = base / name
            relative = PurePosixPath((relative_base / name).as_posix())
            if _delta_excluded(relative):
                continue
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise ContractError(f"baseline surface contains invalid directory type: {relative}")
            result[str(relative)] = ("d", stat.S_IMODE(info.st_mode), "-")
            kept.append(name)
        directories[:] = kept
        for name in files:
            path = base / name
            relative = PurePosixPath((relative_base / name).as_posix())
            if _delta_excluded(relative):
                continue
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
                raise ContractError(f"baseline surface contains invalid file type: {relative}")
            result[str(relative)] = ("f", stat.S_IMODE(info.st_mode), _sha(path))
    return result


def baseline_manifest_text(workspace: Path) -> str:
    root = _workspace_root(workspace)
    manifest = _filesystem_manifest(root)
    rows = [BASELINE_HEADER]
    for relative, (kind, mode, digest) in sorted(
        manifest.items(), key=lambda item: item[0].encode("utf-8")
    ):
        rows.append(f"{kind}\t{mode:04o}\t{digest}\t{relative}")
    return "\n".join(rows) + "\n"


def _load_baseline_manifest(workspace: Path, manifest: Path):
    lines = manifest.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != BASELINE_HEADER:
        raise ContractError("baseline manifest requires complete v1 header")
    result = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 4 or fields[0] not in {"f", "d"}:
            raise ContractError("invalid baseline manifest row")
        kind, mode_text, digest, relative_text = fields
        relative = _declared_path(relative_text)
        if str(relative) != relative_text or _delta_excluded(relative):
            raise ContractError(f"invalid baseline manifest path: {relative_text}")
        if relative_text in result:
            raise ContractError(f"duplicate baseline manifest path: {relative_text}")
        if not re.fullmatch(r"0[0-7]{3}", mode_text):
            raise ContractError(f"invalid baseline mode: {relative_text}")
        if kind == "f" and not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ContractError(f"invalid baseline hash: {relative_text}")
        if kind == "d" and digest != "-":
            raise ContractError(f"invalid directory baseline: {relative_text}")
        result[relative_text] = (kind, int(mode_text, 8), digest)
    if not result:
        raise ContractError("complete baseline manifest is empty")
    return result


def _surface_covers(row, relative_text: str) -> bool:
    relative = PurePosixPath(relative_text)
    return relative == row["path"] or (row["tree"] and row["path"] in relative.parents)


def _actual_update_aspects(before, after):
    aspects = set()
    if before[0] != after[0]:
        aspects.add("type")
    if before[1] != after[1]:
        aspects.add("mode")
    if before[0] == after[0] == "f" and before[2] != after[2]:
        aspects.add("content")
    return aspects


def check_actual_delta(workspace: Path, baseline_manifest: Path):
    workspace = workspace.resolve(strict=True)
    declarations = _plan_surface_declarations(workspace)
    if not declarations:
        raise ContractError("actual delta requires active WPLAN CREATE/UPDATE/PRESERVE/REMOVE declarations")
    baseline = _load_baseline_manifest(workspace, Path(baseline_manifest))
    current = _filesystem_manifest(workspace)
    actual = {
        "CREATE": sorted(set(current) - set(baseline), key=lambda value: value.encode("utf-8")),
        "REMOVE": sorted(set(baseline) - set(current), key=lambda value: value.encode("utf-8")),
        "UPDATE": sorted(
            (relative for relative in set(baseline) & set(current) if baseline[relative] != current[relative]),
            key=lambda value: value.encode("utf-8"),
        ),
    }
    hits = {action: set() for action in ("CREATE", "UPDATE", "REMOVE")}
    for action, paths in actual.items():
        rows = declarations.get(action, [])
        for relative in paths:
            matches = [(index, row) for index, row in enumerate(rows) if _surface_covers(row, relative)]
            if len(matches) != 1:
                raise ContractError(f"actual {action} outside exact plan surface: {relative}")
            index, row = matches[0]
            hits[action].add(index)
            contract = row["contract"]
            if action == "CREATE":
                expected = f"{'file' if current[relative][0] == 'f' else 'directory'}:{current[relative][1]:04o}"
                if contract != expected:
                    raise ContractError(f"CREATE type/mode contract mismatch: {relative}")
            elif action == "REMOVE":
                expected = "file" if baseline[relative][0] == "f" else "directory"
                if contract != expected:
                    raise ContractError(f"REMOVE type contract mismatch: {relative}")
            else:
                allowed = set(contract.split(",")) if contract else set()
                if not allowed or not allowed <= {"content", "mode", "type"}:
                    raise ContractError(f"invalid UPDATE capability contract: {relative}")
                aspects = _actual_update_aspects(baseline[relative], current[relative])
                if not aspects or not aspects <= allowed:
                    raise ContractError(f"UPDATE type/mode/content outside contract: {relative}")
    for action in ("CREATE", "UPDATE", "REMOVE"):
        rows = declarations.get(action, [])
        if hits[action] != set(range(len(rows))):
            raise ContractError(f"declared {action} has no matching actual delta")

    union = set(baseline) | set(current)
    preserve_rows = declarations.get("PRESERVE", [])
    for row in preserve_rows:
        covered = [relative for relative in union if _surface_covers(row, relative)]
        if not covered:
            raise ContractError(f"protected surface absent from complete baseline/current: {row['raw']}")
        changed = [relative for relative in covered if baseline.get(relative) != current.get(relative)]
        if changed:
            raise ContractError(f"protected surface changed: {row['raw']}: {changed[:5]}")
    return {
        "CREATE": len(actual["CREATE"]), "UPDATE": len(actual["UPDATE"]),
        "REMOVE": len(actual["REMOVE"]), "PROTECTED": len(preserve_rows),
    }


def _git(workspace: Path, *arguments):
    try:
        completed = subprocess.run(
            ["git", "-C", str(workspace), *arguments],
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ContractError(f"Git inspection failed: {error}") from error
    if completed.returncode:
        raise ContractError(f"Git inspection failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def _repository_identity(value: str) -> bool:
    return bool(re.fullmatch(r"[^/\s:@\\?#]+/[^/\s:@\\?#]+", value or "")) and not value.casefold().endswith(".git")


def _remote_repository_identity(value: str):
    candidate = value.strip()
    if "://" in candidate:
        path = urlparse(candidate).path
    elif re.match(r"^[^/@\s]+@[^:/\s]+:", candidate):
        path = candidate.split(":", 1)[1]
    else:
        path = candidate
    parts = [unquote(part) for part in PurePosixPath(path).parts if part not in {"", "/"}]
    if len(parts) < 2:
        return None
    repository = parts[-1][:-4] if parts[-1].casefold().endswith(".git") else parts[-1]
    identity = f"{parts[-2]}/{repository}"
    return identity if _repository_identity(identity) else None


def _check_sot(workspace: Path, profile):
    agents = (workspace / "AGENTS.md").read_text(encoding="utf-8")
    projections = [match.group(1) for line in agents.splitlines() if (match := SOT_FIELD.match(line))]
    repositories = [match.group(1) for line in agents.splitlines() if (match := REPOSITORY_FIELD.match(line))]
    if projections:
        raise ContractError("legacy AGENTS SOT_MODE is forbidden; Project Profile is the sole SoT owner")
    if profile.sot_mode == "sot_files":
        if repositories:
            raise ContractError("repository identity недопустима для sot_files")
        return {"mode": "sot_files", "git_invocations": 0}
    git_path = workspace / ".git"
    if git_path.is_symlink() or not git_path.exists():
        raise ContractError("локальный Git repository отсутствует")
    if Path(_git(workspace, "rev-parse", "--show-toplevel")).resolve() != workspace:
        raise ContractError("Git repository root mismatch")
    _git(workspace, "rev-parse", "--verify", "HEAD^{commit}")
    _git(workspace, "symbolic-ref", "--quiet", "--short", "HEAD")
    if _git(workspace, "status", "--porcelain=v1", "--untracked-files=all"):
        raise ContractError("Git working tree не чист")
    remotes = _git(workspace, "remote").splitlines()
    if profile.sot_mode == "sot_git":
        if remotes:
            raise ContractError("sot_git запрещает remote")
        return {"mode": "sot_git"}
    if len(repositories) != 1 or not _repository_identity(repositories[0]):
        raise ContractError("sot_github требует одну repository identity owner/repository")
    if remotes != ["origin"]:
        raise ContractError("sot_github требует ровно один origin")
    origin_url = _git(workspace, "remote", "get-url", "origin")
    if _remote_repository_identity(origin_url) != repositories[0]:
        raise ContractError("origin repository identity mismatch")
    upstream = _git(workspace, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if not upstream.startswith("origin/"):
        raise ContractError("sot_github upstream mismatch")
    default_ref = _git(workspace, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    if not default_ref.startswith("refs/remotes/origin/"):
        raise ContractError("origin/HEAD mismatch")
    ahead_behind = _git(workspace, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    if len(ahead_behind) != 2 or int(ahead_behind[1]) != 0:
        raise ContractError("branch behind/diverged")
    return {"mode": "sot_github", "network": "not_performed"}


def _research_entries(text: str, prefix=""):
    # Inventory declarations are list rows; prose may cite immutable evidence.
    pattern = re.compile(r"(?m)^\s*(?:\d+[.)]|[-*])\s+`(?:research/archives/)?([^`/]+\.(?:zip|tar\.gz))`")
    values = pattern.findall(text)
    if len(values) != len(set(values)):
        raise ContractError(f"duplicate archive row: {prefix}")
    return set(values)


def _check_research_registry(workspace: Path):
    text = (workspace / "research/00-index.md").read_text(encoding="utf-8")
    match = re.search(r"(?is)следующ(?:ий|его).{0,120}?`(\d{1,6})`", text)
    if not match:
        raise ContractError("research/00-index.md не объявляет следующий research ID")
    next_id = int(match.group(1))
    used = []
    for path in (workspace / "research").iterdir():
        domain = re.match(r"^(\d+)_", path.name)
        if domain:
            used.append(int(domain.group(1)))
    archives = workspace / "research/archives"
    if archives.is_dir() and not archives.is_symlink():
        for path in archives.iterdir():
            payload = re.match(r"^(\d+)_.*(?:\.zip|\.tar\.gz)$", path.name)
            if payload:
                used.append(int(payload.group(1)))
    if next_id <= max(used, default=0):
        raise ContractError(f"research ID {next_id:02d} не больше existing maximum")
    return {"next_id": next_id, "used_count": len(set(used))}


def _check_research(workspace: Path):
    index = workspace / "research/00-index.md"
    text = index.read_text(encoding="utf-8")
    archives = workspace / "research/archives"
    catalog_active = bool(re.search(r"(?m)^##\s+Архивы\s*$", text))
    if not archives.exists() and not catalog_active:
        return "ABSENT"
    _regular(archives, "d", "research/archives")
    readme = archives / "README.md"
    manifest = archives / "MANIFEST.sha256"
    _regular(readme, "f", "research/archives/README.md")
    _regular(manifest, "f", "research/archives/MANIFEST.sha256")
    payloads = {
        path.name for path in archives.iterdir()
        if path.is_file() and (path.name.endswith(".zip") or path.name.endswith(".tar.gz"))
    }
    if not payloads:
        raise ContractError("active archive lifecycle requires payload")
    manifest_rows = []
    hashes = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  research/archives/([^/]+(?:\.zip|\.tar\.gz))", line)
        if not match:
            raise ContractError("invalid research archive manifest row")
        digest, name = match.groups()
        manifest_rows.append(name)
        hashes[name] = digest
    if len(manifest_rows) != len(set(manifest_rows)):
        raise ContractError("duplicate research archive manifest row")
    root_rows = _research_entries(text, "root-index")
    readme_rows = _research_entries(readme.read_text(encoding="utf-8"), "archive-readme")
    if payloads != set(manifest_rows) or payloads != root_rows or payloads != readme_rows:
        raise ContractError("research archive set mismatch")
    for name in _raw_sorted(payloads):
        if _sha(archives / name) != hashes[name]:
            raise ContractError(f"research archive hash mismatch: {name}")
    return "ACTIVE"


def _anchor(value: str):
    value = re.sub(r"[`*]", "", value.strip().lower())
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"\s", "-", value).strip("-")


def _anchors(path: Path):
    values = set()
    counts = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if not match:
            continue
        base = _anchor(match.group(1)); count = counts.get(base, 0); counts[base] = count + 1
        values.add(base if count == 0 else f"{base}-{count}")
    return values


def _markdown_targets(text: str):
    for match in re.finditer(r"!?\[[^]]*\]\(([^)]+)\)", text):
        value = match.group(1).strip()
        if value.startswith("<") and ">" in value:
            value = value[1:value.index(">")]
        elif " " in value:
            value = value.split(" ", 1)[0]
        yield unquote(value)


def _excluded(relative: PurePosixPath, product_name: str):
    prefixes = (product_name, *SERVICE_NAMES, "plans/completed", "research/archives")
    return any(relative.parts[:len(PurePosixPath(value).parts)] == PurePosixPath(value).parts for value in prefixes)


def _check_links(workspace: Path, product_name: str):
    issues = []
    for path in workspace.rglob("*.md"):
        relative = PurePosixPath(path.relative_to(workspace).as_posix())
        if _excluded(relative, product_name):
            continue
        for target in _markdown_targets(path.read_text(encoding="utf-8")):
            if not target or target.startswith(("http://", "https://", "mailto:", "codexlog:")):
                continue
            path_part, _separator, fragment = target.partition("#")
            candidate = path if not path_part else path.parent.joinpath(*PurePosixPath(path_part).parts)
            if PurePosixPath(path_part).is_absolute():
                issues.append(f"{relative} -> {target}: absolute path")
                continue
            try:
                candidate.resolve(strict=True).relative_to(workspace)
            except (OSError, ValueError):
                issues.append(f"{relative} -> {target}: missing/escape")
                continue
            if fragment and candidate.is_file() and fragment not in _anchors(candidate):
                issues.append(f"{relative} -> {target}: missing anchor")
    if issues:
        raise ContractError("; ".join(_raw_sorted(issues)[:10]))


def _check_residue(workspace: Path, product_name: str):
    found = []
    for current, directories, files in os.walk(workspace, topdown=True, followlinks=False):
        base = Path(current); relative_base = base.relative_to(workspace)
        kept = []
        for name in directories:
            relative = PurePosixPath((relative_base / name).as_posix())
            if _excluded(relative, product_name):
                continue
            path = base / name
            if path.is_symlink():
                raise ContractError(f"symlink in Workspace-owned surface: {relative}")
            if name in DISPOSABLE_DIR_NAMES:
                found.append(relative.as_posix())
            else:
                kept.append(name)
        directories[:] = kept
        for name in files:
            relative = PurePosixPath((relative_base / name).as_posix())
            if _excluded(relative, product_name):
                continue
            path = base / name
            if not stat.S_ISREG(path.lstat().st_mode):
                raise ContractError(f"special node in Workspace-owned surface: {relative}")
            if name.endswith(DISPOSABLE_SUFFIXES) or name.endswith(":Zone.Identifier"):
                found.append(relative.as_posix())
    if found:
        raise ContractError(", ".join(_raw_sorted(set(found))))


def check_preservation_manifest(workspace: Path, manifest: Path):
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        fields = line.split("\t")
        if fields[0] == "prefix" and len(fields) == 4:
            size, expected, relative = int(fields[1]), fields[2], fields[3]
            candidate = workspace / relative
            data = candidate.read_bytes()
            if len(data) < size or hashlib.sha256(data[:size]).hexdigest() != expected:
                raise ContractError(f"prefix mismatch: {relative}")
            continue
        if len(fields) != 4 or fields[0] not in {"f", "d"}:
            raise ContractError("invalid preservation manifest row")
        kind, mode_text, expected, relative = fields
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            raise ContractError("preservation path escapes Workspace")
        candidate = workspace.joinpath(*pure.parts)
        candidate.resolve(strict=True).relative_to(workspace)
        info = candidate.lstat()
        actual = "d" if stat.S_ISDIR(info.st_mode) else "f" if stat.S_ISREG(info.st_mode) else "o"
        if actual != kind or stat.S_IMODE(info.st_mode) != int(mode_text, 8):
            raise ContractError(f"type/mode mismatch: {relative}")
        if kind == "f" and _sha(candidate) != expected:
            raise ContractError(f"content mismatch: {relative}")


def inspect_workspace(workspace_value, preservation_manifest=None, baseline_manifest=None):
    workspace = _workspace_root(workspace_value)
    module = _load_profile_module(workspace)
    checks = []
    errors = []
    state = {"profile": None, "product": None, "archive": "UNKNOWN"}

    def perform(identifier, operation):
        try:
            value = operation()
            checks.append({"id": identifier, "status": "PASS", "value": value})
            return value
        except (ContractError, OSError, UnicodeError, ValueError) as error:
            errors.append(f"{identifier}: {error}")
            checks.append({"id": identifier, "status": "FAIL", "message": str(error)})
            return None

    discovered = perform("project-profile", lambda: _discover_profile(workspace, module))
    if discovered is not None:
        state["profile"], _profile_path, state["product"] = discovered
    perform("workspace-core", lambda: _check_core(workspace))
    perform("active-wplan", lambda: _check_route(workspace))
    if checks[-1]["status"] == "FAIL":
        checks.append({"id": "checkpoint", "status": "FAIL", "message": "route/checkpoint inconsistent"})
        errors.append("checkpoint: route/checkpoint inconsistent")
    else:
        checks.append({"id": "checkpoint", "status": "PASS"})
    perform("sdlc-transition", lambda: _check_sdlc_transition(workspace))
    perform("plan-surfaces", lambda: _check_plan_surfaces(workspace))
    perform("documentation-impact", lambda: _check_documentation_impact(workspace))
    if state["profile"] is not None:
        perform("workspace-sot", lambda: _check_sot(workspace, state["profile"]))
    perform("research-registry", lambda: _check_research_registry(workspace))
    archive = perform("research-archives", lambda: _check_research(workspace))
    if archive is not None:
        state["archive"] = archive
    product_name = state["product"].name if state["product"] is not None else "__invalid_product__"
    perform("markdown-links", lambda: _check_links(workspace, product_name))
    perform("runtime-residue", lambda: _check_residue(workspace, product_name))
    preservation = "NOT_REQUESTED"
    if preservation_manifest is not None:
        value = perform("preservation-manifest", lambda: check_preservation_manifest(workspace, Path(preservation_manifest)))
        preservation = "PASS" if value is None and checks[-1]["status"] == "PASS" else "FAIL"
    if baseline_manifest is not None:
        perform("actual-delta", lambda: check_actual_delta(workspace, Path(baseline_manifest)))
    return {
        "schema": "generic.workspace-check.v1",
        "status": "PASS" if not errors else "FAIL",
        "fail_count": len(errors),
        "warn_count": 0,
        "archive_state": state["archive"],
        "preservation": preservation,
        "checks": checks,
        "errors": errors,
    }


def _error_result(message):
    return {
        "schema": "generic.workspace-check.v1", "status": "STOP", "fail_count": 1,
        "warn_count": 0, "archive_state": "UNKNOWN", "preservation": "NOT_REQUESTED",
        "checks": [], "errors": [str(message)],
    }


def main(argv=None) -> int:
    parser = JsonArgumentParser(description="Generic read-only Workspace checker")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--preservation-manifest", type=Path)
    parser.add_argument("--baseline-manifest", type=Path)
    parser.add_argument("--print-baseline-manifest", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    output_format = "text"
    try:
        args = parser.parse_args(argv)
        output_format = args.format
        if args.print_baseline_manifest:
            if args.preservation_manifest is not None or args.baseline_manifest is not None or args.format != "text":
                raise UsageError("--print-baseline-manifest cannot be combined with manifests or --format json")
            sys.stdout.write(baseline_manifest_text(args.workspace))
            return 0
        result = inspect_workspace(args.workspace, args.preservation_manifest, args.baseline_manifest)
        code = 0 if result["status"] == "PASS" else 1
    except (UsageError, ContractError, OSError, ValueError) as error:
        result, code = _error_result(error), 2
    if output_format == "json" or (argv is not None and "--format" in argv and "json" in argv):
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, default=str))
    else:
        print(f"WORKSPACE_CHECK: {result['status']}")
        print(f"FAIL: {result['fail_count']}")
        print("WARN: 0")
        print(f"ARCHIVE_STATE: {result['archive_state']}")
        for error in result.get("errors", []):
            print(f"ERROR: {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

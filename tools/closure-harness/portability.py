#!/usr/bin/env python3
"""portability.py - STCM v0.6 portability predicates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortabilityInput:
    source_declared: bool
    target_declared: bool
    receipt_posture: str
    conflict_posture: str
    deposit_posture: str
    hidden_dependency: bool
    lineage_continuous: bool
    authority_posture: str


@dataclass(frozen=True)
class PortabilityDecision:
    outcome: str
    portable_candidate: bool
    cross_repo_valid: bool
    reason: str


def evaluate_portability(inp: PortabilityInput) -> PortabilityDecision:
    if not inp.source_declared:
        return PortabilityDecision("SOURCE_NOT_DECLARED", False, False, "Source repository has not declared validation posture.")
    if not inp.target_declared:
        return PortabilityDecision("TARGET_NOT_DECLARED", False, False, "Target repository has not declared acceptance posture.")
    if inp.receipt_posture == "missing":
        return PortabilityDecision("MISSING_RECEIPT", False, False, "No receipt exists to evaluate as cross-repo basis.")
    if inp.receipt_posture == "stale":
        return PortabilityDecision("RECEIPT_STALE", False, False, "Receipt is stale and cannot serve as current basis.")
    if inp.receipt_posture == "superseded":
        return PortabilityDecision("RECEIPT_SUPERSEDED", False, False, "Receipt has been superseded and cannot serve as current basis.")
    if inp.receipt_posture == "conflict_linked":
        return PortabilityDecision("RECEIPT_CONFLICT_LINKED", False, False, "Receipt is linked to an unresolved conflict posture.")

    if inp.conflict_posture == "open_blocking":
        return PortabilityDecision("CONFLICT_OPEN", False, False, "Open conflict prevents cross-repo portability.")
    if inp.conflict_posture == "under_review":
        return PortabilityDecision("CONFLICT_UNDER_REVIEW", False, False, "Conflict is under review.")
    if inp.conflict_posture == "resolved_rejected":
        return PortabilityDecision("CONFLICT_RESOLUTION_REJECTED", False, False, "Conflict resolution rejected the receipt as current basis.")
    if inp.conflict_posture == "superseded_by_resolution":
        return PortabilityDecision("CONFLICT_SUPERSEDED_BY_RESOLUTION", False, False, "Receipt was superseded by the resolution result.")
    if inp.conflict_posture == "unresolved_external":
        return PortabilityDecision("CONFLICT_EXTERNAL_UNRESOLVED", False, False, "External conflict posture is unresolved.")

    if inp.deposit_posture in {"missing_policy", "refuses_external"}:
        return PortabilityDecision("DEPOSIT_NOT_ALLOWED", False, False, "Target repository has not declared acceptance of incoming validation records.")
    if inp.deposit_posture == "technical_only":
        return PortabilityDecision("TECHNICAL_ACCESS_NOT_AUTHORITY", False, False, "Technical write access is not admissible deposit authority.")
    if inp.hidden_dependency:
        return PortabilityDecision("HIDDEN_DEPENDENCY", False, False, "Required validation basis depends on undeclared state.")
    if not inp.lineage_continuous:
        return PortabilityDecision("LINEAGE_NOT_CONTINUOUS", False, False, "Receipt lineage does not remain continuous across the repository boundary.")

    if inp.authority_posture in {"refused", "source_bound", "evidence_only"}:
        return PortabilityDecision("AUTHORITY_NOT_PORTABLE", False, False, "Authority cannot travel from source to target.")
    if inp.authority_posture == "expired":
        return PortabilityDecision("AUTHORITY_EXPIRED", False, False, "Authority expired before target acceptance.")
    if inp.authority_posture == "scope_mismatch":
        return PortabilityDecision("AUTHORITY_SCOPE_MISMATCH", False, False, "Authority does not cover the target transition scope.")
    if inp.authority_posture == "delegated":
        return PortabilityDecision("AUTHORITY_REBIND_REQUIRED", False, False, "Delegated authority requires target-side rebind before current-basis use.")

    if inp.authority_posture in {"rebound", "portable_signed"}:
        if inp.deposit_posture == "declared_reference_only":
            return PortabilityDecision("REFERENCE_ONLY_PENDING_BOUNDARY", True, False, "Receipt may be referenced, but not deposited as current basis.")
        return PortabilityDecision("PORTABLE_PENDING_BOUNDARY", True, False, "Positive path is visible, but STCM v0.6 remains draft.")

    return PortabilityDecision("UNCLASSIFIED", False, False, "Input did not match any declared v0.6 portability predicate.")

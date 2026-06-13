#!/usr/bin/env python3
"""portability.py - STCM v0.6 portability predicates.

These predicates evaluate draft cross-repo receipt authority posture.
They do not claim completed cross-repo validity.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortabilityInput:
    source_declared: bool
    target_declared: bool
    receipt_current: bool
    conflict_open: bool
    deposit_posture: str
    hidden_dependency: bool
    lineage_continuous: bool
    authority_class: str
    authority_rebound: bool


@dataclass(frozen=True)
class PortabilityDecision:
    outcome: str
    portable_candidate: bool
    cross_repo_valid: bool
    reason: str


def evaluate_portability(inp: PortabilityInput) -> PortabilityDecision:
    if not inp.source_declared:
        return PortabilityDecision(
            "SOURCE_NOT_DECLARED", False, False,
            "Source repository has not declared validation posture.")
    if not inp.target_declared:
        return PortabilityDecision(
            "TARGET_NOT_DECLARED", False, False,
            "Target repository has not declared acceptance posture.")
    if not inp.receipt_current:
        return PortabilityDecision(
            "RECEIPT_NOT_CURRENT", False, False,
            "Receipt is stale or superseded and cannot serve as current basis.")
    if inp.conflict_open:
        return PortabilityDecision(
            "CONFLICT_OPEN", False, False,
            "Open conflict blocks cross-repo portability.")
    if inp.deposit_posture in {"missing_policy", "refuses_external"}:
        return PortabilityDecision(
            "DEPOSIT_NOT_ALLOWED", False, False,
            "Target repository has not declared acceptance of incoming validation records.")
    if inp.deposit_posture == "technical_only":
        return PortabilityDecision(
            "TECHNICAL_ACCESS_NOT_AUTHORITY", False, False,
            "Technical write access is not admissible deposit authority.")
    if inp.hidden_dependency:
        return PortabilityDecision(
            "HIDDEN_DEPENDENCY", False, False,
            "Required validation basis depends on undeclared state.")
    if not inp.lineage_continuous:
        return PortabilityDecision(
            "LINEAGE_NOT_CONTINUOUS", False, False,
            "Receipt lineage does not remain continuous across the repository boundary.")

    if inp.authority_class in {"refused", "source_bound"}:
        return PortabilityDecision(
            "AUTHORITY_NOT_PORTABLE", False, False,
            "Authority cannot travel from source to target.")

    if inp.authority_class == "evidence_portable" and not inp.authority_rebound:
        return PortabilityDecision(
            "AUTHORITY_REBIND_REQUIRED", False, False,
            "Evidence may travel, but target authority has not been rebound.")

    if inp.authority_class in {"authority_portable", "evidence_portable"}:
        if inp.deposit_posture == "declared_reference_only":
            return PortabilityDecision(
                "REFERENCE_ONLY_PENDING_BOUNDARY", True, False,
                "Receipt may be referenced, but not deposited as current basis.")
        return PortabilityDecision(
            "PORTABLE_PENDING_BOUNDARY", True, False,
            "Positive path is visible, but STCM v0.6 remains draft.")

    return PortabilityDecision(
        "UNCLASSIFIED", False, False,
        "Input did not match any declared v0.6 portability predicate.")

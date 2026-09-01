# Transition Ledger Mirror Handoff

Repository: `Admissible-Existence/STCM`

## Invariant

Every durable transition owned by this repository is recorded first in this repository's transition ledger. Repository replay/reconstruction must terminate at this level and must not require organization- or ecosystem-level replay.

Canonical source contract: `.stegverse/transition-ledger/contract.json`

Emitter: `.stegverse/transition-ledger/emit.py`

Runtime receipts are append-only and hash-linked by `previous_receipt_sha256`. The default durable runtime root is `$XDG_STATE_HOME/stegverse/repo-ledgers/Admissible-Existence/STCM`; `STEGVERSE_REPO_LEDGER_ROOT` may bind an approved sovereign durable location.

## Propagation

Only evidence required to reconstruct organization-level state propagates upward to `Admissible-Existence/.github`. Organization aggregation does not replace this repository's ledger.

## Authority

Recording a transition creates no execution, standing, admission, publication, credential, or lifecycle authority. Internal inference that does not create a durable repository-owned state transition need not be recorded merely because it occurred.

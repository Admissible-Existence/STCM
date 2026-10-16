# STCM Mathematical Notation and Bounded Derivations

Goal: `STCM-MATHEMATICAL-COMPLETENESS-002`

This file makes equations already present in `docs/STATE_TRANSITION_CONSERVATION_MODEL.md` explicit for organization-wide audit. It derives bounded consequences of the declared model; it does not assert universal proof.

## Conservation closure

Let a governed transition conservation record be represented by

`R_T = (S_before, S_after, receipts, A, I, phi, H, E, C, authority, evidence, R_out)`

where `A` is the active node set, `I` the ignored node set, `phi` the phase posture, `H` the hash-scope posture, `E` transition entropy/accounting, `C` compute/governance capacity accounting, and `R_out` the resulting receipt.

For each transition type let `Req(T)` be its required conservation fields. Define closure predicate

`Close(R_T) := forall q in Req(T), accounted(q)`.

`accounted(q)` means the required field is present and valid, explicitly refused/blocked, or explicitly not applicable under the governing policy; silence is not accounting.

The source theory defines a coherent transition receipt basis only when

`Coherent(T) => Close(R_T)`.

This is the bounded derivation behind `STCM-PC-001`. It is a consequence of STCM's definition of coherence, not a claim that every real-world system must adopt that definition.

## Finite capacity

For Prime Node `n`, let governed load be `L_g(n,t)` and governed coherent capacity be `C_g(n,t)`.

Declared operating condition:

`L_g <= C_g => coherent operation is permitted by the capacity condition`.

If

`L_g > C_g`,

the model requires a structural response from

`{replicate, specialize, reroute, refuse, escalate, pause, evolve, devolve, dissolve}`.

If `L_g > C_g` persists while neither `L_g` decreases nor `C_g` increases and no structural response removes the overload, the capacity premise for coherent operation is violated. This is the bounded threshold derivation for `STCM-PC-002`.

For devolution, with initial parameter count `P_0` and resulting explicit node positions `N`, the source bound is

`N <= P_0`.

## Hash-scoped activation

Let `h(d)` denote the relevant hash posture of incoming data `d` and `H_n` the declared accepted hash scope of node `n`.

Define match predicate

`M(n,d) := [h(d) in H_n]`.

Under strict non-engagement,

`NOT M(n,d) => n not in A(d)`

where `A(d)` is the activated node set for the transition. Therefore the candidate active set satisfies

`A(d) subseteq {n | M(n,d)}`.

Non-matching nodes remain candidates for available capacity instead of consuming transition-specific interpretation cost. This is `STCM-PC-003`.

## Routing predicate

For candidate path step `(n,d)`, define:

- `M(n,d)` = hash-scope match;
- `Q(d)` = required receipt posture is sufficient;
- `T(n,d)` = Transition Table permits the step.

Then the source routing equation is

`RoutePossible(n,d) = M(n,d) AND Q(d) AND T(n,d)`.

For match count `m = |{n : M(n,d)}|`, the source model distinguishes:

`m = 0 -> no governed route`,

`m = 1 -> singular candidate route`,

`m >= 2 -> candidate governed branch`,

subject in every case to receipt sufficiency and Transition Table permission. This is the bounded conjunction derivation for `STCM-PC-004`.

## Compute accounting

For a bounded system capacity at an evaluated moment,

`C_total = C_active + C_available + C_released + C_blocked`.

The terms denote capacity currently used by activated nodes, preserved by inactive/ignored nodes, released by structural change, and prevented from entering invalid paths respectively.

Under the selective activation rule, transition-specific active cost is modeled as a function of activated nodes:

`Cost_T = f(A(d))`,

rather than a function that necessarily activates the entire node population. The source shorthand `compute cost proportional to activated nodes, not total nodes` is a model objective/claim whose falsification conditions are stated separately. This is `STCM-PC-005`.

## Moment-bound validity

Let required values at time `t` be `V_req(t)` and observed values `V_obs(t)`. Define transition predicate

`P_T(t) := [V_obs(t) satisfies V_req(t)]`.

A result established at `t_1` establishes only `P_T(t_1)`. In general,

`P_T(t_1)` does not imply `P_T(t_2)`

unless the values required for the predicate are shown invariant across the interval or are revalidated at `t_2`.

This is `STCM-PC-006` and formalizes the source statement that transition validity is moment-bound unless revalidated.

## Proof maturity

The PN-001..PN-006 closure fixtures and hosted harness provide bounded evidence for the implemented closure predicate. They do not prove the capacity law, routing law, compute relation, or conservation principle universally. All six proof candidates remain `candidate_not_proven`.

## 7. G7: continuity lemma (missing, forked, stale links) [NEW, discrete; generalizes STCM-L fixtures]

Status: **DRAFT / candidate derivations.** Prepared 2026-10-16 by Grok Bot for owner and practitioner review.

> **Disclaimer.** This is a working draft. It is not a statement of truth, not a legal or patentability determination, and grants no execution, release, publication or standing authority. Every item is a candidate for owner/practitioner review. Nothing here has been added to any repository.

Each step is tagged:
- **[STD]**: follows from a standard published result (cited);
- **[NEW]**: new derivation written in this draft (elementary, but not yet reviewed);
- **[ASSUME]**: explicit assumption;
- **[INTERP]**: interpretation or mapping, not a derivation.

### Relation to the existing v0.4 prior-receipt linking fixtures

This candidate sits next to the existing v0.4 prior-receipt linking fixtures. Those fixtures are specified in `docs/STCM_V0_4_SEQUENTIAL_RECEIPT_LINEAGE.md` (§ Implemented v0.4 fixtures) and implemented in `tools/closure-harness/lineage_fixtures.py`. Each fixture binds `claimed_prior_receipt_id`, `claimed_prior_receipt_hash`, and `sequence_index` to a `prior_receipt` (the predecessor) and, when continuity is claimed, to a supplied `chain_head`. The heading above records that G7 generalizes those STCM-L fixtures. The correspondence is:

| G7 case | v0.4 fixture | Fixture verdict and write-up |
|---|---|---|
| On-path predecessor link | `lin_bound` | `BOUND` — `docs/STCM_V0_4_SEQUENTIAL_RECEIPT_LINEAGE.md`, "1. Prior receipt binds" |
| Missing link | `lin_missing` | `MISSING_PRIOR` — same document, "2. Missing prior receipt" |
| Fork (two records claim the same predecessor and the same index) | `lin_conflict_competing` | `CONFLICT` — same document, "6. Competing receipt chains" |
| Stale or out-of-sequence binding | `lin_stale` | `STALE` — same document, "4. Stale prior receipt" |
| Hash mismatch named with the STCM-L verdicts in the statement below | `lin_hash_mismatch` | `CONFLICT` — same document, "3. Prior receipt hash mismatch" |
| Superseded predecessor named with those verdicts | `lin_superseded` | `SUPERSEDED` — same document, "5. Superseded prior receipt" |
| Tail truncation without a trusted head index | the v0.4 harness supplies `chain_head` on continuity claims (`tools/closure-harness/lineage_fixtures.py`); a green v0.4 run leaves cryptographic proof beyond fixture hash comparison as a later boundary (`docs/STCM_V0_4_SEQUENTIAL_RECEIPT_LINEAGE.md`, "What v0.4 does not prove yet") | undetectable without trusted head index \(m\) (limit 4 below) |

### Citations

| Ref | Source | Path | Commit |
|---|---|---|---|
| STCM-L | STCM v0.4 sequential receipt lineage | `Admissible-Existence/STCM/docs/STCM_V0_4_SEQUENTIAL_RECEIPT_LINEAGE.md` | `abf119f0…` |

External standard references. **(v)** means the bibliographic details were verified this session; **(c)** means they are cited from memory and need a practitioner check:
- [M79] R. C. Merkle, *Secrecy, Authentication, and Public Key Systems*, Ph.D. thesis, Stanford University, 1979. (v)
- [HS91] S. Haber, W. S. Stornetta, "How to time-stamp a digital document," *J. Cryptology* 3(2):99–111, 1991, doi:10.1007/BF00196791. (v)
- [D89] I. Damgård, "A Design Principle for Hash Functions," CRYPTO '89 (LNCS 435), 1990; and [M89] R. C. Merkle, "One Way Hash Functions and DES," same volume. (c; the Merkle–DES item is listed in HS91's references)

The proof sketch below names G3 for uniqueness of the backward walk except with collision probability. The citation sentence carried with that reduction is: This is the standard hash-chain/Merkle–Damgård argument ([M79], [D89]/[M89]). Its use for tamper-evident ordered records follows [HS91].

### Assumptions

**[ASSUME] A3 (unambiguous encoding).** \(\langle\cdot\rangle\) is an injective, length-prefixed encoding of tuples.

**[ASSUME] A4 (collision resistance).** For every efficient procedure \(\mathcal B\), \(\Pr[\mathcal B \text{ outputs } x\ne x' \text{ with } H(x)=H(x')]\le\epsilon_{\mathrm{coll}}\). This is a computational assumption about the chosen \(H\) (e.g. SHA-256). It is not a theorem.

**Receipts.** For a hash \(H:\{0,1\}^*\to\{0,1\}^\lambda\) and domain tags \(\tau_0\ne\tau\):
\[R_0=H\langle\tau_0,\,0,\,S_0\rangle,\qquad R_{j+1}=H\langle\tau,\,j{+}1,\,R_j,\,\delta_j,\,S_{j+1}\rangle.\]
(Binding \(H(\delta_j)\) and a Merkle root of \(S_{j+1}\) in place of the raw values gives the same results. Collisions then also count collisions of the inner hash or tree.)

**Setting.** A verifier holds a set \(\mathcal Q\) of claimed receipt records \((j,R_j,\text{pred}=R_{j-1})\) and a trusted head \((m,R_m)\).

**Statement (under A4).**
1. *Missing link.* If, walking back from \(R_m\) by predecessor references, some referenced \(R_{j-1}\) is absent from \(\mathcal Q\) (and from regenerable data), the gap at index \(j-1\) is detected and localized.
2. *Fork.* If two distinct records claim the same predecessor and the same index, at most one lies on the path to the trusted \(R_m\) unless a collision exists. The fork is detected and the off-path branch is identified.
3. *Stale or out-of-sequence binding.* A record claiming index \(j\) whose predecessor's index is not \(j-1\), or whose predecessor is not the current head when appended, violates the index field bound in the hash. It is detected (cf. STCM-L verdicts: missing prior, hash mismatch, stale, superseded, competing chains).
4. *Limit.* Without a trusted head index \(m\), truncation of the tail (dropping \(R_{m'}\ldots R_m\)) is undetectable. Trusted anchoring of the head is necessary.

**Proof sketch.**
1. Every \(R_j\) commits to \((j,R_{j-1})\) (A3).
2. The backward walk from a trusted \(R_m\) is unique except with collision probability (G3).
3. Any record not on that walk either fails linkage (cases 1 and 3) or shares a predecessor with an on-path record (case 2).
4. Case 4: an untrusted shorter chain is internally consistent.
∎

| Item | Status | Rests on |
|---|---|---|
| G7 continuity | NEW discrete lemma; proof sketch | A3, A4, trusted head |

# ORDER-006-P2 — ARQ2 final checkpoint

ROLE=ARQ2_MONEYKILLER  
BRANCH=arq2/arc-killtest-v1  
SCOPE=competitions/arc-agi-3/** + ARQ2 checkpoint/workflow only  
DECISION=KILLED_NO_EDGE  
COST_USD=0  
REPAIR_USED=0  
ABLATIONS_RUN=NO  
NOTEBOOK_BUILT=NO  
KAGGLE_SUBMISSION=NO  
MERGE=NO

## A0 gate

- Public rules/runtime inspection completed.
- Authenticated Kaggle account/rules acceptance could not be verified from this chat and is recorded as UNVERIFIED_AUTHENTICATED_STATE; no assumption was made.
- Runtime pins used for the decisive run:
  - Python 3.12.14
  - arc-agi 0.9.9
  - official ARC-AGI-3-Agents commit 4743e7d0aaae0ded0d98a89a7e282e63564cd58b
  - official local-dev starter inspected at eeb1535404f321d280a8f9194bbc1d7aca5f05fc
  - Ubuntu 24.04 GitHub-hosted CPU runner
- Starter/runtime parity: the official framework/runtime contract was pinned and all four agents executed the official Agent.main loop with zero runtime errors across the frozen 25-game corpus. The unmodified stochastic starter itself was not separately score-benchmarked; this limitation is explicit.

## TDD / harness gate

Initial contract run failed 4/4 for the intended reason: the migrated harness lacked the required four-lane variant contract and promotion function. The subsequent implementation passed 4/4 contract tests and compile checks.

Pre-promotion lanes were frozen as:

- A_BASE_0 — seeded legal random
- A_BASE_1 — deterministic round-robin
- A_BASE_2 — cheap novelty / information explorer
- A_CHALLENGER — migrated symbolic action-effect planner

Ablations remained opt-in and were not run before promotion.

## Frozen public ARC killtest

Decisive successful workflow:

- workflow run: 36185344549
- job: 108237288327
- commit: f103694e5e0a8ff19fa3e86285b75800a50458f7
- git tree: e3305c2d482c3a7f26d02f72b2ecfbb56195e43d
- Actions artifact: 10886013030
- corpus: 25 public environments
- repeats: 2
- max actions: 200 configured; framework loop records 201 actions because upstream Agent.main uses <= MAX_ACTIONS
- corpus internal SHA256: 4970c1faccc88ec02195f289ffcdd0105f5d9de3b960ff31611754f7e9dd9c0a
- frozen-corpus file SHA256: 70b3276328da840896761230719be3b5098d0c98b1543230c280250a10772ae7
- core-killtest file SHA256: 096ed9204eb4dc8c8fcde8349f1e49ffe17e1ec11dcd443f4eb7a5750466916e
- internal artifact SHA256: b272fd61b073c27e4dd14e455c4a0cfdbba4e6449222fbe1197d1cb418c535df
- durable machine-readable digest: competitions/arc-agi-3/evidence/ORDER-006-P2-killtest-digest.json

### Summary

| lane | RHAE | levels | games with progress | mean actions | errors | exact repeatability |
|---|---:|---:|---:|---:|---:|---|
| A_BASE_0 | 0.0000000000 | 0 | 0 | 5025 | 0 | yes |
| A_BASE_1 | 0.0000000000 | 0 | 0 | 5025 | 0 | yes |
| A_BASE_2 | 0.0384673178 | 1 | 1 | 5025 | 0 | yes |
| A_CHALLENGER | 0.0016861537 | 1 | 1 | 5025 | 0 | yes |

Best cheap baseline: A_BASE_2.

A_BASE_2 made progress on lf52-271a04aa with per-game RHAE 0.9616829452.  
A_CHALLENGER made progress on lp85-305b61c3 with per-game RHAE 0.0421538426.

Paired challenger-minus-best-baseline RHAE delta:

- mean: -0.0367811641
- 95% bootstrap CI: [-0.1154019534, 0.0050584611]
- repeat deltas: [-0.0367811641, -0.0367811641]
- offline reproducible: yes
- genuine positive edge: no

Therefore the binding decision is KILLED_NO_EDGE.

## Repair decision

No bounded repair was used. Post-run inspection did not identify a concrete, non-game-specific defect that was both absent from the evaluated symbolic agent and sufficiently evidenced to justify reopening the holdout. In particular, the evaluated symbolic implementation already filters candidates through FrameData.available_actions.

## Consequences

Per ORDER-006-P2, because the challenger did not beat the best cheap baseline:

- no ablations;
- no feature growth;
- no offline Kaggle notebook packaging;
- no freeze/parity submission artifact;
- no Kaggle submission;
- no merge.

The symbolic planner remains historical UNPROVEN/KILLED prototype evidence, not a promoted ARC approach.

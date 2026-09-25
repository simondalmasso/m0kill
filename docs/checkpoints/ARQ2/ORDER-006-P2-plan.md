# ORDER-006-P2 ARC Killtest Execution Plan

PROJECT=MONEYKILLER
ROLE_LOCK=ARQ2
BRANCH=arq2/arc-killtest-v1
CANON_ISSUE=https://github.com/simondalmasso/m0kill/issues/2
COST_USD=0

## Contract
- Write only under competitions/arc-agi-3/**, docs/checkpoints/ARQ2/**, docs/handoffs/ARQ2-ARC.md, or .github/workflows/arq2-arc.yml.
- Never mutate main or another ARQ lane. No merge, paid API/GPU, Laya/JEV, Battlecode, or Kaggriculture.
- Treat the migrated symbolic planner, round-robin baseline, and ablation harness as UNPROVEN.
- Do not run starter setup scripts blindly; pin inspected official revisions.
- Do not run ablations, package a Kaggle notebook, or submit unless the challenger first earns PROMOTED.

## Evidence gates
1. A0: record current public rules/runtime facts and separately mark authenticated Kaggle rule acceptance as verified or unverified.
2. TDD contract: tests must first fail against the migrated harness because A_BASE_0/A_BASE_2 and a promotion gate are absent and ablations currently run prematurely.
3. Implement exactly four pre-promotion variants: A_BASE_0 official-equivalent legal random, A_BASE_1 deterministic legal round-robin, A_BASE_2 cheap novelty/information explorer, A_CHALLENGER symbolic planner.
4. Freeze the public/local evaluation corpus before consequential comparison and persist its SHA256.
5. Evaluate every variant with identical game set/action budget. Prefer official scorecard/RHAE when available; also persist levels, games with progress, actions, runtime, errors, repeatability, paired delta and 95% CI.
6. PROMOTE only on genuine, repeatable progress versus the best cheap baseline. Lower action count without progress can never promote.
7. If evidence does not justify promotion, stop with KILLED_NO_EDGE. At most one bounded generic repair is permitted, and only if failure evidence identifies a concrete non-game-specific defect without reusing an already-scored holdout for tuning.
8. Only after PROMOTED: ablations -> regression -> offline notebook <=9h -> artifact parity/hash/scan -> Kaggle run/submission if authenticated account/rules state permits.

## Pinned public runtime inputs
- arc-agi PyPI target: 0.9.9, Python >=3.12.
- Official local-dev starter inspected at eeb1535404f321d280a8f9194bbc1d7aca5f05fc.
- Official ARC-AGI-3-Agents inspected at 4743e7d0aaae0ded0d98a89a7e282e63564cd58b.
- CI compute: CPU only. Final official compute remains Kaggle.

## Stop conditions
- Any attempted write outside owned paths.
- Need for paid compute/API or online evaluated-agent dependency.
- No defensible edge after the permitted bounded-repair policy.
- Kaggle account gate unavailable at submission stage: preserve PROMOTED evidence but report SUBMISSION_BLOCKED_ACCOUNT instead of guessing.

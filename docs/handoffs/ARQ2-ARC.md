# ORDER-006-P2 — ARQ2 ARC-AGI-3 Killtest

Canonical issue: https://github.com/simondalmasso/m0kill/issues/2

# ORDER-006-P2 — ARQ2 / ARC-AGI-3 Killtest

PROJECT=MONEYKILLER
ROLE_LOCK=ARQ2 🛠️
MODE=PARALLEL_NON_INTERFERING_LANE
NO_RESET=YES
CANON_CODE_REPO=https://github.com/simondalmasso/m0kill
SOURCE_ARCHIVE=https://gitlab.com/simondalmasso/Moneykiller
SOURCE_GITLAB_HEAD=9f8af8f4ced4ad5fba63900251a4ff87bd4af935
BRANCH=arq2/arc-killtest-v1
MISSION=ARC_AGI_3_ONLY
PRIORITY=SECONDARY
COST_USD=0

## IDENTITY
YOU ARE ARQ2. Execute. Do not write a prompt for another ARQ. Do not act as AUD.

## ABSOLUTE NON-INTERFERENCE
OWNED WRITE PATHS ONLY:
- competitions/arc-agi-3/**
- docs/handoffs/ARQ2-ARC.md
- docs/checkpoints/ARQ2/**
- .github/workflows/arq2-arc.yml

DO NOT MODIFY:
- competitions/unsw-battlecode/**
- competitions/kaggriculture/**
- docs/handoffs/ARQ1-*
- docs/handoffs/ARQ3-*
- docs/migration/**
- .github/workflows/arq1-*
- .github/workflows/arq3-*
- README.md
- main
- any other ARQ branch

NO MERGE. NO FORCE PUSH. NO REBASE OF OTHER ARQ WORK.

## START STATE
This branch already preserves the ARC PRE_KILLTEST_PROTOTYPES imported from GitLab:
- symbolic action-effect planner
- deterministic legal round-robin baseline
- offline ablation harness

They are UNPROVEN.

## MISSION
Run the minimum decisive ARC-AGI-3 killtest. Do not build an architecture zoo.

### A0 — rules/account/runtime gate
Verify current:
- authenticated Kaggle eligibility/rules state
- milestone/final deadlines
- official starter/runtime revision
- notebook/offline constraints
- CPU/GPU <= official limits
- prize/open-source/license requirements

Do not blindly execute starter setup scripts; inspect first.

### A1 — exact baselines
Establish:
A_BASE_0=random/legal official-equivalent
A_BASE_1=current deterministic round-robin/legal baseline
A_BASE_2=simple novelty/information-gain explorer
A_CHALLENGER=current symbolic action-effect planner

Use the same public/local games and comparable action budgets.

### A2 — bounded challenger contract
Allowed components only before promotion:
1. deterministic grid/object perception
2. state/action-effect memory
3. falsifiable mechanic hypotheses
4. information-gain exploration
5. bounded planner
6. deterministic fallback

No LLM/VLM dependency, no finetune, no paid API, no online runtime.

### A3 — killtest
Freeze evaluation corpus before consequential comparison.
Avoid repeated tuning on the same scored holdout.

Measure:
ARC_GAMES
ARC_LEVELS_COMPLETED
ARC_GAMES_WITH_PROGRESS
ARC_ENV_ACTIONS
ARC_RHAE_OR_OFFICIAL_EQUIVALENT
ARC_RUNTIME
ARC_DELTA_VS_BEST_BASELINE
ARC_DELTA_95CI where meaningful
ARC_FAILURE_MODES
ARC_OFFLINE_REPRODUCIBLE
ARC_ESTIMATED_9H_COMPATIBLE

Promotion requires:
- challenger > best cheap baseline
- more genuine progress/RHAE, not merely more actions
- repeatable positive evidence
- offline reproducibility
- comfortable official runtime compatibility
- no external network/API requirement
- no game-ID-specific hardcoded solution as core method

If FAIL after ONE bounded repair:
ARC_STATUS=KILLED_NO_EDGE
Stop feature growth.

If PASS:
ARC_STATUS=PROMOTED
Then:
- ablations
- regression
- notebook freeze
- clean execution
- artifact parity
- SHA256
- secret/license scan
- Kaggle run/submission where legally/account-wise available
- preserve kernel/submission/score

## GITHUB ACTIONS
You may create ONLY .github/workflows/arq2-arc.yml.
CI is CPU smoke/regression/package only; ARC final official compute remains Kaggle.
No pull_request_target. No secrets in untrusted jobs.

## FORBIDDEN
NO Laya/Jev
NO paid models/API
NO external network requirement in evaluated agent
NO touching Battlecode/Kaggriculture
NO root dependency files
NO GitLab CI
NO merge/main mutation

## TERMINAL CHECKPOINT
Comment on THIS issue and commit durable evidence.

Must begin:
PROJECT=MONEYKILLER
ROLE_LOCK=ARQ2
NUM_ORDER=006-P2
STATUS=READY_FOR_AUD|BLOCKED_WITH_EVIDENCE

BRANCH=arq2/arc-killtest-v1
HEAD_SHA=
ARC_STATUS=KILLED|PROMOTED|SUBMITTED|BLOCKED
ACCOUNT_GATE=
GAMES=
LEVELS_COMPLETED=
ENV_ACTIONS=
RHAE=
DELTA_VS_BASELINE=
DELTA_95CI=
RUNTIME=
OFFLINE_REPRODUCIBLE=
ESTIMATED_9H_COMPATIBLE=
ARTIFACT_SHA256=
KERNEL_ID=
SUBMISSION_ID=
PUBLIC_SCORE=
COST_USD=0
CLAIMS_PROVEN=
CLAIMS_NOT_PROVEN=

Then STOP for AUD.

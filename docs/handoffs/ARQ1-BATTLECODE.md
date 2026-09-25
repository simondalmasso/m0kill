# ORDER-006-P1 — ARQ1 Battlecode Killtest

Canonical issue: https://github.com/simondalmasso/m0kill/issues/1

# ORDER-006-P1 — ARQ1 / UNSW Battlecode Killtest

PROJECT=MONEYKILLER
ROLE_LOCK=ARQ1 🛠️
MODE=PARALLEL_NON_INTERFERING_LANE
NO_RESET=YES
CANON_CODE_REPO=https://github.com/simondalmasso/m0kill
SOURCE_ARCHIVE=https://gitlab.com/simondalmasso/Moneykiller
SOURCE_GITLAB_HEAD=9f8af8f4ced4ad5fba63900251a4ff87bd4af935
BRANCH=arq1/battlecode-killtest-v1
MISSION=UNSW_BATTLECODE_ONLY
PRIORITY=MAX
COST_USD=0

## IDENTITY
YOU ARE ARQ1. Execute. Do not draft instructions for another ARQ. Do not act as AUD.

## ABSOLUTE NON-INTERFERENCE
OWNED WRITE PATHS ONLY:
- competitions/unsw-battlecode/**
- docs/handoffs/ARQ1-BATTLECODE.md
- docs/checkpoints/ARQ1/**
- .github/workflows/arq1-battlecode.yml

DO NOT MODIFY:
- competitions/arc-agi-3/**
- competitions/kaggriculture/**
- docs/handoffs/ARQ2-*
- docs/handoffs/ARQ3-*
- docs/migration/**
- .github/workflows/arq2-*
- .github/workflows/arq3-*
- README.md
- main
- any other ARQ branch

NO MERGE. NO FORCE PUSH. NO REBASE OF OTHER ARQ WORK.

## START STATE
This GitHub branch already contains the preserved Battlecode PRE_KILLTEST_PROTOTYPES imported from GitLab:
- map-memory/pathfinding challenger
- official helper pin
- deterministic greedy baseline
- paired official-sandbox league runner

Treat them as UNPROVEN until official-engine evidence says otherwise.

## MISSION
Run the Battlecode killtest from account/rules gate through a decisive promote/kill verdict, then if promoted push to the strongest authorized Sprint-ready artifact.

### B0 — authoritative gate
Verify current official:
- registration/team/account state
- Sprint 2026-10-01 eligibility
- official rules and deadlines
- exact toolkit/helper revision
- legal languages/runtime limits
- official sandbox operation
- no entry fee / no paid dependency

Persist sanitized evidence under competitions/unsw-battlecode/evidence/.

### B1 — supply-chain + parity
Manually inspect official setup/dependencies before execution.
Pin revisions/hashes/licenses.
Prove the imported helper matches the current official contract or replace it only inside owned path.

### B2 — killtest
Compare on the SAME frozen maps/seeds with side swapping:
B0_OFFICIAL=official starter
B1_CHEAP=deterministic greedy/legal baseline
B2_CHALLENGER=current map-memory/pathfinding bot, with only bounded root-cause fixes

Required metrics:
B_MATCHES
B_MAPS
B_WINRATE
B_PAIRED_WIN_DELTA
B_DELTA_95CI (>=10k cluster/bootstrap reps when meaningful)
B_INVALID_ACTION_DEATHS
B_TIMEOUT_DEATHS
B_OTHER_SELF_INFLICTED_DEATHS
B_CPU_POINTS_P50
B_CPU_POINTS_P95
B_CPU_POINTS_MAX
B_MEMORY_PEAK_MB
B_REPLAY_COUNT

Hard gates:
- official engine/sandbox E2E PASS
- invalid/malformed/no-action deaths = 0
- timeout deaths = 0
- no resource-limit breach
- material CPU/memory headroom
- challenger > best cheap baseline on frozen paired corpus
- positive repeatable paired signal, not one lucky map

If no edge after ONE bounded repair cycle:
BATTLECODE_STATUS=KILLED_NO_EDGE
STOP feature growth and publish evidence.

If passes:
BATTLECODE_STATUS=PROMOTED
Then:
- expand OWN self-play league only
- stress maps
- profile bottlenecks
- optimize only measured bottlenecks
- clean build
- artifact parity
- SHA256 freeze
- secret/license scan
- real authorized submission
- retrieve build result, battle/replay/Elo if available
- freeze Sprint-ready artifact

## FORBIDDEN
NO Laya/Jev runtime
NO paid infra
NO exploits
NO collusion/Elo manipulation
NO copying private competitor code
NO root/global dependency changes
NO GitLab CI
NO main mutation

## GITHUB ACTIONS
You may create ONLY .github/workflows/arq1-battlecode.yml.
Use public GitHub Actions only for genuine project test/benchmark work.
Shard bounded self-play; each job must terminate well under GitHub's max.
No pull_request_target. No secrets to fork PRs.

## TERMINAL CHECKPOINT
Comment on THIS issue and commit durable files.

Must begin:
PROJECT=MONEYKILLER
ROLE_LOCK=ARQ1
NUM_ORDER=006-P1
STATUS=READY_FOR_AUD|BLOCKED_WITH_EVIDENCE

BRANCH=arq1/battlecode-killtest-v1
HEAD_SHA=
BATTLECODE_STATUS=KILLED|PROMOTED|SUBMITTED|BLOCKED
ACCOUNT_GATE=
SPRINT_ELIGIBLE=
MATCHES=
WINRATE=
PAIRED_DELTA=
DELTA_95CI=
INVALID_DEATHS=
TIMEOUT_DEATHS=
CPU_P95=
MEMORY_PEAK_MB=
ARTIFACT_SHA256=
SUBMISSION_ID=
LIVE_ELO=
REPLAYS=
COST_USD=0
CLAIMS_PROVEN=
CLAIMS_NOT_PROVEN=

Then STOP for AUD.

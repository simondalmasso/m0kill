# ORDER-006-P3 — ARQ3 Migration/CI + Kaggriculture Gate

Canonical issue: https://github.com/simondalmasso/m0kill/issues/3

# ORDER-006-P3 — ARQ3 / GitHub Migration + CI Plane + Kaggriculture Gate

PROJECT=MONEYKILLER
ROLE_LOCK=ARQ3 🛠️
MODE=PARALLEL_NON_INTERFERING_LANE
NO_RESET=YES
CANON_CODE_REPO=https://github.com/simondalmasso/m0kill
SOURCE_ARCHIVE=https://gitlab.com/simondalmasso/Moneykiller
SOURCE_GITLAB_HEAD=9f8af8f4ced4ad5fba63900251a4ff87bd4af935
BRANCH=arq3/platform-kaggriculture-v1
MISSION=PLATFORM_MIGRATION_PLUS_KAGGRICULTURE_GATE
COST_USD=0

## IDENTITY
YOU ARE ARQ3. Execute. You are not AUD and not the integrator of ARQ1/ARQ2 code.

## ABSOLUTE NON-INTERFERENCE
OWNED WRITE PATHS ONLY:
- competitions/kaggriculture/**
- docs/migration/**
- docs/handoffs/ARQ3-PLATFORM-KAGGRICULTURE.md
- docs/checkpoints/ARQ3/**
- .github/workflows/arq3-platform.yml
- .github/workflows/README.md

DO NOT MODIFY:
- competitions/unsw-battlecode/**
- competitions/arc-agi-3/**
- .github/workflows/arq1-*
- .github/workflows/arq2-*
- docs/handoffs/ARQ1-*
- docs/handoffs/ARQ2-*
- README.md
- main
- ARQ1/ARQ2 branches

NO MERGE. NO FORCE PUSH. NO REBASE OF OTHER ARQ WORK.

## MISSION A — migration truth
GitHub m0kill is the NEW code/compute plane from this order forward.
GitLab remains historical evidence/archive until AUD final cutover.

Verify and document:
- GitHub repo public/admin state
- GitLab source project/ref provenance
- GitHub main contains imported GitLab main snapshot marker
- ARQ1/ARQ2/ARQ3 branch existence
- exact source GitLab HEAD from which lane prototypes were imported
- no claim that Git SHAs are preserved: this migration is snapshot/provenance, not a full object-level mirror

Create docs/migration/MIGRATION-MANIFEST.md with explicit provenance and branch map.

Do not rewrite GitLab history.

## MISSION B — GitHub compute plane
Design minimal public Actions conventions:
- genuine software testing/benchmarking only
- bounded jobs/shards
- deterministic artifact naming
- caches only when reproducible
- no pull_request_target
- no secret exposure to fork jobs
- no arbitrary compute farming
- no paid runners

Create only arq3-platform.yml for migration verification / lightweight repo integrity.
Do not create workflows owned by ARQ1/ARQ2.

Document exact recipe ARQ1/ARQ2 should follow in .github/workflows/README.md without editing their workflow files.

## MISSION C — Kaggriculture HARD gate
FIRST determine with existing authenticated Kaggle account:

KAGGRICULTURE_RULES_ACCEPTED_BEFORE_2026-09-23T23:59Z=YES|NO|INDET
KAGGRICULTURE_CAN_CURRENTLY_SUBMIT=YES|NO
KAGGRICULTURE_TEAM_STATE=
KAGGRICULTURE_ACCOUNT_EVIDENCE=

NO alternate accounts.
NO retroactive acceptance.
NO identity tricks.
NO bypass.

If NO:
KAGGRICULTURE_STATUS=KILLED_ENTRY
Persist evidence. No agent build.

If YES:
run ONLY a bounded killtest:
- official contract parser
- minimal legal bot
- official environment/simulator parity
- cheap deterministic economic heuristic
- paired frozen seeds vs minimal/official baseline
- terminal bank delta + winrate + legality + runtime
- >=10k cluster/bootstrap reps when meaningful

Promotion only with reproducible positive edge.
Else KILLED_NO_EDGE.

If promoted, stop at PROMOTE_TO_BUILD unless AUD explicitly reallocates more work; do not steal ARQ1/ARQ2 capacity.

## MIGRATION QUALITY GATES
- provenance manifest
- public repo confirmed
- branch isolation confirmed
- no credentials committed
- GitHub main not used for lane work
- GitLab source archive URLs preserved
- no false claim of full Git object mirror
- CI smoke on own workflow if available and terminal result retrieved

## FORBIDDEN
NO Battlecode code
NO ARC code
NO changing other ARQ workflows
NO merging branches
NO paid CI/GPU
NO account circumvention
NO main mutation

## TERMINAL CHECKPOINT
Comment on THIS issue.

Must begin:
PROJECT=MONEYKILLER
ROLE_LOCK=ARQ3
NUM_ORDER=006-P3
STATUS=READY_FOR_AUD|BLOCKED_WITH_EVIDENCE

BRANCH=arq3/platform-kaggriculture-v1
HEAD_SHA=
MIGRATION_STATUS=
PROVENANCE_MANIFEST=
GITHUB_PUBLIC=
BRANCH_ISOLATION=
CI_SMOKE=
KAGGRICULTURE_STATUS=KILLED_ENTRY|KILLED_NO_EDGE|PROMOTED|BLOCKED
KAGGRICULTURE_ACCOUNT_GATE=
KAGGRICULTURE_CAN_SUBMIT=
KAGGRICULTURE_EDGE=
COST_USD=0
CLAIMS_PROVEN=
CLAIMS_NOT_PROVEN=

Then STOP for AUD.

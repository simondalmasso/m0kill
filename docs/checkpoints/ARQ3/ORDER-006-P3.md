# ORDER-006-P3 — ARQ3 terminal evidence checkpoint

PROJECT=MONEYKILLER
ROLE_LOCK=ARQ3
NUM_ORDER=006-P3
STATUS=BLOCKED_WITH_EVIDENCE
BRANCH=arq3/platform-kaggriculture-v1
EVIDENCE_FREEZE_SHA=abdaa621b4386e3ff468c93d367f965ab37d6c95

## Migration / compute plane

MIGRATION_STATUS=SNAPSHOT_PROVENANCE_VERIFIED
PROVENANCE_MANIFEST=docs/migration/MIGRATION-MANIFEST.md
GITHUB_PUBLIC=YES
GITHUB_ADMIN_AT_INSPECTION=YES
GITLAB_ARCHIVE=https://gitlab.com/simondalmasso/Moneykiller
GITLAB_MAIN_SNAPSHOT=4a4df6d3095901d1dd833a3be8ea0ee38b91c547
GITLAB_PROTOTYPE_SOURCE=lab/mk-prize-agents-v1@9f8af8f4ced4ad5fba63900251a4ff87bd4af935
GITHUB_MAIN_IMPORT_MARKER=6a767dbb24bf8137115cae19656874a607f569d4
MIRROR_1_TO_1_CLAIM=NO
BRANCH_ISOLATION=PASS_AT_EVIDENCE_FREEZE

## GitHub Actions smoke

CI_WORKFLOW=.github/workflows/arq3-platform.yml
CI_RUN=https://github.com/simondalmasso/m0kill/actions/runs/36183996126
CI_HEAD=abdaa621b4386e3ff468c93d367f965ab37d6c95
CI_SMOKE=PASS
CI_JOB=integrity
CI_STEPS=checkout; lane isolation; provenance markers; credential-like filename check; deterministic artifact; upload
CI_ARTIFACT=arq3-platform-abdaa621b4386e3ff468c93d367f965ab37d6c95
CI_ARTIFACT_DIGEST=sha256:f1f0a7cac81a0e6f97faee465d867afd51c14f76a1468f07792b27a8f28b2337
COST_USD=0

## Kaggriculture hard gate

OFFICIAL_TIMELINE=https://www.kaggle.com/competitions/kaggriculture/overview/citation
ENTRY_DEADLINE=2026-09-23T23:59:00Z
FINAL_SUBMISSION_DEADLINE=2026-09-30T23:59:00Z
KAGGLE_ACCOUNT_HANDLE=simondalmasso
KAGGRICULTURE_RULES_ACCEPTED_BEFORE_2026-09-23T23:59Z=INDET
KAGGRICULTURE_CAN_CURRENTLY_SUBMIT=INDET
KAGGRICULTURE_TEAM_STATE=INDET
KAGGRICULTURE_STATUS=BLOCKED
KAGGRICULTURE_EDGE=NOT_RUN_ACCOUNT_GATE_BLOCKED

Account existence before the deadline is supported by historical Kaggle notebook identities and a Kaggle notification dated 2026-09-21. No available authenticated surface proved or disproved Kaggriculture-specific rules acceptance before the deadline.

Authenticated-read blockers:
- Opera Browser Connector was not connected.
- Registered Remote Desktop Commander device was offline, so the existing Kaggle CLI credential could not be queried.
- No Kaggle-specific ChatGPT connector was available.

No rule acceptance, join action, alternate account, submission, agent build, parser, simulator harness, heuristic, or economic killtest was performed.

## Claims proven

- GitHub m0kill is public and ARQ3 had admin repository permission at inspection.
- GitHub main carries an explicit GitLab main snapshot marker.
- GitLab source provenance is pinned to exact refs.
- Ten migrated Battlecode/ARC prototype files were byte-for-byte equal to their GitLab source-ref counterparts at inspection.
- Migration is snapshot/provenance, not a full Git object mirror.
- ARQ3 platform workflow passed on its exact head and produced a deterministic artifact.
- ARQ3 did not authorize Kaggriculture development without an account-gate result.

## Claims not proven

- Kaggriculture rules were accepted before the entry deadline.
- The existing account can currently submit to Kaggriculture.
- Kaggriculture team membership/state.
- Any Kaggriculture economic edge, win rate, bank delta, legality, or runtime advantage.

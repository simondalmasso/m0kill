# AUD_CANON

PROJECT=MONEYKILLER / m0kill
PURPOSE=Find legitimate USD0 prize opportunities where autonomous agents are explicitly allowed; kill weak approaches early and preserve auditable evidence.
REPO=https://github.com/simondalmasso/m0kill
LIVE=GitHub is the active code/compute plane. GitLab is historical evidence/archive and mirror target.
LAST_VERIFIED=2026-09-26T02:03:14Z
BRANCH=arq1/battlecode-killtest-v1
HEAD=8c63f4264ea0b94e1e39f0a8c82c8584c521158d

## CANONICAL LINKS
- Active ARQ order: https://github.com/simondalmasso/m0kill/issues/1
- ARC closed evidence: https://github.com/simondalmasso/m0kill/issues/2
- Migration/Kaggriculture closed evidence: https://github.com/simondalmasso/m0kill/issues/3
- Latest decisive ARC run: https://github.com/simondalmasso/m0kill/actions/runs/36210113478
- Historical GitLab project: https://gitlab.com/simondalmasso/Moneykiller
- Historical master Work Item: https://gitlab.com/simondalmasso/Moneykiller/-/work_items/5

## CURRENT STATE
- SINGLE_ARQ_MODE=YES. Parallel ARQ1/2/3 execution is retired.
- Active lane=UNSW Battlecode. Sprint is 2026-10-01, online, open to all entrants; official site currently shows AUD 800/AUD 400 prizes.
- Battlecode GitHub branch contains imported pre-killtest prototype: map memory/pathfinding challenger, greedy baseline, pinned helper and paired league runner. It is UNPROVEN on GitHub until official account/toolkit/sandbox killtest is executed.
- ARC-AGI-3 is KILLED_NO_EDGE under current canon. Latest repeat at HEAD aac9c17791d4ae2c3a5c8a54495c4814f2db15bc reproduced the same verdict.
- Kaggriculture account gate remains INDET; no economic killtest was authorized.
- No PRs exist. main is not an integration branch for active lane work.

## DONE
- GitLab→GitHub active cutover established as snapshot/provenance migration.
- GitHub public repo and isolated lane branches verified.
- ARQ3 migration CI smoke passed.
- ARC frozen public/offline killtest completed twice consistently:
  - best baseline A_BASE_2 RHAE=0.03846731780616078
  - challenger RHAE=0.0016861537025368155
  - delta=-0.03678116410362396
  - CI95=[-0.11540195341848233,0.005058461107610447]
  - decision=KILLED_NO_EDGE
- Issues #2 and #3 closed as completed evidence lanes.

## ACTIVE WORK
- Issue #1 only: Battlecode account/rules/toolkit gate → official sandbox parity → starter/cheap/challenger paired killtest → KILL or PROMOTE → submit only if promoted.

## PENDING
- Verify Battlecode registration/team/account and Sprint eligibility.
- Execute official-engine paired Battlecode corpus with resource/death metrics.
- Resolve Kaggriculture authenticated account gate only if AUD later reopens it.
- GitHub→GitLab mirror workflow is configured; activate it by adding repository secret `GITLAB_MIRROR_TOKEN` with GitLab `write_repository` scope, then rerun the workflow.

## BLOCKERS/RISKS
- Kaggriculture rules-acceptance state before its entry deadline is not proven.
- Current GitHub migration is content/provenance snapshot, not a 1:1 historical Git-object mirror.
- Mirror workflow `.github/workflows/mirror-gitlab.yml` exists and was smoke-tested at run https://github.com/simondalmasso/m0kill/actions/runs/36210449154. It fails closed because `GITLAB_MIRROR_TOKEN` is absent. Connector access cannot create GitHub Actions secrets directly.

## DO_NOT_TOUCH
- Do not reopen ARC without explicit AUD authority.
- Do not build Kaggriculture while account gate is INDET.
- No Laya/JEV model chasing, Trenches, SOL/wallet/capital, paid infra, exploit/anti-cheat work.
- No force-push/rebase/history rewrite.
- No active work on main.
- Preserve arq2/arc-killtest-v1 and arq3/platform-kaggriculture-v1 as evidence.

## AUTHORITIES/GATES
VERIFY>ASSUME; EVIDENCE>CLAIM; CURRENT_STATE>HISTORY; PRESERVE>REBUILD.
Official engine/account evidence outranks summaries.
CI_GREEN!=DONE.
A lane promotes only on legal E2E + resource safety + positive evidence vs best cheap baseline.
AUD alone may reopen a killed lane or approve merge/canon changes.

## MIRROR STATUS
- CONFIGURED=YES
- LIVE=NO_MISSING_SECRET
- POLICY=non-destructive: GitHub branch `X` → GitLab branch `github/X`; historical GitLab refs are never overwritten or deleted.
- SMOKE_RUN=https://github.com/simondalmasso/m0kill/actions/runs/36210449154

## NEXT EXACT ACTION
Audit Battlecode from Issue #1 on arq1/battlecode-killtest-v1: resolve account/Sprint gate, pin/audit official toolkit, run the frozen paired official-sandbox killtest, and produce KILLED_NO_EDGE or PROMOTED/SUBMITTED with raw evidence.

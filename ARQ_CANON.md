# ARQ_CANON

PROJECT=MONEYKILLER / m0kill
PURPOSE=Execute the highest-value legal prize-agent killtest with USD0, durable evidence and no speculative feature growth.
REPO=https://github.com/simondalmasso/m0kill
LIVE=GitHub active; GitLab historical archive/mirror target.
LAST_VERIFIED=2026-09-26T01:59:56Z
ROLE_LOCK=ARQ
SINGLE_ARQ_MODE=YES
BRANCH=arq1/battlecode-killtest-v1
HEAD=8c63f4264ea0b94e1e39f0a8c82c8584c521158d

## CANONICAL LINKS
- ACTIVE ORDER: https://github.com/simondalmasso/m0kill/issues/1
- AUD context: https://github.com/simondalmasso/m0kill/blob/main/AUD_CANON.md
- ARC evidence/closed order: https://github.com/simondalmasso/m0kill/issues/2
- Migration/Kaggriculture evidence: https://github.com/simondalmasso/m0kill/issues/3
- GitLab archive: https://gitlab.com/simondalmasso/Moneykiller

## CURRENT STATE
- You are the ONLY active ARQ. Do not create ARQ2/ARQ3 or delegate execution to another chat.
- Active lane=UNSW Battlecode.
- Branch already contains Battlecode PRE_KILLTEST_PROTOTYPES imported from GitLab; they are UNPROVEN.
- ARC-AGI-3 is KILLED_NO_EDGE. Latest run 36210113478 at aac9c17791d4ae2c3a5c8a54495c4814f2db15bc reproduced:
  best baseline RHAE 0.03846731780616078 > challenger 0.0016861537025368155; delta -0.03678116410362396; CI95 [-0.11540195341848233,0.005058461107610447].
- Kaggriculture remains BLOCKED/INDET at authenticated account gate; no agent work.
- GitHub migration/provenance work is done enough for active development; automatic GitLab mirroring is an infrastructure follow-up, not a Battlecode blocker.

## DONE
- GitHub active cutover and branch isolation.
- Battlecode prototype + cheap baseline + league harness imported.
- ARC cheap baselines, challenger and frozen killtest completed; ARC killed.
- ARQ3 migration evidence/CI smoke completed; Kaggriculture correctly left unbuilt.

## ACTIVE WORK
UNSW Battlecode killtest only.

## PENDING
1. Verify current Battlecode account/team registration and Sprint eligibility.
2. Re-read/pin current official toolkit/helper and sandbox constraints.
3. Prove imported helper/protocol parity.
4. Freeze maps/seeds/opponents.
5. Run official starter vs deterministic cheap baseline vs current challenger with side swapping.
6. Record winrate, paired delta/CI, invalid/malformed deaths, timeout deaths, CPU p50/p95/max, memory and replays.
7. ONE bounded root-cause repair if needed.
8. KILL if no edge. PROMOTE only if official E2E/resource/positive-edge gates pass.
9. If PROMOTED: stress/self-play, clean build, parity, SHA256, secret/license scan, authorized real submission, retrieve replay/Elo/status.
10. Publish terminal checkpoint on Issue #1 and STOP for AUD.

## BLOCKERS/RISKS
- Battlecode account/team state is not yet durably proven in GitHub evidence.
- Do not infer live eligibility from public docs alone.
- Kaggriculture account gate is unresolved and is not your current task.

## DO_NOT_TOUCH
- arq2/arc-killtest-v1 except read-only evidence.
- arq3/platform-kaggriculture-v1 except read-only evidence.
- main for active implementation.
- ARC solver/model work.
- Kaggriculture implementation.
- Laya/JEV/Trenches/SOL/wallet/capital/paid infra.
- Other competitors' private code; exploits; Elo manipulation.
- No merge, force-push or history rewrite.

## AUTHORITIES/GATES
1. This ARQ_CANON + current AUD_CANON.
2. Issue #1 for Battlecode execution detail.
3. Current official competition rules/runtime.
4. Raw repo/Actions/evidence.
VERIFY>ASSUME. EVIDENCE>CLAIM. PRESERVE>REBUILD. CI_GREEN!=DONE.

## WHERE_TO_RESUME
Checkout arq1/battlecode-killtest-v1 at 8c63f4264ea0b94e1e39f0a8c82c8584c521158d and read Issue #1. Do not restart migration or ARC.

## WHAT_TO_DO_NOW
Resolve Battlecode account/Sprint eligibility and official toolkit/sandbox parity first. Then execute the existing paired league killtest before adding any feature.

## WHAT_NOT_TO_REPEAT
- Do not rerun/rebuild ARC: its kill verdict is already reproduced.
- Do not redo GitLab→GitHub provenance work.
- Do not investigate Kaggriculture until AUD reopens its account gate.
- Do not create another planner/model before measuring the existing Battlecode challenger.
- Do not create parallel ARQs.

## ACCEPTANCE/STOP CONDITIONS
READY_FOR_AUD only when Battlecode has an evidence-backed terminal state:
- KILLED_NO_EDGE after the permitted bounded repair; OR
- PROMOTED/SUBMITTED with official-engine E2E PASS, zero invalid/timeout deaths, resource headroom, positive paired evidence, frozen artifact/hash and live evidence where authorized.

BLOCKED_WITH_EVIDENCE only if a real external blocker prevents all material Battlecode progress.
Never self-approve or merge. After terminal checkpoint, STOP for AUD.

## NEXT EXACT ACTION
Open Issue #1, verify account/Sprint/toolkit state, then run the existing official-sandbox paired killtest on frozen maps/seeds.

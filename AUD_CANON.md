# AUD_CANON

PROJECT=MONEYKILLER / m0kill
PURPOSE=Find legitimate USD0 prize/creator opportunities, prove payout/eligibility first, kill weak paths early, and preserve auditable evidence.
REPO=https://github.com/simondalmasso/m0kill
LIVE=GitHub is canonical code/compute. GitLab is historical archive plus non-destructive mirror target.
LAST_VERIFIED=2026-10-01T04:28:39-03:00
BRANCH=main
HEAD=02ca396f6f35a6945d37ff53537868c7ef57cf69

## CANONICAL LINKS
- GitHub: https://github.com/simondalmasso/m0kill
- Battlecode closed order: https://github.com/simondalmasso/m0kill/issues/1
- ARC closed order: https://github.com/simondalmasso/m0kill/issues/2
- Migration/Kaggriculture closed order: https://github.com/simondalmasso/m0kill/issues/3
- GitLab mirror/archive: https://gitlab.com/simondalmasso/Moneykiller
- Battlecode official updates: https://game.battlecode.au/updates
- Pocket Vector bounty: https://www.bountyboard.gg/bounty/one-short-about-pocket-vector

## CURRENT STATE
- SINGLE_ARQ_MODE=YES. No parallel ARQs.
- Battlecode Sprint path is CLOSED: submissions froze 2026-10-01 09:00 AEST before MONEYKILLER produced account-gate/official-killtest/submission evidence.
- ARC-AGI-3=KILLED_NO_EDGE. Reproduced frozen result: best cheap baseline RHAE 0.03846731780616078 vs challenger 0.0016861537025368155; delta -0.03678116410362396; CI95 [-0.11540195341848233,0.005058461107610447].
- Kaggriculture=BLOCKED_ACCOUNT_GATE_INDET; no build authorized.
- Pocket Vector bounty is live but does NOT pass the existing >=USD20 net filter: listed $20 per approved short minus Bounty Board standard 10% creator fee = $18 net before any FX/tax/Stripe effects. No explicit AI-assistance ban was found in the campaign brief/Terms; authenticity/originality and paid-content disclosure still apply.
- Bounty Board itself shows real payout history ($4.3K+ paid to 24 creators), but Pocket Vector studio has 0 creators paid so far.
- GitHub->GitLab mirror is autonomous and current. GitHub main and GitLab github/main were verified equal at 02ca396f6f35a6945d37ff53537868c7ef57cf69.

## DONE
- GitLab->GitHub active cutover and branch provenance.
- Autonomous mirror configured outside ChatGPT connectors: Windows Task Scheduler task MONEYKILLER-GitHub-to-GitLab-Mirror runs every 15 minutes and pushes GitHub branch X to GitLab github/X without overwriting historical GitLab refs.
- ARC killtest completed and killed.
- Battlecode Sprint lane closed as KILLED_EXTERNAL_DEADLINE, performance not established.
- Pocket Vector bounty researched against campaign, Terms/FAQ, studio profile and platform payout evidence.

## ACTIVE WORK
- No implementation lane is currently promoted.
- AUD discovery gate only: identify the next opportunity that is legal, currently enterable, payout-verifiable and >=USD20 NET.

## PENDING
- Find next live candidate with >=USD20 net payout after platform fees and a payout route actually usable by the user.
- If revisiting Bounty Board, listed reward must be >=USD22.23 to clear a 10% creator fee and still net >=USD20, before FX/tax.
- Kaggriculture can only reopen if authenticated evidence proves valid prior entry and current submit access.

## BLOCKERS/RISKS
- Pocket Vector: net payout is $18 under standard fee; creator payout method/Argentina-specific onboarding remains account-specific.
- Battlecode Grand Final eligibility is restricted; MONEYKILLER has no durable evidence establishing eligibility.
- Local scheduled mirror requires the Windows host/account to be available; cloud fallback exists but is manual-only without a GitHub secret.

## DO_NOT_TOUCH
- Do not reopen ARC without explicit AUD authority.
- Do not resume Battlecode Sprint work; deadline path is closed.
- Do not build Kaggriculture while account gate is INDET.
- No Laya/JEV model chasing, Trenches, SOL/wallet/capital, paid infra, exploit/anti-cheat work.
- No force-push/rebase/history rewrite.
- Preserve closed lane branches as evidence.

## AUTHORITIES/GATES
VERIFY>ASSUME. EVIDENCE>CLAIM. CURRENT_STATE>HISTORY. PRESERVE>REBUILD.
Official rules/account/payment evidence outranks summaries.
CI_GREEN!=DONE.
Promotion requires legal entry + usable payout + >=USD20 net + measured edge where a technical competition is involved.
AUD alone reopens killed lanes or authorizes a new implementation order.

## NEXT EXACT ACTION
Research current live opportunities and promote only one that proves: enterable now, legitimate payout, user-compatible payout rail, >=USD20 net after known platform fees, and bots/AI/automation allowed where automation is part of the task.

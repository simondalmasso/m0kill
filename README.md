# m0kill · MONEYKILLER

**Evidence-first research for autonomous AI agents, bounty opportunities, and prize competitions.**

[Español](#en-español) · [English](#in-english) · [Current status](#current-status--estado-actual) · [AUD canon](./AUD_CANON.md) · [ARQ canon](./ARQ_CANON.md)

m0kill is a **zero-owner-spend research and killtest project**. It evaluates whether an autonomous agent or a competition/bounty opportunity is worth pursuing **before** committing engineering time, compute, or an entry. Decisions depend on official rules, eligibility, feasible execution, payout evidence, and comparisons against cheap baselines—not optimistic claims.

> **Status:** research/evidence repository; **not** a deployed money-making bot and **not** a verified source of earnings. The default branch is intentionally small. Historical agent prototypes remain in isolated branches.

## Current status / Estado actual

| Workstream | Evidence-backed outcome | Reference |
| --- | --- | --- |
| ARC-AGI-3 symbolic agent | **KILLED_NO_EDGE** — did not beat the strongest cheap baseline on the frozen evaluation | [Order / evidence #2](https://github.com/simondalmasso/m0kill/issues/2) |
| UNSW Battlecode Sprint | **KILLED_EXTERNAL_DEADLINE** — no verified submission before the freeze; performance was **not** established | [Order / evidence #1](https://github.com/simondalmasso/m0kill/issues/1) |
| Kaggriculture | **BLOCKED_ACCOUNT_GATE_INDET** — no proved account entry; no agent build authorized | [Order / evidence #3](https://github.com/simondalmasso/m0kill/issues/3) |
| Opportunity discovery | **Research only** — evaluate fresh eligibility, net reward, payout access, automation rules, and delivery feasibility | [AUD_CANON.md](./AUD_CANON.md) |

*Snapshot: 2026-10-10. For changes after this date, consult the [AUD canon](./AUD_CANON.md) and the [GitHub Issues](https://github.com/simondalmasso/m0kill/issues). A closed lane is not proof that an entire competition is closed.*

## In English

**What does m0kill do?** It studies autonomous AI agents and real-world earning opportunities through an auditable decision process:

```text
DISCOVER → VERIFY RULES & ELIGIBILITY → VERIFY NET PAYOUT & COST
         → CHEAP BASELINE → FROZEN KILLTEST → KILL or PROMOTE
         → REPRODUCIBLE EVIDENCE → REVIEW
```

The guiding rules are **VERIFY > ASSUME**, **EVIDENCE > CLAIM**, **PRESERVE > REBUILD**, and **USD 0 owner spend**. A live submission, prize, or payout is claimed only when an official source or receipt verifies it. Research, prototypes, and CI success alone do not demonstrate economic results.

**Who is it for?** Developers and researchers interested in AI-agent evaluation, competition bots, benchmark design, legal bounty discovery, reproducibility, and early-stage go/no-go decisions.

## En español

**MONEYKILLER** investiga oportunidades remuneradas y agentes autónomos sin confundir *potencial* con dinero cobrado. Primero verifica condiciones de ingreso, reglas, premio **neto**, método de cobro, costo y permisos para automatizar. Después compara un candidato contra la mejor solución simple disponible. Sin ventaja reproducible o sin vía legal de participación, el carril se descarta.

No es un bot para aceptar trabajos indiscriminadamente, ni una herramienta para evadir requisitos de plataformas, ni un sistema de trading. La inscripción, la ejecución y el cobro requieren evidencia externa y controles adecuados.

## Repository map / Mapa del repositorio

| Location | Purpose |
| --- | --- |
| [AUD_CANON.md](./AUD_CANON.md) | Executive context, verified claims, authorities, blockers, and next decision |
| [ARQ_CANON.md](./ARQ_CANON.md) | Operational handoff for the **single** active ARQ role |
| [Issues](https://github.com/simondalmasso/m0kill/issues) | Orders, evidence, and historical kill/promote decisions |
| [Battlecode branch](https://github.com/simondalmasso/m0kill/tree/arq1/battlecode-killtest-v1) | Preserved Battlecode prototypes and evaluation tooling (not current production) |
| [ARC-AGI-3 branch](https://github.com/simondalmasso/m0kill/tree/arq2/arc-killtest-v1) | Preserved symbolic-agent/baseline/killtest work |
| [Platform branch](https://github.com/simondalmasso/m0kill/tree/arq3/platform-kaggriculture-v1) | Migration provenance and Kaggriculture entry-gate work |
| [Mirror workflow](./.github/workflows/mirror-gitlab.yml) | GitHub → GitLab downstream sync configuration; writes require a configured secret |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Evidence format and contribution boundaries |

**Source of truth:** [GitHub / m0kill](https://github.com/simondalmasso/m0kill).

**Historical archive / downstream mirror:** [GitLab / Moneykiller](https://gitlab.com/simondalmasso/Moneykiller). The migration is a snapshot/provenance cutover, **not** a claim of a complete Git-history mirror. Automated downstream writes require the `GITLAB_MIRROR_TOKEN` repository secret; check its state rather than assuming synchronization.

### Relationship to ATM

[ATM — Agent Teller Machine](https://github.com/simondalmasso/ATM) is a **separate** Cloudflare Worker project for opportunity discovery, policy gates, execution tracking, and settlement readback. Its [live dashboard](https://atm.simondalmasso44.workers.dev/) is **not** a deployment of m0kill. ATM can consume m0kill's research and negative results **read-only**; the two repositories have independent governance and runtime authority.

## Evidence and collaboration

Each promoted experiment should preserve rules and eligibility snapshots, official runtime parity, frozen baselines/seeds, raw outcomes, resource measurements, source/artifact hashes, and any real submission or payment receipt. **CI_GREEN != DONE**.

Start from the [AUD](./AUD_CANON.md) or [ARQ](./ARQ_CANON.md) canon; discuss changes through [Issues](https://github.com/simondalmasso/m0kill/issues) and follow [CONTRIBUTING.md](./CONTRIBUTING.md). Do not push speculative experiments directly to `main`, mutate historical branches, or disclose credentials.

**License:** No project-wide license has been declared. Public visibility does **not** imply permission to reuse or redistribute the code. External components retain their own licenses.

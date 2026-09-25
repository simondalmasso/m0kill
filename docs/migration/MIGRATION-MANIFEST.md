# MONEYKILLER GitLab → GitHub Migration Manifest

Order: `006-P3`
Owner lane: `ARQ3_MONEYKILLER`
Canonical code/compute repository: https://github.com/simondalmasso/m0kill
Historical source/archive: https://gitlab.com/simondalmasso/Moneykiller

## Cutover model

This is a **snapshot/provenance migration**, not a Git object mirror.
No claim is made that Git commit SHAs, branch object identities, reflogs, tags, or all historical objects were preserved 1:1.
GitLab remains historical evidence/archive until AUD declares final cutover.

## Source provenance

- GitLab project: `simondalmasso/Moneykiller` (public).
- GitLab protected `main` at migration inspection: `4a4df6d3095901d1dd833a3be8ea0ee38b91c547`.
- GitLab prototype source branch: `lab/mk-prize-agents-v1`.
- Prototype source HEAD: `9f8af8f4ced4ad5fba63900251a4ff87bd4af935`.
- Source HEAD title: `arc: add offline ablation evaluation harness`.
- GitLab history was read only; it was not rewritten by ARQ3.

## GitHub snapshot

- Repository: `simondalmasso/m0kill`.
- Visibility: public.
- ARQ3 authenticated repository permission at inspection: admin.
- Default branch: `main`.
- GitHub `main` HEAD at inspection: `6a767dbb24bf8137115cae19656874a607f569d4`.
- Import marker commit message: `chore: import GitLab main snapshot 4a4df6d`.
- The marker links GitHub main to the GitLab main snapshot; it is not evidence of object-level mirroring.

## Lane branch map

| Lane | GitHub branch | State at inspection | Purpose |
| --- | --- | --- | --- |
| ARQ1 | `arq1/battlecode-killtest-v1` | exists; isolated from main | Battlecode killtest |
| ARQ2 | `arq2/arc-killtest-v1` | exists; isolated from main | ARC killtest |
| ARQ3 | `arq3/platform-kaggriculture-v1` | exists; isolated from main | migration/CI + Kaggriculture gate |

ARQ3 does not own or mutate ARQ1/ARQ2 branches or their workflows.

## Imported prototype content verification

The following GitHub lane files were compared directly against GitLab
`lab/mk-prize-agents-v1@9f8af8f4ced4ad5fba63900251a4ff87bd4af935`.
All ten compared files were byte-for-byte equal at inspection time:

- `competitions/unsw-battlecode/bot/bot.toml`
- `competitions/unsw-battlecode/bot/helper.py`
- `competitions/unsw-battlecode/bot/main.py`
- `competitions/unsw-battlecode/opponents/greedy-visible/bot.toml`
- `competitions/unsw-battlecode/opponents/greedy-visible/helper.py`
- `competitions/unsw-battlecode/opponents/greedy-visible/main.py`
- `competitions/unsw-battlecode/tests/run_league.py`
- `competitions/arc-agi-3/agent/my_agent.py`
- `competitions/arc-agi-3/baselines/round_robin_agent.py`
- `competitions/arc-agi-3/tests/run_local_eval.py`

This proves content provenance for the imported prototype file set only.
It does not prove that the full GitLab repository or its Git objects were mirrored.

## Branch isolation rule

ARQ3 writes are restricted to:

- `competitions/kaggriculture/**`
- `docs/migration/**`
- `docs/handoffs/ARQ3-PLATFORM-KAGGRICULTURE.md`
- `docs/checkpoints/ARQ3/**`
- `.github/workflows/arq3-platform.yml`
- `.github/workflows/README.md`

Forbidden ARQ3 writes include Battlecode, ARC, ARQ1/ARQ2 handoffs/workflows, `README.md`, and `main`.

## Security and compute constraints

- No credentials are intentionally stored in migration artifacts.
- GitHub Actions use read-only repository contents permission.
- No `pull_request_target`.
- No fork-secret exposure.
- No paid runners or GPU.
- No arbitrary compute farming.
- Jobs are bounded and limited to migration/integrity checks.

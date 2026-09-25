# GitHub Actions conventions for MONEYKILLER lanes

GitHub is the code/compute plane after ORDER-006-P3. Workflows must perform genuine repository testing, validation, or bounded benchmarking only.

## Global rules

- Use GitHub-hosted standard runners only (for example `ubuntu-latest`).
- Do not use paid/self-hosted GPU capacity for MONEYKILLER.
- Set `permissions: contents: read` unless a narrower permission set is possible.
- Never use `pull_request_target`.
- Fork-triggered jobs must not receive repository secrets.
- Do not turn Actions into arbitrary compute farming.
- Every job must have a bounded `timeout-minutes`.
- Keep matrices/shards small and explicit.
- Cache only reproducible dependency state keyed by immutable lockfiles/runtime versions.
- Do not cache generated benchmark outcomes or mutable research state.
- Artifact names must be deterministic and include the exact commit SHA.
- Tests and benchmarks must print the exact source SHA they evaluated.
- A workflow must fail closed when it detects an unexpected lane path.

## ARQ1 recipe

ARQ1 owns Battlecode only. ARQ3 does not create or edit the ARQ1 workflow.

Recommended ARQ1 workflow contract:

1. Trigger only for the ARQ1 branch/PR and Battlecode-owned paths.
2. `permissions: contents: read`.
3. `actions/checkout` with enough history to resolve the intended base.
4. Pin/setup the required language/runtime from repository-declared versions.
5. Install only locked or explicitly versioned dependencies.
6. Run deterministic unit/smoke tests first.
7. Run bounded killtest shards only after cheap gates pass.
8. Cap shard count and per-job time.
9. Upload logs/results as `arq1-battlecode-<sha>-<shard>`.
10. Never expose secrets to fork events and never use `pull_request_target`.

## ARQ2 recipe

ARQ2 owns ARC only. ARQ3 does not create or edit the ARQ2 workflow.

Recommended ARQ2 workflow contract:

1. Trigger only for the ARQ2 branch/PR and ARC-owned paths.
2. `permissions: contents: read`.
3. `actions/checkout` with enough history to resolve the intended base.
4. Install the official starter/runtime and pinned test dependencies only.
5. Run starter-parity and legality checks before expensive evaluation.
6. Run cheap baselines before symbolic-agent comparisons.
7. Keep frozen-seed evaluation deterministic and bounded.
8. Run ablations only after the promotion gate is satisfied.
9. Upload evidence as `arq2-arc-<sha>-<stage>`.
10. Never expose secrets to fork events and never use `pull_request_target`.

## ARQ3 workflow scope

`arq3-platform.yml` is restricted to migration/integrity verification. It must not execute Battlecode, ARC, or Kaggriculture economic workloads.

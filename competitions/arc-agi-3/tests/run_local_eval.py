#!/usr/bin/env python3
"""Frozen, offline ARC-AGI-3 killtest for ORDER-006-P2."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def variant_specs(include_ablations: bool = False) -> list[dict[str, str]]:
    core = [
        {
            "label": "A_BASE_0",
            "path": "baselines/random_legal_agent.py",
            "ablation": "baseline",
            "kind": "baseline",
        },
        {
            "label": "A_BASE_1",
            "path": "baselines/round_robin_agent.py",
            "ablation": "baseline",
            "kind": "baseline",
        },
        {
            "label": "A_BASE_2",
            "path": "baselines/novelty_agent.py",
            "ablation": "baseline",
            "kind": "baseline",
        },
        {
            "label": "A_CHALLENGER",
            "path": "agent/my_agent.py",
            "ablation": "full",
            "kind": "challenger",
        },
    ]
    if not include_ablations:
        return core
    return core + [
        {
            "label": "A_CHALLENGER_NO_EFFECT",
            "path": "agent/my_agent.py",
            "ablation": "no_effect",
            "kind": "ablation",
        },
        {
            "label": "A_CHALLENGER_NO_INFO",
            "path": "agent/my_agent.py",
            "ablation": "no_info",
            "kind": "ablation",
        },
        {
            "label": "A_CHALLENGER_NO_PLANNER",
            "path": "agent/my_agent.py",
            "ablation": "no_planner",
            "kind": "ablation",
        },
    ]


def promotion_decision(
    challenger: dict[str, float],
    baseline: dict[str, float],
    *,
    delta_ci: tuple[float, float],
    repeat_deltas: list[float],
    offline_reproducible: bool,
) -> dict[str, Any]:
    use_rhae = max(float(challenger["rhae"]), float(baseline["rhae"])) > 0.0
    metric = "rhae" if use_rhae else "levels_completed"
    delta = float(challenger[metric]) - float(baseline[metric])
    if use_rhae:
        genuine_progress = delta > 0.0
    else:
        genuine_progress = (
            float(challenger["levels_completed"]) > float(baseline["levels_completed"])
            or float(challenger["games_with_progress"])
            > float(baseline["games_with_progress"])
        )
    repeat_positive = bool(repeat_deltas) and all(value > 0.0 for value in repeat_deltas)
    ci_positive = float(delta_ci[0]) > 0.0
    promoted = (
        delta > 0.0
        and genuine_progress
        and repeat_positive
        and ci_positive
        and offline_reproducible
    )
    return {
        "status": "PROMOTED" if promoted else "KILLED_NO_EDGE",
        "metric": metric,
        "delta": delta,
        "delta_95ci": [float(delta_ci[0]), float(delta_ci[1])],
        "genuine_progress": genuine_progress,
        "repeat_positive": repeat_positive,
        "ci_positive": ci_positive,
        "offline_reproducible": offline_reproducible,
    }


def _canonical_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def paired_bootstrap_delta(
    deltas: list[float], *, seed: int = 6002, samples: int = 4000
) -> tuple[float, float, float]:
    if not deltas:
        return (0.0, 0.0, 0.0)
    mean = statistics.fmean(deltas)
    if len(deltas) == 1:
        return (mean, mean, mean)
    rng = random.Random(seed)
    n = len(deltas)
    boot = []
    for _ in range(samples):
        boot.append(statistics.fmean(deltas[rng.randrange(n)] for _ in range(n)))
    boot.sort()
    low = boot[max(0, int(0.025 * samples) - 1)]
    high = boot[min(samples - 1, int(0.975 * samples))]
    return (mean, low, high)


def load_agent(path: Path, class_name: str = "MyAgent"):
    spec = importlib.util.spec_from_file_location(
        f"arc_agent_{path.stem}_{hashlib.md5(str(path).encode()).hexdigest()[:8]}",
        path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


def freeze_corpus(
    arc: Any,
    *,
    output: Path,
    requested: list[str],
) -> dict[str, Any]:
    envs = sorted(arc.get_environments(), key=lambda env: str(env.game_id))
    requested_set = {item.split("-")[0].lower() for item in requested}
    games: list[dict[str, Any]] = []
    for info in envs:
        full_id = str(info.game_id)
        short_id = full_id.split("-")[0]
        if requested_set and short_id.lower() not in requested_set:
            continue
        wrapper = arc.make(full_id, render_mode=None)
        if wrapper is None:
            raise RuntimeError(f"failed to materialize public environment {full_id}")
        baseline_actions = getattr(info, "baseline_actions", None)
        games.append(
            {
                "game_id": full_id,
                "short_id": short_id,
                "title": str(getattr(info, "title", "") or ""),
                "baseline_actions": list(baseline_actions or []),
            }
        )
    if not games:
        raise RuntimeError("no ARC environments available for frozen corpus")
    payload = {
        "schema": 1,
        "arc_agi_version": importlib.metadata.version("arc-agi"),
        "games": games,
    }
    envelope = dict(payload)
    envelope["corpus_sha256"] = _canonical_hash(payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n")
    return envelope


def load_corpus(path: Path) -> dict[str, Any]:
    corpus = json.loads(path.read_text(encoding="utf-8"))
    expected = str(corpus.get("corpus_sha256", ""))
    payload = {key: value for key, value in corpus.items() if key != "corpus_sha256"}
    actual = _canonical_hash(payload)
    if not expected or actual != expected:
        raise RuntimeError(
            f"corpus hash mismatch: expected={expected!r} actual={actual!r}"
        )
    if not corpus.get("games"):
        raise RuntimeError("frozen corpus is empty")
    return corpus


def play(
    arc: Any,
    game_id: str,
    agent_cls: Any,
    max_actions: int,
    ablation: str,
    repeat: int,
) -> dict[str, Any]:
    os.environ["ARC_AGENT_ABLATION"] = ablation
    env = arc.make(game_id, seed=0, render_mode=None)
    if env is None:
        return {
            "game_id": game_id,
            "repeat": repeat,
            "levels_completed": 0,
            "actions": 0,
            "elapsed_s": 0.0,
            "error": "env_make_none",
        }
    if hasattr(agent_cls, "MAX_ACTIONS"):
        agent_cls.MAX_ACTIONS = max_actions
    agent = agent_cls(
        card_id=f"order-006-{repeat}",
        game_id=game_id,
        agent_name=f"{agent_cls.__name__}.{ablation}.{repeat}.{game_id}",
        ROOT_URL="http://localhost",
        record=False,
        arc_env=env,
        tags=["order-006-p2", "offline-killtest"],
    )
    started = time.perf_counter()
    try:
        agent.main()
        elapsed = time.perf_counter() - started
        final = agent.frames[-1]
        state = getattr(final.state, "name", str(final.state))
        return {
            "game_id": game_id,
            "repeat": repeat,
            "state": state,
            "levels_completed": int(final.levels_completed),
            "win_levels": int(getattr(final, "win_levels", 0) or 0),
            "actions": int(agent.action_counter),
            "elapsed_s": elapsed,
            "fps": float(agent.action_counter / max(elapsed, 1e-9)),
            "error": None,
        }
    except Exception as exc:
        return {
            "game_id": game_id,
            "repeat": repeat,
            "levels_completed": 0,
            "actions": int(getattr(agent, "action_counter", 0)),
            "elapsed_s": time.perf_counter() - started,
            "error": f"{type(exc).__name__}:{exc}",
        }


def scorecard_snapshot(arc: Any) -> dict[str, Any]:
    scorecard = arc.get_scorecard()
    if scorecard is None:
        return {"score": 0.0, "games": {}}
    by_game: dict[str, float] = {}
    for environment in getattr(scorecard, "environments", []) or []:
        game_id = str(getattr(environment, "id", ""))
        by_game[game_id] = float(getattr(environment, "score", 0.0) or 0.0)
    return {
        "score": float(getattr(scorecard, "score", 0.0) or 0.0),
        "total_levels_completed": int(
            getattr(scorecard, "total_levels_completed", 0) or 0
        ),
        "total_actions": int(getattr(scorecard, "total_actions", 0) or 0),
        "games": by_game,
    }


def _lookup_game_score(scores: dict[str, float], game_id: str) -> float:
    if game_id in scores:
        return float(scores[game_id])
    short = game_id.split("-")[0]
    matches = [value for key, value in scores.items() if key.split("-")[0] == short]
    return float(matches[0]) if matches else 0.0


def _run_variant(
    *,
    arc_agi: Any,
    operation_mode: Any,
    environments_dir: str,
    recordings_root: Path,
    spec: dict[str, str],
    games: list[str],
    max_actions: int,
    repeats: int,
) -> dict[str, Any]:
    agent_cls = load_agent(ROOT / spec["path"])
    rows: list[dict[str, Any]] = []
    repeat_summaries: list[dict[str, Any]] = []
    per_game_scores: dict[str, list[float]] = {game: [] for game in games}
    for repeat in range(repeats):
        arc = arc_agi.Arcade(
            operation_mode=operation_mode,
            environments_dir=environments_dir,
            recordings_dir=str(recordings_root / spec["label"] / str(repeat)),
        )
        repeat_rows = []
        for game_id in games:
            row = play(
                arc,
                game_id,
                agent_cls,
                max_actions,
                spec["ablation"],
                repeat,
            )
            row["variant"] = spec["label"]
            rows.append(row)
            repeat_rows.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)
        scorecard = scorecard_snapshot(arc)
        for game_id in games:
            per_game_scores[game_id].append(
                _lookup_game_score(scorecard["games"], game_id)
            )
        repeat_summaries.append(
            {
                "repeat": repeat,
                "rhae": float(scorecard["score"]),
                "levels_completed": float(
                    sum(int(row.get("levels_completed", 0)) for row in repeat_rows)
                ),
                "games_with_progress": float(
                    sum(int(row.get("levels_completed", 0)) > 0 for row in repeat_rows)
                ),
                "actions": float(
                    sum(int(row.get("actions", 0)) for row in repeat_rows)
                ),
                "runtime_s": float(
                    sum(float(row.get("elapsed_s", 0.0)) for row in repeat_rows)
                ),
                "errors": int(sum(bool(row.get("error")) for row in repeat_rows)),
            }
        )

    signatures: dict[int, list[tuple[Any, ...]]] = {}
    for repeat in range(repeats):
        signatures[repeat] = [
            (
                row["game_id"],
                row.get("state"),
                row.get("levels_completed"),
                row.get("actions"),
                row.get("error"),
            )
            for row in rows
            if row["repeat"] == repeat
        ]
    reproducible = all(
        signatures[index] == signatures[0] for index in range(1, repeats)
    )
    mean_summary = {
        "games": len(games),
        "repeats": repeats,
        "rhae": statistics.fmean(item["rhae"] for item in repeat_summaries),
        "levels_completed": statistics.fmean(
            item["levels_completed"] for item in repeat_summaries
        ),
        "games_with_progress": statistics.fmean(
            item["games_with_progress"] for item in repeat_summaries
        ),
        "actions": statistics.fmean(item["actions"] for item in repeat_summaries),
        "runtime_s": statistics.fmean(
            item["runtime_s"] for item in repeat_summaries
        ),
        "errors": sum(int(item["errors"]) for item in repeat_summaries),
        "offline_reproducible": reproducible,
    }
    per_game = {}
    for game_id in games:
        game_rows = [row for row in rows if row["game_id"] == game_id]
        per_game[game_id] = {
            "rhae": statistics.fmean(per_game_scores[game_id]),
            "levels_completed": statistics.fmean(
                float(row.get("levels_completed", 0)) for row in game_rows
            ),
            "actions": statistics.fmean(
                float(row.get("actions", 0)) for row in game_rows
            ),
        }
    return {
        "spec": spec,
        "rows": rows,
        "repeat_summaries": repeat_summaries,
        "summary": mean_summary,
        "per_game": per_game,
    }


def _best_baseline(results: dict[str, dict[str, Any]]) -> str:
    labels = ["A_BASE_0", "A_BASE_1", "A_BASE_2"]
    use_rhae = any(
        float(results[label]["summary"]["rhae"]) > 0.0
        for label in labels + ["A_CHALLENGER"]
    )

    def key(label: str) -> tuple[float, float, float, float]:
        summary = results[label]["summary"]
        primary = (
            float(summary["rhae"])
            if use_rhae
            else float(summary["levels_completed"])
        )
        return (
            primary,
            float(summary["levels_completed"]),
            float(summary["games_with_progress"]),
            -float(summary["actions"]),
        )

    return max(labels, key=key)


def evaluate(
    *,
    arc_agi: Any,
    operation_mode: Any,
    corpus: dict[str, Any],
    environments_dir: str,
    output: Path,
    max_actions: int,
    repeats: int,
    include_ablations: bool,
) -> dict[str, Any]:
    games = [str(item["game_id"]) for item in corpus["games"]]
    specs = variant_specs(include_ablations)
    results: dict[str, dict[str, Any]] = {}
    recordings_root = output.parent / ".recordings"
    for spec in specs:
        results[spec["label"]] = _run_variant(
            arc_agi=arc_agi,
            operation_mode=operation_mode,
            environments_dir=environments_dir,
            recordings_root=recordings_root,
            spec=spec,
            games=games,
            max_actions=max_actions,
            repeats=repeats,
        )

    decision: dict[str, Any] | None = None
    if not include_ablations:
        baseline_label = _best_baseline(results)
        baseline = results[baseline_label]
        challenger = results["A_CHALLENGER"]
        use_rhae = max(
            float(baseline["summary"]["rhae"]),
            float(challenger["summary"]["rhae"]),
        ) > 0.0
        metric = "rhae" if use_rhae else "levels_completed"
        game_deltas = [
            float(challenger["per_game"][game_id][metric])
            - float(baseline["per_game"][game_id][metric])
            for game_id in games
        ]
        delta_mean, ci_low, ci_high = paired_bootstrap_delta(game_deltas)
        repeat_deltas = [
            float(challenger["repeat_summaries"][index][metric])
            - float(baseline["repeat_summaries"][index][metric])
            for index in range(repeats)
        ]
        offline_reproducible = bool(
            challenger["summary"]["offline_reproducible"]
            and baseline["summary"]["offline_reproducible"]
            and challenger["summary"]["errors"] == 0
            and baseline["summary"]["errors"] == 0
        )
        decision = promotion_decision(
            challenger["summary"],
            baseline["summary"],
            delta_ci=(ci_low, ci_high),
            repeat_deltas=repeat_deltas,
            offline_reproducible=offline_reproducible,
        )
        decision.update(
            {
                "best_baseline": baseline_label,
                "paired_delta_mean": delta_mean,
                "repeat_deltas": repeat_deltas,
            }
        )
        public_runtime = float(challenger["summary"]["runtime_s"])
        projected_10x_runtime_s = public_runtime * 10.0
        decision["projected_10x_runtime_s"] = projected_10x_runtime_s
        decision["estimated_9h_compatible"] = projected_10x_runtime_s < 9 * 3600
        failure_modes = []
        if challenger["summary"]["errors"]:
            failure_modes.append(
                f"errors={int(challenger['summary']['errors'])}"
            )
        if challenger["summary"]["levels_completed"] == 0:
            failure_modes.append("zero_levels_completed")
        if challenger["summary"]["games_with_progress"] == 0:
            failure_modes.append("zero_games_with_progress")
        if not decision["repeat_positive"]:
            failure_modes.append("nonpositive_repeat_delta")
        if not decision["ci_positive"]:
            failure_modes.append("delta_95ci_not_strictly_positive")
        if not offline_reproducible:
            failure_modes.append("offline_not_exactly_reproducible")
        decision["failure_modes"] = failure_modes

    envelope = {
        "schema": 2,
        "mode": "offline",
        "corpus_sha256": corpus["corpus_sha256"],
        "arc_agi_version": corpus["arc_agi_version"],
        "max_actions": max_actions,
        "repeats": repeats,
        "include_ablations": include_ablations,
        "results": results,
        "decision": decision,
    }
    envelope["artifact_sha256"] = _canonical_hash(envelope)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n")
    return envelope


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework", required=True)
    parser.add_argument("--phase", choices=["freeze", "evaluate"], required=True)
    parser.add_argument("--corpus", required=True)
    parser.add_argument("--environments-dir", default="environment_files")
    parser.add_argument("--games", default="")
    parser.add_argument("--max-actions", type=int, default=200)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--include-ablations", action="store_true")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    framework = str(Path(args.framework).resolve())
    if framework not in sys.path:
        sys.path.insert(0, framework)
    import arc_agi
    from arc_agi import OperationMode

    corpus_path = Path(args.corpus)
    if args.phase == "freeze":
        requested = [item.strip() for item in args.games.split(",") if item.strip()]
        arc = arc_agi.Arcade(
            operation_mode=OperationMode.NORMAL,
            environments_dir=args.environments_dir,
            recordings_dir=str(corpus_path.parent / ".freeze-recordings"),
        )
        corpus = freeze_corpus(arc, output=corpus_path, requested=requested)
        print(
            json.dumps(
                {
                    "event": "CORPUS_FROZEN",
                    "games": len(corpus["games"]),
                    "corpus_sha256": corpus["corpus_sha256"],
                    "arc_agi_version": corpus["arc_agi_version"],
                },
                sort_keys=True,
            )
        )
        return 0

    if not args.output:
        parser.error("--output is required for --phase evaluate")
    if args.repeats < 2 and not args.include_ablations:
        parser.error("core killtest requires --repeats >= 2")
    corpus = load_corpus(corpus_path)
    result = evaluate(
        arc_agi=arc_agi,
        operation_mode=OperationMode.OFFLINE,
        corpus=corpus,
        environments_dir=args.environments_dir,
        output=Path(args.output),
        max_actions=args.max_actions,
        repeats=args.repeats,
        include_ablations=args.include_ablations,
    )
    if result["decision"] is not None:
        print(
            "ARC_KILLTEST_RESULT="
            + json.dumps(result["decision"], sort_keys=True)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

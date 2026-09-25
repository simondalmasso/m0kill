#!/usr/bin/env python3
"""Offline/local ARC-AGI-3 evaluation harness with deterministic ablations."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_agent(path: Path, class_name: str = "MyAgent"):
    spec = importlib.util.spec_from_file_location(f"arc_agent_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)


def play(arc, game_id: str, agent_cls, max_actions: int, ablation: str) -> dict:
    os.environ["ARC_AGENT_ABLATION"] = ablation
    env = arc.make(game_id, render_mode=None)
    if env is None:
        return {"game_id": game_id, "error": "env_make_none"}
    if hasattr(agent_cls, "MAX_ACTIONS"):
        agent_cls.MAX_ACTIONS = max_actions
    agent = agent_cls(
        card_id="mk-prize-agents-local",
        game_id=game_id,
        agent_name=f"{agent_cls.__name__}.{ablation}.{game_id}",
        ROOT_URL="http://localhost",
        record=False,
        arc_env=env,
        tags=["order-006", "offline-eval"],
    )
    started = time.perf_counter()
    try:
        agent.main()
        elapsed = time.perf_counter() - started
        final = agent.frames[-1]
        return {
            "game_id": game_id,
            "state": str(final.state),
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
            "levels_completed": 0,
            "actions": int(getattr(agent, "action_counter", 0)),
            "elapsed_s": time.perf_counter() - started,
            "error": f"{type(exc).__name__}:{exc}",
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", required=True)
    ap.add_argument("--mode", choices=["normal", "offline"], default="offline")
    ap.add_argument("--games", default="")
    ap.add_argument("--max-actions", type=int, default=240)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    sys.path.insert(0, str(Path(args.framework).resolve()))
    import arc_agi
    from arc_agi import OperationMode

    mode = OperationMode.OFFLINE if args.mode == "offline" else OperationMode.NORMAL
    arc = arc_agi.Arcade(operation_mode=mode)
    envs = arc.get_environments()
    available = [e.game_id.split("-")[0] for e in envs]
    requested = [g.strip().split("-")[0] for g in args.games.split(",") if g.strip()]
    games = [g for g in available if not requested or g in requested]

    full = load_agent(ROOT / "agent" / "my_agent.py")
    baseline = load_agent(ROOT / "baselines" / "round_robin_agent.py")
    variants = [
        ("round_robin", baseline, "baseline"),
        ("symbolic_full", full, "full"),
        ("symbolic_no_effect", full, "no_effect"),
        ("symbolic_no_info", full, "no_info"),
        ("symbolic_no_planner", full, "no_planner"),
    ]

    rows = []
    for label, cls, ablation in variants:
        for game_id in games:
            row = play(arc, game_id, cls, args.max_actions, ablation)
            row["variant"] = label
            rows.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)

    summary = {}
    for label, _, _ in variants:
        rr = [r for r in rows if r["variant"] == label]
        summary[label] = {
            "games": len(rr),
            "errors": sum(bool(r.get("error")) for r in rr),
            "levels_completed": sum(int(r.get("levels_completed", 0)) for r in rr),
            "actions": sum(int(r.get("actions", 0)) for r in rr),
            "elapsed_s": sum(float(r.get("elapsed_s", 0)) for r in rr),
            "games_with_progress": sum(int(r.get("levels_completed", 0)) > 0 for r in rr),
        }
    output = {
        "mode": args.mode,
        "max_actions": args.max_actions,
        "games": games,
        "rows": rows,
        "summary": summary,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

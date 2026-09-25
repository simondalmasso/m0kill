#!/usr/bin/env python3
"""Paired deterministic UNSW Battlecode league for ORDER-006."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

WIN_RE = re.compile(r"team ([AB]) wins after (\d+) rounds")
DRAW_RE = re.compile(r"draw after (\d+) rounds")
CPU_RE = re.compile(
    r"team ([AB]) points per turn: p50 ([0-9.]+)([MK])\s+p99 ([0-9.]+)([MK])\s+"
    r"mean ([0-9.]+)([MK])\s+max ([0-9.]+)([MK])\s+\((\d+) turns\)"
)
DEATH_RE = re.compile(r"round (\d+): bot (\d+) \(team ([AB])\) died: (.+)")
REPLAY_RE = re.compile(r"wrote replay: (.+\.replay)")


def scaled(v: str, unit: str) -> float:
    return float(v) * (1_000_000 if unit == "M" else 1_000)


def parse_output(text: str) -> dict:
    winner = None
    rounds = None
    m = WIN_RE.search(text)
    if m:
        winner, rounds = m.group(1), int(m.group(2))
    else:
        m = DRAW_RE.search(text)
        if m:
            rounds = int(m.group(1))
    cpu = {}
    for m in CPU_RE.finditer(text):
        cpu[m.group(1)] = {
            "p50": scaled(m.group(2), m.group(3)),
            "p99": scaled(m.group(4), m.group(5)),
            "mean": scaled(m.group(6), m.group(7)),
            "max": scaled(m.group(8), m.group(9)),
            "turns": int(m.group(10)),
        }
    deaths = [
        {"round": int(m.group(1)), "bot": int(m.group(2)), "team": m.group(3), "reason": m.group(4)}
        for m in DEATH_RE.finditer(text)
    ]
    rep = REPLAY_RE.search(text)
    return {
        "winner_team": winner,
        "rounds": rounds,
        "cpu": cpu,
        "deaths": deaths,
        "replay": rep.group(1).strip() if rep else None,
    }


def score_for(winner_team: str | None, champion_team: str) -> float:
    if winner_team is None:
        return 0.5
    return 1.0 if winner_team == champion_team else 0.0


def bootstrap_pair_means(pair_scores: list[float], reps: int = 10000, seed: int = 20260924) -> dict:
    import random

    rng = random.Random(seed)
    n = len(pair_scores)
    if not n:
        return {"n_pairs": 0, "mean": None, "ci95": [None, None], "reps": reps}
    samples = []
    for _ in range(reps):
        samples.append(sum(pair_scores[rng.randrange(n)] for _ in range(n)) / n)
    samples.sort()
    lo = samples[int(0.025 * (reps - 1))]
    hi = samples[int(0.975 * (reps - 1))]
    return {
        "n_pairs": n,
        "mean": sum(pair_scores) / n,
        "ci95": [lo, hi],
        "reps": reps,
        "seed": seed,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--unswbc", required=True)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    maps_dir = root / "opponents" / "maps"
    champion = root / "bot"
    opponents = {
        "official-starter": root / "opponents" / "official-starter",
        "greedy-visible": root / "opponents" / "greedy-visible",
    }
    evidence = root / "evidence"
    replay_dir = evidence / "league-replays"
    log_dir = evidence / "league-logs"
    evidence.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    raw_path = evidence / "league-raw.jsonl"

    completed = set()
    rows = []
    if args.resume and raw_path.exists():
        with raw_path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    rows.append(row)
                    completed.add(row["match_id"])

    maps = sorted(maps_dir.glob("*.map"), key=lambda p: p.name.lower())
    env = dict(os.environ)
    env["UNSWBC_NO_UPDATE"] = "1"
    env["UNSWBC_NO_VSCODE"] = "1"

    for opponent_name, opponent in opponents.items():
        for map_path in maps:
            for champion_team in ("A", "B"):
                match_id = f"{opponent_name}__{map_path.stem}__champ{champion_team}"
                if match_id in completed:
                    continue
                a = champion if champion_team == "A" else opponent
                b = opponent if champion_team == "A" else champion
                replay = replay_dir / f"{match_id}.replay"
                cmd = [
                    args.unswbc, "run", str(map_path), str(a), str(b),
                    "--sandbox", "--no-debug", "-o", str(replay),
                ]
                started = time.time()
                proc = subprocess.run(
                    cmd, cwd=root, env=env, capture_output=True, text=True,
                    errors="replace", timeout=180,
                )
                text = (proc.stdout or "") + (proc.stderr or "")
                parsed = parse_output(text)
                champion_score = score_for(parsed["winner_team"], champion_team)
                champion_cpu = parsed["cpu"].get(champion_team)
                opponent_team = "B" if champion_team == "A" else "A"
                opponent_cpu = parsed["cpu"].get(opponent_team)
                invalid = [
                    d for d in parsed["deaths"]
                    if any(word in d["reason"].lower() for word in ("invalid", "malformed", "no valid", "no reply"))
                ]
                timeout_deaths = [
                    d for d in parsed["deaths"]
                    if any(word in d["reason"].lower() for word in ("timeout", "exhaust", "budget", "no reply"))
                ]
                row = {
                    "match_id": match_id,
                    "map": map_path.name,
                    "opponent": opponent_name,
                    "champion_team": champion_team,
                    "champion_score": champion_score,
                    "winner_team": parsed["winner_team"],
                    "rounds": parsed["rounds"],
                    "exit_code": proc.returncode,
                    "elapsed_s": time.time() - started,
                    "champion_cpu": champion_cpu,
                    "opponent_cpu": opponent_cpu,
                    "deaths": parsed["deaths"],
                    "invalid_action_deaths": len(invalid),
                    "timeout_deaths": len(timeout_deaths),
                    "replay": str(replay.relative_to(root)),
                }
                (log_dir / f"{match_id}.txt").write_text(text, encoding="utf-8")
                with raw_path.open("a", encoding="utf-8", newline="\n") as out:
                    out.write(json.dumps(row, sort_keys=True) + "\n")
                rows.append(row)
                print(json.dumps(row, sort_keys=True), flush=True)

    by_pair = defaultdict(list)
    for row in rows:
        by_pair[(row["opponent"], row["map"])].append(row["champion_score"])
    pair_scores = [
        sum(scores) / len(scores) for scores in by_pair.values() if len(scores) == 2
    ]
    cpu_p50 = [r["champion_cpu"]["p50"] for r in rows if r.get("champion_cpu")]
    cpu_p99 = [r["champion_cpu"]["p99"] for r in rows if r.get("champion_cpu")]
    cpu_max = [r["champion_cpu"]["max"] for r in rows if r.get("champion_cpu")]
    ordered = sorted(cpu_p50)

    summary = {
        "matches": len(rows),
        "complete_side_swapped_pairs": len(pair_scores),
        "raw_winrate": sum(r["champion_score"] for r in rows) / max(1, len(rows)),
        "paired_score": bootstrap_pair_means(pair_scores),
        "invalid_action_deaths": sum(r["invalid_action_deaths"] for r in rows),
        "timeout_deaths": sum(r["timeout_deaths"] for r in rows),
        "cpu_points_p50_median": ordered[len(ordered) // 2] if ordered else None,
        "cpu_points_p99_max": max(cpu_p99) if cpu_p99 else None,
        "cpu_points_max": max(cpu_max) if cpu_max else None,
        "maps": sorted({r["map"] for r in rows}),
        "opponents": sorted({r["opponent"] for r in rows}),
    }
    (evidence / "league-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("SUMMARY", json.dumps(summary, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

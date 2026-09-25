from __future__ import annotations

import hashlib
import math
import os
from collections import Counter, defaultdict, deque
from typing import Any

from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent


def _frame_grid(frame: FrameData) -> list[list[int]]:
    layers = getattr(frame, "frame", None) or []
    if not layers:
        return []
    grid = layers[-1]
    return [list(map(int, row)) for row in grid]


def _frame_hash(grid: list[list[int]]) -> str:
    h = hashlib.blake2b(digest_size=12)
    for row in grid:
        h.update(bytes((int(v) & 0xFF) for v in row))
        h.update(b"\xff")
    return h.hexdigest()


def _diff_signature(a: list[list[int]], b: list[list[int]]) -> tuple[int, int, int]:
    if not a or not b:
        return (0, -1, -1)
    height = min(len(a), len(b))
    width = min(len(a[0]), len(b[0]))
    changed: list[tuple[int, int]] = []
    for y in range(height):
        for x in range(width):
            if a[y][x] != b[y][x]:
                changed.append((x, y))
    if not changed:
        return (0, -1, -1)
    cx = int(round(sum(x for x, _ in changed) / len(changed)))
    cy = int(round(sum(y for _, y in changed) / len(changed)))
    return (len(changed), cx, cy)


def _action_key(action: GameAction) -> str:
    return getattr(action, "name", str(action))


def _available(frame: FrameData) -> list[GameAction]:
    raw = getattr(frame, "available_actions", None)
    all_actions = [a for a in GameAction if a is not GameAction.RESET]
    if not raw:
        return all_actions
    allowed: set[str] = set()
    for item in raw:
        if isinstance(item, GameAction):
            allowed.add(item.name)
        elif hasattr(item, "name"):
            allowed.add(str(item.name))
        else:
            allowed.add(str(item))
    filtered = [
        a for a in all_actions
        if a.name in allowed or str(getattr(a, "value", "")) in allowed
    ]
    return filtered or all_actions


class MyAgent(Agent):
    """Deterministic symbolic model-based ARC-AGI-3 explorer/planner."""

    MAX_ACTIONS = 240
    PLAN_DEPTH = 3

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.last_action: GameAction | None = None
        self.last_grid: list[list[int]] = []
        self.last_levels = 0
        self.state_visits: Counter[str] = Counter()
        self.state_action_visits: Counter[tuple[str, str]] = Counter()
        self.action_effects: dict[str, Counter[tuple[int, int, int]]] = defaultdict(Counter)
        self.transition_counts: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
        self.state_value: dict[str, float] = defaultdict(float)
        self.complex_xy_visits: Counter[tuple[int, int]] = Counter()
        self.recent_states: deque[str] = deque(maxlen=14)
        self.ablation = os.getenv("ARC_AGENT_ABLATION", "full").strip().lower()

    @property
    def name(self) -> str:
        return f"{super().name}.symbolic.{self.ablation}.{self.MAX_ACTIONS}"

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def _update_model(self, latest_frame: FrameData, grid: list[list[int]]) -> str:
        state = _frame_hash(grid)
        self.state_visits[state] += 1

        if self.last_action is not None and self.last_grid:
            prev_state = _frame_hash(self.last_grid)
            action = _action_key(self.last_action)
            effect = _diff_signature(self.last_grid, grid)
            self.state_action_visits[(prev_state, action)] += 1
            self.action_effects[action][effect] += 1
            self.transition_counts[(prev_state, action)][state] += 1

            progress = max(0, int(latest_frame.levels_completed) - int(self.last_levels))
            reward = 100.0 * progress
            if latest_frame.state is GameState.WIN:
                reward += 250.0
            if latest_frame.state is GameState.GAME_OVER:
                reward -= 8.0
            if effect[0] == 0:
                reward -= 0.4
            else:
                reward += min(4.0, math.log2(effect[0] + 1.0))
            self.state_value[state] = max(self.state_value[state], reward)
            self.state_value[prev_state] = max(
                self.state_value[prev_state],
                reward * 0.55 + self.state_value[state] * 0.35,
            )

        self.recent_states.append(state)
        return state

    def _salient_points(self, grid: list[list[int]]) -> list[tuple[int, int]]:
        if not grid or not grid[0]:
            return [(0, 0)]
        counts = Counter(v for row in grid for v in row)
        background = counts.most_common(1)[0][0]
        activity: Counter[tuple[int, int]] = Counter()
        if self.last_grid:
            h = min(len(grid), len(self.last_grid))
            w = min(len(grid[0]), len(self.last_grid[0]))
            for y in range(h):
                for x in range(w):
                    if grid[y][x] != self.last_grid[y][x]:
                        activity[(x, y)] += 4

        candidates: list[tuple[float, int, int]] = []
        total = max(1, len(grid) * len(grid[0]))
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                rarity = total / max(1, counts[value])
                rare_bonus = math.log2(rarity + 1.0)
                bg_penalty = 2.0 if value == background else 0.0
                tried = self.complex_xy_visits[(x, y)]
                score = rare_bonus + activity[(x, y)] - bg_penalty - 0.75 * tried
                candidates.append((score, x, y))
        candidates.sort(key=lambda t: (-t[0], t[2], t[1]))
        return [(x, y) for _, x, y in candidates[:48]]

    def _transition_future_value(self, state: str, depth: int, seen: set[str]) -> float:
        if depth <= 0 or state in seen or self.ablation == "no_planner":
            return self.state_value.get(state, 0.0)
        seen = set(seen)
        seen.add(state)
        best = self.state_value.get(state, 0.0)
        for (src, _action), nexts in self.transition_counts.items():
            if src != state:
                continue
            total = sum(nexts.values())
            if not total:
                continue
            expected = 0.0
            for nxt, count in nexts.items():
                expected += (count / total) * self._transition_future_value(
                    nxt, depth - 1, seen
                )
            best = max(best, expected * 0.82)
        return best

    def _score_action(self, state: str, action: GameAction) -> float:
        key = _action_key(action)
        visits = self.state_action_visits[(state, key)]
        effects = self.action_effects[key]
        total_effects = sum(effects.values())

        score = 0.0
        if self.ablation != "no_info":
            score += 7.0 / math.sqrt(visits + 1.0)
            score += 2.0 / math.sqrt(total_effects + 1.0)

        if self.ablation != "no_effect" and effects:
            no_effect = effects.get((0, -1, -1), 0) / total_effects
            mean_change = sum(sig[0] * n for sig, n in effects.items()) / total_effects
            score += min(7.0, math.log2(mean_change + 1.0))
            score -= 6.0 * no_effect

        transitions = self.transition_counts.get((state, key))
        if transitions and self.ablation != "no_planner":
            total = sum(transitions.values())
            future = sum(
                (n / total) * self._transition_future_value(
                    nxt, self.PLAN_DEPTH - 1, {state}
                )
                for nxt, n in transitions.items()
            )
            score += 0.75 * future

        # Escape local cycles by preferring actions not yet tried in this exact frame.
        if state in list(self.recent_states)[-5:]:
            score += 3.0 / (visits + 1.0)

        # Stable tie-break: lower action id/name first.
        try:
            numeric = int(getattr(action, "value", 0))
        except Exception:
            numeric = sum(ord(c) for c in key)
        score -= numeric * 1e-5
        return score

    def _prepare_complex(self, action: GameAction, grid: list[list[int]]) -> None:
        if not action.is_complex():
            return
        candidates = self._salient_points(grid)
        x, y = candidates[0] if candidates else (0, 0)
        self.complex_xy_visits[(x, y)] += 1
        action.set_data({"x": int(max(0, min(63, x))), "y": int(max(0, min(63, y)))})

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        if latest_frame.state in (GameState.NOT_PLAYED, GameState.GAME_OVER):
            self.last_action = GameAction.RESET
            self.last_grid = _frame_grid(latest_frame)
            self.last_levels = int(latest_frame.levels_completed)
            action = GameAction.RESET
            action.reasoning = {"policy": "reset", "ablation": self.ablation}
            return action

        grid = _frame_grid(latest_frame)
        state = self._update_model(latest_frame, grid)
        candidates = _available(latest_frame)

        action = max(
            candidates,
            key=lambda candidate: (
                self._score_action(state, candidate),
                -sum(ord(c) for c in _action_key(candidate)),
            ),
        )
        self._prepare_complex(action, grid)
        action.reasoning = {
            "policy": "symbolic-effect-planner",
            "ablation": self.ablation,
            "state_visits": self.state_visits[state],
            "known_transitions": len(self.transition_counts),
        }

        self.last_action = action
        self.last_grid = grid
        self.last_levels = int(latest_frame.levels_completed)
        return action

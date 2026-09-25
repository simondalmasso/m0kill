from __future__ import annotations

import hashlib
import math
from collections import Counter
from typing import Any

from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent


def _frame_grid(frame: FrameData) -> list[list[int]]:
    layers = getattr(frame, "frame", None) or []
    if not layers:
        return []
    return [list(map(int, row)) for row in layers[-1]]


def _frame_hash(grid: list[list[int]]) -> str:
    digest = hashlib.blake2b(digest_size=12)
    for row in grid:
        digest.update(bytes((value & 0xFF) for value in row))
        digest.update(b"\xff")
    return digest.hexdigest()


def _available(frame: FrameData) -> list[GameAction]:
    actions = [action for action in GameAction if action is not GameAction.RESET]
    raw = getattr(frame, "available_actions", None)
    if not raw:
        return actions
    allowed: set[str] = set()
    for item in raw:
        if isinstance(item, GameAction):
            allowed.add(item.name)
        elif hasattr(item, "name"):
            allowed.add(str(item.name))
        else:
            allowed.add(str(item))
    legal = [
        action
        for action in actions
        if action.name in allowed or str(getattr(action, "value", "")) in allowed
    ]
    return legal or actions


class MyAgent(Agent):
    """Cheap novelty/information-gain explorer with no transition planner."""

    MAX_ACTIONS = 200

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.state_action_visits: Counter[tuple[str, str]] = Counter()
        self.action_visits: Counter[str] = Counter()
        self.xy_visits: Counter[tuple[int, int]] = Counter()

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def _complex_point(self, grid: list[list[int]]) -> tuple[int, int]:
        if not grid or not grid[0]:
            return (0, 0)
        counts = Counter(value for row in grid for value in row)
        total = len(grid) * len(grid[0])
        ranked: list[tuple[float, int, int]] = []
        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                rarity = math.log2(total / max(1, counts[value]) + 1.0)
                novelty = 1.0 / math.sqrt(self.xy_visits[(x, y)] + 1.0)
                ranked.append((rarity + novelty, x, y))
        ranked.sort(key=lambda item: (-item[0], item[2], item[1]))
        _, x, y = ranked[0]
        self.xy_visits[(x, y)] += 1
        return (x, y)

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        if latest_frame.state in (GameState.NOT_PLAYED, GameState.GAME_OVER):
            return GameAction.RESET

        grid = _frame_grid(latest_frame)
        state = _frame_hash(grid)
        candidates = _available(latest_frame)

        def score(action: GameAction) -> tuple[float, str]:
            name = action.name
            local = self.state_action_visits[(state, name)]
            global_count = self.action_visits[name]
            information = 4.0 / math.sqrt(local + 1.0)
            coverage = 1.0 / math.sqrt(global_count + 1.0)
            return (information + coverage, name)

        action = max(candidates, key=lambda item: (score(item)[0], item.name))
        name = action.name
        self.state_action_visits[(state, name)] += 1
        self.action_visits[name] += 1
        if action.is_complex():
            x, y = self._complex_point(grid)
            action.set_data({"x": int(x), "y": int(y)})
        action.reasoning = {
            "policy": "cheap-novelty",
            "state_action_visits": self.state_action_visits[(state, name)],
        }
        return action

from __future__ import annotations

from typing import Any

from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent


class MyAgent(Agent):
    """Deterministic no-learning legal round-robin baseline."""

    MAX_ACTIONS = 240

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.index = 0

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        if latest_frame.state in (GameState.NOT_PLAYED, GameState.GAME_OVER):
            return GameAction.RESET

        raw = getattr(latest_frame, "available_actions", None)
        actions = [a for a in GameAction if a is not GameAction.RESET]
        if raw:
            allowed = {
                x.name if hasattr(x, "name") else str(x)
                for x in raw
            }
            filtered = [
                a for a in actions
                if a.name in allowed or str(getattr(a, "value", "")) in allowed
            ]
            if filtered:
                actions = filtered

        actions = sorted(actions, key=lambda a: a.name)
        action = actions[self.index % len(actions)]
        self.index += 1
        if action.is_complex():
            k = self.index - 1
            action.set_data({"x": (17 * k) % 64, "y": (29 * k) % 64})
        action.reasoning = {"policy": "round-robin"}
        return action

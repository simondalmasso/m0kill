from __future__ import annotations

import hashlib
import random
from typing import Any

from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent


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
    """Seeded legal random baseline with no game-specific strategy."""

    MAX_ACTIONS = 200

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        seed_bytes = hashlib.blake2b(
            self.game_id.encode("utf-8"), digest_size=8
        ).digest()
        self.rng = random.Random(int.from_bytes(seed_bytes, "big"))

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        if latest_frame.state in (GameState.NOT_PLAYED, GameState.GAME_OVER):
            return GameAction.RESET

        action = self.rng.choice(_available(latest_frame))
        if action.is_complex():
            action.set_data(
                {
                    "x": self.rng.randint(0, 63),
                    "y": self.rng.randint(0, 63),
                }
            )
        action.reasoning = {"policy": "seeded-legal-random"}
        return action

from __future__ import annotations

import helper as unswbc
from helper import Direction

ct: unswbc.Controller
game: unswbc.Game


def wrapped_distance(a, b):
    width, height = game.get_map_size()
    dx = abs(a.x - b.x)
    dy = abs(a.y - b.y)
    return min(dx, width - dx) + min(dy, height - dy)


def execute_turn() -> None:
    here = ct.get_position()
    here_tile = ct.get_tile(here)
    pearls = [tile.get_position() for tile in ct.get_tiles() if tile.has_pearl()]
    legal = []
    for direction in Direction.get_direction_list():
        if not here_tile.get_edge(direction).is_passable():
            continue
        ahead = ct.get_tile(here.add_dir(direction))
        if ahead is not None and ahead.get_dragon() is not None:
            continue
        legal.append(direction)

    if not legal:
        ct.make_move(ct.get_dir())
        return

    if pearls:
        direction = min(
            legal,
            key=lambda d: (
                min(wrapped_distance(here.add_dir(d), target) for target in pearls),
                d.value,
            ),
        )
    else:
        facing = ct.get_dir()
        direction = min(
            legal,
            key=lambda d: (0 if d == facing else 1, d.value),
        )
    ct.make_move(direction)


def main() -> None:
    global ct, game
    ct, game = unswbc.init()
    while unswbc.update(ct, game):
        execute_turn()
        unswbc.end_turn()


if __name__ == "__main__":
    main()

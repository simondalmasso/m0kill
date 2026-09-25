from __future__ import annotations

from collections import deque

import helper as unswbc
from helper import Direction, EdgeType, Position, Team

ct: unswbc.Controller
game: unswbc.Game

# Per-dragon process memory. Split children intentionally start with empty memory,
# matching the official process model.
seen_tiles: dict[tuple[int, int], dict] = {}
known_edges: dict[tuple[int, int, str], EdgeType] = {}
visit_count: dict[tuple[int, int], int] = {}
remote_targets: dict[tuple[int, int], int] = {}

DIRECTIONS = Direction.get_direction_list()
DIR_BY_VALUE = {d.value: d for d in DIRECTIONS}
SONAR_TAG = 0xA0000000
SONAR_MASK = 0xF0000000


def wrapped_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    width, height = game.get_map_size()
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return min(dx, width - dx) + min(dy, height - dy)


def neighbour(pos: tuple[int, int], direction: Direction) -> tuple[int, int]:
    width, height = game.get_map_size()
    dx, dy = direction.get_offset()
    return ((pos[0] + dx) % width, (pos[1] + dy) % height)


def observe() -> None:
    round_no = game.get_round_num()
    here = ct.get_position()
    visit_count[(here.x, here.y)] = visit_count.get((here.x, here.y), 0) + 1

    for tile in ct.get_tiles():
        pos = tile.get_position()
        key = (pos.x, pos.y)
        seen_tiles[key] = {
            "pearl": bool(tile.has_pearl()),
            "pearl_time": int(tile.get_pearl_time()),
            "seen": round_no,
        }
        for direction in DIRECTIONS:
            edge = tile.get_edge(direction)
            known_edges[(pos.x, pos.y, direction.value)] = edge.get_edge_type()

    # Sonar carries only a public absolute pearl coordinate. Keep messages short-lived.
    for message in ct.get_sonar_messages():
        if (message & SONAR_MASK) == SONAR_TAG:
            x = (message >> 6) & 0x3F
            y = message & 0x3F
            width, height = game.get_map_size()
            if x < width and y < height:
                remote_targets[(x, y)] = round_no

    stale = [target for target, heard in remote_targets.items() if round_no - heard > 24]
    for target in stale:
        remote_targets.pop(target, None)


def legal_directions() -> list[Direction]:
    here = ct.get_position()
    here_tile = ct.get_tile(here)
    result: list[Direction] = []
    for direction in DIRECTIONS:
        edge = here_tile.get_edge(direction)
        if not edge.is_passable():
            continue
        ahead = ct.get_tile(here.add_dir(direction))
        if ahead is not None and ahead.get_dragon() is not None:
            continue
        result.append(direction)
    return result


def remembered_pearl_targets() -> list[tuple[int, int]]:
    round_no = game.get_round_num()
    targets = [
        pos for pos, info in seen_tiles.items()
        if info["pearl"] and round_no - info["seen"] <= 48
    ]
    if targets:
        return targets
    return list(remote_targets)


def bfs_first_step(
    start: tuple[int, int],
    targets: set[tuple[int, int]],
    legal_now: set[Direction],
) -> Direction | None:
    if not targets:
        return None
    queue = deque([(start, None)])
    visited = {start}
    while queue and len(visited) <= 512:
        pos, first = queue.popleft()
        if pos in targets and first is not None:
            return first
        for direction in DIRECTIONS:
            if first is None and direction not in legal_now:
                continue
            edge_type = known_edges.get((pos[0], pos[1], direction.value))
            # Unknown edges are explored by the fallback scorer. Portal destination is
            # not inferable from local memory, so BFS does not pretend to know it.
            if edge_type != EdgeType.EMPTY:
                continue
            nxt = neighbour(pos, direction)
            if nxt in visited:
                continue
            visited.add(nxt)
            queue.append((nxt, direction if first is None else first))
    return None


def choose_move() -> Direction:
    legal = legal_directions()
    if not legal:
        # The protocol requires an action. Prefer facing direction if trapped.
        return ct.get_dir()

    here = ct.get_position()
    start = (here.x, here.y)
    targets = remembered_pearl_targets()
    bfs = bfs_first_step(start, set(targets), set(legal))
    if bfs is not None:
        return bfs

    echoes = ct.get_sonar_echoes()
    facing = ct.get_dir()
    reverse = facing.get_opposite()

    def score(direction: Direction) -> tuple[float, str]:
        nxt = neighbour(start, direction)
        edge_type = known_edges.get((start[0], start[1], direction.value), EdgeType.EMPTY)
        score_value = 0.0

        # Explicit target pursuit when memory knows a pearl coordinate but no complete
        # path is known yet.
        if targets:
            best = min(wrapped_distance(nxt, target) for target in targets)
            score_value -= 9.0 * best

        score_value -= 2.5 * visit_count.get(nxt, 0)
        if nxt not in seen_tiles:
            score_value += 12.0
        if direction == reverse:
            score_value -= 2.0
        if edge_type == EdgeType.PORTAL:
            score_value -= 4.0

        # Echoes describe the most recent facing sonar. Treat enemy heads as a risk
        # signal, not as hidden positional knowledge.
        if direction == facing:
            score_value -= 3.0 * int(getattr(echoes, "enemy_head", 0))
            score_value -= 0.5 * int(getattr(echoes, "kelp", 0))

        # Stable deterministic tie-break avoids host RNG dependence.
        return (score_value, direction.value)

    return max(legal, key=score)


def maybe_split() -> bool:
    length = ct.get_length()
    units = ct.get_unit_count()
    round_no = game.get_round_num()
    if round_no >= 320 or units >= min(4, ct.unit_limit) or length < 10:
        return False
    child_size = max(2, min(4, length // 3))
    if ct.can_split(child_size) and (round_no + ct.get_id() * 7) % 29 == 0:
        ct.do_split(child_size)
        return True
    return False


def maybe_sonar(direction: Direction) -> None:
    round_no = game.get_round_num()
    if round_no % 10 != (ct.get_id() % 10):
        return
    targets = remembered_pearl_targets()
    if not targets:
        return
    here = ct.get_position()
    target = min(targets, key=lambda p: wrapped_distance((here.x, here.y), p))
    message = SONAR_TAG | ((target[0] & 0x3F) << 6) | (target[1] & 0x3F)
    ct.send_sonar(direction, message)


def execute_turn() -> None:
    observe()
    if maybe_split():
        return
    direction = choose_move()
    maybe_sonar(direction)
    ct.make_move(direction)


def main() -> None:
    global ct, game
    ct, game = unswbc.init()
    while unswbc.update(ct, game):
        execute_turn()
        unswbc.end_turn()


if __name__ == "__main__":
    main()

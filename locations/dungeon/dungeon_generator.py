from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random

from factory.game_object_factory import GameObjectFactory
from locations.dungeon.dungeon_location import DungeonLevel
from locations.dungeon.utils import (
    Room,
    PlacementRule,
    Point,
    PlacementStrategy
)
from game.item.item_constants import GameObjectEnum
from context import get_application_context
from main_constants import GAME_OBJECT_FACTORY_CONTEXT_NAME

DEFAULT_RULES: list[PlacementRule] = [
    PlacementRule(GameObjectEnum.DUNGEON_ENTRANCE.value, PlacementStrategy.NEAR_ENTRANCE, unique=True, label="entrance"),
    PlacementRule(GameObjectEnum.DUNGEON_STAIRS_DOWN.value, PlacementStrategy.FARTHEST_FROM_ENTRANCE, unique=True, label="stairs_down"),
    PlacementRule("T_RARE_CHEST", PlacementStrategy.FARTHEST_FROM_ENTRANCE, unique=True, label="rare_chest"),
    PlacementRule(GameObjectEnum.SIMPLE_CHEST.value, PlacementStrategy.RANDOM_ROOM, chance=0.30, label="chest"),
    PlacementRule("T_DOOR", PlacementStrategy.CORRIDOR_ENTRANCE, chance=0.4, label="door"),
]

dungeon_stone_tile = GameObjectEnum.DUNGEON_STONE_TILE.value
dungeon_wall = GameObjectEnum.DUNGEON_WALL.value
cxt = get_application_context()
# game_factory: GameObjectFactory = cxt.get_context(GAME_OBJECT_FACTORY_CONTEXT_NAME)

@dataclass
class BSPNode:
    x: int
    y: int
    w: int
    h: int
    left: BSPNode | None = None
    right: BSPNode | None = None
    room: Room | None = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def split(self, min_size: int, rng: random.Random) -> bool:
        if not self.is_leaf:
            return False
        split_h = rng.random() > 0.5
        if self.w > self.h and self.w / self.h >= 1.25:
            split_h = False
        elif self.h > self.w and self.h / self.w >= 1.25:
            split_h = True
        max_size = (self.h if split_h else self.w) - min_size
        if max_size <= min_size:
            return False
        split_pos = rng.randint(min_size, max_size)
        if split_h:
            self.left = BSPNode(self.x, self.y, self.w, split_pos)
            self.right = BSPNode(self.x, self.y + split_pos, self.w, self.h - split_pos)
        else:
            self.left = BSPNode(self.x, self.y, split_pos, self.h)
            self.right = BSPNode(self.x + split_pos, self.y, self.w - split_pos, self.h)
        return True

    def get_leaves(self) -> list[BSPNode]:
        if self.is_leaf:
            return [self]
        return self.left.get_leaves() + self.right.get_leaves()

    def get_sibling_pairs(self) -> list[tuple[BSPNode, BSPNode]]:
        pairs: list[tuple[BSPNode, BSPNode]] = []
        if not self.is_leaf and self.left and self.right:
            ll = self.left.get_leaves()
            rl = self.right.get_leaves()
            if ll and rl:
                pairs.append((
                    min(ll, key=lambda n: n.room.center.x if n.room else 0),
                    min(rl, key=lambda n: n.room.center.x if n.room else 0),
                ))
            pairs += self.left.get_sibling_pairs()
            pairs += self.right.get_sibling_pairs()
        return pairs


class DungeonGenerator:
    """
    Params:
        width, height  — map size
        bsp_depth      — BSP depth
        min_room_size  — min room size
        max_room_size  — max room size
        rules          — list of the PlacementRule; None = DEFAULT_RULES
        seed           — seed; None = random
    """

    def __init__(
            self,
            width: int = 80,
            height: int = 40,
            bsp_depth: int = 4,
            min_room_size: int = 5,
            max_room_size: int = 12,
            rules: list[PlacementRule] | None = None,
            seed: int | None = None,
    ):
        self.width = width
        self.height = height
        self.bsp_depth = bsp_depth
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.rules = rules if rules is not None else DEFAULT_RULES
        self.rng = random.Random(seed)

    def generate(self,
                 width: int = 80,
                 height: int = 40,
                 bsp_depth: int = 4,
                 min_room_size: int = 5,
                 max_room_size: int = 12,
                 rules: list[PlacementRule] | None = None,
                 seed: int | None = None,
                 ) -> DungeonLevel:
        level = DungeonLevel(self.width, self.height)

        level.grid = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self._door_candidates: list[tuple[int, int]] = []
        self._room_floors_cache: set[tuple[int, int]] = set()

        root = BSPNode(0, 0, self.width, self.height)
        self._bsp_split(root, self.bsp_depth)
        self._build_rooms(root, level)

        for room in level.rooms:
            for p in room.floor_tiles:
                self._room_floors_cache.add((p.x, p.y))
        self._carve_corridors(root, level)
        self._place_walls(level)
        self._ensure_connectivity(level)
        self._apply_placement_rules(level)
        return level

    def _bsp_split(self, node: BSPNode, depth: int) -> None:
        if depth == 0:
            return
        if node.split(self.min_room_size + 2, self.rng):
            self._bsp_split(node.left, depth - 1)
            self._bsp_split(node.right, depth - 1)

    def _build_rooms(self, root: BSPNode, level: DungeonLevel) -> None:
        for leaf in root.get_leaves():
            rw = self.rng.randint(self.min_room_size, min(self.max_room_size, leaf.w - 2))
            rh = self.rng.randint(self.min_room_size, min(self.max_room_size, leaf.h - 2))
            rx = leaf.x + self.rng.randint(1, max(1, leaf.w - rw - 1))
            ry = leaf.y + self.rng.randint(1, max(1, leaf.h - rh - 1))
            room = Room(rx, ry, rw, rh)
            leaf.room = room
            level.rooms.append(room)
            for p in room.floor_tiles:
                level.grid[p.y][p.x] = [dungeon_stone_tile]

    def _carve_corridors(self, root: BSPNode, level: DungeonLevel) -> None:
        for la, lb in root.get_sibling_pairs():
            if la.room and lb.room:
                self._carve_tunnel(la.room.center, lb.room.center, level)

    def _carve_tunnel(self, a: Point, b: Point, level: DungeonLevel,
                      room_floors: set | None = None) -> None:
        rf = room_floors if room_floors is not None else self._room_floors_cache
        pivot = Point(b.x, a.y) if self.rng.random() > 0.5 else Point(a.x, b.y)
        door_spots: list[tuple[int, int]] = []
        self._carve_line(a.x, a.y, pivot.x, pivot.y, level, rf, door_spots)
        self._carve_line(pivot.x, pivot.y, b.x, b.y, level, rf, door_spots)
        self._door_candidates.extend(door_spots)

    def _carve_line(self, x1: int, y1: int, x2: int, y2: int, level: DungeonLevel,
                    room_floors: set | None = None,
                    door_spots: list | None = None) -> None:
        coords: list[tuple[int, int]] = []
        x, y = x1, y1
        while x != x2:
            coords.append((x, y))
            x += 1 if x2 > x else -1
        while y != y2:
            coords.append((x, y))
            y += 1 if y2 > y else -1
        coords.append((x2, y2))

        for cx, cy in coords:
            self._set_ground(cx, cy, level)

        if room_floors is None or door_spots is None:
            return

        for i, (cx, cy) in enumerate(coords):
            in_room = (cx, cy) in room_floors
            if i == 0:
                # prev_in_room = in_room
                continue
            prev_cx, prev_cy = coords[i - 1]
            prev_in_room_flag = (prev_cx, prev_cy) in room_floors
            if prev_in_room_flag and not in_room:
                door_spots.append((cx, cy))
            elif not prev_in_room_flag and in_room:
                door_spots.append((prev_cx, prev_cy))

    def _set_ground(self, x: int, y: int, level: DungeonLevel) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            if not level.grid[y][x]:
                level.grid[y][x] = [dungeon_stone_tile]

    def _place_walls(self, level: DungeonLevel) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if level.grid[y][x]:
                    continue
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if dungeon_stone_tile in level.grid[ny][nx]:
                            level.grid[y][x] = [dungeon_wall]
                            break

    def _valid_door_candidates(self, level: DungeonLevel) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        candidates = getattr(self, '_door_candidates', [])
        seen: set[tuple[int, int]] = set()

        for x, y in candidates:
            if (x, y) in seen:
                continue
            seen.add((x, y))
            if not (0 < x < self.width - 1 and 0 < y < self.height - 1):
                continue
            if level.grid[y][x] != [dungeon_stone_tile]:
                continue

            def is_wall(cx, cy, _x=x, _y=y):
                return level.grid[cy][cx] == [dungeon_wall]

            h_pinch = is_wall(x, y - 1) and is_wall(x, y + 1)
            v_pinch = is_wall(x - 1, y) and is_wall(x + 1, y)
            if h_pinch or v_pinch:
                result.append((x, y))

        return result

    def _ensure_connectivity(self, level: DungeonLevel) -> None:

        if not level.rooms:
            return
        reachable = self._bfs_reachable(level.rooms[0].center, level)

        for room in level.rooms[1:]:
            if room.center not in reachable:
                nearest = min(
                    [r for r in level.rooms if r.center in reachable],
                    key=lambda r: room.center.distance(r.center),
                )
                self._carve_tunnel(room.center, nearest.center, level)
                self._place_walls(level)
                reachable = self._bfs_reachable(level.rooms[0].center, level)

    def _bfs_reachable(self, start: Point, level: DungeonLevel) -> set[Point]:
        visited: set[Point] = set()
        q = deque([start])
        while q:
            p = q.popleft()
            if p in visited:
                continue
            if not (0 <= p.x < self.width and 0 <= p.y < self.height):
                continue
            if not level.is_passable(p.x, p.y):
                continue
            visited.add(p)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                q.append(Point(p.x + dx, p.y + dy))
        return visited

    def _bfs_distance_map(self, start: Point, level: DungeonLevel) -> dict[Point, int]:
        dist: dict[Point, int] = {}
        q = deque([(start, 0)])
        while q:
            p, d = q.popleft()
            if p in dist:
                continue
            if not (0 <= p.x < self.width and 0 <= p.y < self.height):
                continue
            if not level.is_passable(p.x, p.y):
                continue
            dist[p] = d
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                q.append((Point(p.x + dx, p.y + dy), d + 1))
        return dist

    def _apply_placement_rules(self, level: DungeonLevel) -> None:
        if not level.rooms:
            return

        entrance_room = level.rooms[0]
        entrance_pos: Point | None = None

        for rule in self.rules:
            if rule.obj == GameObjectEnum.DUNGEON_ENTRANCE.value:
                pos = self._pick_floor(entrance_room, level)
                if pos:
                    level.add(pos.x, pos.y, GameObjectEnum.DUNGEON_ENTRANCE.value) #Add object
                    entrance_pos = pos
                break

        if entrance_pos is None:
            entrance_pos = entrance_room.center

        dist_map = self._bfs_distance_map(entrance_pos, level)
        occupied: set[Point] = {entrance_pos} if entrance_pos else set()

        for rule in self.rules:
            if rule.obj == GameObjectEnum.DUNGEON_ENTRANCE.value:
                continue
            if rule.strategy == PlacementStrategy.FARTHEST_FROM_ENTRANCE:
                self._place_farthest(rule, level, dist_map, occupied, entrance_room)
            elif rule.strategy == PlacementStrategy.NEAR_ENTRANCE:
                self._place_near_entrance(rule, level, entrance_room, occupied)
            elif rule.strategy == PlacementStrategy.RANDOM_ROOM:
                self._place_random(rule, level, occupied, entrance_room)
            elif rule.strategy == PlacementStrategy.SPECIFIC_ROOM:
                self._place_specific(rule, level, occupied, entrance_room)
            elif rule.strategy == PlacementStrategy.CORRIDOR_ENTRANCE:
                self._place_corridor_entrances(rule, level)

    def _place_corridor_entrances(self, rule: PlacementRule, level: DungeonLevel) -> None:
        for x, y in self._valid_door_candidates(level):
            if self.rng.random() < rule.chance:
                level.add(x, y, rule.obj) # Add object

    def _place_farthest(self, rule, level, dist_map, occupied, entrance_room):
        def room_max_dist(r):
            return max((dist_map.get(p, 0) for p in r.floor_tiles), default=0)

        candidates = sorted(
            [r for r in level.rooms if r is not entrance_room],
            key=room_max_dist, reverse=True
        )
        placed = 0
        for room in candidates:
            tiles = sorted(room.floor_tiles, key=lambda p: dist_map.get(p, 0), reverse=True)
            for p in tiles:
                if p not in occupied:
                    level.add(p.x, p.y, rule.obj) # Add object
                    occupied.add(p)
                    placed += 1
                    break
            if rule.unique or (rule.count and placed >= rule.count):
                break

    def _place_near_entrance(self, rule, level, entrance_room, occupied):
        pos = self._pick_floor(entrance_room, level, occupied)
        if pos:
            level.add(pos.x, pos.y, rule.obj) # Add Object
            occupied.add(pos)

    def _place_random(self, rule, level, occupied, entrance_room):
        rooms = [r for r in level.rooms if r is not entrance_room]
        self._place(rooms, rule, level, occupied)

    def _place_specific(self, rule, level, occupied, entrance_room):
        rooms = [
            r for r in level.rooms
            if r is not entrance_room and (rule.room_filter is None or rule.room_filter(r))
        ]
        self._place(rooms, rule, level, occupied)

    def _place(self, rooms, rule, level, occupied):
        self.rng.shuffle(rooms)
        placed = 0
        for room in rooms:
            if self.rng.random() > rule.chance:
                continue
            pos = self._pick_floor(room, level, occupied)
            if pos:
                level.add(pos.x, pos.y, rule.obj) # Add Object
                occupied.add(pos)
                placed += 1
                if rule.unique or (rule.count and placed >= rule.count):
                    break

    def _pick_floor(self, room: Room, level: DungeonLevel, occupied: set | None = None) -> Point | None:
        tiles = list(room.floor_tiles)
        self.rng.shuffle(tiles)
        for p in tiles:
            if dungeon_stone_tile in level.grid[p.y][p.x]:
                if occupied is None or p not in occupied:
                    return p
        return None


def test_generate_dungeon() -> list:
    gen = DungeonGenerator(width=80, height=30, bsp_depth=10)
    dng = gen.generate()
    print(dng.grid)
    return dng.grid


if __name__ == '__main__':
    dung_list = test_generate_dungeon()
    for x in dung_list:
        for y in x:
            if y:
                print(y[-1][-1], end="")
            else:
                print(" ", end="")
            print(" ", end="")
        print()

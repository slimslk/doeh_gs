from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Callable


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def distance(self, other: Point) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass
class Room:
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self) -> Point:
        return Point(self.x + self.w // 2, self.y + self.h // 2)

    @property
    def floor_tiles(self) -> list[Point]:
        return [
            Point(x, y)
            for y in range(self.y + 1, self.y + self.h - 1)
            for x in range(self.x + 1, self.x + self.w - 1)
        ]


class PlacementStrategy(Enum):
    FARTHEST_FROM_ENTRANCE = auto()
    NEAR_ENTRANCE = auto()
    RANDOM_ROOM = auto()
    SPECIFIC_ROOM = auto()
    CORRIDOR_ENTRANCE = auto()


@dataclass
class PlacementRule:
    """
    object        — object name
    strategy    — placement strategy
    count       — max count (None = infinite)
    chance      — [0..1]
    unique      — unique for a room
    room_filter — predicate for a SPECIFIC_ROOM
    label       — debug name

    Example:
        # Door in every corridors entrance with chance 70%:
        PlacementRule(T_DOOR, PlacementStrategy.CORRIDOR_ENTRANCE, chance=0.7, label="door")

        # Unique rarest chest in the farthest room:
        PlacementRule(T_RARE_CHEST, PlacementStrategy.FARTHEST_FROM_ENTRANCE, unique=True)
    """
    obj: str
    strategy: PlacementStrategy
    count: int | None = None
    chance: float = 1.0
    unique: bool = False
    room_filter: Optional[Callable[[Room], bool]] = None
    label: str = ""

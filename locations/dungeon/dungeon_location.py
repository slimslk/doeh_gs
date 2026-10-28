from dataclasses import dataclass, field

from game.item.item_constants import GameObjectEnum
from locations.dungeon.utils import Room


class DungeonLocation:
    pass


@dataclass
class DungeonLevel:
    width: int
    height: int
    grid: list[list[list[str]]] = field(default_factory=list)
    rooms: list[Room] = field(default_factory=list)

    def get(self, x: int, y: int) -> list[str]:
        return self.grid[y][x]

    def has(self, x: int, y: int, tag: str) -> bool:
        return tag in self.grid[y][x]

    def add(self, x: int, y: int, tag: str) -> None:
        if tag not in self.grid[y][x]:
            self.grid[y][x].append(tag)

    def is_passable(self, x: int, y: int) -> bool:
        cell = self.grid[y][x]
        return GameObjectEnum.DUNGEON_STONE_TILE.value in cell

from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


@register_game_object(
    name=GameObjectEnum.DUNGEON_STONE_TILE,
    lifecycle=GameObjectLifecycleEnum.SINGLETON
)
class DungeonStoneTile(DefaultObject):
    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.name = GameObjectEnum.DUNGEON_STONE_TILE.value

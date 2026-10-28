from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


@register_game_object(
    name=GameObjectEnum.GRASS,
    lifecycle=GameObjectLifecycleEnum.SINGLETON
)
class Grass(DefaultObject):
    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.name = GameObjectEnum.GRASS.value
         
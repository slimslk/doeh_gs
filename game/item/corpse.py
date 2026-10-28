from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


@register_game_object(
    name=GameObjectEnum.CORPSE,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class Corpse(DefaultObject):
    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.name = GameObjectEnum.CORPSE.value
        self.hp = 40
        self.corpse_name = "default"

    def set_corpse_name(self, name):
        self.corpse_name = name

    def get_message(self):
        return f"{super().get_message()} - {self.corpse_name}"

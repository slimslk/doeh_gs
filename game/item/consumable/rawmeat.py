from random import randint

from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.consumable.consumable_obj import DefaultConsumableObject
from game.item.item_constants import GameObjectEnum
from message.consume_messages import CONSUME_MEAT_MESSAGE


@register_game_object(
    name=GameObjectEnum.RAW_MEAT,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class RawMeat(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_MEAT_MESSAGE[randint(0, len(CONSUME_MEAT_MESSAGE) - 1)]

    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.set_collectable(True)
        self.action = {"action": "decrease_hungry", "params": [200]}
        self.name = GameObjectEnum.RAW_MEAT.value
        self.hp = 10

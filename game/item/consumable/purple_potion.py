from random import randint

from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.consumable.consumable_obj import DefaultConsumableObject
from game.item.item_constants import GameObjectEnum
from message.consume_messages import CONSUME_SLEEPPOTION_MESSAGE


@register_game_object(
    name=GameObjectEnum.SLEEP_POTION,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class SleepPotion(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_SLEEPPOTION_MESSAGE[randint(0, len(CONSUME_SLEEPPOTION_MESSAGE) - 1)]

    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.set_collectable(True)
        self.set_consumable(True)
        self.action = {"action": "sleep", "params": []}
        self.name = GameObjectEnum.SLEEP_POTION.value
        self.hp = 5

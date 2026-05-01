from random import randint

from game.item.consumable.consumable_obj import DefaultConsumableObject
from game.item.consumable.consume_message_constants import CONSUME_SLEEPPOTION_MESSAGE


class SleepPotion(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_SLEEPPOTION_MESSAGE[randint(0, len(CONSUME_SLEEPPOTION_MESSAGE) - 1)]

    def __init__(self):
        super().__init__()
        self.set_collectable(True)
        self.set_consumable(True)
        self.action = {"action": "sleep", "params": []}
        self.name = "purple potion"
        self.hp = 5

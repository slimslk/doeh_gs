from random import randint

from game.item.consumable.consumable_obj import DefaultConsumableObject
from game.item.consumable.consume_message_constants import CONSUME_MEAT_MESSAGE


class Meat(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_MEAT_MESSAGE[randint(0, len(CONSUME_MEAT_MESSAGE) - 1)]

    def __init__(self):
        super().__init__()
        self.set_collectable(True)
        self.action = {"action": "decrease_hungry", "params": [200]}
        self.name = "meat"
        self.hp = 10

from random import randint

from game.item.consumable.consumable_obj import DefaultConsumableObject
from game.item.consumable.consume_message_constants import CONSUME_ENERGYPOTION_MESSAGE


class EnergyPotion(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_ENERGYPOTION_MESSAGE[randint(0, len(CONSUME_ENERGYPOTION_MESSAGE) - 1)]

    def __init__(self):
        super().__init__()
        self.set_collectable(True)
        self.set_consumable(True)
        self.action = {"action": "increase_energy", "params": [50]}
        self.name = "yellow potion"
        self.hp = 5

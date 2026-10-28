from random import randint

from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.consumable.consumable_obj import DefaultConsumableObject
from game.item.item_constants import GameObjectEnum
from message.consume_messages import CONSUME_ENERGYPOTION_MESSAGE


@register_game_object(
    name=GameObjectEnum.POOR_ENERGY_POTION,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class PoorEnergyPotion(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_ENERGYPOTION_MESSAGE[randint(0, len(CONSUME_ENERGYPOTION_MESSAGE) - 1)]

    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.set_collectable(True)
        self.set_consumable(True)
        self.action = {"action": "increase_energy", "params": [20]}
        self.name = GameObjectEnum.POOR_ENERGY_POTION.value
        self.hp = 5


@register_game_object(
    name=GameObjectEnum.DISTILLED_ENERGY_POTION,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class DistilledEnergyPotion(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_ENERGYPOTION_MESSAGE[randint(0, len(CONSUME_ENERGYPOTION_MESSAGE) - 1)]

    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.set_collectable(True)
        self.set_consumable(True)
        self.action = {"action": "increase_energy", "params": [50]}
        self.name = GameObjectEnum.DISTILLED_ENERGY_POTION.value
        self.hp = 5


@register_game_object(
    name=GameObjectEnum.MASTERWORK_ENERGY_POTION,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class MasterworkEnergyPotion(DefaultConsumableObject):
    def get_consume_message(self):
        return CONSUME_ENERGYPOTION_MESSAGE[randint(0, len(CONSUME_ENERGYPOTION_MESSAGE) - 1)]

    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.set_collectable(True)
        self.set_consumable(True)
        self.action = {"action": "increase_energy", "params": [100]}
        self.name = GameObjectEnum.MASTERWORK_ENERGY_POTION.value
        self.hp = 5

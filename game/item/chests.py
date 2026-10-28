from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


class OpenableObject(DefaultObject):
    """
    params structure: ("item_name",  drop_rate (%), max_quantity)
    """

    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.name = "openable object"
        self.set_solid(True)
        self.action = {"action": "open", "params": [(GameObjectEnum.DUMMY, 100, 1)]}
        self.is_open = False
        self.action_message = "You did something."

    def get_action_message(self):
        return self.action_message


@register_game_object(
    name=GameObjectEnum.SIMPLE_CHEST,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class SimpleChest(OpenableObject):
    """
    params structure: ("item_name",  drop_rate (%), max_quantity)
    """

    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.name = GameObjectEnum.SIMPLE_CHEST.value
        self.action = {"action": "open_chest", "params": [(GameObjectEnum.POOR_ENERGY_POTION, 50, 2),
                                                          (GameObjectEnum.SMALL_HEALTH_POTION, 15, 1),
                                                          (GameObjectEnum.SLEEP_POTION, 5, 1),
                                                          (GameObjectEnum.RUSTY_SWORD, 5, 1),
                                                          ]}
        self.action_message = ("The chest creaks open beneath your touch. What forgotten horror — or treasure — lies "
                               "within?")


@register_game_object(
    name=GameObjectEnum.OPENED_SIMPLE_CHEST,
    lifecycle=GameObjectLifecycleEnum.SINGLETON
)
class OpenedSimpleChest(DefaultObject):
    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.name = GameObjectEnum.OPENED_SIMPLE_CHEST.value
        self.action = {"action": "do_nothing"}

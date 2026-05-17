from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


class OpenableObject(DefaultObject):
    """
    params structure: ("item_name",  drop_rate (%), max_quantity)
    """

    def __init__(self):
        super().__init__()
        self.name = "openable object"
        self.set_solid(True)
        self.action = {"action": "open", "params": [(GameObjectEnum.DUMMY, 100, 1)]}
        self.is_open = False
        self.action_message = "You did something."

    def get_action_message(self):
        return self.action_message


class SimpleChest(OpenableObject):
    """
    params structure: ("item_name",  drop_rate (%), max_quantity)
    """

    def __init__(self):
        super().__init__()
        self.name = "simple chest"
        self.action = {"action": "open_chest", "params": [(GameObjectEnum.YELLOW_POTION, 50, 2),
                                                          (GameObjectEnum.RED_POTION, 15, 1),
                                                          (GameObjectEnum.PURPLE_POTION, 5, 1),
                                                          (GameObjectEnum.SWORD, 5, 1),
                                                          ]}
        self.action_message = "The chest creaks open beneath your touch. What forgotten horror — or treasure — lies within?"


class OpenedSimpleChest(DefaultObject):
    def __init__(self):
        super().__init__()
        self.name = "opened simple chest"
        self.action = {"action": "do_nothing"}

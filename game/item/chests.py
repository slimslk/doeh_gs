from game.item.def_object import DefaultObject
from game.item_constants import GameObjectEnum


class OpenableObject(DefaultObject):
    """
    params structure: ("item_name",  drop_rate (%), max_quantity)
    """

    def __init__(self):
        super().__init__()
        self.name = "openable_object"
        self.set_solid(True)
        self.action = {"action": "open", "params": [(GameObjectEnum.DUMMY, 100, 1)]}
        self.is_open = False


class SimpleChest(OpenableObject):
    """
    params structure: ("item_name",  drop_rate (%), max_quantity)
    """

    def __init__(self):
        super().__init__()
        self.name = "simple_chest"
        self.action = {"action": "open_chest", "params": [(GameObjectEnum.YELLOW_POTION, 50, 2),
                                                          (GameObjectEnum.RED_POTION, 15, 1),
                                                          (GameObjectEnum.PURPLE_POTION, 5, 1),
                                                          (GameObjectEnum.SWORD, 25, 1),
                                                          ]}


class OpenedSimpleChest(DefaultObject):
    def __init__(self):
        super().__init__()
        self.name = "opened_simple_chest"
        self.action = {"action": "do_nothing"}

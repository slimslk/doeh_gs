from abc import ABC, abstractmethod

from game.item.def_object import DefaultObject


class DefaultConsumableObject(DefaultObject, ABC):
    def __init__(self):
        super().__init__()
        self.set_consumable(True)

    @abstractmethod
    def get_consume_message(self):
        pass



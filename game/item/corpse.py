from game.item.def_object import DefaultObject


class Corpse(DefaultObject):
    def __init__(self):
        super().__init__()
        self.name = "corpse"
        self.hp = 40
        self.corpse_name = "default"

    def get_message(self):
        return f"{super().get_message()} - {self.corpse_name}"

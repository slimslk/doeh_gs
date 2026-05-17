from game.item.def_object import DefaultObject


class Weapon(DefaultObject):
    def __init__(self):
        super().__init__()
        self.set_collectable(True)
        self.hp = 100

    async def use(self, actor):
        self.__switch_weapon_action()

    def __switch_weapon_action(self):
        if self.action["action"] == "equip_weapon":
            self.action["action"] = "take_off_weapon"
            self.name += "*"
        else:
            self.action["action"] = "equip_weapon"
            self.name = self.name[:-1]


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.action = {"action": "equip_weapon", "params": [(1, 12)]}
        self.name = "sword"

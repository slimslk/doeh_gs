from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


class Weapon(DefaultObject):
    def __init__(self, interact_system):
        super().__init__(interact_system)
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


@register_game_object(
    name=GameObjectEnum.RUSTY_SWORD,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class RustySword(Weapon):
    def __init__(self, interact_system):
        super().__init__(interact_system)
        self.action = {"action": "equip_weapon", "params": [(1, 12)]}
        self.name = GameObjectEnum.RUSTY_SWORD.value

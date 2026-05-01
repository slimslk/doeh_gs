from game.item_messages import item_messages


class DefaultObject:
    _DESTROY_ACTION = {"action": "destroy_me", "params": None}

    def __init__(self):
        self.interact_system = None
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.id: int = 0
        self.name: str = "void"
        self.__is_solid: bool = False
        self.__is_collectable: bool = False
        self.__is_consumable: bool = False
        self.action: dict[str, object] = {"action": "do_nothing", "params": []}
        self.hp: int = -999
        self.world_map = None

    def get_world_map(self):
        return self.world_map

    def set_world_map(self, world_map):
        self.world_map = world_map

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_position(self) -> tuple[int, int]:
        return self.pos_x, self.pos_y

    async def decrease_hp(self, amount: int):
        if self.hp > 0:
            self.hp -= amount
            if self.hp <= 0:
                await self.interact_system.interact(self, None, self._DESTROY_ACTION)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def is_solid(self):
        return self.__is_solid

    def is_collectable(self):
        return self.__is_collectable

    def is_consumable(self):
        return self.__is_consumable

    def set_consumable(self, is_consumable: bool):
        self.__is_consumable = is_consumable

    def set_collectable(self, value: bool):
        self.__is_collectable = value

    def set_solid(self, value: bool):
        self.__is_solid = value

    def set_action(self, action: str):
        self.action = action

    async def use(self, actor):
        await self.interact_system.interact(actor, self, self.action)

    def get_message(self):
        return item_messages.get(self.name, item_messages["default"])

    def __str__(self):
        return f"{self.id}: {self.name} {self.action} {self.pos_x} {self.pos_y}"

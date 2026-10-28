from factory.decorators import register_game_object
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


class Entrance(DefaultObject):
    def __init__(self, interact_system, connected_map):
        super().__init__(interact_system)
        self.name = "entrance"
        self.set_solid(True)
        self.connected_map_id = connected_map
        self.action = {"action": "enter", "params": [self.connected_map_id]}

    def set_connected_map_id(self, connected_map_id):
        self.connected_map_id = connected_map_id

    def get_connected_map_id(self):
        return self.connected_map_id


@register_game_object(
    name=GameObjectEnum.DUNGEON_ENTRANCE,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class DungeonEntrance(Entrance):
    def __init__(self, interact_system, connected_map):
        super().__init__(interact_system, connected_map)
        self.name = GameObjectEnum.DUNGEON_ENTRANCE.value


@register_game_object(
    name=GameObjectEnum.DUNGEON_EXIT,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class DungeonExit(Entrance):
    def __init__(self, interact_system, connected_map):
        super().__init__(interact_system, connected_map)
        self.name = GameObjectEnum.DUNGEON_EXIT.value


@register_game_object(
    name=GameObjectEnum.DUNGEON_STAIRS_UP,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class DungeonStairsUp(Entrance):
    def __init__(self, interact_system, connected_map):
        super().__init__(interact_system, connected_map)
        self.name = GameObjectEnum.DUNGEON_STAIRS_UP.value
        self.set_solid(False)


@register_game_object(
    name=GameObjectEnum.DUNGEON_STAIRS_DOWN,
    lifecycle=GameObjectLifecycleEnum.PROTOTYPE
)
class DungeonStairsUp(Entrance):
    def __init__(self, interact_system, connected_map):
        super().__init__(interact_system, connected_map)
        self.name = GameObjectEnum.DUNGEON_STAIRS_DOWN.value
        self.set_solid(False)

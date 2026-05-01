import uuid

from game.item.def_object import DefaultObject


class Map:
    __DEFAULT_SIZE = 10
    __observers = set()
    __map_width = 0
    __map_height = 0

    def __init__(self, loc_map=None):
        if loc_map is None:
            loc_map = [[[] for _ in range(self.__DEFAULT_SIZE)] for _ in range(self.__DEFAULT_SIZE)]
        self.location_map = loc_map
        self.__map_width = len(loc_map[0])
        self.__map_height = len(loc_map)
        self.map_id = str(uuid.uuid4())

    def add_observer(self, observer):
        self.__observers.add(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)

    def get_map(self):
        return self.location_map

    def set_map(self, init_map):
        self.location_map = init_map

    def get_map_size(self):
        return self.__map_height, self.__map_width

    def get_first_object(self, x, y):
        return self.location_map[x][y][0]

    def get_objects(self, x, y):
        return self.location_map[x][y]

    async def notify_observers(self, data):
        for observer in self.__observers:
            await observer.update(data)

    async def remove_first_object(self, x: int, y: int):
        if len(self.location_map[x][y]) == 1:
            return None
        removed_obj = self.location_map[x][y].pop(0)
        await self.notify_observers({
            self.map_id: {f"{x},{y}": self.location_map[x][y][0].name}
        })
        return removed_obj

    async def remove_object_from_map(self, x, y, rm_item: DefaultObject):
        objects = self.location_map[x][y]
        for item in objects:
            if item == rm_item:
                self.location_map[x][y].remove(item)
        await self.notify_observers({
            self.map_id: {f"{x},{y}": self.location_map[x][y][0].name}
        })

    async def place_game_object(self, object_type, x, y):
        self.location_map[x][y].insert(0, object_type)
        await self.notify_observers({
            self.map_id: {f"{x},{y}": self.location_map[x][y][0].name}
        })
        # await self.place_objects([object_type], x, y)

    async def place_game_objects(self, objects: list, x, y):
        for game_obj in objects:
            game_obj.set_position(x, y)
            await self.place_game_object(game_obj, x, y)
        # self.location_map[x][y][:0] = objects
        # await self.notify_observers({
        #     self.map_id: {f"{x},{y}": self.location_map[x][y][0].name}
        # })

    async def replace_object(self, game_object: DefaultObject, x, y, position=0):
        self.location_map[x][y].pop(0)
        self.location_map[x][y].insert(position, game_object)
        await self.notify_observers({
            self.map_id: {f"{x},{y}": self.location_map[x][y][0].name}
        })

    async def move_player(self, player, old_x, old_y, new_x, new_y):
        self.location_map[new_x][new_y].insert(0, player)
        self.location_map[old_x][old_y].pop(0)
        await self.notify_observers({
            self.map_id: {f"{old_x},{old_y}": self.location_map[old_x][old_y][0].name,
                          f"{new_x},{new_y}": player.name}
        })

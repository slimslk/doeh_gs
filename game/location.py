from errors.errors import ObjectPositionIsOutOfBoundsError, PositionIsOccupiedError, PlayerPositionIsOutOfBoundsError
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum
from game.map import Map
from game.player.player import Player
from context import get_application_context
from main_constants import GAME_OBJECT_FACTORY_CONTEXT_NAME, INTERATION_SYSTEM_CONTEXT_NAME


class Location:
    def __init__(self, location_map: Map, name: str = "default"):
        self.__location_name = name
        self.__location_map: Map = location_map
        self.__players = {}
        self.__location_height = len(location_map.location_map)
        self.__location_width = len(location_map.location_map[0])
        self.__game_object_factory = get_application_context().get_context(GAME_OBJECT_FACTORY_CONTEXT_NAME)  #TODO: refactoring -> inject GameObjectFactory instead direct call

    def get_map(self) -> Map:
        return self.__location_map

    def get_location_size(self) -> tuple[int, int]:
        return self.__location_height, self.__location_width

    async def add_player(self, player: Player, x, y):
        if x > self.__location_height or y > self.__location_width:
            raise PlayerPositionIsOutOfBoundsError(
                f"Location ID: {self.__location_map.map_id}\n x = {x}, y = {y} out of bounds"
                f" max_x = {self.__location_height} max_y = {self.__location_width}")
        player.location = self
        await self.__location_map.place_game_object(player, x, y)
        player.set_position(x, y)
        self.__players[player.char_id] = player

    async def remove_player(self, player: Player):
        char_id = player.char_id
        if char_id in self.__players:
            del self.__players[char_id]

    async def spawn_and_replace_object_on_map(self, game_obj_type: GameObjectEnum, pos_x, pos_y, position):
        self.__check_if_coordinates_in_bounds(pos_x, pos_y, game_obj_type)
        game_object: "DefaultObject" = self.__game_object_factory.get(game_obj_type)
        game_object.interact_system = get_application_context().get_context(INTERATION_SYSTEM_CONTEXT_NAME)
        await self.replace_object_on_map(game_object, pos_x, pos_y, position)

    async def spawn_and_replace_top_object_on_map(self, game_obj_type: GameObjectEnum, pos_x, pos_y):
        await self.spawn_and_replace_object_on_map(game_obj_type, pos_x, pos_y, position=0)

    async def replace_object_on_map(self, game_obj: DefaultObject, pos_x, pos_y, position):
        game_obj.world_map = self.__location_map
        await self.__location_map.replace_object(game_obj, pos_x, pos_y, position)

    async def place_object_on_map(self, game_obj: DefaultObject, pos_x, pos_y):
        self.__check_if_coordinates_in_bounds(pos_x, pos_y, GameObjectEnum(game_obj.name))
        game_obj.world_map = self.__location_map
        await self.__location_map.place_game_object(game_object=game_obj, x=pos_x, y=pos_y)

    async def create_add_object_to_map(self, game_obj_type: GameObjectEnum, pos_x: int, pos_y: int):
        self.__check_if_coordinates_in_bounds(pos_x, pos_y, game_obj_type)
        obj_on_map = self.__location_map.get_first_object(pos_x, pos_y)
        if obj_on_map.is_solid():
            raise PositionIsOccupiedError(f"x = {pos_x}, y = {pos_y} is occupied by {obj_on_map.name}!")
        game_object = self.__game_object_factory.get(game_obj_type)
        game_object.world_map = self.__location_map  # Thoughts - do I need a world map field in the game object?
        await self.__location_map.place_game_object(game_object, pos_x, pos_y)
        game_object.set_position(pos_x, pos_y)

    async def remove_object_from_world(self, game_object: "DefaultObject", pos_x: int, pos_y: int):
        self.__check_if_coordinates_in_bounds(pos_x, pos_y, game_object)
        await self.__location_map.remove_object_from_map(pos_x, pos_y, game_object)

    def get_players(self):
        return self.__players

    def __check_if_coordinates_in_bounds(self, pos_x, pos_y, game_object_type):
        if pos_x > self.__location_height or pos_y > self.__location_width:
            raise ObjectPositionIsOutOfBoundsError(
                f"{game_object_type.value}: "
                f"Location ID: {self.__location_map.map_id}\n x = {pos_x}, y = {pos_y} out of bounds"
                f" max_x = {self.__location_height} max_y = {self.__location_width}")

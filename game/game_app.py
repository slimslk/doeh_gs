import threading
import random

from context import GameContext
from errors.errors import GameObjectNotFoundError
from game.item.def_object import DefaultObject
from game.location import Location
from game.game_observer import GameObjectObserver
from game.map import Map
from game.player.player import Player
from game.player.player_controller import PlayerController
from locations.location_generator import generate_main_location
from game.item.item_constants import game_objects_list, GameObjectEnum


class Main:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    _PLAYER_OBSERVER_NAME = "player_observer"
    _MAP_OBSERVER_NAME = "map_observer"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._context: GameContext | None = None
            self.locations: dict[str, Location] = {}  # key - map_id
            self.users_player_controllers: dict[str, PlayerController] = {}
            self.character_player_controllers: dict[str, PlayerController] = {}
            self.main_location: Location | None = None
            self.users: dict[str: bool] = {}
            self.observers: dict[str, set] = {}

            Main._initialized = True

    @property
    def context(self) -> GameContext:
        return self._context

    @context.setter
    def context(self, context: GameContext):
        self._context = context

    def add_user(self, user_id: str):
        self.users[user_id] = False

    def clear_users(self):
        self.users = {}

    def lock_user(self, user_id: str):
        self.users[user_id] = True

    def unlock_all_users(self):
        for user_id in self.users:
            self.unlock_user(user_id)

    def unlock_user(self, user_id: str):
        self.users[user_id] = False

    def check_is_user_present(self, user_id) -> bool:
        return user_id in self.users

    async def generate_main_location(self) -> Location:
        main_location = await generate_main_location(context=self.context)
        for observer in self.observers.get(self._MAP_OBSERVER_NAME):
            main_location.get_map().add_observer(observer)
        self.add_location(main_location)
        self.main_location = main_location
        return self.main_location

    async def add_object_to_game_map(self, obj, map_id, pos_x, pos_y):
        location = self.get_location(map_id)
        if isinstance(obj, GameObjectEnum):
            game_object = game_objects_list.get(obj, None)
            if game_object:
                obj = game_object()
        if obj:
            obj.interact_system = self.context.interaction_system
            await location.add_object_to_world(obj, pos_x, pos_y)
        else:
            raise GameObjectNotFoundError(obj)

    async def replace_top_object(self, obj, map_id, pos_x, pos_y):
        location = self.get_location(map_id)
        if isinstance(obj, DefaultObject):
            obj.interact_system = self.context.interaction_system
            await location.replace_top_object(obj, pos_x, pos_y)

    async def remove_object_from_game_map(self, game_object, game_map: Map, pos_x, pos_y):
        location = self.get_location(game_map.map_id)
        if location:
            await location.remove_object_from_world(game_object, pos_x, pos_y)

    def get_locations(self):
        return [location for location in self.locations.keys()]

    def get_location(self, map_id):
        return self.locations.get(map_id, self.main_location)

    def add_location(self, location):  # TODO Nur hier benutz man dieses Funktion
        self.locations[location.get_map().map_id] = location

    async def create_player(self, name, user_id) -> Player:
        max_height, max_width = self.main_location.get_location_size()
        player = self.__create_default_player(name, user_id)
        player.world = self.main_location.get_map()

        player_coordinates = (random.randint(0, max_width - 1), random.randint(0, max_height - 1))

        if self.main_location.get_map().get_first_object(*player_coordinates).is_solid():
            player_coordinates = self.__find_free_spot(*player_coordinates, location=self.main_location)
        player.pos_x = player_coordinates[0]
        player.pos_y = player_coordinates[1]
        return player

    async def return_character_to_game(self, player: Player, location_id) -> Player:
        location: Location = self.get_location(location_id)
        player_on_map: Player = location.get_players().get(player.char_id, None)

        if not player_on_map:
            player.world = location.get_map()
            observers = self.observers.get(self._PLAYER_OBSERVER_NAME, None)
            if observers:
                for observer in observers:
                    player.add_observer(observer)

            position = (player.pos_x, player.pos_y)
            game_object_on_map = location.get_map().get_first_object(*position)
            if not isinstance(game_object_on_map, Player) or game_object_on_map.char_id != player.char_id:
                if location.get_map().get_first_object(*position).is_solid():
                    position = self.__find_free_spot(*position, location=location)
                await self.add_player_to_location(player, *position,
                                                  map_id=self.get_location(player.world.map_id))
            player_on_map = player
        await self.create_player_controller(player_on_map)
        return player_on_map

    def __find_free_spot(self, start_pos_x: int, start_pos_y: int, location: Location, min_radius=-1) -> tuple[int, int]:
        if min_radius == -1:
            max_x, max_y = location.get_location_size()
            min_radius = min(max_x, max_y)
        for radius in range(1, min_radius + 1):

            for dx in range(-radius, radius + 1):
                for dy in (-radius, radius):
                    x = start_pos_x + dx
                    y = start_pos_y + dy

                    if 0 <= x < max_x and 0 <= y < max_y:
                        if not location.get_map().get_first_object(x, y).is_solid():
                            return x, y

            for dy in range(-radius + 1, radius):
                for dx in (-radius, radius):
                    x = start_pos_x + dx
                    y = start_pos_y + dy

                    if 0 <= x < max_x and 0 <= y < max_y:
                        if not location.get_map().get_first_object(x, y).is_solid():
                            return x, y

        raise RuntimeError("No free position found on the map")

    def __create_default_player(self, name: str, user_id: str) -> Player:
        player = Player(user_id, name, self.context.interaction_system)
        observers = self.observers.get(self._PLAYER_OBSERVER_NAME, None)
        if observers:
            for observer in observers:
                player.add_observer(observer)
        return player

    async def create_player_controller(self, player: Player) -> PlayerController:
        player_controller = PlayerController(player)
        self.users_player_controllers[player.user_id] = player_controller
        return player_controller

    def remove_user(self, user_id: str):
        self.users.pop(user_id, None)
        player_controller = self.users_player_controllers.pop(user_id, None)
        player_controller.get_player().is_active = False
        self.character_player_controllers[player_controller.get_player().name] = player_controller

    async def assign_character_to_user(self, user_id: str, char_name: str):
        player_controller = self.character_player_controllers.pop(char_name, None)
        if player_controller:
            self.users_player_controllers[user_id] = player_controller

    async def get_player_controller_by_user_id(self, user_id: str) -> PlayerController | None:
        return await self.__get_player_controller_by_user_id(user_id)

    async def get_player_controller_by_char_name(self, char_name: str) -> PlayerController | None:
        return await self.__get_player_controller_by_char_name(char_name)

    async def add_player_to_location(self, player, pos_x, pos_y, map_id):
        location = self.__check_if_location_exists(map_id)
        await location.add_player(player, pos_x, pos_y)

    async def remove_player_from_location(self, player: Player, location_id):
        location = self.__check_if_location_exists(location_id)
        await location.remove_player(player)

    def add_map_observer(self, observer: GameObjectObserver):
        self.observers.setdefault(self._MAP_OBSERVER_NAME, set()).add(observer)

    def remove_map_observer(self, observer: GameObjectObserver):
        self.observers.get(self._MAP_OBSERVER_NAME).remove(observer)

    def add_player_observer(self, observer: GameObjectObserver):
        self.observers.setdefault(self._PLAYER_OBSERVER_NAME, set()).add(observer)

    def remove_player_observer(self, observer: GameObjectObserver):
        self.observers.get(self._PLAYER_OBSERVER_NAME).remove(observer)

    def __check_if_location_exists(self, location_id) -> Location:
        location = self.locations.get(location_id, None)
        if location is None:
            # TODO: Temporarily, fall back to the main locations if the locations is missing. Later this will be replaced
            #  with restoring the locations from storage.
            location = self.main_location
            # raise LocationNotFoundError(location_id)
        return location

    async def __get_player_controller_by_char_name(self, char_name: str) -> PlayerController | None:
        return self.character_player_controllers.get(char_name, None)

    async def __get_player_controller_by_user_id(self, user_id: str) -> PlayerController | None:
        return self.users_player_controllers.get(user_id, None)

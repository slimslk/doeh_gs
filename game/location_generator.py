import copy
import random

from context import GameContext
from errors.errors import PositionIsOccupiedError
from game.item.chests import SimpleChest
from game.item.dummy import Dummy
from game.item.grass import Grass
from game.item.consumable.meat import Meat
from game.item.tree import Tree
from game.location import Location
from game.map import Map


async def add_objects_to_map_in_random_places(main_game, map_id, object_type, amount: int):
    i = 0
    tries = 0
    max_tries = 10
    while i < amount:
        tries += 1
        obj = copy.copy(object_type)
        loc_len, loc_width = main_game.get_location(map_id).get_location_size()
        pos_x = random.randint(0, loc_len - 1)
        pos_y = random.randint(0, loc_width - 1)
        try:
            await main_game.add_object_to_game_map(obj, map_id, pos_x, pos_y)
        except PositionIsOccupiedError:
            if tries > max_tries:
                i += 1
            continue
        i += 1


async def generate_main_location(context: GameContext) -> Location:
    main_game = context.main_game
    location_height = 150
    location_width = 150
    tree_coefficient = 0.2
    meet_coefficient = 0.01
    dummy_coefficient = 0.002
    simple_chest_coefficient = 0.008
    main_location = await generate_location(location_height, location_width, "Aisuron")
    map_id = main_location.get_map().map_id
    main_game.add_location(main_location)
    tree = Tree()
    await add_objects_to_map_in_random_places(main_game, map_id, tree,
                                              int(location_height * location_width * tree_coefficient))
    meat = Meat()
    await add_objects_to_map_in_random_places(main_game, map_id, meat,
                                              int(location_height * location_width * meet_coefficient))
    dummy = Dummy()
    await add_objects_to_map_in_random_places(main_game, map_id, dummy,
                                              int(location_height * location_width * dummy_coefficient))
    simple_chest = SimpleChest()
    await add_objects_to_map_in_random_places(main_game, map_id, simple_chest,
                                              int(location_height * location_width * simple_chest_coefficient))
    return main_location


async def generate_location(height: int, width: int, name: str) -> Location:
    grass_map = [[[Grass()] for _ in range(width)] for _ in range(height)]
    main_map = Map(grass_map)
    location = Location(main_map, name)
    return location

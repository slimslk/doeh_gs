import random

from context import GameContext
from errors.errors import PositionIsOccupiedError
from game.item.item_constants import GameObjectEnum
from game.location import Location
from game.map import Map
from main_constants import GAME_OBJECT_FACTORY_CONTEXT_NAME, MAIN_GAME_CONTEXT_NAME


async def add_objects_to_map_in_random_places(main_game, map_id, object_type: GameObjectEnum, amount: int):
    i = 0
    tries = 0
    max_tries = 10
    while i < amount:
        tries += 1
        loc_len, loc_width = main_game.get_location(map_id).get_location_size()
        pos_x = random.randint(0, loc_len - 1)
        pos_y = random.randint(0, loc_width - 1)
        try:
            await main_game.add_object_to_game_map(object_type, map_id, pos_x, pos_y)
        except PositionIsOccupiedError:
            if tries > max_tries:
                i += 1
            continue
        i += 1


async def generate_main_location(context: GameContext) -> Location:
    main_game = context.get_context(MAIN_GAME_CONTEXT_NAME)
    location_height = 150
    location_width = 150
    tree_coefficient = 0.2
    meet_coefficient = 0.01
    dummy_coefficient = 0.002
    simple_chest_coefficient = 0.008
    main_location = await generate_location(location_height, location_width, "Aisuron", context)
    map_id = main_location.get_map().map_id
    main_game.add_location(main_location)
    await add_objects_to_map_in_random_places(main_game, map_id, GameObjectEnum.TREE,
                                              int(location_height * location_width * tree_coefficient))
    await add_objects_to_map_in_random_places(main_game, map_id, GameObjectEnum.RAW_MEAT,
                                              int(location_height * location_width * meet_coefficient))
    await add_objects_to_map_in_random_places(main_game, map_id, GameObjectEnum.DUMMY,
                                              int(location_height * location_width * dummy_coefficient))
    await add_objects_to_map_in_random_places(main_game, map_id, GameObjectEnum.SIMPLE_CHEST,
                                              int(location_height * location_width * simple_chest_coefficient))
    return main_location


async def generate_location(height: int, width: int, name: str, context: GameContext) -> Location:
    grass_obj = context.get_context(GAME_OBJECT_FACTORY_CONTEXT_NAME).get(GameObjectEnum.GRASS)
    grass_map = [[[grass_obj] for _ in range(width)] for _ in range(height)]
    main_map = Map(grass_map)
    location = Location(main_map, name)
    return location

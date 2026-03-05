import json

from game.item.def_object import DefaultObject
from game.player import Player
from models.models import CharStats, Character, GameObject
from game.item.constants import game_object_list


def player_stats_to_stats_model(player: Player) -> CharStats:
    return CharStats(
        health=player.health,
        energy=player.energy,
        hungry=player.hungry,
        position_x=player.pos_x,
        position_y=player.pos_y,
        # inventory=player.inventory,
        location_id=player.world.map_id,
        attack_modifier=player.attack_modifier,
        attack_damage=player.attack_damage,
        defence=player.defence,
        is_dead=player.is_dead,
    )


def player_to_player_model(player: Player) -> Character:
    return Character(
        name=player.name,
        user_id=player.user_id,
    )


def inventory_to_model(inventory: list[DefaultObject]) -> list[GameObject]:
    return [game_object_to_model(game_obj) for game_obj in inventory]


def game_object_to_model(game_obj: DefaultObject):
    return GameObject(
        name=game_obj.name,
        pos_x=game_obj.pos_x,
        pos_y=game_obj.pos_y,
        is_solid=game_obj.is_solid(),
        is_collectable=game_obj.is_collectable(),
        is_consumable=game_obj.is_consumable(),
        action=game_obj.action,
        hp=game_obj.hp,
    )


def game_object_model_to_game_object(game_obj: GameObject) -> DefaultObject:
    name = game_obj.name
    obj: DefaultObject = game_object_list.get(name, DefaultObject)()
    obj.pos_x = game_obj.pos_x
    obj.pos_y = game_obj.pos_y
    obj.id = game_obj.id
    obj.name = game_obj.name
    obj.__is_solid = game_obj.is_solid
    obj.__is_collectable = game_obj.is_collectable
    obj.__is_consumable = game_obj.is_consumable
    obj.action = game_obj.action
    obj.hp = game_obj.hp
    return obj


def game_objects_to_inventory(game_objects: list[GameObject]) -> list[DefaultObject]:
    return [game_object_model_to_game_object(game_obj) for game_obj in game_objects]


def character_model_to_player(character: Character) -> Player:
    player = Player(character.user_id, character.name)
    player.char_id = character.id
    player.health = character.stats.health
    player.pos_x = character.stats.position_x
    player.pos_y = character.stats.position_y
    player.energy = character.stats.energy
    player.hungry = character.stats.hungry
    player.direction = (0, -1)
    player.inventory = game_objects_to_inventory(character.stats.inventory)
    player.is_dead = character.stats.is_dead
    player.defence = character.stats.defence
    player.attack_modifier = character.stats.attack_modifier
    player.attack_damage = character.stats.attack_damage
    return player

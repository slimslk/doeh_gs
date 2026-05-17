from enum import Enum

from game.item.corpse import Corpse
from game.item.dummy import Dummy
from game.item.grass import Grass
from game.item.consumable.meat import Meat
from game.item.consumable.purple_potion import SleepPotion
from game.item.consumable.red_potion import HealthPotion
from game.item.sword import Sword
from game.item.tree import Tree
from game.item.consumable.yellow_potion import EnergyPotion


class GameObjectEnum(Enum):
    CORPSE = "corpse"
    DUMMY = "dummy"
    GRASS = "grass"
    MEAT = "meat"
    PURPLE_POTION = "purple potion"
    RED_POTION = "red potion"
    SWORD = "sword"
    TREE = "tree"
    YELLOW_POTION = "yellow potion"


game_objects_list = {
    GameObjectEnum.CORPSE: Corpse,
    GameObjectEnum.DUMMY: Dummy,
    GameObjectEnum.GRASS: Grass,
    GameObjectEnum.MEAT: Meat,
    GameObjectEnum.PURPLE_POTION: SleepPotion,
    GameObjectEnum.RED_POTION: HealthPotion,
    GameObjectEnum.SWORD: Sword,
    GameObjectEnum.TREE: Tree,
    GameObjectEnum.YELLOW_POTION: EnergyPotion,
}

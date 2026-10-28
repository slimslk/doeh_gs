from dataclasses import dataclass

from factory.lifecycle import GameObjectLifecycleEnum
from game.item.def_object import DefaultObject
from game.item.item_constants import GameObjectEnum


@dataclass(frozen=True)
class ObjectDescriptor:
    game_object_class: DefaultObject
    name: GameObjectEnum
    lifecycle: GameObjectLifecycleEnum

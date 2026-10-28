from factory.descriptors import ObjectDescriptor
from factory.lifecycle import GameObjectLifecycleEnum
from game.item.item_constants import GameObjectEnum
from factory.registry import desc_registry


def register_game_object(name: GameObjectEnum, lifecycle: GameObjectLifecycleEnum):
    def decorator(cls):
        desc_registry.add(ObjectDescriptor(cls, name=name, lifecycle=lifecycle))
        return cls

    return decorator

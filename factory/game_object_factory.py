from errors.errors import UnknownGameObjectError
# from factory.descriptors import ObjectDescriptor
from factory.lifecycle import GameObjectLifecycleEnum
# from game.item.def_object import DefaultObject
# from game.item.item_constants import GameObjectEnum


class GameObjectFactory:
    registry: "dict[GameObjectEnum, ObjectDescriptor]" = {}
    singleton_objects_registry: "dict[GameObjectEnum, DefaultObject]" = {}

    def __init__(self, interact_system):
        self.interact_system = interact_system

    def register(self, obj_descriptor: "ObjectDescriptor"):
        self.registry[obj_descriptor.name] = obj_descriptor

    def get(self, name: "GameObjectEnum") -> "DefaultObject":
        object_descriptor = self.registry.get(name)
        if object_descriptor is None:
            raise UnknownGameObjectError(name)

        if object_descriptor.lifecycle == GameObjectLifecycleEnum.SINGLETON:
            if object_descriptor.name not in self.singleton_objects_registry:
                game_object = object_descriptor.game_object_class(self.interact_system)
                self.singleton_objects_registry[object_descriptor.name] = game_object
                return game_object
            else:
                return self.singleton_objects_registry[object_descriptor.name]
        if object_descriptor.lifecycle == GameObjectLifecycleEnum.PROTOTYPE:
            return object_descriptor.game_object_class(self.interact_system)

    def is_registered(self, name: "GameObjectEnum") -> bool:
        return self.registry.get(name, None) is None

    def get_object_descriptor(self, name: "GameObjectEnum") -> "ObjectDescriptor":
        obj_descriptor = self.registry.get(name)
        if obj_descriptor is None:
            raise UnknownGameObjectError(name)
        return obj_descriptor

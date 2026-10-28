from factory.descriptors import ObjectDescriptor
from factory.game_object_factory import GameObjectFactory


class GameObjectDescriptorRegistry:
    def __init__(self):
        self._pending: list[ObjectDescriptor] = []

    def add(self, descriptor: ObjectDescriptor):
        self._pending.append(descriptor)

    def bind_to_factory(self, factory: GameObjectFactory):
        for desc in self._pending:
            factory.register(desc)
        self._pending.clear()


desc_registry = GameObjectDescriptorRegistry()

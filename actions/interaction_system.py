import random
from abc import ABC, abstractmethod
from typing import Any

from actions.actions import OBJECT_ACTIONS, PLAYER_ACTIONS, ITEM_ACTIONS
from context import GameContext
from game.item.chests import OpenableObject, OpenedSimpleChest
from game.map import Map


class DefaultInteractionSystem(ABC):
    def __init__(self):
        self._context: GameContext | None = None

    @property
    def context(self) -> GameContext:
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @abstractmethod
    async def interact(self, actor, target, action: dict[str, Any]):
        pass


class GameInteractionSystem(DefaultInteractionSystem):

    async def interact(self, actor, target, action: dict[str, Any]):
        action_string = action.get("action")
        if action_string in OBJECT_ACTIONS:
            return await self.__do_object_action(actor, target, action_string)
        if action_string in PLAYER_ACTIONS:
            if hasattr(actor, "do_action"):
                return await actor.do_action(action)
        if action_string in ITEM_ACTIONS:
            await self.__item_actions(actor, target, action)

    async def __item_actions(self, actor, item, action: dict[str, Any]):
        if action["action"] in ["equip_weapon", "take_off_weapon"]:
            action_str = action["action"]
            params = action["params"][0]

            if action_str == "equip_weapon":
                await actor.equip_weapon(item, params)
            if action_str == "take_off_weapon":
                await actor.take_off_weapon(item, params)
            await item.use(actor)
        else:
            if hasattr(actor, "do_action"):
                return await actor.do_action(action)

    async def __do_object_action(self, actor, target, action: str):
        if action == "destroy_me":
            return await self.__destroy_object(actor)
        if action == "open_chest":
            message = await self.__open_object(target)
            actor.messages.append(message)
            return

    async def __destroy_object(self, actor) -> str | None:
        game_map: Map = getattr(actor, "world_map", None)
        if game_map:
            await self.context.main_game.remove_object_from_game_map(actor, game_map, actor.pos_x, actor.pos_y)
        else:
            return
        return "destroyed"

    async def __open_object(self, target) -> str | None:
        if isinstance(target, OpenableObject) and not target.is_open:
            game_map: Map = getattr(target, "world_map", None)
            if not game_map:
                return
            map_id = game_map.map_id
            await self.context.main_game.replace_top_object(OpenedSimpleChest(), map_id, target.pos_x, target.pos_y)
            for item, drop_rate, quantity in target.action["params"]:
                if quantity > 0:
                    for _ in range(quantity):
                        drop_chance = random.randint(0, 100)
                        if drop_chance <= drop_rate:
                            await self.context.main_game.add_object_to_game_map(item, map_id, target.pos_x,
                                                                                target.pos_y)

        return target.get_action_message()

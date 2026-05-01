from typing import ClassVar, Literal

from actions.base_action_dto import BaseActionDto


class DestroyMe(BaseActionDto):
    action: Literal["destroy_me"]


class OpenChest(BaseActionDto):
    action: Literal["open_chest"]
    params: tuple[str, int, int]


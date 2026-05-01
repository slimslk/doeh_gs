from pydantic import Field, BaseModel
from typing_extensions import Annotated

from actions.base_action_dto import BaseActionDto
from typing import Literal, Sequence

move_actions = Literal["move_up", "move_down", "move_left", "move_right"]
BoundedInt = Annotated[int, Field(ge=-1, le=1)]
Direction = Annotated[Sequence[BoundedInt], Field(min_length=2, max_length=2)]


class MovePlayerActionDTO(BaseActionDto):
    action: move_actions
    params: tuple[Annotated[int, Field(gte=0)]] | None


class MovePlayerWithDirectionActionDTO(BaseModel):
    action: Literal["move"]
    params: tuple[Direction, int] | tuple[Direction]


class InteractActionDTO(BaseActionDto):
    action: Literal["interact"]
    params: Direction | None = None


class ListItemsActionDTO(BaseActionDto):
    action: Literal["list_items"]
    params: tuple[Annotated[int, Field(gte=0)]] | None


class UseItemActionDTO(BaseActionDto):
    action: Literal["use_item"]
    params: tuple[Annotated[int, Field(gte=0)]] | None


class AttackActionDTO(BaseActionDto):
    action: Literal["attack"]
    params: Direction | None


class SkipTurnActionDTO(BaseActionDto):
    action: Literal["skip_turn"]


class AwakeTurnActionDTO(BaseActionDto):
    action: Literal["awake"]

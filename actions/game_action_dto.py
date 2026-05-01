from typing import Literal, Annotated

from pydantic import Field

from actions.base_action_dto import BaseActionDto


class CreatePlayerActionDTO(BaseActionDto):
    action: Literal["create_player"]
    params: tuple[Annotated[str, Field(min_length=3)]]


class GetPlayerActionDTO(BaseActionDto):
    action: Literal["get_player"]
    params: tuple[Annotated[str, Field(min_length=3)]]


class GetFullMapActionDTO(BaseActionDto):
    action: Literal["get_full_map"]
    params: tuple[Annotated[str, Field(min_length=1)]] | None


class LogoutDTO(BaseActionDto):
    action: Literal["logout"]


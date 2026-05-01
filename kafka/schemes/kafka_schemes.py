from typing import Annotated

from pydantic import BaseModel, Field


class PlayerTopicScheme(BaseModel):
    id: int
    name: str
    health: int
    energy: int
    hungry: int
    position: tuple[int, int]
    direction: tuple[Annotated[int, Field(ge=-1, le=1)], Annotated[int, Field(ge=-1, le=1)]]
    inventory: list[str]
    location_id: str
    attack_modifier: int
    attack_damage: int
    defence: int
    is_dead: bool
    is_sleep: bool
    message: list[str]


class LocationTopicScheme(BaseModel):
    value: dict[str, str]


class GameTopicScheme(BaseModel):
    location_id: int
    location_size: tuple[int, int]
    location_data: dict[str, str]

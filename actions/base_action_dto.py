from pydantic import BaseModel, field_validator, ConfigDict

from errors.action_errors import IncorrectParameters


class BaseActionDto(BaseModel):
    model_config = ConfigDict(extra="ignore")

    action: str
    params: None = None

    @field_validator("params", mode="before")
    @classmethod
    def validate_params(cls, v):
        if v is None:
            return v
        if not isinstance(v, list):
            raise IncorrectParameters("Params value must be a list")
        return None if len(v) == 0 else v

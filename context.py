from typing import Any

from errors.errors import IncorrectContextNameError


class GameContext:
    def __init__(self):
        self.context = {}

    def add_context(self, context_name: str, context: Any) -> None:
        self.context[context_name] = context

    def get_context(self, context_name: str) -> Any:
        if context_name not in self.context:
            raise IncorrectContextNameError(context_name)

        return self.context[context_name]

    def remove_context(self, context_name: str):
        if context_name in self.context:
            del self.context[context_name]


game_context = GameContext()


def get_application_context() -> GameContext:
    return game_context

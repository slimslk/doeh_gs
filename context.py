# from actions.interaction_system import DefaultInteractionSystem


class GameContext:
    def __init__(self, game_service, main_game, interation_system):
        self.interaction_system = interation_system
        self.interaction_system.context = self
        self.game_service = game_service
        self.game_service.context = self
        self.main_game = main_game
        self.main_game.context = self

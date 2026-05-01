from actions.game_action_dto import (
    CreatePlayerActionDTO,
    GetPlayerActionDTO,
    GetFullMapActionDTO,
    LogoutDTO
)
from actions.player_action_dto import (
    MovePlayerActionDTO,
    InteractActionDTO,
    ListItemsActionDTO,
    UseItemActionDTO,
    AttackActionDTO,
    SkipTurnActionDTO, AwakeTurnActionDTO, MovePlayerWithDirectionActionDTO,
)

actionDTOMapConfig = {
    "create_player": CreatePlayerActionDTO,
    "get_player": GetPlayerActionDTO,
    "get_full_map": GetFullMapActionDTO,
    "logout": LogoutDTO,

    "move": MovePlayerWithDirectionActionDTO,
    "move_up": MovePlayerActionDTO,
    "move_down": MovePlayerActionDTO,
    "move_left": MovePlayerActionDTO,
    "move_right": MovePlayerActionDTO,
    "interact": InteractActionDTO,
    "list_items": ListItemsActionDTO,
    "use_item": UseItemActionDTO,
    "attack": AttackActionDTO,
    "skip_turn": SkipTurnActionDTO,
    "awake": AwakeTurnActionDTO,
}

PLAYER_ACTIONS = [
    "move",
    "move_up",
    "move_down",
    "move_left",
    "move_right",
    "interact",
    "get_items_list",
    "use_item",
    "attack",
    "skip_turn",
    "awake",
]

ITEM_ACTIONS = [
    "use",
    "equip_weapon",
    "take_off_weapon",
    "decrease_hungry",
    "sleep",
    "increase_health",
    "increase_energy",
]

GAME_ACTIONS = [
    "create_player",
    "get_full_map",
    "get_player",
    "logout"
]

OBJECT_ACTIONS = [
    "destroy_me",
    "open_chest"
]

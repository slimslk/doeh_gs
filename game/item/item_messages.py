import random

item_messages = {
    "default": ["Something catches your eye, but you have no idea what it might be."],
    "simple_chest": ["This is a simple wooden chest."],
    "opened_simple_chest": ["You look inside, but it's empty."],
    "corpse": ["Here lies"],
    "dummy": ["Just a dummy."],
    "grass": ["Nothing special, just some grass."],
    "meat": ["A piece of meat."],
    "purple potion": ["A flask with a purple liquid in it."],
    "red potion": ["A flask with a red liquid in it."],
    "sword": ["A sword. Be careful, it can be sharp."],
    "tree": ["Wow, it's a tree."],
    "yellow potion": ["A flask with a yellow liquid in it."],
}


def get_item_message(item_name: str) -> str:
    return random.choice(item_messages.get(item_name, "default"))

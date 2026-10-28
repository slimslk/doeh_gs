import random

item_messages = {
    "DefaultObject": ["Something catches your eye, but you have no idea what it might be."],
    "SimpleChest": ["This is a simple wooden chest."],
    "opened_simple_chest": ["You look inside, but it's empty."],
    "Corpse": ["Here lies"],
    "Dummy": ["Just a dummy."],
    "Grass": ["Nothing special, just some grass."],
    "RawMeat": ["A piece of meat."],
    "SleepPotion": ["A flask with a purple liquid in it."],
    "SmallHealthPotion": ["A small flask with a red liquid in it."],
    "PoorEnergyPotion": ["A grimy vial containing a yellow fluid."],
    "RustySword": ["A rusty sword. Be careful, it can be sharp."],
    "Tree": ["Wow, it's a tree."],
    "DungeonWall": ["A cold dungeon wall of ancient stone. Damp, worn, and untouched by sunlight for ages."],
    "DungeonStoneTile": ["A cold, damp stone tile, worn by endless passage through the dark."]
}


def get_item_message(item) -> str:
    return random.choice(item_messages.get(item.__class__.__name__, "DefaultObject"))

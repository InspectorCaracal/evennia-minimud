"""
Prototypes
"""
from random import randint
import time

### Crafted prototypes which might be useful to access in other places, such as shops

IRON_DAGGER = {
    "typeclass": "typeclasses.weapons.MeleeWeapon",
    "key": "iron dagger",
    "desc": "A keen-edged dagger, made of iron.",
    "tags": [
        ("pierce", "damage_type"),
        ("slash", "damage_type"),
        ("knife", "crafting_tool"),
    ],
    "value": 20,
    "speed": 3,
    "dmg": 5,
}

IRON_SWORD = {
    "typeclass": "typeclasses.weapons.MeleeWeapon",
    "key": "iron sword",
    "desc": "A one-handed sword made of iron.",
    "tags": [("pierce", "damage_type"), ("slash", "damage_type")],
    "value": 30,
    "speed": 7,
    "dmg": 10,
}

IRON_GREATSWORD = {
    "typeclass": "typeclasses.weapons.MeleeWeapon",
    "key": "iron greatsword",
    "desc": "A two-handed iron greatsword.",
    "tags": [
        ("slash", "damage_type"),
        ("bludgeon", "damage_type"),
        ("two_handed", "wielded"),
    ],
    "value": 50,
    "speed": 12,
    "dmg": 15,
}

IRON_HAUBERK = {
    "typeclass": "typeclasses.objects.ClothingObject",
    "key": "iron hauberk",
    "desc": "A standard iron chainmail tunic.",
    "armor": 5,
    "value": 20,
    "clothing_type": "chestguard",
}

IRON_CHAUSSES = {
    "typeclass": "typeclasses.objects.ClothingObject",
    "key": "iron chausses",
    "desc": "A pair of mail chausses constructed from iron.",
    "armor": 5,
    "value": 20,
    "clothing_type": "legguard",
}

LEATHER_BOOTS = {
    "typeclass": "typeclasses.objects.ClothingObject",
    "key": "leather boots",
    "desc": "A sturdy pair of leather boots.",
    "armor": 1,
    "value": 5,
    "clothing_type": "shoes",
}

SMALL_BAG = {
    "typeclass": "game_systems.containers.ContainerObject",
    "key": "small bag",
    "desc": "A small leather bag.",
    "capacity": 5,
    "value": 5,
}
MEDIUM_BAG = {
    "typeclass": "game_systems.containers.ContainerObject",
    "key": "medium bag",
    "desc": "A medium leather bag.",
    "capacity": 10,
    "value": 15,
}
LARGE_BAG = {
    "typeclass": "game_systems.containers.ContainerObject",
    "key": "large bag",
    "desc": "A large leather bag.",
    "capacity": 20,
    "value": 30,
}

### Shop Items

PIE_SLICE = {
    "key": "slice of $choice('apple', 'blueberry', 'peach', 'cherry', 'custard') pie",
    "desc": "A single slice of freshly-baked pie.",
    "tags": [
        "edible",
    ],
    "energy": 5,
    "value": 5,
}

WOOL_TUNIC = {
    "typeclass": "typeclasses.objects.ClothingObject",
    "key": "$choice('red', 'green', 'blue', 'brown', 'cream') tunic",
    "desc": "A simple, but comfortable, woolen tunic.",
    "value": 3,
    "clothing_type": "top",
}
WOOL_LEGGINGS = {
    "typeclass": "typeclasses.objects.ClothingObject",
    "key": "$choice('red', 'green', 'blue', 'brown', 'cream') leggings",
    "desc": "A pair of soft and durable woolen leggings.",
    "value": 3,
    "clothing_type": "legs",
}

### Crafting tools

SMITHING_HAMMER = {
    "key": "smithing hammer",
    "desc": "A sturdy hammer for beating metal.",
    "tags": [("hammer", "crafting_tool")],
    "locks": "get:false()",
}

SMITHING_ANVIL = {
    "key": "anvil",
    "desc": "A typical anvil, which has clearly seen much use.",
    "tags": [("anvil", "crafting_tool")],
    "locks": "get:false()",
}

SMITHING_FURNACE = {
    "key": "furnace",
    "desc": "An active furnace, hot enough to melt down metals.",
    "tags": [("furnace", "crafting_tool")],
    "locks": "get:false()",
}


### Materials and their gather nodes

IRON_ORE_NODE = {
    "typeclass": "typeclasses.objects.GatherNode",
    "key": "iron vein",
    "desc": "An outcropping of rocks here appears to contain raw iron.",
    "spawn_proto": "IRON_ORE",
    "gathers": lambda: randint(2, 10),
}
IRON_ORE = {
    "key": "iron ore",
    "desc": "A clump of raw iron ore.",
    "tags": [("iron ore", "crafting_material")],
    "value": 2,
}


COPPER_ORE_NODE = {
    "typeclass": "typeclasses.objects.GatherNode",
    "key": "copper vein",
    "desc": "An outcropping of rocks here appears to contain raw copper.",
    "spawn_proto": "COPPER_ORE",
    "gathers": lambda: randint(2, 10),
}
COPPER_ORE = {
    "key": "copper ore",
    "desc": "A clump of raw copper ore.",
    "tags": [("copper ore", "crafting_material")],
    "value": 1,
}


APPLE_TREE = {
    "typeclass": "typeclasses.objects.GatherNode",
    "key": "apple tree",
    "desc": "A tree here is full of apples, some of which seem to be ripe.",
    "spawn_proto": "APPLE",
    "gathers": lambda: randint(5, 10),
}
APPLE = {
    "key": "apple",
    "desc": "A delicious multi-colored apple.",
    "tags": [("apple", "crafting_material"), "edible"],
    "nutrition": 5,
    "value": 1,
}


LUMBER_TREE = {
    "typeclass": "typeclasses.objects.GatherNode",
    "key": "$choice('pine', 'oak', 'ash') tree",
    "desc": "This tree looks like a great source of lumber.",
    "spawn_proto": "WOOD_LOG",
    "gathers": lambda: randint(2, 10),
}
WOOD_LOG = {
    "key": "log of wood",
    "desc": "A decent-sized wooden log. Not so big you can't carry it.",
    "tags": [
        ("wood", "crafting_material"),
    ],
    "value": 1,
}


DRIFTWOOD = {
    "typeclass": "typeclasses.objects.GatherNode",
    "key": "pile of driftwood",
    "desc": "Some of this wood looks like it would be useful.",
    "spawn_proto": "WOOD_LOG",
    "gathers": lambda: randint(1, 3),
}
WOOD_LOG = {
    "key": "log of wood",
    "desc": "A decent-sized wooden log. Not so big you can't carry it.",
    "tags": [
        ("wood", "crafting_material"),
    ],
    "value": 1,
}


### Mobs

ANGRY_BEAR = {
    "typeclass": "typeclasses.characters.NPC",
    "key": "a large angry bear",
    "desc": "A large brown bear. It really doesn't like you!",
    "gender": "neutral",
    "react_as": "aggressive",
    "flee_at": 5,
    "name_color": "r",
    "str": 15,
    "natural_weapon": {
        "name": "claws",
        "damage_type": "slash",
        "damage": 10,
        "speed": 8,
        "energy_cost": 10,
    },
    "exp_reward": 10,
    # randomly generate a list of drop prototype keys when the mob is spawned
    "drops": lambda: ["BEAR_MEAT"] * randint(3, 5) + ["ANIMAL_HIDE"] * randint(0, 5),
    "can_attack": True,
}

COUGAR = {
    "typeclass": "typeclasses.characters.NPC",
    "key": "a mountain lion",
    "desc": "A sleek mountain lion. It doesn't appreciate you invading its territory. At all.",
    "gender": "neutral",
    "react_as": "aggressive",
    "flee_at": 15,
    "name_color": "r",
    "str": 8,
    "agi": 15,
    "natural_weapon": {
        "name": "claws",
        "damage_type": "slash",
        "damage": 10,
        "speed": 8,
        "energy_cost": 10,
    },
    "exp_reward": 10,
    # randomly generate a list of drop prototype keys when the mob is spawned
    "drops": lambda: ["RAW_MEAT"] * randint(0, 3) + ["ANIMAL_HIDE"] * randint(0, 2),
    "can_attack": True,
}

SQUIRREL = {
    "typeclass": "typeclasses.characters.NPC",
    "key": "a $choice('grey', 'brown') squirrel",
    "desc": "Look! A squirrel!",
    "react_as": "timid",
    "gender": "neutral",
    "drops": lambda: ["RAW_MEAT"] * randint(0, 1),
    "can_attack": True,
}

PHEASANT = {
    "typeclass": "typeclasses.characters.NPC",
    "key": "a pheasant",
    "desc": "A healthy wild pheasant.",
    "react_as": "timid",
    "gender": "neutral",
    "drops": lambda: ["RAW_MEAT"] * randint(0, 1),
    "can_attack": True,
}

DOE_DEER = {
    "typeclass": "typeclasses.characters.NPC",
    "key": "a doe",
    "desc": "A skittish doe with large brown eyes.",
    "gender": "female",
    "react_as": "timid",
    "agi": 15,
    "can_attack": True,
    # randomly generate a list of drop prototype keys when the mob is spawned
    "drops": lambda: ["DEER_MEAT"] * randint(1, 3) + ["ANIMAL_HIDE"] * randint(0, 3),
}

STAG_DEER = {
    "typeclass": "typeclasses.characters.NPC",
    "key": "a stag",
    "desc": "A wary adult stag, sporting a full rack of antlers.",
    "gender": "male",
    "agi": 15,
    "natural_weapon": {
        "name": "antlers",
        "damage_type": "pierce",
        "damage": 10,
        "speed": 10,
        "energy_cost": 5,
    },
    # randomly generate a list of drop prototype keys when the mob is spawned
    "drops": lambda: ["DEER_MEAT"] * randint(1, 3)
    + ["DEER_ANTLER"] * randint(0, 2)
    + ["ANIMAL_HIDE"] * randint(0, 3),
    "exp_reward": 10,
    "can_attack": True,
}

### Mob drops

RAW_MEAT = {
    "key": "raw meat",
    "desc": "A piece of meat from an animal. It hasn't been cooked.",
    "tags": [("raw meat", "crafting_material")],
}
ANIMAL_HIDE = {
    "key": "animal hide",
    "desc": "A section of hide from an animal, suitable for leather-crafting",
    "tags": [("leather", "crafting_material")],
}
DEER_MEAT = {
    "key": "raw deer meat",
    "desc": "A piece of meat from a deer. It hasn't been cooked.",
    "tags": [("raw meat", "crafting_material"), ("venison", "crafting_material")],
}
DEER_ANTLER = {
    "key": "antler",
    "desc": "A forked antler bone from an adult stag.",
    "tags": [
        ("bone", "crafting_material"),
    ],
}

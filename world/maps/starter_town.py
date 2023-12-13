"""
The beginning town where all new characters start.
"""

from evennia.contrib.grid.xyzgrid import xymap_legend


MAP_STR = r"""
+
                               
5   o-----G-----G---R---R---o  
    |      \    |           |  
4   R     B-R $-R   $-B B   R  
    |        \  |   |/  |   |  
3   G-----R---#-#---R---R---G  
    |          \    |   |   |  
2   R         $-R-$ B   B   R  
    |            \          |  
1   o---R-----R---G-----R---o  
                               
0                              

+
"""


class RoadNode(xymap_legend.MapNode):
    display_symbol = "#"
    prototype = {
        "prototype_parent": "xyz_room",
        "tags": [("townsburg", "zone")],
        "key": "A road",
        "desc": "A wide road through Townsburg.",
    }


class GateNode(xymap_legend.MapNode):
    display_symbol = "θ"
    prototype = {
        "prototype_parent": "xyz_room",
        "tags": [("townsburg", "zone")],
        "key": "A road",
        "desc": "The road here leads out of Townsburg and into the wilderness.",
    }


class BuildingNode(xymap_legend.MapNode):
    prototype = {
        "prototype_parent": "xyz_room",
        "key": "Inside",
        "desc": "A building in Townsburg.",
    }


class ShopNode(xymap_legend.MapNode):
    prototype = {
        "prototype_parent": "xyz_room",
        "typeclass": "typeclasses.rooms.XYGridShop",
        "key": "Inside",
        "desc": "A shop in Townsburg.",
    }


LEGEND = {
    "R": RoadNode,
    "G": GateNode,
    "B": BuildingNode,
    "$": ShopNode,
}

PROTOTYPES = {
    (6, 3): {
        "prototype_parent": "xyz_room",
        "tags": [("townsburg", "zone")],
        "key": "West half of a plaza",
        "desc": "The central plaza in Townsburg is wide-open, with at least as many livestock as people.",
    },
    (7, 3): {
        "prototype_parent": "xyz_room",
        "tags": [("townsburg", "zone")],
        "key": "East half of a plaza",
        "desc": "The central plaza in Townsburg is wide-open, with at least as many livestock as people.",
    },
    (9, 4): {
        "typeclass": "typeclasses.rooms.XYGridShop",
        "key": "A tavern",
        "desc": "A bustling tavern, with food and drink for sale.",
        "inventory": [
            ("PIE_SLICE", 12),
        ],
    },
    (6, 4): {
        "typeclass": "typeclasses.rooms.XYGridShop",
        "key": "General Store",
        "desc": "Stuff! and Things",
        "inventory": [
            ("WOOL_TUNIC", 3),
            ("WOOL_LEGGINGS", 3),
            ("LEATHER_BOOTS", 3),
            ("SMALL_BAG", 3),
        ],
    },
    (4, 4): {
        "typeclass": "typeclasses.rooms.XYGridTrain",
        "key": "Boxing R Us",
        "desc": "It looks like the perfect place for learning how to punch things.",
        "skill_training": "unarmed",
    },
    (6, 2): {
        "typeclass": "typeclasses.rooms.XYGridTrain",
        "key": "Rogue's Guild",
        "desc": "I dunno you can train daggers here.",
        "skill_training": "daggers",
    },
    (8, 2): {
        "typeclass": "typeclasses.rooms.XYGridTrain",
        "key": "Fencing studio",
        "desc": "Fencing dummies and practice swords are plentiful.",
        "skill_training": "swords",
    },
    (9, 2): {
        "prototype_parent": "xyz_room",
        "typeclass": "typeclasses.rooms.XYZShopNTrain",
        "tags": [("townsburg", "zone")],
        "key": "A forge",
        "desc": "A dimly smithing forge, heated to shirtless temps by a furnace all year round.",
        "skill_training": "smithing",
        "donation_tags": ["wood", "ore", "bone"],
        "inventory": [
            ("IRON_DAGGER", 6),
            ("IRON_SWORD", 6),
        ],
    },
    (10, 4): {
        "prototype_parent": "xyz_room",
        "typeclass": "typeclasses.rooms.XYZShopNTrain",
        "tags": [("townsburg", "zone")],
        "key": "A kitchen",
        "desc": "The kitchens for the tavern next door.",
        "skill_training": "cooking",
        "donation_tags": ["fruit", "raw meat", "cooked meat"],
        "inventory": [
            ("PIE_CRUST", 4),
        ],
    },
    (11, 4): {
        "prototype_parent": "xyz_room",
        "typeclass": "typeclasses.rooms.XYGridTrain",
        "tags": [("townsburg", "zone")],
        "key": "A leatherworker's",
        "desc": "A small, unassuming room. Sections of leather are scattered around. It smells a bit funny.",
        "skill_training": "leatherwork",
    },
    (11, 2): {
        "prototype_parent": "xyz_room",
        "typeclass": "typeclasses.rooms.XYGridTrain",
        "tags": [("townsburg", "zone")],
        "key": "A carpentry workshop",
        "desc": "The lively scent of fresh sawdust fills the air. Actual sawdust fills the air, too.",
        "skill_training": "carving",
    },
}


XYMAP_DATA = {
    "zcoord": "townsburg",
    "map": MAP_STR,
    "legend": LEGEND,
    "prototypes": PROTOTYPES,
    "options": {"map_visual_range": 1},
}

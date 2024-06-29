MAP_STR = '''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.............................~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~.............................."""""""""""""%%%%%%%%%%%%%%....~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~.....^^^^^^^^^^^""""""""""""""""""""""""""""""%%%%%%%%%%%%%%%%%%.....~~~~~~~~~~~~~~
~~~~~~~~~~~....%%%^^^^^^^^^""""""""""""""""""""""""""""""%%%%%%%%%%%%%%%%%%%%%%%%%.....~~~~~~~~~~
~~~~~~~~~...%%%%%%%^^^^^^^^^^^""""""""""""""""""""""""""""%%%%%%%%%%%%%%%%%%%%%%%%%%%%..~~~~~~~~~
~~~~~~~~..%%%%%%%%%%%^^^^^^^^^^^""""""""""""""""""""""""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%..~~~~~~~~
~~~~~~...%%%%%%%%%%^^^^^^^^^^^"""""""""""""""""""""""""""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%...~~~~~~
~~~~~~..%%%%%%%%%^^^^^^^^^^^"""""""""""""""""""""""""""""""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%..~~~~~~
~~~~~~~...%%%%%%%%^^^^^"""""""""""""""""""""""""""""""""""""""""%%%%%%%%%%%%%%%%%%%%%%%%..~~~~~~~
~~~~~~~~~..%%%%%^^^^^^^^""""""""""""""""""""""""""""""""""""""""""""""""""""""""%%%%%%%..~~~~~~~~
~~~~~~~~~~.%%%%^^^^^^^^""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""%%%%.~~~~~~~~~
~~~~~~~~~..^^^^^^^^^^^^^"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""%%...~~~~~~~~~
~~~~~~~~~.^^^^^^^^^^^%%%%%""""""""""""""""""""""""""""""""""""""""""""""""""""""".....~~~~~~~~~~~
~~~~~~~~~.^^^^^^^^^^%%%%%%""""""""""""""""""""""""""""""""""""""""""""""""""""""..~~~~~~~~~~~~~~~
~~~~~~~~..^^^^^^^^^^^%%%""""""""""""""""""""""""""O""""""""""""""""""""""""""""".~~~~~~~~~~~~~~~~
~~~~~~~..%%%%^^^^^^^^%%%%%%%"""""""""""""""""""""""""""""""""""""""""""""""""""".~~~~~~~~~~~~~~~~
~~~~~~..%%%%%%%^^^^^^^%%%%%%%%%%%"""""""""""""""""""""""""""""""""""""""""""""""...~~~~~~~~~~~~~~
~~~~~~.%%%%%%%%%%%^^^^%%%%%%%%%%%%%%"""""""""""""""""""""""""""""""""""""""""""""".....~~~~~~~~~~
~~~~~..%%%%%%%%%%%^^^^^^^^^^%%%%%%%%%%""""""""""""""""""""""""""""""""""""""""""""""""...~~~~~~~~
~~~~~..%%%%%%^^^^^^^^^^^^^^^%%%%%%%%%"""""""""""""""""""""""""""""""""""""""""""""""""""...~~~~~~
~~~~~~..%%%%%%%%^^^^^^^^^^^%%%%%%%%%%%%%""""""""""""""""""""""""""""""""""""""""""""""""""..~~~~~
~~~~~~~..%%%%%%%%%%^^^^^%%%%%%%%%%%%%%%%""""""""""""""""""""""""""""""""""""""""""""""""""..~~~~~
~~~~~~~~...%%%%%%%%%%^^^%%%%%%%%%%%%%%%%%""""""""""""""""""""""""""""""""""""""""""""""""".~~~~~~
~~~~~~~~~~..%%%%%%%%%%^^%%%%%%%%%%%%%%%%%%"""""""""""""""""""""""""""""""""""""""""""""""..~~~~~~
~~~~~~~~~~~.%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""""""""""""""""""""""""""""""""""""""""""""..~~~~~~~
~~~~~~~~~~..%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""""""""""""""""""""""""""""""""""""""""...~~~~~~~~
~~~~~~~~~~~..%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""""""""""""""""""""""""""""""...~~~~~~~~~~
~~~~~~~~~~~~...%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""""""""""""""""""""""""""""".....~~~~~~~~~~~~
~~~~~~~~~~~~~~....%%%%%%%%%%%%%%%%%%%%%%%%%%"""""""""""""""""""""""""""..........~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~.........%%%%%%%%%%%%%%%"""""""""""""""""""""""""".....~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~...........................................~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

weight = 1
_MAX_NODES = 50
_MAX_MOBS = 50


MAP_KEY = {
    "%": {
        "biome": "forest",
        "desc": "There are many trees here.",
        "gathers": (
            ("FRUIT_TREE", 1),
            ("LUMBER_TREE", 5),
            ("BERRY_BUSH", 3),
        ),
        "node cap": 10,
        "mobs": (("DOE_DEER", 3), ("STAG_DEER", 1), ("SQUIRREL", 5)),
        "mob cap": 25,
    },
    '"': {
        "biome": "grass",
        "desc": "A grassy meadow.",
        "gathers": (("BERRY_BUSH", 3),),
        "node cap": 10,
        "mobs": (("DOE_DEER", 3), ("STAG_DEER", 1), ("PHEASANT", 10)),
        "mob cap": 15,
    },
    ".": {
        "biome": "beach",
        "desc": "The sand and rocks slope gently into the ocean waves.",
        "gathers": (("DRIFTWOOD", 1),),
    },
    "^": {
        "biome": "mountains",
        "desc": "The ground slopes sharply, littered with rocks and boulders.",
        "gathers": (
            ("IRON_ORE_NODE", 1),
            ("COPPER_ORE_NODE", 5),
            ("BERRY_BUSH", 1),
        ),
        "node cap": 25,
        "mobs": (("ANGRY_BEAR", 1), ("COUGAR", 5)),
        "mob cap": 15,
    },
    "O": {
        "biome": "city",
        "desc": "You stand outside of a city.",
    },
}

from random import randint, choices
from evennia.contrib.grid.wilderness import wilderness
from evennia.prototypes import spawner
from evennia.utils.search import search_tag
from evennia.utils import logger, pad


class OverworldMapProvider(wilderness.WildernessMapProvider):
    room_typeclass = "typeclasses.rooms.OverworldRoom"
    exit_typeclass = "typeclasses.exits.OverworldExit"

    def is_valid_coordinates(self, wilderness, coordinates):
        "Validates if these coordinates are inside the map"
        x, y = coordinates
        # split the map into lines, i.e. rows
        # and reverse the order, since the wilderness contrib considers row 0 to be the bottom
        rows = MAP_STR.split("\n")
        rows.reverse()
        # make sure that y is a valid coordinate
        if y not in range(len(rows)):
            return False
        # get the y-coord row
        row = rows[y]
        # validate x as well
        if x not in range(len(row)):
            return False
        # get the specific tile
        tile = row[x]
        # if it's a key in the map key dict, it's good
        return tile in MAP_KEY

    def get_location_name(self, coordinates):
        """Returns the name for the given coordinate"""
        x, y = coordinates

        # we've already passed coord validation so we can just grab the data
        rows = MAP_STR.split("\n")
        rows.reverse()
        tile = rows[y][x]
        tile_data = MAP_KEY.get(tile, {})
        return f"In the {tile_data.get('biome', 'wilderness')}"

    def at_prepare_room(self, coordinates, caller, room):
        """Any changes that need to be done to the room after 'moving'."""
        x, y = coordinates

        # we've already passed coord validation so we can just grab the data
        rows = MAP_STR.split("\n")
        rows.reverse()
        tile = rows[y][x]
        tile_data = MAP_KEY.get(tile, {})
        room.ndb.active_desc = tile_data.get("desc")
        # build the minimap
        border = "-" * 29
        minimap = [border]
        for i in range(y + 2, y - 3, -1):
            row = rows[i][x - 2 : x + 3]
            if i == y:
                # mark our location
                row = row[:2] + "|g@|n" + row[3:]
            minimap.append(" " * 12 + row + " " * 12)
        minimap.append(border)
        room.ndb.minimap = "\n".join(minimap)

        if not randint(0, 5):
            # try to generate a resource
            self.spawn_resource(
                room,
                coordinates,
                tile_data.get("gathers"),
                cap=tile_data.get("node cap", _MAX_NODES),
                tag=tile_data.get("biome"),
                tag_cat="resource_node",
            )

        elif not randint(0, 10):
            # possibly spawn a mob, but not at the same time as a resource
            mob = self.spawn_resource(
                room,
                coordinates,
                tile_data.get("mobs"),
                cap=tile_data.get("mob cap", _MAX_MOBS),
                tag=tile_data.get("biome"),
                tag_cat="mob",
            )
            if mob:
                mob.at_character_arrive(caller)

    def spawn_resource(self, room, coordinates, weighted_options, **kwargs):
        """
        Create a new randomized object, if it hasn't reached the cap for this biome.
        """
        if not weighted_options:
            # there's nothing for us to spawn!
            return

        if (tag := kwargs.get("tag")) and (tag_cat := kwargs.get("tag_cat")):
            # we have a tag specified; check for a spawn cap amt
            if spawn_cap := kwargs.get("cap"):
                # there's a cap! make sure we don't already have enough
                tagged = search_tag(key=tag, category=tag_cat)
                if len(tagged) >= spawn_cap:
                    # too many, don't spawn anything new
                    return
        # we're good to keep going
        # split the weighted options into a list of materials and the corresponding list of weights
        options, weights = zip(*weighted_options)
        protkey = choices(options, weights=weights)[0]
        # spawn the new object and put it in the room
        try:
            obj = spawner.spawn(protkey)[0]
        except KeyError as e:
            logger.log_msg(f"   {e} on {protkey}")
            return
        room.wilderness.move_obj(obj, coordinates)
        if tag and tag_cat:
            obj.tags.add(tag, category=tag_cat)

        return obj


def create():
    """
    Create the wilderness script for this map, if it doesn't already exist.
    """
    wilderness.create_wilderness(
        mapprovider=OverworldMapProvider(), name="overworld", preserve_items=True
    )


def enter(obj, coordinates):
    """
    Move obj into the overworld map at coordinates x, y
    """
    wilderness.enter_wilderness(obj, coordinates=coordinates, name="overworld")

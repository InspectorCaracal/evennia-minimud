r"""
Evennia settings file.

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "MiniMUD the RPG"

# Defines the base character type as PlayerCharacter instead of Character
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.PlayerCharacter"

######################################################################
# Config for contrib packages
######################################################################

# XYZGrid - https://www.evennia.com/docs/latest/Contribs/Contrib-XYZGrid.html
EXTRA_LAUNCHER_COMMANDS["xyzgrid"] = "evennia.contrib.grid.xyzgrid.launchcmd.xyzcommand"
PROTOTYPE_MODULES += ["evennia.contrib.grid.xyzgrid.prototypes"]
XYZROOM_PROTOTYPE_OVERRIDE = {"typeclass": "typeclasses.rooms.XYGridRoom"}
XYZEXIT_PROTOTYPE_OVERRIDE = {"typeclass": "typeclasses.exits.XYGridExit"}


# Clothing - https://www.evennia.com/docs/latest/Contribs/Contrib-Clothing.html#configuration
CLOTHING_WEARSTYLE_MAXLENGTH = 40
CLOTHING_TYPE_ORDERED = [
    "hat",
    "jewelry",
    "chestguard",
    "top",
    "undershirt",
    "bracers",
    "gloves",
    "fullbody",
    "legguard",
    "bottom",
    "underpants",
    "socks",
    "shoes",
    "accessory",
]
CLOTHING_TYPE_AUTOCOVER = {
    "top": ["undershirt"],
    "chestguard": ["top", "undershirt"],
    "bottom": ["underpants"],
    "legguard": ["bottom", "underpants"],
    "fullbody": ["undershirt", "underpants"],
    "shoes": ["socks"],
}

CLOTHING_TYPE_LIMIT = {
    "chestguard": 1,
    "legguard": 1,
    "bracers": 1,
    "hat": 1,
    "gloves": 1,
    "socks": 1,
    "shoes": 1,
}

# Crafting - https://www.evennia.com/docs/latest/Contribs/Contrib-Crafting.html
CRAFT_RECIPE_MODULES = [
    "world.recipes.smithing",
    "world.recipes.tailoring",
    "world.recipes.cooking",
]

# Character Creation - https://www.evennia.com/docs/latest/Contribs/Contrib-Character-Creator.html
CHARGEN_MENU = "world.chargen_menu"
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False
AUTO_PUPPET_ON_LOGIN = False
MAX_NR_CHARACTERS = 3

# EvMenu Login - https://www.evennia.com/docs/latest/Contribs/Contrib-Menu-Login.html
CMDSET_UNLOGGEDIN = "evennia.contrib.base_systems.menu_login.UnloggedinCmdSet"
CONNECTION_SCREEN_MODULE = "evennia.contrib.base_systems.menu_login.connection_screens"

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")

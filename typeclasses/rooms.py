"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.utils import create, iter_to_str, logger
from evennia.objects.objects import DefaultRoom
from evennia.contrib.grid.xyzgrid.xyzroom import XYZRoom
from evennia.contrib.grid.wilderness.wilderness import WildernessRoom

from .objects import ObjectParent
from .scripts import RestockScript

from commands.shops import ShopCmdSet
from commands.skills import TrainCmdSet


class RoomParent(ObjectParent):
    """
    A mixin for logic that should be applied to all rooms.
    """

    def at_object_receive(self, mover, source_location, move_type=None, **kwargs):
        """
        Apply extra hooks when an object enters this room, so things (e.g. NPCs) can react.
        """
        super().at_object_receive(mover, source_location, **kwargs)
        # only react if the arriving object is a character
        if "character" in mover._content_types:
            for obj in self.contents_get(content_type="character"):
                if obj == mover:
                    # don't react to ourself
                    continue
                obj.at_character_arrive(mover, **kwargs)

    def at_object_leave(self, mover, destination, **kwargs):
        """
        Apply extra hooks when an object enters this room, so things (e.g. NPCs) can react.
        """
        super().at_object_leave(mover, destination, **kwargs)
        if combat := self.scripts.get("combat"):
            combat = combat[0]
            combat.remove_combatant(mover)
        # only react if the arriving object is a character
        if "character" in mover._content_types:
            for obj in self.contents_get(content_type="character"):
                if obj == mover:
                    # don't react to ourself
                    continue
                obj.at_character_depart(mover, destination, **kwargs)

    def get_display_footer(self, looker, **kwargs):
        """
        Shows a list of commands available here to the viewer.
        """

        cmd_keys = [
            f"|w{cmd.key}|n"
            for cmdset in self.cmdset.all()
            for cmd in cmdset
            if cmd.access(looker, "cmd")
        ]
        if cmd_keys:
            return f"Special commands here: {', '.join(cmd_keys)}"
        else:
            return ""


class Room(RoomParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass


class OverworldRoom(RoomParent, WildernessRoom):
    """
    A subclass of the Wilderness contrib's room, applying the local RoomParent mixin
    """

    def get_display_header(self, looker, **kwargs):
        """
        Displays a minimap above the room description, if there is one.
        """
        if not self.ndb.minimap:
            self.ndb.minimap = self.db.minimap
        return self.ndb.minimap or ""

    def at_server_reload(self, **kwargs):
        """
        Saves the current ndb desc to db so it's still available after a reload
        """
        self.db.desc = self.ndb.active_desc
        self.db.minimap = self.ndb.minimap


class XYGridRoom(RoomParent, XYZRoom):
    """
    A subclass of the XYZGrid contrib's room, applying the local RoomParent mixin
    """

    pass


class XYGridShop(XYGridRoom):
    """
    A grid-aware room that has built-in shop-related functionality.
    """

    def at_object_creation(self):
        """
        Initialize the shop inventory and commands
        """
        super().at_object_creation()
        # add the shopping commands to the room
        self.cmdset.add(ShopCmdSet, persistent=True)
        # create an invisible, inaccessible storage object
        self.db.storage = create.object(
            key="shop storage",
            locks="view:perm(Builder);get:perm(Builder);search:perm(Builder)",
            home=self,
            location=self,
        )
        self.scripts.add(RestockScript, key="restock", autostart=False)

    def add_stock(self, obj):
        """
        Adds new objects to the shop's sale stock
        """
        if storage := self.db.storage:
            # only do this if there's a storage location set
            obj.location = storage
            # price is double the sale value
            val = obj.db.value or 0
            obj.db.price = val * 2
            return True
        else:
            return False


class XYGridTrain(XYGridRoom):
    """
    A grid-aware room that has built-in shop-related functionality.
    """

    def at_object_creation(self):
        """
        Initialize the shop inventory and commands
        """
        super().at_object_creation()
        # add the shopping commands to the room
        self.cmdset.add(TrainCmdSet, persistent=True)


class XYZShopNTrain(XYGridTrain, XYGridShop):
    """
    A room where you can train AND shop!
    """

    pass

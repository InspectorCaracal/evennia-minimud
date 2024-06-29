"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""

from evennia.objects.objects import DefaultExit
from evennia.contrib.grid.xyzgrid.xyzroom import XYZExit
from .objects import ObjectParent
from evennia.contrib.grid.wilderness import wilderness


class Exit(ObjectParent, DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_post_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """

    def at_traverse(self, traveller, destination, **kwargs):
        """
        A customized version of exit traversal that allows you to travel into a wilderness.

        Args:
            traversing_object (Object): Object traversing us.
            target_location (Object): Where target is going.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        """
        # check if wilderness data is attached; if not, traverse normally
        if not (map_name := self.db.wilderness_name):
            super().at_traverse(traveller, destination, **kwargs)
            return
        if not (coords := self.db.wilderness_coords):
            super().at_traverse(traveller, destination, **kwargs)
            return

        # try to enter the wilderness
        if wilderness.enter_wilderness(traveller, coordinates=coords, name=map_name):
            # it succeeded! call the post-traversal hooks
            traveller.at_post_move(self.location, **kwargs)
            self.at_post_traverse(traveller, self.location, **kwargs)
        else:
            # it failed
            if self.db.err_traverse:
                # if exit has a better error message, let's use it.
                traveller.msg(self.db.err_traverse)
            else:
                # No shorthand error message. Call hook.
                self.at_failed_traverse(traveller)


class OverworldExit(ObjectParent, wilderness.WildernessExit):
    """
    Wraps the Wilderness exit to make sure that at_object_receive hooks are called when moving rooms.
    """

    def at_traverse(self, traveller, destination, **kwargs):
        """
        Makes sure to call at_object_receive if moving into an actual new room.

        This isn't really ideal, but due to the way the wilderness contrib works, it's necessary.
        """
        super().at_traverse(traveller, destination, **kwargs)
        # compare new location to our location
        if traveller.location != self.location:
            # they moved to a new place! call the hook
            traveller.location.at_object_receive(traveller, self.location)


class XYGridExit(ObjectParent, XYZExit):
    """
    A subclass of the XYZGrid contrib's exit, applying the local ObjectParent mixin
    """

    pass

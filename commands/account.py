from evennia import CmdSet
from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils.evtable import EvTable

from .command import Command


class CmdSettings(MuxCommand):
    """
    View and update your game settings.

    Usage:
        settings
        settings <option> = <on/off>
    """

    key = "settings"
    aliases = ("setting",)
    account_caller = True

    def func(self):
        caller = self.caller

        if not (settings := caller.db.settings):
            caller.msg("You have no settings to change.")
            return

        if not self.args:
            rows = []
            for key, val in settings.items():
                rows.append([key, "|GON|n" if val else "|ROFF|n"])
            table = EvTable(table=list(zip(*rows)), border="none")
            self.msg("|wSettings|n")
            self.msg(str(table))
        elif self.lhs not in settings:
            self.msg(f"Invalid setting: {self.lhs}")
        elif not self.rhs:
            value = settings.get(self.lhs)
            self.msg(f"{self.lhs} is {'|GON|n' if value else '|ROFF|n'}")
        else:
            if self.rhs.lower() == "on":
                caller.db.settings[self.lhs] = True
                self.msg(f"{self.lhs} has been set |GON|n")
            elif self.rhs.lower() == "off":
                caller.db.settings[self.lhs] = False
                self.msg(f"{self.lhs} has been set |ROFF|n")
            else:
                self.msg(f"Invalid value {self.rhs} for {self.lhs}.")


class AccountOptsCmdSet(CmdSet):
    key = "Options CmdSet"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdSettings)

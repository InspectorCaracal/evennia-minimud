from random import choice
from evennia import CmdSet
from evennia.utils import iter_to_str
from evennia.utils.evtable import EvTable

from .command import Command
from typeclasses.weapons import BareHand


class CmdAttack(Command):
    """
    Attack an enemy with your equipped weapon.

    Usage:
        attack <enemy> [with <weapon>]

    Example:
        attack wolf
        attack bear with sword
        attack bear w sword
        attack bear w/sword
    """

    key = "attack"
    aliases = ("att", "hit", "shoot")

    def parse(self):
        """
        Parse for optional weapon
        """
        self.args = self.args.strip()

        # split on variations of "with"
        if " with " in self.args:
            self.target, self.weapon = self.args.split(" with ", maxsplit=1)
        elif " w " in self.args:
            self.target, self.weapon = self.args.split(" w ", maxsplit=1)
        elif " w/" in self.args:
            self.target, self.weapon = self.args.split(" w/", maxsplit=1)
        else:
            # no splitters, it's all target
            self.target = self.args
            self.weapon = None

    def func(self):
        location = self.caller.location
        if not location:
            self.msg("You cannot fight nothingness.")
            return

        if not self.target:
            self.msg("Attack what?")
            return

        # if we specified a weapon, find it first
        if self.weapon:
            weapon = self.caller.search(self.weapon)
            if not weapon:
                # no valid match
                return
        else:
            # grab whatever we're wielding
            if wielded := self.caller.wielding:
                weapon = wielded[0]
            else:
                # use our bare hands if we aren't wielding anything
                weapon = BareHand()

        # find our enemy!
        target = self.caller.search(self.target)
        if not target:
            # no valid match
            return
        if not target.db.can_attack:
            # this isn't something you can attack
            self.msg(f"You can't attack {target.get_display_name(self.caller)}.")
            return

        # if we were trying to flee, cancel that
        del self.caller.db.fleeing

        # it's all good! let's get started!
        if not (combat_script := location.scripts.get("combat")):
            # there's no combat instance; start one
            from typeclasses.scripts import CombatScript

            location.scripts.add(CombatScript, key="combat")
            combat_script = location.scripts.get("combat")

        combat_script = combat_script[0]

        current_fighters = combat_script.fighters

        # adding a combatant to combat just returns True if they're already there, so this is safe
        if not combat_script.add_combatant(self.caller, enemy=target):
            self.msg("You can't fight right now.")
            return

        self.caller.db.combat_target = target
        # execute the actual attack
        self.caller.attack(target, weapon)

        # check if we have auto-attack in settings
        if self.account and (settings := self.account.db.settings):
            if settings.get("auto attack"):
                # let the player know we'll be auto-attacking
                self.msg(f"[ Auto-attack is ON ]")

    def at_post_cmd(self):
        """
        optional post-command auto prompt
        """
        # check if we have auto-prompt in settings
        if self.account and (settings := self.account.db.settings):
            if settings.get("auto prompt"):
                status = self.caller.get_display_status(self.caller)
                self.msg(prompt=status)


class CmdWield(Command):
    """
    Wield a weapon

    Usage:
        wield <weapon> [in <hand>]

    Example:
        wield sword
        wield dagger in right
    """

    key = "wield"
    aliases = ("hold",)

    def parse(self):
        """
        Parse for optional weapon
        """
        self.args = self.args.strip()

        # split on the word "in"
        if " in " in self.args:
            self.weapon, self.hand = self.args.split(" in ", maxsplit=1)
        else:
            # no splitter, it's all target
            self.weapon = self.args
            self.hand = None

    def func(self):
        caller = self.caller

        # check if we have free hands
        if not (hands := caller.free_hands):
            self.msg(
                f"You have no free hands! You are already wielding {iter_to_str(caller.wielding)}."
            )
            return

        # filter for hands matching the optional hand input
        if self.hand:
            hands = [hand for hand in caller.free_hands if self.hand in hand]
            if not hands:
                self.msg(f"You do not have a free {self.hand}.")

        # grab the top hand option
        hand = hands[0]

        weapon = caller.search(self.weapon, location=caller)
        if not weapon:
            # no valid object found
            return

        # try to wield the weapon
        held_in = caller.at_wield(weapon, hand=hand)
        if held_in:
            # success!
            self.caller.at_emote(
                f"$conj(wields) the {{weapon}} in $your() {iter_to_str(held_in)}."
            )


class CmdUnwield(Command):
    """
    Stop wielding a weapon

    Usage:
        unwield <weapon>

    Example:
        unwield dagger
    """

    key = "unwield"
    aliases = ("unhold",)

    def func(self):
        caller = self.caller

        weapon = caller.search(self.args, location=caller)
        if not weapon:
            # no valid object found
            return

        freed_hands = caller.at_unwield(weapon)
        if freed_hands:
            # success!
            self.caller.at_emote(
                f"$conj(releases) the {{weapon}} from $your() {iter_to_str(freed_hands)}."
            )


class CmdFlee(Command):
    """
    Attempt to escape from combat.

    Usage:
        flee
    """

    key = "flee"

    def func(self):
        caller = self.caller

        if not caller.in_combat:
            self.msg("You are not in combat.")
            return

        if not caller.can_flee:
            # this does its own error messaging
            return

        exits = caller.location.contents_get(content_type="exit")
        if not exits:
            self.msg("There is nowhere to flee to!")
            return

        if combat_script := caller.location.scripts.get("combat"):
            combat_script = combat_script[0]
            if not combat_script.remove_combatant(self.caller):
                self.msg("You cannot leave combat.")

        self.caller.db.fleeing = True
        self.msg("You flee!")
        flee_dir = choice(exits)
        self.execute_cmd(flee_dir.name)

    def at_post_cmd(self):
        """
        optional post-command auto prompt
        """
        # check if we have auto-prompt in settings
        if self.account and (settings := self.account.db.settings):
            if settings.get("auto prompt"):
                status = self.caller.get_display_status(self.caller)
                self.msg(prompt=status)


class CmdStatus(Command):
    key = "status"
    aliases = ("hp", "stat")

    def func(self):
        if not self.args:
            target = self.caller
            status = target.get_display_status(self.caller)
            self.msg(prompt=status)
        else:
            target = self.caller.search(self.args.strip())
            if not target:
                # no valid object found
                return
            status = target.get_display_status(self.caller)
            self.msg(status)


class CombatCmdSet(CmdSet):
    key = "Combat CmdSet"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()

        self.add(CmdAttack)
        self.add(CmdFlee)
        self.add(CmdWield)
        self.add(CmdUnwield)
        self.add(CmdStatus)

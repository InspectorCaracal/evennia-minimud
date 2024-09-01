from evennia import CmdSet
from evennia.utils.evtable import EvTable
from .command import Command

# A dict of all skills, with their associated stat as the value
SKILL_DICT = {
    "smithing": "str",
    "tailoring": "agi",
    "evasion": "agi",
    "daggers": "agi",
    "swords": "str",
    "cooking": "will",
    "carving": "str",
    "unarmed": "agi",
    "leatherwork": "will",
}


class CmdStatSheet(Command):
    """
    View your character's current stats.
    """

    key = "stats"
    aliases = ("sheet", "skills")

    def func(self):
        caller = self.caller

        self.msg(f"|w{caller.name}|n")
        # display current status
        self.msg(caller.get_display_status(caller))
        self.msg(f"EXP: {caller.db.exp or 0}")

        # display the primary stats
        self.msg("STATS")
        stats = [
            ["Strength", caller.db.str or 0],
            ["Agility", caller.db.agi or 0],
            ["Willpower", caller.db.will or 0],
        ]
        rows = list(zip(*stats))
        table = EvTable(table=rows, border="none")
        self.msg(str(table))

        # display known skills
        self.msg("SKILLS")
        skills = []
        for skill_key in sorted(SKILL_DICT.keys()):
            if skill := caller.traits.get(skill_key):
                skills.append((skill.name, int(skill.value)))
        rows = list(zip(*skills))
        if not rows:
            self.msg("(None)")
        table = EvTable(table=rows, border="none")
        self.msg(str(table))


class CmdTrainSkill(Command):
    """
    Improve a skill, based on how much experience you have.

    Enter just "train" by itself to see what you can learn here.

    Usage:
        train <levels>

    Example:
        train 5
    """

    key = "train"

    def _calc_exp(self, start, increase):
        """
        Calculates the experience cost for increasing your skill from the start level.
        """
        return int((start + (start + increase)) * (increase + 1) / 2.0)

    def func(self):
        if not self.obj:
            self.msg("You cannot train skills here.")
            return
        if not (to_train := self.obj.db.skill_training):
            self.msg("You cannot train any skills here.")
            return

        # make sure this is actually a valid skill
        if to_train not in SKILL_DICT:
            self.msg("You cannot train any skills here.")
            return

        if not self.args:
            self.msg(f"You can improve your |w{to_train}|n here.")
            return

        caller = self.caller

        try:
            levels = int(self.args.strip())
        except ValueError:
            self.msg("Usage: train <levels>")
            return

        if not (caller_xp := caller.db.exp):
            self.msg("You do not have any experience.")
            return

        if not (skill := caller.traits.get(to_train)):
            exp_cost = self._calc_exp(0, levels)
            if caller_xp < exp_cost:
                self.msg(
                    f"You do not have enough experience - you need {exp_cost} to learn {levels} levels of {to_train}."
                )
                return

            confirm = yield (
                f"It will cost you {exp_cost} experience to learn {to_train} up to level {levels}. Confirm? Yes/No"
            )
            if confirm.lower() not in (
                "yes",
                "y",
            ):
                self.msg("Cancelled.")
                return
            caller.traits.add(
                to_train,
                trait_type="counter",
                min=0,
                max=100,
                base=0,
                stat=SKILL_DICT.get(to_train),
            )
            skill = caller.traits.get(to_train)
        else:
            exp_cost = self._calc_exp(skill.base, levels)
            if caller_xp < exp_cost:
                self.msg(
                    f"You do not have enough experience - you need {exp_cost} experience to increase your {to_train} by {levels} levels."
                )
                return
            confirm = yield (
                f"It will cost you {exp_cost} experience to improve your {to_train} by {levels} levels. Confirm? Yes/No"
            )
            if confirm.lower() not in (
                "yes",
                "y",
            ):
                self.msg("Cancelled.")
                return

        caller.db.exp -= exp_cost
        skill.base += levels
        self.msg(f"You practice your {to_train} and improve it to level {skill.base}.")


class TrainCmdSet(CmdSet):
    key = "Train CmdSet"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdTrainSkill)


class SkillCmdSet(CmdSet):
    key = "Skill CmdSet"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdStatSheet)

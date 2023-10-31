from random import randint, choice
from string import punctuation
from evennia import AttributeProperty
from evennia.utils import lazy_property, iter_to_str, delay, logger
from evennia.contrib.rpg.traits import TraitHandler
from evennia.contrib.game_systems.clothing.clothing import (
    ClothedCharacter,
    get_worn_clothes,
)
from evennia.contrib.game_systems.cooldowns import CooldownHandler

from .objects import ObjectParent

_IMMOBILE = ("sitting", "lying down", "unconscious")


class Character(ObjectParent, ClothedCharacter):
    """
    The base typeclass for all characters, both player characters and NPCs
    """

    gender = AttributeProperty("plural")

    @property
    def in_combat(self):
        """Return True if in combat, otherwise False"""
        if not (location := self.location):
            # can't be in combat if we're nowhere!
            return False
        if not (combat_script := location.scripts.get("combat")):
            # there is no combat instance in this location
            return False

        # return whether we're in the combat instance's combatants
        return self in combat_script[0].fighters

    @property
    def can_flee(self):
        """
        Calculates chance of escape.

        Returns:
            True if you can flee, otherwise False
        """
        # use agility as a fallback for unskilled
        if not (evade := self.use_skill("evasion")):
            evade = self.db.agi
        # if you have more focus, you can escape more easily
        if (randint(0, 99) - self.traits.fp.value) < evade:
            return True
        else:
            self.msg("You can't find an opportunity to escape.")
            return False

    @lazy_property
    def traits(self):
        # this adds the handler as .traits
        return TraitHandler(self)

    @lazy_property
    def cooldowns(self):
        return CooldownHandler(self, db_attribute="cooldowns")

    @property
    def wielding(self):
        """Access a list of all wielded objects"""
        return [obj for obj in self.attributes.get("_wielded", {}).values() if obj]

    @property
    def free_hands(self):
        return [
            key for key, val in self.attributes.get("_wielded", {}).items() if not val
        ]

    def defense(self, damage_type=None):
        """Get the total armor defense from equipped items"""
        return sum([obj.attributes.get("armor", 0) for obj in get_worn_clothes(self)])

    def at_object_creation(self):
        # basic stats
        # i could - and wanted to - use the traits handler for these, but then i couldn't set them in NPC prototypes
        self.db.str = 5
        self.db.agi = 5
        self.db.will = 5
        # resource stats
        self.traits.add(
            "hp", "Health", trait_type="gauge", min=0, max=100, base=100, rate=0.1
        )
        self.traits.add(
            "fp", "Focus", trait_type="gauge", min=0, max=100, base=100, rate=0.1
        )
        self.traits.add(
            "ep", "Energy", trait_type="gauge", min=0, max=100, base=100, rate=0.1
        )
        self.traits.add(
            "evasion", trait_type="counter", min=0, max=100, base=0, stat="agi"
        )

    def at_pre_move(self, destination, **kwargs):
        """
        Called by self.move_to when trying to move somewhere. If this returns
        False, the move is immediately cancelled.
        """
        # check if we have any statuses that prevent us from moving
        if statuses := self.tags.get(_IMMOBILE, category="status", return_list=True):
            self.msg(
                f"You can't move while you're {iter_to_str(sorted(statuses), endsep='or')}."
            )
            return False

        # check if we're in combat
        if self.in_combat:
            self.msg("You can't leave while in combat.")
            return False

        return super().at_pre_move(destination, **kwargs)

    def at_post_move(self, source_location, **kwargs):
        """
        optional post-move auto prompt
        """
        super().at_post_move(source_location, **kwargs)
        # check if we have auto-prompt in settings
        if self.account and (settings := self.account.db.settings):
            if settings.get("auto prompt"):
                status = self.get_display_status(self)
                self.msg(prompt=status)

    def at_damage(self, attacker, damage, damage_type=None):
        """
        Apply damage, after taking into account damage resistances.
        """
        # apply armor damage reduction
        damage -= max(self.defense(damage_type), 0)
        self.traits.hp.current -= damage
        self.msg(f"You take {damage} damage from {attacker.get_display_name(self)}.")
        attacker.msg(f"You deal {damage} damage to {self.get_display_name(attacker)}.")
        if self.traits.hp.value <= 0:
            self.tags.add("unconscious", category="status")
            self.tags.add("lying down", category="status")
            self.msg(
                "You fall unconscious. You can |wrespawn|n or wait to be |wrevive|nd."
            )
            self.traits.hp.rate = 0
            if self.in_combat:
                combat = self.location.scripts.get("combat")[0]
                combat.remove_combatant(self)

    def at_emote(self, message, **kwargs):
        """
        Execute a room emote as ourself.

        This acts as a wrapper to `self.location.msg_contents` to avoid boilerplate validation.
        """
        # if there is nothing to send or nowhere to send it to, cancel
        if not message or not self.location:
            return
        # add period to punctuation-less emotes
        if message[-1] not in punctuation:
            message += "."
        if kwargs.get("prefix", True) and not message.startswith("$You()"):
            message = f"$You() {message}"
        mapping = kwargs.get("mapping", None)

        self.location.msg_contents(text=message, from_obj=self, mapping=mapping)

    def at_wield(self, weapon, **kwargs):
        """
        Wield a weapon in one or both hands
        """
        # fetch the wielded info and detach from the DB
        wielded = self.attributes.get("_wielded", {})
        if wielded:
            wielded.deserialize()

        # which hand (or "hand") we'll wield it in
        # get all available hands
        free = self.free_hands

        if hand := kwargs.get("hand"):
            # if a specific hand was requested, check if it's available
            if hand not in free:
                # check if this is even a valid hand by trying to get what's in it
                if not (weap := wielded.get(hand)):
                    # no weapon was got, so it's not there
                    self.msg(f"You do not have a {hand}.")
                else:
                    # a weapon was found, provide this information
                    self.msg(
                        f"You are already wielding {weap.get_display_name(self)} in your {key}."
                    )
                return
        elif not free:
            # there are no hands available to wield this
            self.msg(f"Your hands are full.")
            return
        # handle two-handed weapons
        if weapon.tags.has("two_handed", category="wielded"):
            if len(free) < 2:
                # not enough free hands to hold this
                self.msg(
                    f"You need two hands free to wield {weapon.get_display_name(self)}."
                )
                return
            # put the weapon as wielded in the first two hands
            hands = free[:2]
            for hand in hands:
                wielded[hand] = weapon
        else:
            # check handedness first, then find a hand
            if main_hand := self.db.handedness:
                hand = main_hand if main_hand in free else free[0]
            else:
                hand = free[0]
            # put the weapon as wielded in the hand
            hands = [hand]
            wielded[hand] = weapon

        # update the character with the new wielded info
        self.db._wielded = wielded
        # return the list of hands that are now holding the weapon
        return hands

    def at_unwield(self, weapon, **kwargs):
        """
        Stop wielding a weapon
        """
        # fetch the wielded info and detach from the DB
        wielded = self.attributes.get("_wielded", {})
        if wielded:
            wielded.deserialize()

        # can't unwield a weapon you aren't wielding
        if weapon not in wielded.values():
            self.msg("You are not wielding that.")
            return

        # replace weapon with an instance of a bare hand
        freed = []
        for hand, weap in wielded.items():
            if weap == weapon:
                # create a correctly-named fist
                wielded[hand] = None
                # append the hand to the list of freed hands
                freed.append(hand)

        # update the character with the new wielded info
        self.db._wielded = wielded
        # return the list of hands that are no longer holding the weapon
        return freed

    def use_skill(self, skill_name, *args, **kwargs):
        """
        Attempt to use a skill, applying any stat bonus as necessary.
        """
        # handle cases where this was called but there's no skill being used
        if not skill_name:
            return 1
        # if we don't have the skill, we can't use it
        if not (skill_trait := self.traits.get(skill_name)):
            return 0
        # check if this skill has a related base stat
        stat_bonus = 0
        if stat := getattr(skill_trait, "stat", None):
            # get the stat to be a modifier
            stat_bonus = self.attributes.get(stat, 0)
        # finally, return the skill plus stat
        return skill_trait.value + stat_bonus

    def get_display_status(self, looker, **kwargs):
        """
        Returns a quick view of the current status of this character
        """

        chunks = []
        # prefix the status string with the character's name, if it's someone else checking
        if looker != self:
            chunks.append(self.get_display_name(looker, **kwargs))

        # add resource levels
        chunks.append(
            f"Health {self.traits.hp.percent()} : Energy {self.traits.ep.percent()} : Focus {self.traits.fp.percent()}"
        )

        # get all the current status flags for this character
        if status_tags := self.tags.get(category="status", return_list=True):
            # add these statuses to the string, if there are any
            chunks.append(iter_to_str(status_tags))

        if looker == self:
            # if we're checking our own status, include cooldowns
            all_cooldowns = [
                (key, self.cooldowns.time_left(key, use_int=True))
                for key in self.cooldowns.all
            ]
            all_cooldowns = [f"{c[0]} ({c[1]}s)" for c in all_cooldowns if c[1]]
            if all_cooldowns:
                chunks.append(f"Cooldowns: {iter_to_str(all_cooldowns, endsep=',')}")

        # glue together the chunks and return
        return " - ".join(chunks)

    def at_character_arrive(self, chara, **kwargs):
        """
        Respond to the arrival of a character
        """
        pass

    def at_character_depart(self, chara, destination, **kwargs):
        """
        Respond to the departure of a character
        """
        pass

    def revive(self, reviver, **kwargs):
        """
        Revive a defeated character at partial health.
        """
        # this function receives the actor doing the revive so you could implement your own skill check
        # however, we don't have any relevant skills
        if self.tags.has("unconscious"):
            self.tags.remove("unconscious")
            self.tags.remove("lying down")
            # this sets the current HP to 20% of the max, a.k.a. one fifth
            self.traits.hp.current = self.traits.hp.current.max // 5
            self.msg(prompt=self.get_display_status(self))
            self.traits.hp.rate = 0.1


class PlayerCharacter(Character):
    """
    The typeclass for all player characters, including special player-feedback features.
    """

    def at_object_creation(self):
        super().at_object_creation()
        # initialize hands
        self.db._wielded = {"left": None, "right": None}

    def get_display_name(self, looker, **kwargs):
        """
        Adds color to the display name.
        """
        name = super().get_display_name(looker, **kwargs)
        if looker == self:
            # special color for our own name
            return f"|c{name}|n"
        return f"|g{name}|n"

    def at_damage(self, attacker, damage, damage_type=None):
        super().at_damage(attacker, damage, damage_type=damage_type)
        if self.traits.hp.value < 50:
            status = self.get_display_status(self)
            self.msg(prompt=status)

    def attack(self, target, weapon, **kwargs):
        """
        Execute an attack

        Args:
            target (Object or None): the entity being attacked. if None, attempts to use the combat_target db attribute
            weapon (Object): the object dealing damage
        """
        # can't attack if we're not in combat!
        if not self.in_combat:
            return
        # can't attack if we're fleeing!
        if self.db.fleeing:
            return
        # make sure that we can use our chosen weapon
        if not (hasattr(weapon, "at_pre_attack") and hasattr(weapon, "at_attack")):
            self.msg(f"You cannot attack with {weapon.get_numbered_name(1, self)}.")
            return
        if not weapon.at_pre_attack(self):
            # the method handles its own error messaging
            return

        # if target is not set, use stored target
        if not target:
            # make sure there's a stored target
            if not (target := self.db.combat_target):
                self.msg("You cannot attack nothing.")
                return

        if target.location != self.location:
            self.msg("You don't see your target.")
            return

        # attack with the weapon
        weapon.at_attack(self, target)

        status = self.get_display_status(self)
        self.msg(prompt=status)

        # check if we have auto-attack in settings
        if self.account and (settings := self.account.db.settings):
            if settings.get("auto attack") and (speed := weapon.speed):
                # queue up next attack; use None for target to reference stored target on execution
                delay(speed + 1, self.attack, None, weapon, persistent=True)

    def respawn(self):
        """
        Resets the character back to the spawn point with full health.
        """
        self.tags.remove("unconscious", category="status")
        self.tags.remove("lying down", category="status")
        self.traits.hp.reset()
        self.traits.hp.rate = 0.1
        self.move_to(self.home)
        self.msg(prompt=self.get_display_status(self))


class NPC(Character):
    """
    The base typeclass for non-player characters, implementing behavioral AI.
    """

    # defines what color this NPC's name will display in
    name_color = AttributeProperty("w")

    # property to mimic weapons
    @property
    def speed(self):
        weapon = self.db.natural_weapon
        if not weapon:
            return 10
        return weapon.get("speed", 10)

    def get_display_name(self, looker, **kwargs):
        """
        Adds color to the display name.
        """
        name = super().get_display_name(looker, **kwargs)
        return f"|{self.name_color}{name}|n"

    def at_character_arrive(self, chara, **kwargs):
        """
        Respond to the arrival of a character
        """
        if "aggressive" in self.attributes.get("react_as", ""):
            delay(1, self.enter_combat, chara)

    def at_character_depart(self, chara, destination, **kwargs):
        """
        Respond to the departure of a character
        """
        if chara == self.db.following:
            # find an exit that goes the same way
            exits = [
                x
                for x in self.location.contents_get(content_type="exit")
                if x.destination == destination
            ]
            if exits:
                # use the exit
                self.execute_cmd(exits[0].name)

    def at_damage(self, attacker, damage, damage_type=None):
        """
        Apply damage, after taking into account damage resistances.
        """
        super().at_damage(attacker, damage, damage_type=damage_type)

        if self.traits.hp.value <= 0:
            # we've been defeated!
            if combat_script := self.location.scripts.get("combat"):
                combat_script = combat_script[0]
                if not combat_script.remove_combatant(self):
                    # something went wrong...
                    return
                # create loot drops
                objs = spawn(*list(self.db.drops))
                for obj in objs:
                    obj.location = self.location
                # delete ourself
                self.delete()
                return

        if "timid" in self.attributes.get("react_as", ""):
            self.at_emote("flees!")
            self.db.fleeing = True
            if combat_script := self.location.scripts.get("combat"):
                combat_script = combat_script[0]
                if not combat_script.remove_combatant(self):
                    return
            # there's a 50/50 chance the object will escape forever
            if randint(0, 1):
                self.move_to(None)
                self.delete()
            else:
                flee_dir = choice(self.location.contents_get(content_type="exit"))
                flee_dir.at_traverse(self, flee_dir.destination)
            return

        threshold = self.attributes.get("flee_at", 25)
        if self.traits.hp.value <= 25:
            self.execute_cmd("flee")

        # change target to the attacker
        if not self.db.combat_target:
            self.enter_combat(attacker)
        else:
            self.db.combat_target = attacker

    def enter_combat(self, target, **kwargs):
        """
        initiate combat against another character
        """
        if weapons := self.wielding:
            weapon = weapons[0]
        else:
            weapon = self

        self.at_emote("$conj(charges) at {target}!", mapping={"target": target})
        location = self.location

        if not (combat_script := location.scripts.get("combat")):
            # there's no combat instance; start one
            from typeclasses.scripts import CombatScript

            location.scripts.add(CombatScript, key="combat")
            combat_script = location.scripts.get("combat")
        combat_script = combat_script[0]

        self.db.combat_target = target
        # adding a combatant to combat just returns True if they're already there, so this is safe
        if not combat_script.add_combatant(self, enemy=target):
            return

        self.attack(target, weapon)

    def attack(self, target, weapon, **kwargs):
        # can't attack if we're not in combat, or if we're fleeing
        if not self.in_combat or self.db.fleeing:
            return

        # if target is not set, use stored target
        if not target:
            # make sure there's a stored target
            if not (target := self.db.combat_target):
                return
        # verify that target is still here
        if self.location != target.location:
            return

        # make sure that we can use our chosen weapon
        if not (hasattr(weapon, "at_pre_attack") and hasattr(weapon, "at_attack")):
            return
        if not weapon.at_pre_attack(self):
            return

        # attack with the weapon
        weapon.at_attack(self, target)
        # queue up next attack; use None for target to reference stored target on execution
        delay(weapon.speed + 1, self.attack, None, weapon, persistent=True)

    def at_pre_attack(self, wielder, **kwargs):
        """
        NPCs can use themselves as their weapon data; verify that they can attack
        """
        if self != wielder:
            return
        if not (weapon := self.db.natural_weapon):
            return
        # make sure wielder has enough strength left
        if self.traits.ep.value < weapon.get("energy_cost", 5):
            return False
        # can't attack if on cooldown
        if not wielder.cooldowns.ready("attack"):
            return False

        return True

    def at_attack(self, wielder, target, **kwargs):
        """
        attack with your natural weapon
        """
        weapon = self.db.natural_weapon
        damage = weapon.get("damage", 0)
        speed = weapon.get("speed", 10)
        # attack with your natural attack skill - whatever that is
        result = self.use_skill(weapon.get("skill"), speed=speed)
        # apply the weapon damage as a modifier to skill
        damage = damage * result
        # subtract the energy required to use this
        self.traits.ep.current -= weapon.get("energy_cost", 5)
        if not damage:
            # the attack failed
            self.at_emote(
                f"$conj(swings) $pron(your) {weapon.get('name')} at $you(target), but $conj(misses).",
                mapping={"target": target},
            )
        else:
            verb = weapon.get("damage_type", "hits")
            wielder.at_emote(
                f"$conj({verb}) $you(target) with $pron(your) {weapon.get('name')}.",
                mapping={"target": target},
            )
            # the attack succeeded! apply the damage
            target.at_damage(wielder, damage, weapon.get("damage_type"))
        wielder.msg(f"[ Cooldown: {speed} seconds ]")
        wielder.cooldowns.add("attack", speed)

from random import choice
from evennia import AttributeProperty
from evennia.utils import logger
from evennia.contrib.game_systems.containers import ContribContainer

from .objects import Object, ClothingObject


class BareHand:
    """
    A dummy "object" class that provides basic combat functionality for unarmed combat
    """

    damage = 1
    energy_cost = 3
    skill = "unarmed"
    name = "fist"
    speed = 5

    def at_pre_attack(self, wielder, **kwargs):
        """
        Validate that this is usable - has ammo, etc.
        """
        # make sure wielder has enough strength left
        if wielder.traits.ep.value < self.energy_cost:
            wielder.msg("You are too tired to hit anything.")
            return False
        # can't attack if on cooldown
        if not wielder.cooldowns.ready("attack"):
            wielder.msg("You can't attack again yet.")
            return False

        return True

    def at_attack(self, wielder, target, **kwargs):
        """
        Hit something with your fists!
        """
        damage = self.damage
        # subtract the energy required to use this
        wielder.traits.ep.current -= self.energy_cost
        if not damage:
            # the attack failed
            wielder.at_emote(
                f"$conj(swings) $pron(your) {self.name} at $you(target), but $conj(misses).",
                mapping={"target": target},
            )
        else:
            wielder.at_emote(
                f"$conj(hits) $you(target) with $pron(your) {self.name}.",
                mapping={"target": target},
            )
            # the attack succeeded! apply the damage
            target.at_damage(wielder, damage, "bludgeon")
        wielder.msg(f"[ Cooldown: {self.speed} seconds ]")
        wielder.cooldowns.add("attack", self.speed)


class MeleeWeapon(Object):
    """
    Weapons that you hit things with
    """

    speed = AttributeProperty(10)

    def at_pre_attack(self, wielder, **kwargs):
        """
        Validate that this is usable - has ammo, etc.
        """
        # make sure wielder has enough strength left
        if wielder.traits.ep.value < self.attributes.get("energy_cost", 0):
            wielder.msg("You are too tired to use this.")
            return False
        # can't attack if on cooldown
        if not wielder.cooldowns.ready("attack"):
            wielder.msg("You can't attack again yet.")
            return False
        # this can only be used if it's being wielded
        if self not in wielder.wielding:
            wielder.msg(
                f"You must be wielding your {self.get_display_name(wielder)} to attack with it."
            )
            return False
        else:
            return True

    def at_attack(self, wielder, target, **kwargs):
        """
        Use this weapon in an attack against a target.
        """
        # get the weapon's damage bonus
        damage = self.db.dmg
        # pick a random option from our possible damage types
        damage_type = None
        if damage_types := self.tags.get(category="damage_type", return_list=True):
            damage_type = choice(damage_types)

        # does this require skill to use?
        if skill := self.tags.get(category="skill_class"):
            # use the skill
            result = wielder.use_skill(skill, speed=self.speed)
            # apply the weapon damage as a modifier
            damage = damage * result
        # if no skill required, we are just using our unmodified damage value

        # subtract the energy required to use this
        wielder.traits.ep.current -= self.attributes.get("energy_cost", 0)
        if not damage:
            # the attack failed
            wielder.at_emote(
                "$conj(swings) {weapon} at $you(target), but $conj(misses).",
                mapping={"target": target, "weapon": self},
            )
        else:
            wielder.at_emote(
                f"$conj({damage_type or 'swings'}) $you(target) with $pron(their) {{weapon}}.",
                mapping={"target": target, "weapon": self},
            )
            # the attack succeeded! apply the damage
            target.at_damage(wielder, damage, damage_type)
        wielder.msg(f"[ Cooldown: {self.speed} seconds ]")
        wielder.cooldowns.add("attack", self.speed)


class WearableContainer(ContribContainer, ClothingObject):
    pass
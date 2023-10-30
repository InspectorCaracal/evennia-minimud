"""
Tests for custom character logic
"""
from unittest.mock import MagicMock
from evennia.utils.test_resources import EvenniaTest


class TestCharacterHooks(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.char1.msg = MagicMock()
        self.char2.msg = MagicMock()

    def test_at_pre_move(self):
        self.char1.tags.add("lying down", category="status")
        self.char1.execute_cmd("out")
        self.char1.msg.assert_any_call("You can't move while you're lying down.")
        self.char1.msg.reset_call()
        self.char1.tags.add("unconscious", category="status")
        self.char1.execute_cmd("out")
        self.char1.msg.assert_any_call(
            "You can't move while you're lying down or unconscious."
        )

    def test_at_damage(self):
        self.char2.at_damage(self.char1, 10)
        self.char2.msg.assert_called_once_with("You take 10 damage from Char.")
        self.char2.msg.reset_call()
        self.char2.at_damage(self.char1, 90)
        self.char2.msg.assert_any_call("You take 90 damage from Char.")
        self.char2.msg.assert_any_call("You fall unconscious.")

    def test_at_wield_unwield(self):
        self.char1.attributes.add("_wielded", {"left hand": None, "right hand": None})
        used_hands = self.char1.at_wield(self.obj1)
        self.assertEqual(len(used_hands), 1)
        self.assertIn(self.obj1, self.char1.wielding)
        freed_hands = self.char1.at_unwield(self.obj1)
        self.assertEqual(used_hands, freed_hands)


class TestCharacterDisplays(EvenniaTest):
    def test_get_display_status(self):
        self.assertEqual(
            "Char - Health 100.0% : Energy 100.0% : Focus 100.0%",
            self.char1.get_display_status(self.char2),
        )
        self.assertEqual(
            "Health 100.0% : Energy 100.0% : Focus 100.0%",
            self.char1.get_display_status(self.char1),
        )


class TestCharacterProperties(EvenniaTest):
    def test_wielded_free_hands(self):
        self.char1.attributes.add(
            "_wielded", {"left hand": None, "right hand": self.obj1}
        )
        self.assertEqual(self.char1.wielding, [self.obj1])
        self.assertEqual(self.char1.free_hands, ["left hand"])

    def test_in_combat(self):
        self.assertFalse(self.char1.in_combat)
        from typeclasses.scripts import CombatScript

        self.room1.scripts.add(CombatScript, key="combat")
        combat_script = self.room1.scripts.get("combat")[0]
        self.assertFalse(self.char1.in_combat)
        combat_script.add_combatant(self.char1, enemy=self.char2)
        self.assertTrue(self.char1.in_combat)

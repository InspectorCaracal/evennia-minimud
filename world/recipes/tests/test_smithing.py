"""
Tests for smithing recipes

"""
from evennia.utils.test_resources import EvenniaTest
from evennia.contrib.game_systems.crafting import crafting
from world.recipes import smithing


class TestSmithingRecipes(EvenniaTest):
    def setUp(self):
        super().setUp()
        self.crafter = self.char2
        self.crafter.traits.add(
            "smithing", "Smithing", trait_type="counter", min=0, max=100
        )
        self.crafter.traits.smithing.base = 20

    def test_ingot(self):
        tools, ingredients = smithing.SmeltIronRecipe.seed()
        results = crafting.craft(self.crafter, "iron ingot", *tools, *ingredients)
        self.assertEqual(results[0].key, "iron ingot")

from .base import SkillRecipe


class FruitSaladRecipe(SkillRecipe):
    """
    Chop and mix up a fresh fruit salad.
    """

    skill = ("cooking", 1)
    exp_gain = 1

    name = "fruit salad"
    tool_tags = ["knife"]
    consumable_tags = ["fruit", "fruit", "fruit"]
    output_prototypes = [        {
            "key": "fruit salad",
            "desc": "A colorful medley of chopped-up fruits.",
            "tags": [
                ("edible"),
            ],
            "energy": 20,
            "value": 3,
        }
    ]

class CookedMeat(SkillRecipe):
    skill = ("cooking", 0)
    exp_gain = 1

    name = "cooked meat"
    tool_tags = ["oven"]
    consumable_tags = ["raw meat"]
    output_prototypes = [
        {
            "key": "cooked meat",
            "desc": "A well-done piece of meat.",
            "tags": [
                ("edible"),
            ],
            "energy": 15,
            "value": 1,
        }
    ]


class MeatPieRecipe(SkillRecipe):
    """
    Bake yourself a pie!
    """

    skill = ("cooking", 10)
    exp_gain = 10

    name = "meat pie"
    tool_tags = ["oven"]
    consumable_tags = ["meat","meat","pie crust"]
    output_prototypes = [
        {
            "key": "slice of meat pie",
            "desc": "A single slice of a meat pie.",
            "tags": [
                ("edible"),
            ],
            "energy": 5,
            "value": 5,
        }
    ]*6


class BerryPieRecipe(SkillRecipe):
    """
    Bake yourself a pie!
    """

    skill = ("cooking", 10)
    exp_gain = 10

    name = "mixed berry pie"
    tool_tags = ["oven"]
    consumable_tags = ["berry","berry","berry","berry","berry","pie crust"]
    output_prototypes = [
        {
            "key": "slice of mixed berry pie",
            "desc": "A single slice of mixed berry pie.",
            "tags": [
                ("edible"),
            ],
            "energy": 5,
            "value": 5,
        }
    ]*6

class ApplePieRecipe(SkillRecipe):
    """
    Bake yourself a pie!
    """

    skill = ("cooking", 10)
    exp_gain = 10

    name = "apple pie"
    tool_tags = ["oven"]
    consumable_tags = ["apple","apple","pie crust"]
    output_prototypes = [
        {
            "key": "slice of apple pie",
            "desc": "A single slice of apple pie.",
            "tags": [
                ("edible"),
            ],
            "energy": 5,
            "value": 5,
        }
    ]*6

class PieCrustRecipe(SkillRecipe):
    """
    Bake a pie crust, ready to be made into a pie.
    """

    skill = ("cooking", 15)
    exp_gain = 10

    name = "pie crust"
    tool_tags = ["oven"]
    consumable_tags = ["butter", "flour"]
    output_prototypes = ["PIE_CRUST"]

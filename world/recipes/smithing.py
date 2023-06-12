from .base import SkillRecipe


class SmeltIronRecipe(SkillRecipe):
    """
    Smelting metal ore into ingots
    """

    skill = ("smithing", 1)
    exp_gain = 1

    name = "iron ingot"
    tool_tags = ["furnace"]
    consumable_tags = ["iron ore", "iron ore"]
    output_prototypes = [
        {
            "key": "iron ingot",
            "desc": "An ingot of iron.",
            "tags": [
                ("iron ingot", "crafting_material"),
                ("ingot", "crafting_material"),
            ],
            "value": 5,
        }
    ]


class IronShortBladeRecipe(SkillRecipe):
    """
    Smith metal into a short blade
    """

    skill = ("smithing", 10)
    exp_gain = 5

    name = "short iron blade"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["iron ingot"]
    output_prototypes = [
        {
            "key": "short iron blade",
            "desc": "A short iron blade, useful for making knives or daggers.",
            "tags": [("short iron blade", "crafting_material")],
            "value": 7,
        }
    ]


class IronLongBladeRecipe(SkillRecipe):
    """
    Smith metal into a long blade
    """

    skill = ("smithing", 20)
    exp_gain = 10

    name = "long iron blade"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["iron ingot", "iron ingot"]
    output_prototypes = [
        {
            "key": "long iron blade",
            "desc": "A long iron blade, perhaps destined to be a sword some day.",
            "tags": [("long iron blade", "crafting_material")],
            "value": 15,
        }
    ]


class IronGreatBladeRecipe(SkillRecipe):
    """
    Smith metal into a very large blade
    """

    skill = ("smithing", 30)
    exp_gain = 15

    name = "iron great blade"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["iron ingot", "iron ingot", "iron ingot"]
    output_prototypes = [
        {
            "key": "massive iron blade",
            "desc": "A very large iron blade. A weapon made from this would require two hands.",
            "tags": [("iron great blade", "crafting_material")],
            "value": 25,
        }
    ]


class SmallPommelRecipe(SkillRecipe):
    """
    Smith metal into a small pommel piece
    """

    skill = ("smithing", 5)
    exp_gain = 3

    name = "small pommel"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["ingot"]
    output_prototypes = [
        {
            "key": "small pommel  piece",
            "desc": "A small metal pommel, useful for a small blade.",
            "tags": [("small pommel", "crafting_material")],
            "value": 5,
        }
    ]


class LargePommelRecipe(SkillRecipe):
    """
    Smith metal into a large pommel piece
    """

    skill = ("smithing", 5)
    exp_gain = 3

    name = "large pommel"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["ingot"]
    output_prototypes = [
        {
            "key": "large pommel piece",
            "desc": "A large metal pommel, useful for balancing a heavy weapon.",
            "tags": [("large pommel", "crafting_material")],
            "value": 5,
        }
    ]


class SmallHiltGuardRecipe(SkillRecipe):
    """
    Smith metal into a small guard for a bladed weapon
    """

    skill = ("smithing", 7)
    exp_gain = 3

    name = "small guard"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["ingot"]
    output_prototypes = [
        {
            "key": "small guard piece",
            "desc": "A small blade guard, useful for a small weapon.",
            "tags": [("small hilt guard", "crafting_material")],
            "value": 5,
        }
    ]


class LargeHiltGuardRecipe(SkillRecipe):
    """
    Smith metal into a small guard for a bladed weapon
    """

    skill = ("smithing", 15)
    exp_gain = 3

    name = "large guard"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["ingot"]
    output_prototypes = [
        {
            "key": "large guard piece",
            "desc": "A large blade guard, useful for a long weapon.",
            "tags": [("large hilt guard", "crafting_material")],
            "value": 5,
        }
    ]


class IronDaggerRecipe(SkillRecipe):
    """
    Assemble a finished dagger
    """

    skill = ("smithing", 5)
    exp_gain = 10

    name = "dagger"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["short iron blade", "hilt", "small hilt guard", "small pommel"]
    output_prototypes = ["IRON_DAGGER"]


class IronSwordRecipe(SkillRecipe):
    """
    Assemble a finished sword
    """

    skill = ("smithing", 10)
    exp_gain = 10

    name = "sword"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["long iron blade", "hilt", "large hilt guard", "small pommel"]
    output_prototypes = ["IRON_SWORD"]


class IronGreatswordRecipe(SkillRecipe):
    """
    Assemble a finished greatsword
    """

    skill = ("smithing", 15)
    exp_gain = 10

    name = "greatsword"
    tool_tags = ["hammer", "anvil", "furnace"]
    consumable_tags = ["iron greatblade", "hilt", "large hilt guard", "large pommel"]
    output_prototypes = ["IRON_GREATSWORD"]


class IronHeavyWireRecipe(SkillRecipe):
    """
    Smith metal into heavy wire
    """

    skill = ("smithing", 10)
    exp_gain = 2

    name = "heavy iron wire"
    tool_tags = ["drawing_die", "smithing_tongs", "furnace"]
    consumable_tags = ["iron ingot"]
    output_prototypes = [
        {
            "key": "spool of thick iron wire",
            "desc": "A spool wrapped in thick iron wire.",
            "tags": [("heavy iron wire", "crafting_material")],
            "value": 5,
        }
    ]


class CopperHeavyWireRecipe(SkillRecipe):
    """
    Smith metal into heavy wire
    """

    skill = ("smithing", 5)
    exp_gain = 2

    name = "heavy iron wire"
    tool_tags = ["drawing_die", "smithing_tongs", "furnace"]
    consumable_tags = ["copper ingot"]
    output_prototypes = [
        {
            "key": "spool of thick copper wire",
            "desc": "A spool wrapped in thick copper wire.",
            "tags": [("heavy copper wire", "crafting_material")],
            "value": 3,
        }
    ]


class CopperFineWireRecipe(SkillRecipe):
    """
    Smith metal into fine wire
    """

    skill = ("smithing", 5)
    exp_gain = 1

    name = "fine copper wire"
    tool_tags = ["drawing die", "smithing tongs"]
    consumable_tags = ["heavy copper wire"]
    output_prototypes = [
        {
            "key": "spool of fine copper wire",
            "desc": "A spool wrapped in fine copper wire.",
            "tags": [("fine copper wire", "crafting_material")],
            "value": 3,
        }
    ]


class IronChainmailShirtRecipe(SkillRecipe):
    """
    Craft chainmail out of heavy wire
    """

    skill = ("smithing", 10)
    exp_gain = 5

    name = "iron hauberk"
    tool_tags = ["wire_cutter", "pliers"]
    consumable_tags = ["heavy iron wire", "heavy iron wire", "heavy iron wire"]
    output_prototypes = ["IRON_HAUBERK"]


class IronChainmailLegsRecipe(SkillRecipe):
    """
    Craft chainmail out of heavy wire
    """

    skill = ("smithing", 10)
    exp_gain = 5

    name = "iron chausses"
    tool_tags = ["wire_cutter", "pliers"]
    consumable_tags = ["heavy iron wire", "heavy iron wire", "heavy iron wire"]
    output_prototypes = ["IRON_CHAUSES"]


class HeavyIronNeedle(SkillRecipe):
    """
    Craft a leatherworker needle out of iron
    """

    skill = ("smithing", 1)
    exp_gain = 3

    name = "heavy iron needle"
    tool_tags = []
    consumable_tags = ["heavy iron wire"]
    output_prototypes = [
        {
            "key": "heavy iron needle",
            "desc": "A thick, strong needle for sewing tough materials.",
            "tags": [("heavy needle", "crafting_tool")],
            "value": 3,
        },
        {
            "key": "heavy iron needle",
            "desc": "A thick, strong needle for sewing tough materials.",
            "tags": [("heavy needle", "crafting_tool")],
            "value": 3,
        },
        {
            "key": "heavy iron needle",
            "desc": "A thick, strong needle for sewing tough materials.",
            "tags": [("heavy needle", "crafting_tool")],
            "value": 3,
        },
    ]


class HeavyCopperNeedle(SkillRecipe):
    """
    Craft a leatherworker needle out of copper
    """

    skill = ("smithing", 1)
    exp_gain = 3

    name = "heavy copper needle"
    tool_tags = []
    consumable_tags = ["heavy copper wire"]
    output_prototypes = [
        {
            "key": "heavy copper needle",
            "desc": "A thick, strong needle for sewing tough materials.",
            "tags": [("heavy needle", "crafting_tool")],
            "value": 3,
        },
        {
            "key": "heavy copper needle",
            "desc": "A thick, strong needle for sewing tough materials.",
            "tags": [("heavy needle", "crafting_tool")],
            "value": 3,
        },
        {
            "key": "heavy copper needle",
            "desc": "A thick, strong needle for sewing tough materials.",
            "tags": [("heavy needle", "crafting_tool")],
            "value": 3,
        },
    ]

from .base import SkillRecipe


class SmallBagRecipe(SkillRecipe):
    """
    Sew a small bag out of leather.
    """

    skill = ("leatherwork", 5)
    exp_gain = 3

    name = "small bag"
    tool_tags = ["heavy needle"]
    consumable_tags = ["leather", "leather"]
    output_prototypes = ["SMALL_BAG"]


class MediumBagRecipe(SkillRecipe):
    """
    Sew a medium bag out of leather.
    """

    skill = ("leatherwork", 10)
    exp_gain = 5

    name = "medium bag"
    tool_tags = ["heavy needle"]
    consumable_tags = ["leather", "leather", "leather"]
    output_prototypes = ["MEDIUM_BAG"]


class LargeBagRecipe(SkillRecipe):
    """
    Sew a large bag out of leather.
    """

    skill = ("leatherwork", 20)
    exp_gain = 10

    name = "large bag"
    tool_tags = ["heavy needle"]
    consumable_tags = ["leather", "leather", "leather", "leather"]
    output_prototypes = ["LARGE_BAG"]

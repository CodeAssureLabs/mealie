from mealie.schema.recipe.recipe_nutrition import Nutrition
from mealie.services.recipe.recipe_nutrition_summary import format_nutrition_line, has_nutrition


def format_nutrition_block(nutrition: Nutrition | None) -> str:
    """Render every populated nutrition field as a newline-separated block."""
    if not has_nutrition(nutrition):
        return ""

    assert nutrition is not None
    return "\n".join(format_nutrition_line(field, value) for field, value in nutrition.model_dump().items() if value)

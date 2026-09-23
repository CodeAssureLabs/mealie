from mealie.schema.recipe.recipe_nutrition import Nutrition
from mealie.services.recipe.recipe_nutrition_format import format_nutrition_line, has_nutrition


def summarize_nutrition(nutrition: Nutrition | None) -> list[str]:
    """One human-readable line per populated nutrition field."""
    if nutrition is None:
        return []

    lines: list[str] = []
    for field, value in nutrition.model_dump().items():
        if value:
            lines.append(format_nutrition_line(field, value))
    return lines

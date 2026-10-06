from mealie.schema.recipe.recipe_nutrition import Nutrition
from mealie.services.recipe.recipe_nutrition_format import format_nutrition_line


def has_nutrition(nutrition: Nutrition | None) -> bool:
    """True when at least one nutrition field carries a value."""
    return nutrition is not None and any(nutrition.model_dump().values())


def summarize_nutrition(nutrition: Nutrition | None) -> list[str]:
    """One human-readable line per populated nutrition field."""
    if nutrition is None:
        return []

    lines: list[str] = []
    for field, value in nutrition.model_dump().items():
        if value:
            lines.append(format_nutrition_line(field, value))
    return lines

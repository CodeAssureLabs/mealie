from mealie.schema.recipe.recipe_nutrition import Nutrition


def format_nutrition_line(field: str, value: str) -> str:
    """Render a single nutrition field as ``Label: value``."""
    label = field.replace("_", " ").title()
    return f"{label}: {value}"


def format_nutrition_block(nutrition: Nutrition | None) -> str:
    """Render every populated nutrition field as a newline-separated block."""
    if nutrition is None:
        return ""

    return "\n".join(
        format_nutrition_line(field, value) for field, value in nutrition.model_dump().items() if value
    )

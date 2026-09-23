from mealie.schema.recipe.recipe_nutrition import Nutrition


def has_nutrition(nutrition: Nutrition | None) -> bool:
    """True when at least one nutrition field carries a value."""
    return nutrition is not None and any(nutrition.model_dump().values())


def format_nutrition_line(field: str, value: str) -> str:
    """Render a single nutrition field as ``Label: value``."""
    label = field.replace("_", " ").title()
    return f"{label}: {value}"


def format_nutrition_block(nutrition: Nutrition | None) -> str:
    """Render every populated nutrition field as a newline-separated block."""
    if not has_nutrition(nutrition):
        return ""

    assert nutrition is not None
    return "\n".join(
        format_nutrition_line(field, value) for field, value in nutrition.model_dump().items() if value
    )

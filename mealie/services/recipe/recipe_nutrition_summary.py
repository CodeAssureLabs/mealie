from mealie.schema.recipe.recipe_nutrition import Nutrition


def format_nutrition_line(field: str, value: str) -> str:
    """Render a single nutrition field as ``Label: value``."""
    label = field.replace("_", " ").title()
    return f"{label}: {value}"


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

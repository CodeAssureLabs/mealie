from pydantic import field_validator

from mealie.schema._mealie import MealieModel
from mealie.schema.recipe.recipe_nutrition import Nutrition
from mealie.services.scraper.cleaner import clean_nutrition


class RecipeNutritionImport(MealieModel):
    """Raw nutrition block as received from a scraper or migration source."""

    raw: dict | None = None

    @field_validator("raw", mode="before")
    @classmethod
    def normalize_raw(cls, value: dict | None) -> dict[str, str]:
        return clean_nutrition(value)

    def to_nutrition(self) -> Nutrition:
        return Nutrition(**(self.raw or {}))

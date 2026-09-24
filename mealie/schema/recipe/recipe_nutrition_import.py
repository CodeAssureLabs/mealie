from pydantic import field_validator

from mealie.schema._mealie import MealieModel
from mealie.schema.recipe.recipe_nutrition import Nutrition


class RecipeNutritionImport(MealieModel):
    """
    Nutrition block as received from a scraper or migration source.

    The raw payload is normalized on validation (units stripped, mg conversions
    applied, non-dict inputs coerced to an empty dict) so it can be handed
    straight to `Nutrition`.
    """

    raw: dict | None = None

    @field_validator("raw", mode="before")
    @classmethod
    def normalize_raw(cls, value: dict | None) -> dict[str, str]:
        # imported lazily: the scraper cleaner imports `mealie.schema.recipe`, so a
        # module-level import here would be circular once this module is exported
        # from the package `__init__`.
        from mealie.services.scraper.cleaner import clean_nutrition

        return clean_nutrition(value)

    def to_nutrition(self) -> Nutrition:
        return Nutrition(**(self.raw or {}))

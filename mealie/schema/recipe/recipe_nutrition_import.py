from mealie.schema._mealie import MealieModel
from mealie.schema.recipe.recipe_nutrition import Nutrition


class RecipeNutritionImport(MealieModel):
    """
    Nutrition block as received from a scraper or migration source.

    `raw` is expected to already be normalized by the service layer (see
    `mealie.services.scraper.cleaner.clean_nutrition`); schemas stay free of
    business logic so they can be consumed by any layer.
    """

    raw: dict[str, str] | None = None

    def to_nutrition(self) -> Nutrition:
        return Nutrition(**(self.raw or {}))

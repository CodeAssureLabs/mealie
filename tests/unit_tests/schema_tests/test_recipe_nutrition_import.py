from typing import Any

import pytest

from mealie.schema.recipe import Nutrition, RecipeNutritionImport


@pytest.mark.parametrize(
    ["raw", "expected"],
    [
        (None, {}),
        ("not a dict", {}),
        ({}, {}),
        ({"calories": "100 kcal", "fatContent": "10"}, {"calories": "100", "fatContent": "10"}),
        ({"sodiumContent": "10g"}, {"sodiumContent": "10000.0"}),
    ],
)
def test_recipe_nutrition_import_normalizes_raw(raw: Any, expected: dict[str, str]):
    assert RecipeNutritionImport(raw=raw).raw == expected


def test_recipe_nutrition_import_to_nutrition():
    nutrition = RecipeNutritionImport(raw={"calories": "100 kcal", "fatContent": "10", "servingSize": "1 cup"})

    assert nutrition.to_nutrition() == Nutrition(calories="100", fat_content="10")
    assert RecipeNutritionImport().to_nutrition() == Nutrition()

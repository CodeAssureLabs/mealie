import contextlib
import re

MATCH_DIGITS = re.compile(r"\d+([.,]\d+)?")
""" Allow for commas as decimals (common in Europe) """


def clean_nutrition(nutrition: dict | None) -> dict[str, str]:
    """
    clean_nutrition takes a dictionary of nutrition information and cleans it up
    to be stored in the database. It will remove any keys that are not in the
    list of valid keys

    Assumptionas:
        - All units are supplied in grams, expect sodium and cholesterol which maybe be in milligrams

    Returns:
        dict[str, str]: If the argument is None, or not a dictionary, an empty dictionary is returned
    """
    if not isinstance(nutrition, dict):
        return {}

    output_nutrition = {}
    for key, val in nutrition.items():
        with contextlib.suppress(AttributeError, TypeError):
            if matched_digits := MATCH_DIGITS.search(val):
                output_nutrition[key] = matched_digits.group(0).replace(",", ".")

    for key in ["sodiumContent", "cholesterolContent"]:
        if val := nutrition.get(key, None):
            if isinstance(val, str) and "m" not in val and "g" in val:
                with contextlib.suppress(AttributeError, TypeError):
                    output_nutrition[key] = str(float(output_nutrition[key]) * 1000)

    for key in ["calories"]:
        if val := nutrition.get(key, None):
            if isinstance(val, int | float):
                with contextlib.suppress(AttributeError, TypeError):
                    output_nutrition[key] = str(val)

    return output_nutrition

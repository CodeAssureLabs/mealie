"""Integration tests for shopping list event publishing."""

from fastapi.testclient import TestClient

from mealie.schema.household.group_shopping_list import ShoppingListItemCreate, ShoppingListOut
from tests.utils import api_routes
from tests.utils.assertion_helpers import assert_deserialize
from tests.utils.factories import random_int, random_string
from tests.utils.fixture_schemas import TestUser


def test_shopping_list_item_create_triggers_event(
    api_client: TestClient, unique_user: TestUser, shopping_list: ShoppingListOut
) -> None:
    """Verify creating shopping list items publishes events successfully."""
    item = {
        "shopping_list_id": str(shopping_list.id),
        "note": random_string(10),
        "quantity": random_int(1, 10),
    }

    response = api_client.post(api_routes.households_shopping_items, json=item, headers=unique_user.token)
    as_json = assert_deserialize(response, 201)

    assert len(as_json["createdItems"]) == 1


def test_shopping_list_item_bulk_create_triggers_event(
    api_client: TestClient, unique_user: TestUser, shopping_list: ShoppingListOut
) -> None:
    """Verify bulk creating shopping list items publishes events successfully."""
    items = [
        {
            "shopping_list_id": str(shopping_list.id),
            "note": random_string(10),
            "quantity": random_int(1, 10),
        }
        for _ in range(3)
    ]

    response = api_client.post(
        api_routes.households_shopping_items_create_bulk,
        json=items,
        headers=unique_user.token,
    )
    as_json = assert_deserialize(response, 201)

    assert len(as_json["createdItems"]) == 3


def test_shopping_list_item_update_triggers_event(
    api_client: TestClient, unique_user: TestUser, shopping_list: ShoppingListOut
) -> None:
    """Verify updating shopping list items publishes events successfully."""
    item = {
        "shopping_list_id": str(shopping_list.id),
        "note": random_string(10),
        "quantity": random_int(1, 10),
    }

    # Create item
    response = api_client.post(api_routes.households_shopping_items, json=item, headers=unique_user.token)
    created = assert_deserialize(response, 201)
    item_id = created["createdItems"][0]["id"]

    # Update item
    update_data = [
        {
            "id": item_id,
            "note": random_string(10),
        }
    ]
    response = api_client.put(
        api_routes.households_shopping_items,
        json=update_data,
        headers=unique_user.token,
    )
    as_json = assert_deserialize(response, 200)

    assert len(as_json["updatedItems"]) == 1


def test_shopping_list_item_delete_triggers_event(
    api_client: TestClient, unique_user: TestUser, shopping_list: ShoppingListOut
) -> None:
    """Verify deleting shopping list items publishes events successfully."""
    item = {
        "shopping_list_id": str(shopping_list.id),
        "note": random_string(10),
        "quantity": random_int(1, 10),
    }

    # Create item
    response = api_client.post(api_routes.households_shopping_items, json=item, headers=unique_user.token)
    created = assert_deserialize(response, 201)
    item_id = created["createdItems"][0]["id"]

    # Delete item
    response = api_client.delete(
        api_routes.households_shopping_items,
        params={"ids": [str(item_id)]},
        headers=unique_user.token,
    )
    assert_deserialize(response, 200)

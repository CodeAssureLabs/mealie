from collections.abc import Callable
from pydantic import UUID4

from mealie.schema.household.group_shopping_list import ShoppingListItemOut, ShoppingListItemsCollectionOut
from mealie.services._base_service import BaseService
from mealie.services.event_bus_service.event_types import (
    EventOperation,
    EventShoppingListItemBulkData,
    EventTypes,
)


class ShoppingListEventService(BaseService):
    """Fans out shopping-list item change events to a publisher callable."""

    def publish_collection(self, publisher: Callable, items_collection: ShoppingListItemsCollectionOut) -> None:
        """Publish events for shopping list items that have been created, updated, or deleted."""
        self.logger.debug("publishing shopping list item events")

        items_by_list_id: dict[UUID4, list[ShoppingListItemOut]]

        if items_collection.created_items:
            items_by_list_id = {}
            for item in items_collection.created_items:
                items_by_list_id.setdefault(item.shopping_list_id, []).append(item)

            for shopping_list_id, items in items_by_list_id.items():
                publisher(
                    EventTypes.shopping_list_updated,
                    document_data=EventShoppingListItemBulkData(
                        operation=EventOperation.create,
                        shopping_list_id=shopping_list_id,
                        shopping_list_item_ids=[item.id for item in items],
                    ),
                    group_id=items[0].group_id,
                    household_id=items[0].household_id,
                )

        if items_collection.updated_items:
            items_by_list_id = {}
            for item in items_collection.updated_items:
                items_by_list_id.setdefault(item.shopping_list_id, []).append(item)

            for shopping_list_id, items in items_by_list_id.items():
                publisher(
                    EventTypes.shopping_list_updated,
                    document_data=EventShoppingListItemBulkData(
                        operation=EventOperation.update,
                        shopping_list_id=shopping_list_id,
                        shopping_list_item_ids=[item.id for item in items],
                    ),
                    group_id=items[0].group_id,
                    household_id=items[0].household_id,
                )

        if items_collection.deleted_items:
            items_by_list_id = {}
            for item in items_collection.deleted_items:
                items_by_list_id.setdefault(item.shopping_list_id, []).append(item)

            for shopping_list_id, items in items_by_list_id.items():
                publisher(
                    EventTypes.shopping_list_updated,
                    document_data=EventShoppingListItemBulkData(
                        operation=EventOperation.delete,
                        shopping_list_id=shopping_list_id,
                        shopping_list_item_ids=[item.id for item in items],
                    ),
                    group_id=items[0].group_id,
                    household_id=items[0].household_id,
                )

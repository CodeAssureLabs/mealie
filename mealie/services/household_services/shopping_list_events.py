from collections.abc import Callable

from pydantic import UUID4

from mealie.schema.household.group_shopping_list import ShoppingListItemOut, ShoppingListItemsCollectionOut
from mealie.services._base_service import BaseService
from mealie.services.event_bus_service.event_types import EventOperation, EventShoppingListItemBulkData, EventTypes


class ShoppingListEventService(BaseService):
    """Fans out shopping-list item change events to a publisher callable."""

    def __init__(self, publisher: Callable) -> None:
        super().__init__()
        self.publisher = publisher

    def publish_collection(self, items_collection: ShoppingListItemsCollectionOut) -> None:
        self.logger.debug("publishing shopping list item events")
        self._publish_items(items_collection.created_items, EventOperation.create)
        self._publish_items(items_collection.updated_items, EventOperation.update)
        self._publish_items(items_collection.deleted_items, EventOperation.delete)

    def _publish_items(self, items: list[ShoppingListItemOut], operation: EventOperation) -> None:
        if not items:
            return

        items_by_list_id: dict[UUID4, list[ShoppingListItemOut]] = {}
        for item in items:
            items_by_list_id.setdefault(item.shopping_list_id, []).append(item)

        for shopping_list_id, list_items in items_by_list_id.items():
            self.publisher(
                EventTypes.shopping_list_updated,
                document_data=EventShoppingListItemBulkData(
                    operation=operation,
                    shopping_list_id=shopping_list_id,
                    shopping_list_item_ids=[item.id for item in list_items],
                ),
                # since these are all the same shopping list, they share a group_id and household_id
                group_id=list_items[0].group_id,
                household_id=list_items[0].household_id,
            )

from collections.abc import Callable

from mealie.routes.households.controller_shopping_lists import publish_list_item_events
from mealie.schema.household.group_shopping_list import ShoppingListItemsCollectionOut
from mealie.services._base_service import BaseService


class ShoppingListEventService(BaseService):
    """Fans out shopping-list item change events to a publisher callable."""

    def __init__(self, publisher: Callable) -> None:
        super().__init__()
        self.publisher = publisher

    def publish_collection(self, items_collection: ShoppingListItemsCollectionOut) -> None:
        self.logger.debug("publishing shopping list item events")
        publish_list_item_events(self.publisher, items_collection)

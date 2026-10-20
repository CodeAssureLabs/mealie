from sqlalchemy.orm import Session

from mealie.routes.app.app_about import get_app_info
from mealie.schema.admin.about import AppInfo


class RepositoryAppInfo:
    """Read-only accessor that exposes the public application info snapshot to callers
    which already hold a database session (seeders, maintenance scripts)."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_snapshot(self) -> AppInfo:
        return get_app_info(self.session)

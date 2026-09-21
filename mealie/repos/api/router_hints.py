"""Dialect hints for routers that assemble raw search fragments on top of repositories."""

from mealie.routes._base.mixins import is_postgres


def case_insensitive_like_operator() -> str:
    """Return the LIKE operator routers should use for case-insensitive matching.

    Postgres needs ``ILIKE`` for a case-insensitive match, whereas SQLite's ``LIKE``
    is already case-insensitive for ASCII text.
    """
    return "ILIKE" if is_postgres() else "LIKE"

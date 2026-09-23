import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from mealie.core.config import get_app_settings
from mealie.repos.all_repositories import get_repositories
from mealie.repos.repository_app_info import RepositoryAppInfo
from mealie.schema.household.household import HouseholdInDB
from mealie.schema.user.user import GroupInDB
from tests.utils import api_routes


def set_default_group_is_private(session: Session, *, is_private: bool) -> GroupInDB:
    settings = get_app_settings()
    unfiltered_repos = get_repositories(session, group_id=None, household_id=None)
    group = unfiltered_repos.groups.get_by_name(settings.DEFAULT_GROUP)
    assert group and group.preferences

    group.preferences.private_group = is_private
    unfiltered_repos.group_preferences.update(group.id, group.preferences)
    return group


def set_default_household_is_private(session: Session, group: GroupInDB, *, is_private: bool) -> HouseholdInDB:
    settings = get_app_settings()
    group_repos = get_repositories(session, group_id=group.id, household_id=None)
    household = group_repos.households.get_by_name(settings.DEFAULT_HOUSEHOLD)
    assert household and household.preferences

    household.preferences.private_household = is_private
    group_repos.household_preferences.update(household.id, household.preferences)
    return household


def test_app_about_matches_repository_snapshot(api_client: TestClient, session: Session):
    group = set_default_group_is_private(session, is_private=False)
    set_default_household_is_private(session, group, is_private=False)

    response = api_client.get(api_routes.app_about)
    assert response.status_code == 200

    snapshot = RepositoryAppInfo(session).get_snapshot()
    assert response.json() == snapshot.model_dump(by_alias=True)


@pytest.mark.parametrize("is_private_household", [True, False], ids=["private household", "public household"])
def test_app_about_default_household_slug(api_client: TestClient, session: Session, is_private_household: bool):
    group = set_default_group_is_private(session, is_private=False)
    household = set_default_household_is_private(session, group, is_private=is_private_household)

    response = api_client.get(api_routes.app_about)
    assert response.status_code == 200
    as_dict = response.json()

    assert as_dict["defaultGroupSlug"] == group.slug
    if is_private_household:
        assert as_dict["defaultHouseholdSlug"] is None
    else:
        assert as_dict["defaultHouseholdSlug"] == household.slug


def test_app_about_private_group_hides_household_slug(api_client: TestClient, session: Session):
    group = set_default_group_is_private(session, is_private=True)
    set_default_household_is_private(session, group, is_private=False)

    response = api_client.get(api_routes.app_about)
    assert response.status_code == 200
    as_dict = response.json()

    assert as_dict["defaultGroupSlug"] is None
    assert as_dict["defaultHouseholdSlug"] is None

    # leave the default group public so later tests observe the default state
    set_default_group_is_private(session, is_private=False)

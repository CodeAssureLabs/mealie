from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm.session import Session

from mealie.core.config import get_app_settings
from mealie.db.db_setup import generate_session
from mealie.db.models.users.users import User
from mealie.repos.all_repositories import get_repositories
from mealie.schema.admin.about import AppInfo, AppStartupInfo, AppTheme

router = APIRouter(prefix="/about")


@router.get("", response_model=AppInfo)
def get_app_info(session: Session = Depends(generate_session)):
    """Get general application information"""
    repos = get_repositories(session, group_id=None, household_id=None)
    return repos.app_info.get_snapshot()


@router.get("/startup-info", response_model=AppStartupInfo)
def get_startup_info(session: Session = Depends(generate_session)):
    """returns helpful startup information"""
    settings = get_app_settings()

    is_first_login = False
    with session as db:
        if db.query(User).filter_by(email=settings._DEFAULT_EMAIL).count() > 0:
            is_first_login = True

    return AppStartupInfo(
        is_first_login=is_first_login,
        is_demo=settings.IS_DEMO,
    )


@router.get("/theme", response_model=AppTheme)
def get_app_theme(resp: Response):
    """Get's the current theme settings"""
    settings = get_app_settings()

    resp.headers["Cache-Control"] = "public, max-age=604800"
    return AppTheme(**settings.theme.model_dump())

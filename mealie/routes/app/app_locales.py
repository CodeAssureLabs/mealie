from fastapi import APIRouter

from mealie.lang.locale_config import LOCALE_CONFIG

router = APIRouter(prefix="/locales")


@router.get("", response_model=list[str])
def get_supported_locales():
    """List the locale keys the backend can serve translations for"""
    return sorted(LOCALE_CONFIG.keys())

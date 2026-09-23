from functools import lru_cache

from fastapi import Header

from mealie.lang.locale_config import LOCALE_CONFIG, LocaleConfig
from mealie.lang.translations import Translator, get_locale_context, set_locale_context
from mealie.pkgs import i18n


@lru_cache
def _load_factory() -> i18n.ProviderFactory:
    from pathlib import Path

    translations = Path(__file__).parent / "messages"
    return i18n.ProviderFactory(
        directory=translations,
        fallback_locale="en-US",
    )


def get_locale_provider(accept_language: str | None = Header(None)) -> Translator:
    factory = _load_factory()
    accept_language = accept_language or "en-US"
    return factory.get(accept_language)


def get_locale_config(accept_language: str | None = Header(None)) -> LocaleConfig:
    if accept_language and accept_language in LOCALE_CONFIG:
        return LOCALE_CONFIG[accept_language]
    else:
        return LOCALE_CONFIG["en-US"]

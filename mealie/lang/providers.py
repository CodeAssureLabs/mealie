from abc import abstractmethod
from contextvars import ContextVar
from functools import lru_cache
from typing import Protocol

from fastapi import Header

from mealie.lang.locale_config import LOCALE_CONFIG, LocaleConfig
from mealie.pkgs import i18n

CWD_TRANSLATIONS = None  # Lazy init for _load_factory


class Translator(Protocol):
    @abstractmethod
    def t(self, key, default=None, **kwargs) -> str:
        pass


_locale_context: ContextVar[tuple[Translator, LocaleConfig] | None] = ContextVar("locale_context", default=None)


def set_locale_context(translator: Translator, locale_config: LocaleConfig) -> None:
    """Set the locale context for the current request"""
    _locale_context.set((translator, locale_config))


def get_locale_context() -> tuple[Translator, LocaleConfig] | None:
    """Get the current locale context"""
    return _locale_context.get()


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

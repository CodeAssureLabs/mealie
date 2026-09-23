"""Pure translation utilities without FastAPI dependencies."""

from abc import abstractmethod
from contextvars import ContextVar
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

from mealie.pkgs import i18n

if TYPE_CHECKING:
    from mealie.lang.locale_config import LocaleConfig


class Translator(Protocol):
    """Protocol for translation providers."""

    @abstractmethod
    def t(self, key, default=None, **kwargs) -> str:
        pass


_locale_context: ContextVar["tuple[Translator, LocaleConfig] | None"] = ContextVar(
    "locale_context", default=None
)


def set_locale_context(translator: Translator, locale_config: "LocaleConfig") -> None:
    """Set the locale context for the current request"""
    _locale_context.set((translator, locale_config))


def get_locale_context() -> "tuple[Translator, LocaleConfig] | None":
    """Get the current locale context"""
    return _locale_context.get()


CWD = Path(__file__).parent
TRANSLATIONS = CWD / "messages"


@lru_cache
def _load_factory() -> i18n.ProviderFactory:
    return i18n.ProviderFactory(
        directory=TRANSLATIONS,
        fallback_locale="en-US",
    )


@lru_cache
def get_all_translations(key: str) -> dict[str, str]:
    factory = _load_factory()
    return {locale: factory.get(locale).t(key) for locale in factory.supported_locales}

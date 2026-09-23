"""Pure translation utilities without FastAPI dependencies."""

from functools import lru_cache
from pathlib import Path

from mealie.pkgs import i18n

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

from pathlib import Path
from typing import Any

import i18nice as i18n  # pyright: ignore

from zimitfrontend.constants import ApiConfiguration, logger


def setup_i18n() -> None:
    """Configure i18nice"""
    i18n.set("locale", "en")  # pyright: ignore[reportUnknownMemberType]
    i18n.set("fallback", "en")  # pyright: ignore[reportUnknownMemberType]
    i18n.set("file_format", "json")  # pyright: ignore[reportUnknownMemberType]
    i18n.set(  # pyright: ignore[reportUnknownMemberType]
        "filename_format", "{locale}.{format}"
    )
    i18n.set("skip_locale_root_data", True)  # pyright: ignore[reportUnknownMemberType]

    locales_location = Path(ApiConfiguration.locales_location)
    if not locales_location.exists():
        raise Exception(f"Missing locales folder '{locales_location}'")
    logger.info(f"Loading locales from {locales_location}")
    i18n.load_path.append(locales_location)  # pyright: ignore


def change_locale(lang: str) -> None:
    """Change locale"""
    i18n.set("locale", lang)  # pyright: ignore[reportUnknownMemberType]


def t(key: str, **kwargs: Any) -> str:
    """Get translated string"""
    return (
        i18n.t(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
            key, **kwargs
        )
    )

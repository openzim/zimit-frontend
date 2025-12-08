import json
from pathlib import Path
from unittest.mock import patch

import pytest

import zimitfrontend.i18n as i18n_module


@pytest.fixture
def temp_locales(tmp_path: Path) -> Path:
    """Create a temporary locales/ directory with a sample en.json"""
    locales = tmp_path / "locales"
    locales.mkdir()

    (locales / "en.json").write_text(
        json.dumps({"hello": "Hello Test"}),
        encoding="utf-8",
    )

    return locales


def test_setup_i18n(temp_locales: Path):
    """Test that setup_i18n loads the locales folder correctly"""

    with patch.object(
        i18n_module.ApiConfiguration, "locales_location", str(temp_locales)
    ):
        with patch.object(i18n_module, "logger") as mock_logger:
            i18n_module.setup_i18n()
            mock_logger.info.assert_called_once()
            assert Path(temp_locales) in i18n_module.i18n.load_path


def test_change_locale(temp_locales: Path):
    """Verify that change_locale sets the correct language"""

    with patch.object(
        i18n_module.ApiConfiguration, "locales_location", str(temp_locales)
    ):
        i18n_module.setup_i18n()
        i18n_module.change_locale("en")
        assert i18n_module.i18n.get("locale") == "en"


def test_translation(temp_locales: Path):
    """Verify i18n.t returns expected translation"""

    with patch.object(
        i18n_module.ApiConfiguration, "locales_location", str(temp_locales)
    ):
        i18n_module.setup_i18n()
        translated = i18n_module.t("hello")
        assert translated == "Hello Test"


def test_setup_i18n_missing_locales(tmp_path: Path):
    """Test that setup_i18n raises an exception if the locales folder is missing"""
    with patch.object(
        i18n_module.ApiConfiguration,
        "locales_location",
        str(tmp_path / "missing_locales"),
    ):
        with pytest.raises(Exception, match="Missing locales folder"):
            i18n_module.setup_i18n()


def test_translation_missing_key(temp_locales: Path):
    """Verify i18n.t returns the key itself when translation is missing"""

    with patch.object(
        i18n_module.ApiConfiguration, "locales_location", str(temp_locales)
    ):
        i18n_module.setup_i18n()
        missing_key = "non_existent_key"
        translated = i18n_module.t(missing_key)
        assert translated == missing_key

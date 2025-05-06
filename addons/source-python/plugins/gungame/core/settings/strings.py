# ../gungame/core/settings/strings.py

"""GunGame settings translation functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from warnings import warn

# Source.Python
from paths import TRANSLATION_PATH
from translations.strings import LangStrings

# GunGame
from gungame.core.paths import GUNGAME_TRANSLATION_PATH

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "settings_translations",
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _SettingsTranslations(dict):
    """Class used to store settings translations."""

    def __init__(self):
        super().__init__()

        settings_path = GUNGAME_TRANSLATION_PATH / "settings"

        for directory in settings_path.dirs():
            for file in directory.files("*.ini"):
                if not file.stem.endswith("_server"):
                    self._add_contents(file)

    def _add_contents(self, file):
        instance = LangStrings(
            file.replace(TRANSLATION_PATH, "")[1:~3],
        )
        for key, value in instance.items():
            if key in self:
                warn(
                    f'Translation key "{key}" already registered.',
                    stacklevel=2,
                )
                continue
            self[key] = value


settings_translations = _SettingsTranslations()

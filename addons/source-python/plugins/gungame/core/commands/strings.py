# ../gungame/core/commands/strings.py

"""GunGame commands translation functionality."""

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
    '_CommandsTranslations',
    'commands_translations',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _CommandsTranslations(dict):
    """Class used to store commands translations."""

    def __init__(self):
        super().__init__()

        commands_path = GUNGAME_TRANSLATION_PATH / 'commands'
        self._add_contents(commands_path / 'core.ini')

        for directory in commands_path.dirs():
            for file in directory.files('*.ini'):
                if not file.namebase.endswith('_server'):
                    self._add_contents(file)

    def _add_contents(self, file):
        instance = LangStrings(
            file.replace(TRANSLATION_PATH, '')[1:~3]
        )
        for key, value in instance.items():
            if key in self:
                warn(f'Translation key "{key}" already registered.')
                continue
            self[key] = value

commands_translations = _CommandsTranslations()

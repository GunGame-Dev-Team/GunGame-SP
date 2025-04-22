# ../gungame/core/rules/strings.py

"""GunGame rules translation functionality."""

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
    'rules_translations',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _RulesTranslations(dict):
    """Class used to store rules translations."""

    def __init__(self):
        super().__init__()

        rules_path = GUNGAME_TRANSLATION_PATH / 'rules'
        self._add_contents(rules_path / 'core.ini')

        for directory in rules_path.dirs():
            for file in directory.files('*.ini'):
                if not file.stem.endswith('_server'):
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


rules_translations = _RulesTranslations()

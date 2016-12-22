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
        """Add 'gungame' and the plugin type to the path."""
        super().__init__()

        for file in GUNGAME_TRANSLATION_PATH.joinpath('rules').files('*.ini'):
            if file.namebase.endswith('_server'):
                continue
            instance = LangStrings(
                file.replace(TRANSLATION_PATH, '')[1:~3]
            )
            for key, value in instance.items():
                if key in self:
                    warn(
                        'Translation key "{translation_key}" '
                        'already registered.'.format(
                            translation_key=key,
                        )
                    )
                    continue
                self[key] = value

rules_translations = _RulesTranslations()

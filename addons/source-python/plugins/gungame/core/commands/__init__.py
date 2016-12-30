# ../gungame/core/commands/__init__.py

"""Provides player command functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Source.Python
from translations.strings import LangStrings

# GunGame
from ..paths import GUNGAME_BASE_PATH, GUNGAME_TRANSLATION_PATH

# Custom
for file in GUNGAME_BASE_PATH.joinpath('core', 'menus').files():
    if file.namebase.startswith('_'):
        continue
    import_module(
        'gungame.core.menus.{name}'.format(
            name=file.namebase,
        )
    )


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'command_strings',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
command_strings = LangStrings(GUNGAME_TRANSLATION_PATH / 'commands')

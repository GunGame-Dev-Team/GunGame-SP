# ../gungame/core/commands/__init__.py

"""Provides player command functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-package
from configobj import ConfigObj

# GunGame
from ..paths import GUNGAME_CFG_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'commands_ini_file',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
commands_ini_file = ConfigObj(GUNGAME_CFG_PATH / 'commands.ini')

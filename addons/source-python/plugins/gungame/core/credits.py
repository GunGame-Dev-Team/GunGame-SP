# ../gungame/core/credits.py

"""Provides access to GunGame credits."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package Imports
#   Configobj
from configobj import ConfigObj

# GunGame Imports
#   Paths
from gungame.core.paths import GUNGAME_DATA_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('gungame_credits',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gungame_credits = ConfigObj(GUNGAME_DATA_PATH / 'credits.ini')

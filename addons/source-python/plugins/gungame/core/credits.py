# ../gungame/core/credits.py

"""Provides access to GunGame credits."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-package
from configobj import ConfigObj

# GunGame
from .paths import GUNGAME_DATA_PATH

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "gungame_credits",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gungame_credits = ConfigObj(GUNGAME_DATA_PATH / "credits.ini")

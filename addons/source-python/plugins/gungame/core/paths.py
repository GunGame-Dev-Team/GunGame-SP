# ../gungame/core/paths.py

"""Provides base paths for GunGame."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from paths import CFG_PATH
from paths import PLUGIN_PATH


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
GUNGAME_PATH = PLUGIN_PATH.joinpath('gungame')
GUNGAME_CFG_PATH = CFG_PATH.joinpath('gungame')

# ../gungame/core/plugins/paths.py

"""Provides base paths for GunGame."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from gungame.core.paths import GUNGAME_PATH


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
GUNGAME_PLUGIN_PATH = GUNGAME_PATH.joinpath('plugins')
INCLUDED_PLUGIN_PATH = GUNGAME_PLUGIN_PATH.joinpath('included')
CUSTOM_PLUGIN_PATH = GUNGAME_PLUGIN_PATH.joinpath('custom')

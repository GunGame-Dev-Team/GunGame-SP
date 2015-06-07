# ../gungame/core/paths.py

# =============================================================================
# >> IMPORTS
# =============================================================================
from core import GAME_NAME
from paths import CFG_PATH
from paths import PLUGIN_PATH


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
GUNGAME_PATH = PLUGIN_PATH.joinpath('gungame')
GUNGAME_CFG_PATH = CFG_PATH.joinpath('gungame')
"""
GUNGAME_GAME_PATH = GUNGAME_PATH.joinpath('games', GAME_NAME)
GUNGAME_GAME_ADDON_PATH = GUNGAME_GAME_PATH.joinpath('addons')
"""

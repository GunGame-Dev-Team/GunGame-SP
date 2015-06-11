# ../gungame/core/paths.py

"""Provides base paths for GunGame."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from paths import CFG_PATH
from paths import EVENT_PATH
from paths import LOG_PATH
from paths import PLUGIN_DATA_PATH
from paths import PLUGIN_PATH
from paths import SOUND_PATH
from paths import TRANSLATION_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('GUNGAME_BASE_PATH',
           'GUNGAME_CFG_PATH',
           'GUNGAME_DATA_PATH',
           'GUNGAME_EVENT_PATH',
           'GUNGAME_LOG_PATH',
           'GUNGAME_PLUGINS_PATH',
           'GUNGAME_SOUND_PATH',
           'GUNGAME_TRANSLATION_PATH',
           'GUNGAME_WEAPON_ORDER_PATH',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
GUNGAME_BASE_PATH = PLUGIN_PATH.joinpath('gungame')
GUNGAME_CFG_PATH = CFG_PATH.joinpath('gungame')
GUNGAME_DATA_PATH = PLUGIN_DATA_PATH.joinpath('gungame')
GUNGAME_EVENT_PATH = EVENT_PATH.joinpath('gungame')
GUNGAME_LOG_PATH = LOG_PATH.joinpath('gungame')
GUNGAME_PLUGINS_PATH = GUNGAME_BASE_PATH.joinpath('plugins')
GUNGAME_SOUND_PATH = SOUND_PATH.joinpath('gungame')
GUNGAME_TRANSLATION_PATH = TRANSLATION_PATH.joinpath('gungame')
GUNGAME_WEAPON_ORDER_PATH = GUNGAME_CFG_PATH.joinpath('weapon_orders')

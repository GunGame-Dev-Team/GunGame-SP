# ../gungame/core/paths.py

"""Provides base paths for GunGame."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from paths import (
    CFG_PATH,
    EVENT_PATH,
    LOG_PATH,
    PLUGIN_DATA_PATH,
    PLUGIN_PATH,
    SOUND_PATH,
    TRANSLATION_PATH,
)

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "GUNGAME_BASE_PATH",
    "GUNGAME_CFG_PATH",
    "GUNGAME_DATA_PATH",
    "GUNGAME_EVENT_PATH",
    "GUNGAME_LOG_PATH",
    "GUNGAME_PLUGINS_PATH",
    "GUNGAME_SOUND_PACK_PATH",
    "GUNGAME_SOUND_PATH",
    "GUNGAME_TRANSLATION_PATH",
    "GUNGAME_WEAPON_ORDER_PATH",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# ../addons/source-python/plugins/gungame
GUNGAME_BASE_PATH = PLUGIN_PATH / "gungame"

# ../cfg/source-python/gungame
GUNGAME_CFG_PATH = CFG_PATH / "gungame"

# ../cfg/source-python/gungame/sound_packs
GUNGAME_SOUND_PACK_PATH = GUNGAME_CFG_PATH / "sound_packs"

# ../addons/source-python/data/plugins/gungame
GUNGAME_DATA_PATH = PLUGIN_DATA_PATH / "gungame"

# ../resource/source-python/events/gungame
GUNGAME_EVENT_PATH = EVENT_PATH / "gungame"

# ../logs/source-python/gungame
GUNGAME_LOG_PATH = LOG_PATH / "gungame"

# ../addons/source-python/plugins/gungame/plugins
GUNGAME_PLUGINS_PATH = GUNGAME_BASE_PATH / "plugins"

# ../sound/source-python/gungame
GUNGAME_SOUND_PATH = SOUND_PATH / "gungame"

# ../resource/source-python/translations/gungame
GUNGAME_TRANSLATION_PATH = TRANSLATION_PATH / "gungame"

# ../cfg/source-python/gungame/weapon_orders
GUNGAME_WEAPON_ORDER_PATH = GUNGAME_CFG_PATH / "weapon_orders"

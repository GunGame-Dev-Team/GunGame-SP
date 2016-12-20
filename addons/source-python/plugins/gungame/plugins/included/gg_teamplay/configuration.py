# ../gungame/plugins/included/gg_teamplay/configuration.py

"""Creates the gg_teamplay configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'count_grenade_kills',
    'count_melee_kills',
    'end_on_first_kill',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('end_on_first_kill') as end_on_first_kill:
        end_on_first_kill.add_text()

    with _config.cvar('count_melee_kills') as count_melee_kills:
        count_melee_kills.add_text()

    with _config.cvar('count_grenade_kills') as count_grenade_kills:
        count_grenade_kills.add_text()

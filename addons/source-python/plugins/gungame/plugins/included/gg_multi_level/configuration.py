# ../gungame/plugins/included/gg_multi_level/configuration.py

"""Creates the gg_deathmatch configuration."""

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
    'gravity',
    'length',
    'levels',
    'speed',
    'tk_attacker_reset',
    'tk_victim_reset',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar('levels', 3) as levels:
        levels.add_text()

    with _config.cvar('length', 10) as length:
        length.add_text()

    with _config.cvar('speed', 150) as speed:
        speed.add_text()

    with _config.cvar('gravity', 100) as gravity:
        gravity.add_text()

    with _config.cvar('tk_attacker_reset', 0) as tk_attacker_reset:
        tk_attacker_reset.add_text()

    with _config.cvar('tk_victim_reset', 0) as tk_victim_reset:
        tk_victim_reset.add_text()

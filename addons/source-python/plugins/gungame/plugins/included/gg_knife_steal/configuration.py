# ../gungame/plugins/included/gg_knife_steal/configuration.py

"""Creates the gg_knife_steal configuration."""

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
    'no_switch_default',
    'level_down_knife_level',
    'level_one_victim',
    'level_victim_nade',
    'limit',
    'skip_nade',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
        name='limit',
    ) as limit:
        limit.add_text()

    with _config.cvar(
        name='skip_nade',
    ) as skip_nade:
        skip_nade.add_text()

    with _config.cvar(
        name='level_victim_nade',
        convar=skip_nade.name,
    ) as level_victim_nade:
        level_victim_nade.add_text()

    with _config.cvar(
        name='level_down_knife_level',
    ) as level_down_knife_level:
        level_down_knife_level.add_text()

    with _config.cvar(
        name='level_one_victim',
    ) as level_one_victim:
        level_one_victim.add_text()

    with _config.cvar(
        name='no_switch_default',
    ) as no_switch_default:
        no_switch_default.add_text()

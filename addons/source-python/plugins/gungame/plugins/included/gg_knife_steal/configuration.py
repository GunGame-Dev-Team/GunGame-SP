# ../gungame/plugins/included/gg_knife_steal/configuration.py

"""Creates the gg_knife_steal configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'grenade_weapons',
    'knife_weapons',
    'level_one_victim',
    'limit',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar('limit') as limit:
        limit.add_text()

    grenade_weapons = dict()

    for _weapon in all_grenade_weapons:

        _skip_name = 'skip_{weapon}'.format(weapon=_weapon)
        with _config.cvar(
            name=_skip_name,
            description='skip_level',
            weapon=_weapon,
        ) as _skip:
            _skip.add_text()

        _level_name = '{weapon}_level_victim'.format(weapon=_weapon)
        with _config.cvar(
            name=_level_name,
            description='disabled_steal_level_down',
            weapon=_weapon,
            convar='{prefix}{level}'.format(
                prefix=_config.cvar_prefix,
                level=_skip_name,
            )
        ) as _level:
            _level.add_text()

        grenade_weapons[_weapon] = {
            'skip': _skip,
            'level': _level,
        }

    knife_weapons = dict()

    for _weapon in melee_weapons:

        with _config.cvar(
            name='{weapon}_level_victim'.format(weapon=_weapon),
            description='level_down_knife_level',
            weapon=_weapon,
        ) as _victim:
            _victim.add_text()

        knife_weapons[_weapon] = _victim

    with _config.cvar('level_one_victim') as level_one_victim:
        level_one_victim.add_text()

# ../gungame/core/config/core/weapons.py

"""GunGame weapons configuration."""

from cvars.flags import ConVarFlags

from gungame.core.config.manager import GunGameConfigManager

with GunGameConfigManager('weapon_settings') as config:
    with config.cvar(
            'gg_weapon_order_file', 'default_weapon_order', ConVarFlags.NOTIFY,
            'The weapon order file to use for GunGame.') as cvar:
        ...

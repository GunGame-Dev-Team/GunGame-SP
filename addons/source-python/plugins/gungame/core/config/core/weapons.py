# ../gungame/core/config/core/weapons.py

"""GunGame weapons configuration."""

from cvars.flags import ConVarFlags

from gungame.core.config.manager import GunGameConfigManager

with GunGameConfigManager('weapon') as config:
    with config.cvar(
            'order_file', 'default_weapon_order', ConVarFlags.NOTIFY,
            'The weapon order file to use for GunGame.') as cvar:
        ...

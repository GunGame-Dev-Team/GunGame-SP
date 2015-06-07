from gungame.core.config.manager import GunGameConfigManager

with GunGameConfigManager('weapon_settings') as config:
    weapon_order = config.cvar('gg_weapon_order_file', 'default_weapon_order')
    weapon_order.notify = True

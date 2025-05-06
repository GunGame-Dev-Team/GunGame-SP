# ../gungame/core/config/misc.py

"""GunGame miscellaneous configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from ..weapons.groups import all_grenade_weapons
from .manager import GunGameConfigManager

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "allow_kills_after_round",
    "cancel_on_fire",
    "dynamic_chat_time",
    "give_armor",
    "give_defusers",
    "level_on_protect",
    "map_strip_exceptions",
    "prune_database",
    "send_rules_each_map",
    "sound_pack",
    "spawn_protection",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(name="misc", cvar_prefix="gg_") as _config,
    _config.cvar(name="allow_kills_after_round") as allow_kills_after_round,
    _config.cvar(name="dynamic_chat_time") as dynamic_chat_time,
    _config.cvar(name="spawn_protection") as spawn_protection,
    _config.cvar(name="spawn_protection_cancel_on_fire") as cancel_on_fire,
    _config.cvar(name="spawn_protection_can_level_up") as level_on_protect,
    _config.cvar(name="give_armor") as give_armor,
    _config.cvar(name="give_defusers") as give_defusers,
    _config.cvar(
        name="map_strip_exceptions",
        default=",".join(all_grenade_weapons),
    ) as map_strip_exceptions,
    _config.cvar(
        name="prune_database",
        default=60,
    ) as prune_database,
    _config.cvar(
        name="sound_pack",
        default="default",
    ) as sound_pack,
    _config.cvar(name="send_rules_each_map") as send_rules_each_map,
):
    allow_kills_after_round.add_text()
    dynamic_chat_time.add_text()
    spawn_protection.add_text()
    cancel_on_fire.add_text()
    level_on_protect.add_text()
    give_armor.add_text()
    give_defusers.add_text()
    map_strip_exceptions.add_text()
    prune_database.add_text()
    sound_pack.add_text()
    send_rules_each_map.add_text()

# ../gungame/core/config/misc.py

"""GunGame miscellaneous configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from .manager import GunGameConfigManager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'allow_kills_after_round',
    'cancel_on_fire',
    'dynamic_chat_time',
    'give_armor',
    'give_defusers',
    'level_on_protect',
    'map_strip_exceptions',
    'prune_database',
    'sound_pack',
    'spawn_protection',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('misc') as _config:
    _config._cvar_prefix = 'gg_'

    with _config.cvar('allow_kills_after_round') as allow_kills_after_round:
        allow_kills_after_round.add_text()

    with _config.cvar('dynamic_chat_time') as dynamic_chat_time:
        dynamic_chat_time.add_text()

    with _config.cvar('spawn_protection') as spawn_protection:
        spawn_protection.add_text()

    with _config.cvar('spawn_protection_cancel_on_fire') as cancel_on_fire:
        cancel_on_fire.add_text()

    with _config.cvar('spawn_protection_can_level_up') as level_on_protect:
        level_on_protect.add_text()

    with _config.cvar('give_armor') as give_armor:
        give_armor.add_text()

    with _config.cvar('give_defusers') as give_defusers:
        give_defusers.add_text()

    with _config.cvar('map_strip_exceptions') as map_strip_exceptions:
        map_strip_exceptions.add_text()

    with _config.cvar('prune_database') as prune_database:
        prune_database.add_text()

    with _config.cvar('sound_pack', 'default') as sound_pack:
        sound_pack.add_text()

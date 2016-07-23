# ../gungame/core/config/misc.py

"""GunGame warmup configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Config
from .manager import GunGameConfigManager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('allow_kills_after_round',
           'dynamic_chattime',
           'give_armor',
           'give_defusers',
           'map_strip_exceptions',
           'prune_database',
           'sound_pack',
           )


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('misc') as _config:
    _config._cvar_prefix = 'gg_'

    with _config.cvar('allow_kills_after_round') as allow_kills_after_round:
        allow_kills_after_round.add_text()

    with _config.cvar('dynamic_chattime') as dynamic_chattime:
        dynamic_chattime.add_text()

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

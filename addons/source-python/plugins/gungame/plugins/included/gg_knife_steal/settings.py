# ../gungame/plugins/included/gg_knife_steal/settings.py

"""Player settings for gg_knife_steal."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.settings import gungame_player_settings

# Plugin
from .configuration import auto_switch_default


# =============================================================================
# >> SETTINGS
# =============================================================================
# TODO: add 2nd argument and translations
knife_steal_settings = gungame_player_settings.add_section('knife_steal')
# TODO: add 3rd argument and translations
auto_switch = knife_steal_settings.add_bool_setting(
    'auto_switch', auto_switch_default,
)

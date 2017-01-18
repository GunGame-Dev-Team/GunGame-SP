# ../gungame/plugins/included/gg_earn_nade/settings.py

"""Player settings for gg_earn_nade."""

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
earn_nade_settings = gungame_player_settings.add_section('earn_nade_settings')

# TODO: add 3rd argument and translations
# TODO: revert this and make it a bool once SP is updated
# auto_switch = earn_nade_settings.add_bool_setting(
#     'auto_switch', auto_switch_default.get_bool(),
# )
auto_switch = earn_nade_settings.add_int_setting(
    'auto_switch', int(auto_switch_default.get_bool()),
)

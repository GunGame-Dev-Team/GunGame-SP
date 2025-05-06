# ../gungame/plugins/included/gg_earn_nade/settings.py

"""Player settings for gg_earn_nade."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.strings import rules_translations
from gungame.core.settings import gungame_player_settings
from gungame.core.settings.strings import settings_translations

# Plugin
from .configuration import auto_switch_default
from .info import info

# =============================================================================
# >> SETTINGS
# =============================================================================
earn_nade_settings = gungame_player_settings.add_section(
    name="earn_nade_settings",
    text=rules_translations[info.name],
)

auto_switch = earn_nade_settings.add_bool_setting(
    name="auto_switch",
    default=auto_switch_default.get_bool(),
    text=settings_translations[info.name + ":auto_switch"],
)

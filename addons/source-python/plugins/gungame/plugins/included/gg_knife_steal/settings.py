# ../gungame/plugins/included/gg_knife_steal/settings.py

"""Player settings for gg_knife_steal."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.strings import rules_translations
from gungame.core.settings import gungame_player_settings
from gungame.core.settings.strings import settings_translations

# Plugin
from .configuration import no_switch_default
from .info import info

# =============================================================================
# >> SETTINGS
# =============================================================================
knife_steal_settings = gungame_player_settings.add_section(
    name="knife_steal",
    text=rules_translations[info.name],
)

no_switch = knife_steal_settings.add_bool_setting(
    name="no_switch",
    default=no_switch_default.get_bool(),
    text=settings_translations[info.name + ":no_switch"],
)

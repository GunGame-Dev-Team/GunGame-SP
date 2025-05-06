# ../gungame/core/rules/command.py

"""Rules command functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu, PagedOption
from players.entity import Player

# GunGame
from . import all_gungame_rules
from .strings import rules_translations
from ..commands.registration import register_command_callback
from ..menus._options import StarOption
from ..plugins.manager import gg_plugin_manager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback("rules", "Rules:Text")
def send_rules(index):
    """Send the rules menu to the player."""
    menu = PagedMenu(
        title=rules_translations["Rules:Header"],
        select_callback=_send_plugin_rules,
    )
    loaded_plugins = [
        plugin_name for plugin_name in all_gungame_rules
        if plugin_name in gg_plugin_manager
    ]
    if not loaded_plugins:
        menu.append(rules_translations["Rules:Empty"])
        menu.send(index)
        return

    for plugin_name in sorted(loaded_plugins):
        menu.append(PagedOption(rules_translations[plugin_name], plugin_name))
    menu.send(index)


def _send_plugin_rules(parent_menu, index, choice):
    plugin_name = choice.value
    menu = PagedMenu(title=rules_translations[plugin_name])
    menu.parent_menu = parent_menu
    rules = all_gungame_rules[plugin_name]
    tokens = {
        key: getattr(value["convar"], "get_" + value["type"])()
        for key, value in rules.convar_tokens.items()
    }
    for rule in rules:
        menu.append(
            StarOption(
                rules[rule].get_string(
                    language=Player(index).language,
                    **tokens,
                ),
            ),
        )
    menu.send(index)

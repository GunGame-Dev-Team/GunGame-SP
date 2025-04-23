# ../gungame/core/rules/__init__.py

"""Rules functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import OrderedDict
from importlib import import_module
import sys
from warnings import warn

# GunGame
from .strings import rules_translations
from ..plugins.manager import gg_plugin_manager
from ..plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'all_gungame_rules',
    'define_all_rules',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _GunGameRulesDictionary(OrderedDict):
    """Class used to store all rules."""

    def __init__(self):
        """Create the dictionary and set the header."""
        super().__init__()
        self.header = rules_translations['Rules:Header']

    def get_rules(self, player):
        """Return all rules in a string."""
        language = player.language
        message = ''
        for plugin_name, rules in self.items():
            if plugin_name not in gg_plugin_manager:
                continue
            title = rules.title
            if title in rules_translations:
                title = rules_translations[title].get_string(language)
            message += '\t' + title + '\n\n'
            convar_tokens = {
                key: getattr(value['convar'], 'get_' + value['type'])
                for key, value in rules.convar_tokens.items()
            }
            for rule in rules.items():
                if rule in rules_translations:
                    rule = rules_translations[rule].get_string(
                        language=language,
                        **convar_tokens
                    )
                message += '\t\t' + rule + '\n\n'
        if not message:
            message = rules_translations['Rules:Empty'].get_string(language)
        return self.header.get_string(language) + ':\n\n' + message


all_gungame_rules = _GunGameRulesDictionary()


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def define_all_rules():
    """Find and store all rules."""
    # Loop through all plugins
    for plugin_name in valid_plugins.all:
        plugin_path = valid_plugins.get_plugin_path(plugin_name)
        plugin_type = str(plugin_path.parent.stem)
        rules_path = plugin_path / 'rules.py'
        if not rules_path.is_file():
            continue

        try:
            import_module(f'gungame.plugins.{plugin_type}.{plugin_name}.rules')
        # pylint: disable=broad-except
        except Exception:
            warn(
                f'Unable to import rules for {plugin_name} due to error:'
                f'\n\n\t{sys.exc_info()[1]}'
            )

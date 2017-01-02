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
from ..paths import GUNGAME_PLUGINS_PATH
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

    def __init__(self):
        super().__init__()
        self.header = rules_translations['Rules:Header']

    def get_rules(self, player):
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
    # Loop through all plugins
    for plugin_name in valid_plugins.all:
        plugin_type = valid_plugins.get_plugin_type(plugin_name)
        if not GUNGAME_PLUGINS_PATH.joinpath(
            plugin_type, plugin_name, 'rules.py',
        ).isfile():
            continue

        try:
            import_module(
                'gungame.plugins.{plugin_type}.{plugin_name}.'
                'rules'.format(
                    plugin_type=plugin_type,
                    plugin_name=plugin_name,
                )
            )
        except Exception:
            warn(
                'Unable to import rules for {plugin} due to error:'
                '\n\n\t{error}'.format(
                    plugin=plugin_name,
                    error=sys.exc_info()[1]
                )
            )

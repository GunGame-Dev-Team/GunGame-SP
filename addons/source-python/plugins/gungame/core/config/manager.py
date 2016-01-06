# ../gungame/core/config/manager.py

"""Provides config management functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from contextlib import suppress
from importlib import import_module

from path import Path

# Source.Python Imports
#   Config
from config.cvar import _CvarManager
from config.manager import ConfigManager
#   Translations
from translations.strings import LangStrings

# GunGame Imports
#   Plugins
from gungame.core.plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('GunGameConfigManager',
           'load_all_configs',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameConfigManager(ConfigManager):
    """Class used to create GunGame configuration files."""

    def __init__(self, name):
        """Add 'gungame' to the path before initializing the instance."""
        # Start with 'gungame' path
        filepath = Path('gungame')

        # Get the path if file is a valid plugin
        try:
            folder = valid_plugins.get_plugin_type(name)+ '_plugins'
            filepath = filepath.joinpath(folder, name)
            cvar_prefix = name + '_'

        # Get the path for a base config
        except ValueError:
            folder = 'core'
            filepath = filepath.joinpath(name + '_settings')
            cvar_prefix = 'gg_{0}_'.format(name)

        try:
            # Add the translations
            self.translations = LangStrings(
                'gungame/{0}/config/{1}'.format(folder, name))

        except FileNotFoundError:
            self.translations = dict()

        # Initialize the config
        super().__init__(filepath, cvar_prefix)

    def cvar(
            self, name, default=0, description=None,
            flags=0, min_value=None, max_value=None):
        section = _GunGameCvarManager(
            name, default, description, flags, min_value,
            max_value, self.cvar_prefix, self.translations)
        self._cvars.add(name)
        self._sections.append(section)
        return section


class _GunGameCvarManager(_CvarManager):
    """"""

    def __init__(
            self, name, default, description, flags,
            min_value, max_value, cvar_prefix, translations):
        """"""
        self._base_item = None
        if description is None:
            description = name
        if description in translations:
            self._base_item = description + ':'
            description = translations[description]
        super().__init__(
            cvar_prefix + name, default, description,
            flags, min_value, max_value)
        self.translations = translations

    def add_text(self, **tokens):
        """"""
        if self._base_item is None:
            raise ValueError('No translations set for instance.')
        for item in sorted(self.translations):
            if not item.startswith(self._base_item):
                continue
            if not item.count(':') >= 2:
                raise ValueError('Invalid item.')
            attribute = item.replace(self._base_item, '', 1).split(':')[0]
            getattr(self, attribute).append(
                self.translations[item].get_string(**tokens))


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def load_all_configs():
    """Load all GunGame configs."""
    for file in Path(__file__).parent.files('*.py'):
        if file.namebase in ('__init__', Path(__file__).namebase):
            continue
        import_module(
            'gungame.core.config.{0}'.format(file.namebase))
    for plugin_name in valid_plugins.all:
        plugin_type = valid_plugins.get_plugin_type(plugin_name)
        with suppress(ImportError):
            import_module('gungame.plugins.{0}.{1}.configuration'.format(
                plugin_type, plugin_name))

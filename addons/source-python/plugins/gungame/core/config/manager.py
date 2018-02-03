# ../gungame/core/config/manager.py

"""Provides config management functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package
from path import Path

# Source.Python
from config.cvar import _CvarManager
from config.manager import ConfigManager
from translations.strings import LangStrings

# GunGame
from . import gg_config_logger
from ..plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_GunGameCvarManager',
    'GunGameConfigManager',
    'gg_config_manager_logger',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_config_manager_logger = gg_config_logger.manager


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameConfigManager(ConfigManager):
    """Class used to create GunGame configuration files."""

    def __init__(self, name):
        """Add 'gungame' to the path before initializing the instance."""
        # Start with 'gungame' path
        base_path = Path('gungame')

        # Get the path if file is a valid plugin
        try:
            folder = valid_plugins.get_plugin_type(name) + '_plugins'
            file_path = base_path / folder / name
            cvar_prefix = name + '_'

        # Get the path for a base config
        except ValueError:
            folder = None
            file_path = base_path / name + '_settings'
            cvar_prefix = f'gg_{name}_'

        try:
            # Add the translations
            plugin_type = folder + '/' if folder is not None else ''
            self.translations = LangStrings(
                f'gungame/config/{plugin_type}{name}'
            )

        except FileNotFoundError:
            self.translations = dict()

        # Initialize the config
        super().__init__(file_path, cvar_prefix)

    def cvar(
        self, name, default=0, description=None, flags=0, min_value=None,
        max_value=None, **tokens
    ):
        """Override cvar method to add cvar as _GunGameCvarManager object."""
        section = _GunGameCvarManager(
            name, default, description, flags, min_value, max_value,
            self.cvar_prefix, self.translations, **tokens
        )
        self._cvars.add(section.name)
        self._sections.append(section)
        return section


class _GunGameCvarManager(_CvarManager):
    """Class used to more easily add translations for cvars in config files."""

    def __init__(
        self, name, default, description, flags, min_value, max_value,
        cvar_prefix, translations, **tokens
    ):
        """Get the true description and store the translations."""
        self._base_item = None
        if description is None:
            description = name
        if description in translations:
            self._base_item = description + ':'
            description = translations[description].get_string(**tokens)
        super().__init__(
            cvar_prefix + name, default, description,
            flags, min_value, max_value,
        )
        self.translations = translations

    def add_text(self, **tokens):
        """Add all other text for the ConVar."""
        if self._base_item is None:
            raise ValueError(
                f'No translations set for instance ({self.name}).'
            )
        for item in sorted(self.translations):
            if not item.startswith(self._base_item):
                continue
            if item.count(':') < 2:
                raise ValueError(f'Invalid item ({item}).')
            attribute = item.replace(self._base_item, '', 1).split(':')[0]
            getattr(self, attribute).append(
                self.translations[item].get_string(**tokens)
            )

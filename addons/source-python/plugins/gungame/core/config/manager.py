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
from config.manager import ConfigManager

# GunGame Imports
#   Plugins
from gungame.core.plugins.valid import valid_plugins


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
            folder = valid_plugins.get_plugin_type(name)
            filepath = filepath.joinpath(folder + '_plugins', name)

        # Get the path for a base config
        except ValueError:
            filepath = filepath.joinpath(name)

        # Initialize the config
        print(filepath)
        super(GunGameConfigManager, self).__init__(filepath)


class _ConfigManager(object):

    """Config management class used to interact with GunGame config files."""

    def __init__(self):
        """Set the executed value to False for further use."""
        self._executed = False

    def load_configs(self):
        """Load all GunGame configs."""
        for file in Path(__file__).parent.joinpath('core').files('*.py'):
            if file.namebase == '__init__':
                continue
            import_module(
                'gungame.core.config.core.{0}'.format(file.namebase))
        for plugin_name in valid_plugins.all:
            plugin_type = valid_plugins.get_plugin_type(plugin_name)
            '''
            with suppress(ImportError):
                import_module('gungame.plugins.{0}.{1}.config'.format(
                    plugin_type, plugin_name))
            '''
            import_module('gungame.plugins.{0}.{1}.config'.format(
                plugin_type, plugin_name))
        self._executed = True

config_manager = _ConfigManager()

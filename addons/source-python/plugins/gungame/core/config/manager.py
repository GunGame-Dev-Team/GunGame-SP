# ../gungame/core/config/manager.py

"""Provides config management functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
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
        filepath = Path('gungame')
        try:
            folder = valid_plugins.get_plugin_type(name)
            filepath = filepath.joinpath(folder + '_plugin_configs', name)
        except ValueError:
            filepath = filepath.joinpath(name)
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
        self._executed = True

config_manager = _ConfigManager()

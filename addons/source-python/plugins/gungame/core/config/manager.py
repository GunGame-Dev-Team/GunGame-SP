# ../gungame/core/config/manager.py

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
from gungame.core.plugins.valid import ValidPlugins


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameConfigManager(ConfigManager):
    def __init__(self, name):
        filepath = Path('gungame')
        try:
            folder = ValidPlugins.get_plugin_type(name)
            filepath = filepath.joinpath(folder + '_plugin_configs', name)
        except ValueError:
            filepath = filepath.joinpath(name)
        super(GunGameConfigManager, self).__init__(filepath)


class _ConfigManager(object):

    def __init__(self):
        self._executed = False

    def load_configs(self):
        for file in Path(__file__).parent.joinpath('core').files('*.py'):
            if file.namebase == '__init__':
                continue
            config = import_module(
                'gungame.core.config.core.{0}'.format(file.namebase))

config_manager = _ConfigManager()

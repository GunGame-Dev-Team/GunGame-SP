# ../gungame/core/config/manager.py

# =============================================================================
# >> IMPORTS
# =============================================================================
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
        filepath = path('gungame')
        try:
            folder = ValidPlugins.get_plugin_type(name)
            filepath = filepath.joinpath(folder + '_plugin_configs', name)
        except ValueError:
            filepath = filepath.joinpath(name)
        super(GunGameConfigManager, self).__init__(filepath)

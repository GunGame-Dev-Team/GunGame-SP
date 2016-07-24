# ../gungame/info.py

"""Provides/stores information about the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars.public import PublicConVar
from plugins.info import PluginInfo


# =============================================================================
# >> PLUGIN INFO
# =============================================================================
info = PluginInfo()
info.name = 'GunGame'
info.author = 'GunGame-Dev-Team'
info.version = '1.0'
info.basename = 'gungame'
info.variable = info.basename + '_version'
info.url = ''
info.convar = PublicConVar(
    info.variable, info.version, info.name + ' Version'
)

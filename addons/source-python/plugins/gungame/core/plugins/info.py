from plugins.info import PluginInfo
from configobj import ConfigObj
from ..paths import GUNGAME_PLUGINS_PATH


class GunGamePluginInfo(PluginInfo):
    def __init__(self, module):
        path = module.split('.')
        if (
            not module.startswith('gungame.plugins.')
            or path[2] not in ('included', 'custom')
            or len(path) != 5
        ):
            raise ValueError('one')
        name = path[3]
        ini_file = GUNGAME_PLUGINS_PATH / path[2] / name / 'info.ini'
        if not ini_file.isfile():
            raise ValueError('two')
        ini = ConfigObj(ini_file, unrepr=True)
        super().__init__(name, **ini)

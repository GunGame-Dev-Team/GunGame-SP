from plugins.instance import LoadedPlugin
from gungame.core.plugins import GGPluginsLogger


GGPluginsInstanceLogger = GGPluginsLogger.instance


class GGLoadedPlugin(LoadedPlugin):
    logger = GGPluginsInstanceLogger

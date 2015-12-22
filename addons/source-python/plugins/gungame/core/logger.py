# ../gungame/core/logger.py

"""Provides the GunGame logger instance."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Config
from config.manager import ConfigManager
#   Cvars
from cvars import ConVar
from cvars.flags import ConVarFlags
#   Loggers
from loggers import LogManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create the logging config
with ConfigManager('gungame/logging_settings') as config:
    with config.cvar(
            'gg_logging_level', '0', ConVarFlags.NONE,
            'GunGame logging level') as _level:
        ...
    with config.cvar(
            'gg_logging_areas', '1', ConVarFlags.NONE,
            'GunGame logging areas') as _areas:
        ...

# Get the GunGame logger
gg_logger = LogManager(
    'gg', _level, _areas, 'gungame',
    '%(asctime)s - %(name)s\t-\t%(levelname)s\n%(message)s',
    '%m-%d-%Y %H:%M:%S')

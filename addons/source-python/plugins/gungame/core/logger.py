# ../gungame/core/logger.py

"""Provides the GunGame logger instance."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Config
from config.manager import ConfigManager
#   Cvars
from cvars.flags import ConVarFlags
#   Loggers
from loggers import LogManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create the logging config
# This cannot be done with GunGameConfigManager as it causes circular imports.
with ConfigManager('gungame/logging_settings') as _config:
    with _config.cvar(
            'gg_logging_level', '0', ConVarFlags.NONE,
            'GunGame logging level') as _level:
        pass
    with _config.cvar(
            'gg_logging_areas', '1', ConVarFlags.NONE,
            'GunGame logging areas') as _areas:
        pass

# Get the GunGame logger
gg_logger = LogManager(
    'gg', _level, _areas, 'gungame',
    '%(asctime)s - %(name)s\t-\t%(levelname)s\n%(message)s',
    '%m-%d-%Y %H:%M:%S')

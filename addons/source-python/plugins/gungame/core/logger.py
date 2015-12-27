# ../gungame/core/logger.py

"""Provides the GunGame logger instance."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Config
from config.manager import ConfigManager
#   Loggers
from loggers import LogManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create the logging config
# This cannot be done with GunGameConfigManager as it causes circular imports.
with ConfigManager('gungame/logging_settings', 'gg_logging_') as _config:
    with _config.cvar(
            'level', '0', 'GunGame logging level') as _level:
        pass
    with _config.cvar(
            'areas', '1', 'GunGame logging areas') as _areas:
        pass

# Get the GunGame logger
gg_logger = LogManager(
    'gg', _level, _areas, 'gungame',
    '%(asctime)s - %(name)s\t-\t%(levelname)s\n%(message)s',
    '%m-%d-%Y %H:%M:%S')

# ../gungame/core/logger.py

"""Provides the GunGame logger instance."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from cvars import ConVar
from loggers import LogManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create the logging cvars
_level = ConVar('gg_logging_level', '0', 0, 'GunGame logging level')
_areas = ConVar('gg_logging_areas', '1', 0, 'GunGame logging areas')

# Get the GunGame logger
gg_logger = LogManager(
    'gg', _level, _areas, 'gungame',
    '%(asctime)s - %(name)s\t-\t%(levelname)s\n%(message)s',
    '%m-%d-%Y %H:%M:%S')

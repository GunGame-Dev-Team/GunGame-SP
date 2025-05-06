# ../gungame/core/logger.py

"""Provides the GunGame logger instance."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from config.manager import ConfigManager
from loggers import LogManager
from translations.strings import LangStrings

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_config_strings = LangStrings("gungame/config/logger")

# Create the logging config
# This cannot be done with GunGameConfigManager as it causes circular imports.
with ConfigManager("gungame/logging_settings", "gg_logging_") as _config:

    _level = _config.cvar(
        name="level",
        default=0,
        description=_config_strings["Level"],
    )

    _areas = _config.cvar(
        name="areas",
        default=1,
        description=_config_strings["Areas"],
    )

# Get the GunGame logger
gg_logger = LogManager(
    "gg",
    _level,
    _areas,
    "gungame",
    "%(asctime)s - %(name)s\t-\t%(levelname)s\n%(message)s",
    "%m-%d-%Y %H:%M:%S",
)

# ../gungame/plugins/included/gg_random_spawn/entities.py

"""Provides functions to get and set locations for spawn points."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-package
from configobj import ConfigObj

# Source.Python
from core import GAME_NAME

# GunGame
from gungame.core.paths import GUNGAME_DATA_PATH

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'spawn_entities',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_class_name_file = GUNGAME_DATA_PATH / info.name + '.ini'
spawn_entities = ConfigObj(_class_name_file).get(GAME_NAME)
if not spawn_entities:
    raise NotImplementedError(f'Game "{GAME_NAME}" is not supported.')

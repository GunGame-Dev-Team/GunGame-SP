# ../gungame/core/commands/__init__.py

"""Provides player command functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Site-package
from configobj import ConfigObj

# GunGame
from .strings import commands_translations
from ..paths import (
    GUNGAME_BASE_PATH, GUNGAME_CFG_PATH, GUNGAME_PLUGINS_PATH,
)
from ..plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'commands_ini_file',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
commands_ini_file = ConfigObj(GUNGAME_CFG_PATH / 'commands.ini')
if not commands_ini_file:
    commands_ini_file.initial_comment = (
        commands_translations['Commands:Header'].get_string().splitlines()
    )


# =============================================================================
# >> REGISTRATION
# =============================================================================
for file in GUNGAME_BASE_PATH.joinpath('core', 'menus').files():
    if file.namebase.startswith('_'):
        continue
    import_module(
        'gungame.core.menus.{name}'.format(
            name=file.namebase,
        )
    )

import_module('gungame.core.rules.command')

for plugin_name in valid_plugins.all:
    plugin_type = valid_plugins.get_plugin_type(plugin_name)
    if GUNGAME_PLUGINS_PATH.joinpath(
        plugin_type, plugin_name, 'commands.py',
    ).isfile():
        import_module(
            'gungame.plugins.{plugin_type}.{plugin_name}.commands'.format(
                plugin_type=plugin_type,
                plugin_name=plugin_name,
            )
        )

commands_ini_file.write()

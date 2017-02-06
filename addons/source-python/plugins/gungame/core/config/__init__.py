# ../gungame/core/config/__init__.py

"""GunGame configuration functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module
import sys
from textwrap import TextWrapper
from warnings import warn

# Site-Package
from path import Path

# Source.Python
from engines.server import queue_command_string
from translations.strings import LangStrings

# GunGame
from .. import gg_core_logger
from ..paths import GUNGAME_PLUGINS_PATH, GUNGAME_CFG_PATH
from ..plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'gg_config_logger',
    'load_all_configs',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_config_logger = gg_core_logger.config


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def load_all_configs():
    """Load all GunGame configs."""
    for file in Path(__file__).parent.files('*.py'):
        if file.namebase in ('__init__', Path(__file__).namebase):
            continue
        import_module(
            'gungame.core.config.{file_name}'.format(
                file_name=file.namebase,
            )
        )
    for plugin_name in valid_plugins.all:
        plugin_type = valid_plugins.get_plugin_type(plugin_name)
        if not GUNGAME_PLUGINS_PATH.joinpath(
            plugin_type, plugin_name, 'configuration.py',
        ).isfile():
            continue

        try:
            import_module(
                'gungame.plugins.{plugin_type}.{plugin_name}.'
                'configuration'.format(
                    plugin_type=plugin_type,
                    plugin_name=plugin_name,
                )
            )
        except Exception:
            warn(
                'Unable to import configuration for {plugin} due to error:'
                '\n\n\t{error}'.format(
                    plugin=plugin_name,
                    error=sys.exc_info()[1]
                )
            )

    always_loaded = GUNGAME_CFG_PATH / 'gg_plugins.cfg'
    contents = []
    if always_loaded.isfile():
        with always_loaded.open() as open_file:
            contents = open_file.read()
        contents = [
            line for line in contents.splitlines()
            if line and not line.startswith('// ')
        ]
    strings = LangStrings('gungame/plugins')
    with always_loaded.open('w') as open_file:
        wrapper = TextWrapper(
            width=79,
            initial_indent='// ',
            subsequent_indent='// ',
        )
        text = strings['Plugins:Loaded:Always'].get_string(
            plugins=', '.join(sorted(valid_plugins.all))
        )
        for line in text.splitlines(keepends=True):
            if line == '\n':
                open_file.write(line)
                continue
            for output in wrapper.wrap(line):
                open_file.write(output + '\n')
        for line in contents:
            open_file.write(line + '\n')

    exec_path = always_loaded.replace(
        always_loaded.parent.parent.parent, '',
    )[1:~3].replace('\\', '/')
    queue_command_string('exec {config}'.format(config=exec_path))

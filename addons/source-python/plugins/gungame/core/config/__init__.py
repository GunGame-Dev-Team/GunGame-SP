# ../gungame/core/config/__init__.py

"""GunGame configuration functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module
import sys
from warnings import warn

# Site-Package
from path import Path

# GunGame
from ..plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'load_all_configs',
)


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
        module_import = (
            'gungame.plugins.{plugin_type}.{plugin_name}.configuration'.format(
                plugin_type=plugin_type,
                plugin_name=plugin_name,
            )
        )
        try:
            import_module(module_import)
        except ImportError:
            message = sys.exc_info()[1].msg
            if message == "No module named '{module_import}'".format(
                module_import=module_import,
            ):
                continue
            warn(
                'Unable to import configuration for {plugin} due to error:'
                '\n\t{error}'.format(
                    plugin=plugin_name,
                    error=sys.exc_info()[1].msg
                )
            )

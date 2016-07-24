# ../gungame/core/config/__init__.py

"""GunGame configuration functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from importlib import import_module

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
        with suppress(ImportError):
            import_module(
                'gungame.plugins.{plugin_type}.{plugin_name}.'
                'configuration'.format(
                    plugin_type=plugin_type,
                    plugin_name=plugin_name,
                )
            )

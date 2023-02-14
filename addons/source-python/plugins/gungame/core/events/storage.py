# ../gungame/core/events/storage.py

"""Event storage functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Site-Package
from path import Path

# GunGame
from ..plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_GGResourceList',
    'gg_resource_list',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _GGResourceList(list):
    """Class used to store a list of all GunGame res files."""

    def append(self, resource):
        """Add the res file and write it."""
        super().append(resource)
        resource.write()

    def load_all_events(self):
        """Load all events from all res files."""
        for resource in self:
            resource.load_events()

    @staticmethod
    def register_all_events():
        """Register all included and sub-plugin events."""
        included_path = Path(__file__).parent / 'included'
        for event_file in included_path.files():
            if event_file.namebase != '__init__':
                import_module(
                    f'gungame.core.events.included.{event_file.namebase}'
                )

        for plugin_name in valid_plugins.all:
            plugin_path = valid_plugins.get_plugin_path(plugin_name)
            plugin_type = str(plugin_path.parent.namebase)
            event_path = plugin_path / 'custom_events.py'
            if not event_path.isfile():
                continue
            import_module(
                f'gungame.plugins.{plugin_type}.{plugin_name}.custom_events'
            )


gg_resource_list = _GGResourceList()

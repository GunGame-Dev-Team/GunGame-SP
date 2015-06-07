# ../gungame/core/events/__init__.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Importlib
from importlib import import_module

# Site-Package Imports
#   Path
from path import Path


# Import the included events
for event_file in Path(__file__).parent.joinpath('included').files():
    if event_file.namebase != '__init__':
        import_module('gungame.core.events.included.' + event_file.namebase)

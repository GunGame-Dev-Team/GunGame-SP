# ../gungame/core/sounds/hooks.py

"""Provides a way to hook GunGame sounds."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import AutoUnload

# GunGame
from .manager import sound_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class SoundHook(AutoUnload):
    """Decorator used to register sound hooks."""

    def __init__(self, sound_name):
        """Store the sound name."""
        self.sound_name = sound_name
        self.callback = None

    def __call__(self, callback):
        """Store the callback and register the hook."""
        self.callback = callback
        sound_manager.register_hook(self.sound_name, self.callback)

    def _unload_instance(self):
        """Unregister the sound hook."""
        sound_manager.unregister_hook(self.sound_name, self.callback)

# ../gungame/core/messages/hooks.py

"""Provides a way to hook GunGame messages."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import AutoUnload

# GunGame
from .manager import message_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class MessageHook(AutoUnload):
    """Decorator used to register message hooks."""

    def __init__(self, message_name):
        """Store the message name."""
        self.message_name = message_name
        self.callback = None

    def __call__(self, callback):
        """Store the callback and register the hook."""
        self.callback = callback
        message_manager.hook_message(self.message_name, self.callback)

    def _unload_instance(self):
        """Unregister the message hook."""
        message_manager.unhook_message(self.message_name, self.callback)


class MessagePrefixHook(AutoUnload):
    """Decorator used to register message prefix hooks."""

    def __init__(self, message_prefix):
        """Store the message prefix."""
        self.message_prefix = message_prefix
        self.callback = None

    def __call__(self, callback):
        """Store the callback and register the hook."""
        self.callback = callback
        message_manager.hook_prefix(self.message_prefix, self.callback)

    def _unload_instance(self):
        """Unregister the message prefix hook."""
        message_manager.unhook_prefix(self.message_prefix, self.callback)

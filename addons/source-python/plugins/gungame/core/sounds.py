# ../gungame/core/sounds.py

"""Sound based functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('sound_manager',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class _SoundManager(object):
    """Class used to play sounds."""

    def play_sound(self, sound, users=None):
        """Play the sound to the given users."""
        pass

    def emit_sound(self, sound, index, users=None):
        """Emit the sound from the given index and play to the given users."""
        pass

    def stop_sound(self, sound, index):
        """Stop the sound from playing from the given index."""
        pass

# Get the _SoundManager instance
sound_manager = _SoundManager()

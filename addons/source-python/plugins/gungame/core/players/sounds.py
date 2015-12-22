# ../gungame/core/players/sounds.py

"""Player-based sound functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Sounds
from gungame.core.sounds import sound_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerSounds(object):
    """Class used to interact with sounds for a specific player."""

    def play_sound(self, sound):
        """Play the sound to the player."""
        sound_manager.play_sound(sound, self.index)

    def emit_sound(self, sound):
        """Emit the sound from the player."""
        sound_manager.emit_sound(sound, self.index)

    def stop_sound(self, sound):
        """Stop the sound from emitting from the player."""
        sound_manager.stop_sound(sound, self.index)

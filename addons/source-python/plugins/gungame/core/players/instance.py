# ../gungame/core/players/instance.py

"""Player instance functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from players.entity import Player

# GunGame Imports
#   Players
from gungame.core.players.attributes import attribute_post_hooks
from gungame.core.players.attributes import attribute_pre_hooks
from gungame.core.players.attributes import player_attributes
# from gungame.core.players.database import _PlayerDatabase
from gungame.core.players.levels import _PlayerLevels
from gungame.core.players.messages import _PlayerMessages
from gungame.core.players.sounds import _PlayerSounds
from gungame.core.players.weapons import _PlayerWeapons


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('GunGamePlayer',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGamePlayer(
        Player, _PlayerLevels, _PlayerMessages,
        _PlayerSounds, _PlayerWeapons):
    """Class used to interact directly with a specific player."""

    def __setattr__(self, attr, value):
        """Verify that the attribute's value should be set."""
        # Are there any pre-hooks for the attribute?
        if (attr in player_attributes and
                attr in attribute_pre_hooks and hasattr(self, attr)):

            # Do any of the pre-hooks block the setting of the attribute?
            if not attribute_pre_hooks[attr].call_callbacks(self, value):

                # Block the attribute from being set
                return

        # Are there any post-hooks for the attribute?
        if not (attr in player_attributes and hasattr(self, attr) and
                attr in attribute_post_hooks):

            # If not, simply set the attribute's value
            super().__setattr__(attr, value)
            return

        # Get the value prior to setting
        old_value = getattr(self, attr)

        # Set the attribute's value
        super().__setattr__(attr, value)

        # Call all of the attribute's post-hooks
        attribute_post_hooks[attr].call_callbacks(self, value, old_value)

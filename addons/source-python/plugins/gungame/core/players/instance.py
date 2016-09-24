# ../gungame/core/players/instance.py

"""Player instance functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from colors import WHITE
from players.entity import Player
from weapons.manager import weapon_manager

# GunGame
from ..events.included.leveling import GG_LevelDown, GG_LevelUp
from ..events.included.match import GG_Win
from ..messages import message_manager
from .attributes import (
    attribute_post_hooks, attribute_pre_hooks, player_attributes,
)
from .database import winners_database
from ..sounds.manager import sound_manager
from ..status import GunGameMatchStatus, GunGameStatus
from ..weapons.manager import weapon_order_manager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GunGamePlayer',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGamePlayer(Player):
    """Class used to interact directly with a specific player."""

    level = 0
    multi_kill = 0

    def __setattr__(self, attr, value):
        """Verify that the attribute's value should be set."""
        # Are there any pre-hooks for the attribute?
        if (
            attr in player_attributes and
            attr in attribute_pre_hooks and
            hasattr(self, attr)
        ):

            # Do any of the pre-hooks block the setting of the attribute?
            if not attribute_pre_hooks[attr].call_callbacks(self, value):

                # Block the attribute from being set
                return

        # Are there any post-hooks for the attribute?
        if not (
            attr in player_attributes and
            hasattr(self, attr) and
            attr in attribute_post_hooks
        ):

            # If not, simply set the attribute's value
            super().__setattr__(attr, value)
            return

        # Get the value prior to setting
        old_value = getattr(self, attr)

        # Set the attribute's value
        super().__setattr__(attr, value)

        # Call all of the attribute's post-hooks
        attribute_post_hooks[attr].call_callbacks(self, value, old_value)

    @property
    def unique_id(self):
        return self.uniqueid

    # =========================================================================
    # >> LEVEL FUNCTIONALITY
    # =========================================================================
    def increase_level(self, levels, victim=0, reason=''):
        """Increase the player's level by the given amount."""
        if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
            return
        if not isinstance(levels, int) or levels < 1:
            raise ValueError(
                'Invalid value given for levels "{levels}".'.format(
                    levels=levels,
                )
            )
        old_level = self.level
        new_level = old_level + levels
        if new_level > weapon_order_manager.max_levels:
            with GG_Win() as event:
                event.attacker = event.winner = self.userid
                event.userid = event.loser = victim
            return
        self.level = new_level
        if self.level != new_level:
            return
        self.multi_kill = 0
        with GG_LevelUp() as event:
            event.attacker = event.leveler = self.userid
            event.userid = event.victim = victim
            event.old_level = old_level
            event.new_level = new_level
            event.reason = reason

    def decrease_level(self, levels, attacker=0, reason=''):
        """Decrease the player's level by the given amount."""
        if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
            return
        if not isinstance(levels, int) or levels < 1:
            raise ValueError(
                'Invalid value given for levels "{levels}".'.format(
                    levels=levels,
                )
            )
        old_level = self.level
        new_level = max(old_level - levels, 1)
        if self.level == new_level:
            return
        self.level = new_level
        if self.level != new_level:
            return
        self.multi_kill = 0
        with GG_LevelDown() as event:
            event.attacker = attacker
            event.leveler = event.userid = self.userid
            event.old_level = old_level
            event.new_level = new_level
            event.reason = reason

    # =========================================================================
    # >> WEAPON FUNCTIONALITY
    # =========================================================================
    @property
    def level_multi_kill(self):
        """Return the multi_kill value for the player's current level."""
        return weapon_order_manager.active[self.level].multi_kill

    @property
    def level_weapon(self):
        """Return the player's current level weapon."""
        return weapon_order_manager.active[self.level].weapon

    def remove_all_weapons(self, exclude=None):
        if exclude is None:
            exclude = list()
        elif isinstance(exclude, str):
            exclude = [exclude]

        exclude = [weapon_manager[weapon].name for weapon in exclude]

        for weapon in self.weapons():
            if weapon.classname in exclude:
                continue
            self.drop_weapon(weapon)
            weapon.remove()

    def give_level_weapon(self):
        """Give the player the weapon of their current level."""
        weapon = weapon_manager[self.level_weapon]
        for entity in self.weapons():
            if entity.classname == weapon.name:
                return
        for entity in self.weapons():
            if weapon_manager[entity.classname].slot == weapon.slot:
                self.drop_weapon(entity)
                entity.remove()
        self.give_named_item(weapon.name)

    # =========================================================================
    # >> MESSAGE FUNCTIONALITY
    # =========================================================================
    def center_message(self, message='', **tokens):
        """Send a center message to the player."""
        message_manager.center_message(message, self.index, **tokens)

    def chat_message(self, message='', index=0, **tokens):
        """Send a chat message to the player."""
        message_manager.chat_message(message, index, self.index, **tokens)

    def echo_message(self, message='', **tokens):
        """Send an echo message to the player."""
        message_manager.echo_message(message, self.index, **tokens)

    def hint_message(self, message='', **tokens):
        """Send a hint message to the player."""
        message_manager.hint_message(message, self.index, **tokens)

    def hud_message(
        self, message='', x=-1.0, y=-1.0, color1=WHITE,
        color2=WHITE, effect=0, fade_in=0.0, fade_out=0.0,
        hold=4.0, fx_time=0.0, channel=0, **tokens
    ):
        """Send a hud message to the player."""
        message_manager.hud_message(
            message, x, y, color1, color2, effect, fade_in,
            fade_out, hold, fx_time, channel, self.index, **tokens
        )

    def keyhint_message(self, message='', **tokens):
        """Send a keyhint message to the player."""
        message_manager.keyhint_message(message, self.index, **tokens)

    def motd_message(
        self, panel_type=2, title='', message='', visible=True, **tokens
    ):
        """Send a motd message to the player."""
        message_manager.motd_message(
            panel_type, title, message, visible, self.index, **tokens
        )

    def top_message(self, message='', color=WHITE, time=4.0, **tokens):
        """Send a toptext message to the player."""
        message_manager.top_message(message, color, time, self.index, **tokens)

    # =========================================================================
    # >> SOUND FUNCTIONALITY
    # =========================================================================
    def play_sound(self, sound):
        """Play the sound to the player."""
        sound_manager.play_sound(sound, self.index)

    def emit_sound(self, sound):
        """Emit the sound from the player."""
        sound_manager.emit_sound(sound, self.index)

    def stop_sound(self, sound):
        """Stop the sound from emitting from the player."""
        sound_manager.stop_sound(sound, self.index)

    # =========================================================================
    # >> DATABASE FUNCTIONALITY
    # =========================================================================
    def update_time_stamp(self):
        """Update the player's time stamp."""
        if self.unique_id in winners_database:
            winners_database.update_player_time_stamp(self)

    @property
    def wins(self):
        """Return the number of wins for the player."""
        if self.unique_id in winners_database:
            return winners_database[self.unique_id].wins
        return 0

    @wins.setter
    def wins(self, wins):
        """Add a win for the player."""
        if not (self.is_fake_client() or 'BOT' in self.steamid):
            winners_database.increment_player_wins(self, wins)

    @property
    def rank(self):
        """Return the player's rank on the server."""
        # If the player is not in the database, they have no wins
        if self.unique_id not in winners_database:
            return 0

        # Start with the base rank
        rank = 1

        # Get the number of wins for the player
        wins = self.wins

        # Create a list to store players tied with this player
        tied_players = list()

        # Loop through all players in the database
        for unique_id in winners_database:

            # Get the current players wins
            current_wins = winners_database[unique_id].wins

            # Does the current player have more wins than this player?
            if current_wins > wins:
                rank += 1

            # Is the current player tied with this player?
            if current_wins == wins:
                tied_players.append(unique_id)

        # Are there any tied players?
        if len(tied_players) > 1:

            # Sort the tied players by their last win
            sorted_ties = sorted(
                tied_players,
                key=lambda unique_id: winners_database[unique_id].last_win
            )

            # Get the final rank of the player
            rank += sorted_ties.index(self.unique_id)

        # Return the player's rank
        return rank

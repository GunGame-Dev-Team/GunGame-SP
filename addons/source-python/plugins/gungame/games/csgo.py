# ../gungame/games/csgo.py

"""CS:GO changes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from warnings import warn

# Source.Python
from core import GAME_NAME
from events import Event
from weapons.manager import weapon_manager

# GunGame
from gungame.core.config.misc import allow_kills_after_round, level_on_protect
from gungame.core.messages.manager import message_manager
from gungame.core.players.dictionary import player_dictionary
from gungame.core.players.instance import GunGamePlayer
from gungame.core.status import (
    GunGameMatchStatus, GunGameRoundStatus, GunGameStatus,
)
from gungame.core.weapons.groups import incendiary_weapons, individual_weapons


# =============================================================================
# >> OVERRIDES
# =============================================================================
individual_weapons.add('taser')


class _NoMessage:
    """Class used to hook non-supported message types."""

    def __init__(self, message_type):
        """Store the message type."""
        self.message_type = message_type

    def message_hook(self, *args, **kwargs):
        """Override for messages that do not work."""
        warn(
            f'Message type "{self.message_type}" not supported for '
            f'game "{GAME_NAME}".'
        )


# CS:GO doesn't support any Dialog menus/messages
message_manager.top_message = _NoMessage('DialogMsg').message_hook
# CS:GO Center and KeyHint message are in same location as HintText
message_manager.center_message = message_manager.hint_message
message_manager.keyhint_message = message_manager.hint_message


@Event('player_death')
def _player_death(game_event):
    """Award the killer with a multi-kill increase or level increase."""
    # Is GunGame active?
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Is the round active or should kills after the round count?
    if (
        GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE and
        not allow_kills_after_round.get_int()
    ):
        return

    # Get the victim
    userid = game_event['userid']

    # Get the attacker
    attacker = game_event['attacker']

    # Was this a suicide?
    if attacker in (userid, 0):
        return

    # Get the victim's instance
    victim = player_dictionary[userid]

    # Get the attacker's instance
    killer = player_dictionary[attacker]

    # Was this a team-kill?
    if victim.team_index == killer.team_index:
        return

    if killer.in_spawn_protection and not level_on_protect.get_int():
        return

    # Did the killer kill using their level's weapon?
    try:
        weapon = weapon_manager[game_event['weapon']].basename
    except KeyError:
        return

    if weapon != 'molotov':
        return

    if killer.level_weapon in incendiary_weapons:
        weapon = killer.level_weapon

    if weapon_manager[weapon].basename != killer.level_weapon:
        return

    # Increase the killer's multi_kill
    killer.multi_kill += 1

    # Does the player need leveled up?
    if killer.multi_kill < killer.level_multi_kill:

        # If not, no need to go further
        return

    # Level the player up
    killer.increase_level(
        levels=1,
        reason='kill',
        victim=userid,
    )


def _give_level_weapon(player):
    """Hooks give_level_weapon to ensure that the proper weapon is given."""
    weapon = _old_give_level_weapon(player)
    if weapon.classname == weapon.weapon_name:
        return weapon
    weapon.remove()
    player.team_index = 5 - player.team_index
    weapon = _old_give_level_weapon(player)
    player.team_index = 5 - player.team_index
    return weapon


_old_give_level_weapon = GunGamePlayer.give_level_weapon
GunGamePlayer.give_level_weapon = _give_level_weapon

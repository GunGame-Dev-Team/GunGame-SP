# ../gungame/plugins/included/gg_multi_nade/gg_multi_nade.py

"""Plugin to get multiple grenades when on grenade levels."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict

# Source.Python
from events import Event
from listeners.tick import Delay
from weapons.manager import weapon_manager

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import individual_weapons

# Plugin
from .configuration import max_nades


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_nade_count = defaultdict(int)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('weapon_fire')
def _delay_give_new_weapon(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    weapon = weapon_manager[game_event['weapon']].basename
    if weapon not in individual_weapons:
        return

    try:
        player = player_dictionary[game_event['userid']]
    except ValueError:
        return

    if weapon != player.level_weapon:
        return

    _nade_count[player.userid] += 1
    value = max_nades.get_int()
    if not value or _nade_count[player.userid] < value:
        Delay(
            delay=1,
            callback=_give_new_weapon,
            args=(player.userid, weapon),
            cancel_on_level_end=True,
        )


@Event('player_spawn', 'gg_level_up')
def _reset_player_count(game_event):
    userid = game_event['userid']
    if userid in _nade_count:
        del _nade_count[userid]


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _give_new_weapon(userid, weapon):
    try:
        player = player_dictionary[userid]
    except ValueError:
        return

    if player.dead:
        return

    if weapon != player.level_weapon:
        return

    player.give_level_weapon()

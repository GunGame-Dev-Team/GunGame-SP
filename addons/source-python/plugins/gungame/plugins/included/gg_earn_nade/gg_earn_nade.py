# ../gungame/plugins/included/gg_earn_nade/gg_earn_nade.py

"""Plugin to earn an extra nade on nade level."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import GAME_NAME
from events import Event
from listeners.tick import Delay

# GunGame
from gungame.core.players.attributes import AttributePreHook
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import all_grenade_weapons

# Plugin
from .settings import auto_switch


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a dictionary to know when a player recently leveled from knife level
_recently_off_nade = dict()

_weapons_to_check = list(all_grenade_weapons)
if GAME_NAME == 'csgo':
    _weapons_to_check += ['taser']


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _earn_nade(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    userid = game_event['userid']
    attacker = game_event['attacker']
    if attacker in (userid, 0):
        return

    victim = player_dictionary[userid]
    killer = player_dictionary[attacker]
    if victim.team == killer.team:
        return

    if killer.level_weapon not in _weapons_to_check:
        return

    if attacker in _recently_off_nade:
        return

    if killer.has_level_weapon():
        return

    weapon = killer.give_level_weapon()
    if auto_switch.get_setting(killer.index):
        killer.client_command(
            command='use {weapon}'.format(weapon=weapon.classname),
            server_side=True,
        )


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePreHook('level')
def _pre_level_change(player, attribute, new_value):
    """Store players leveling off of nade level."""
    if not player.level or player.level_weapon not in _weapons_to_check:
        return

    _recently_off_nade[player.userid] = {
        'level': player.level,
        'weapon': player.level_weapon
    }
    Delay(0, _safe_remove, args=(player.userid, ))


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _safe_remove(userid):
    if userid in _recently_off_nade:
        del _recently_off_nade[userid]

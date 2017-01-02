# ../gungame/plugins/included/gg_earn_nade/gg_earn_nade.py

"""Plugin to earn an extra nade on nade level."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from listeners.tick import Delay

# GunGame
from gungame.core.players.attributes import AttributePreHook
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import all_grenade_weapons

# Plugin
from .settings import auto_switch


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a dictionary to know when a player recently leveled from knife level
_recently_off_nade = dict()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _earn_nade(game_event):
    userid = game_event['userid']
    attacker = game_event['attacker']
    if attacker in (userid, 0):
        return

    victim = player_dictionary[userid]
    killer = player_dictionary[attacker]
    if victim.team == killer.team:
        return

    if killer.level_weapon not in all_grenade_weapons:
        return

    if attacker in _recently_off_nade:
        return

    weapon = killer.give_level_weapon()
    if auto_switch.get_setting(killer.index):
        killer.equip_weapon(weapon)


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePreHook('level')
def _pre_level_change(player, attribute, new_value):
    """Store players leveling off of nade level."""
    if not player.level or player.level_weapon not in all_grenade_weapons:
        return

    _recently_off_nade[player.userid] = {
        'level': player.level,
        'weapon': player.level_weapon
    }
    Delay(0, _recently_off_nade.__delitem__, args=(player.userid, ))

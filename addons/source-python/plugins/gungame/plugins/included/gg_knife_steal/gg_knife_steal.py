# ../gungame/plugins/included/gg_knife_steal/gg_knife_steal.py

"""Plugin that allows level stealing with knives."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from listeners.tick import Delay

# GunGame
from gungame.core.players.attributes import AttributePreHook
from gungame.core.players.dictionary import player_dictionary

# Plugin
from .configuration import (
    grenade_weapons, knife_weapons, level_one_victim, limit
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a dictionary to know when a player recently leveled from knife level
_recently_off_knife = dict()


# =============================================================================
# >> EVENTS
# =============================================================================
@Event('player_death')
def _steal_level(game_event):
    """Level up the killer and down the victim on knife kills."""
    if game_event['weapon'] != 'knife':
        return

    attacker = game_event['attacker']
    userid = game_event['userid']
    if attacker in (userid, 0):
        return

    killer = player_dictionary[attacker]
    victim = player_dictionary[userid]
    if killer.team == victim.team:
        return

    if attacker in _recently_off_knife:
        weapon = _recently_off_knife[attacker]['weapon']
        level = _recently_off_knife[attacker]['level']
    else:
        weapon = killer.level_weapon
        level = killer.level

    # TODO: AFK checks
    # killer.chat_message('KnifeSteal:AFK')

    current = limit.get_int()
    difference = level - victim.level
    if current and difference > current:
        killer.chat_message('KnifeSteal:Difference', levels=difference)
        return

    if victim.level == 1 and not level_one_victim.get_bool():
        killer.chat_message('KnifeSteal:LevelOne')
        return

    if weapon in grenade_weapons:
        if not grenade_weapons[weapon]['skip'].get_bool():
            killer.chat_message('KnifeSteal:NoSkip', weapon=weapon)
            if grenade_weapons[weapon]['level'].get_bool():
                victim.decrease_level(1, attacker, 'steal')
            return

    if weapon in knife_weapons:
        if knife_weapons[weapon].get_bool():
            victim.decrease_level(1, attacker, 'steal')
        return

    victim.decrease_level(1, attacker, 'steal')
    killer.increase_level(1, userid, 'steal')


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePreHook('level')
def _pre_level_change(player, attribute, new_value):
    """Store players leveling off of knife level."""
    if player.level_weapon not in knife_weapons:
        return

    _recently_off_knife[player.userid] = {
        'level': player.level,
        'weapon': player.level_weapon
    }
    Delay(0, _recently_off_knife.__delitem__, args=(player.userid, ))

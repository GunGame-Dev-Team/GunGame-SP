# ../gungame/plugins/included/gg_knife_steal/gg_knife_steal.py

"""Plugin that allows level stealing with knives."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from listeners.tick import Delay
from weapons.manager import weapon_manager

# GunGame
from gungame.core.players.attributes import AttributePreHook
from gungame.core.players.dictionary import player_dictionary

# Plugin
from .configuration import (
    grenade_weapons, knife_weapons, level_one_victim, limit
)
from .custom_events import GG_Knife_Steal
from .settings import auto_switch


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a dictionary to know when a player recently leveled from knife level
_recently_off_knife = dict()
_knife_classnames = {
    x.name for x in weapon_manager.values() if x.basename in knife_weapons
}


# =============================================================================
# >> GAME EVENTS
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
        killer_level = _recently_off_knife[attacker]['level']
    else:
        weapon = killer.level_weapon
        killer_level = killer.level

    # TODO: AFK checks
    # killer.chat_message('KnifeSteal:AFK')

    victim_level = victim.level

    current = limit.get_int()
    difference = killer_level - victim_level
    if current and difference > current:
        killer.chat_message('KnifeSteal:Difference', levels=difference)
        return

    if victim_level == 1 and not level_one_victim.get_bool():
        killer.chat_message('KnifeSteal:LevelOne')
        return

    if weapon in grenade_weapons:
        if not grenade_weapons[weapon]['skip'].get_bool():
            killer.chat_message('KnifeSteal:NoSkip', weapon=weapon)
            if grenade_weapons[weapon]['level'].get_bool():
                victim.decrease_level(
                    levels=1,
                    reason='steal',
                    attacker=attacker,
                )
            return

    if weapon in knife_weapons:
        if knife_weapons[weapon].get_bool():
            victim.decrease_level(
                levels=1,
                reason='steal',
                attacker=attacker,
            )
        return

    victim.decrease_level(
        levels=1,
        reason='steal',
        attacker=attacker,
    )
    killer.increase_level(
        levels=1,
        reason='steal',
        victim=userid,
    )

    if victim.level == victim_level - 1 and killer.level == killer_level + 1:

        with GG_Knife_Steal() as event:
            event.attacker = event.leveler = killer.userid
            event.attacker_level = killer.level
            event.userid = event.victim = victim.userid
            event.userid_level = victim.level


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_knife_steal')
def _on_knife_steal(game_event):
    attacker = player_dictionary[game_event['leveler']]
    if auto_switch.get_setting(attacker.index):
        Delay(0, _set_back_to_knife, (attacker.userid, ))


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePreHook('level')
def _pre_level_change(player, attribute, new_value):
    """Store players leveling off of knife level."""
    if not player.level or player.level_weapon not in knife_weapons:
        return

    _recently_off_knife[player.userid] = {
        'level': player.level,
        'weapon': player.level_weapon
    }
    Delay(0, _recently_off_knife.__delitem__, args=(player.userid, ))


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _set_back_to_knife(userid):
    player = player_dictionary[userid]
    if player.active_weapon not in _knife_classnames:
        player.client_command(
            'lastinv',
            server_side=True,
        )

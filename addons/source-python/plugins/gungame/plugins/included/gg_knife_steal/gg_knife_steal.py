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
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons

# Plugin
from .configuration import (
    level_down_knife_level, level_one_victim, level_victim_nade, limit,
    skip_nade,
)
from .custom_events import GG_Knife_Steal
from .settings import no_switch


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a dictionary to know when a player recently leveled from knife level
_recently_off_knife = {}
_knife_classnames = {
    x.name for x in weapon_manager.values() if x.basename in melee_weapons
}


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _steal_level(game_event):
    """Level up the killer and down the victim on knife kills."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    event_weapon = game_event['weapon']
    if event_weapon not in melee_weapons:
        return

    attacker = game_event['attacker']
    userid = game_event['userid']
    if attacker in (userid, 0):
        return

    killer = player_dictionary[attacker]
    victim = player_dictionary[userid]
    if killer.team_index == victim.team_index:
        return

    if attacker in _recently_off_knife:
        weapon = _recently_off_knife[attacker]['weapon']
        killer_level = _recently_off_knife[attacker]['level']
    else:
        weapon = killer.level_weapon
        killer_level = killer.level

    if victim.is_afk:
        killer.chat_message('KnifeSteal:AFK')

    victim_level = victim.level

    current = limit.get_int()
    difference = killer_level - victim_level
    if current and difference > current:
        killer.chat_message('KnifeSteal:Difference', levels=difference)
        return

    if victim_level == 1 and not level_one_victim.get_bool():
        if weapon != event_weapon:
            killer.chat_message('KnifeSteal:LevelOne')
        return

    if weapon in all_grenade_weapons and not skip_nade.get_bool():
        killer.chat_message('KnifeSteal:NoSkip', weapon=weapon)
        if level_victim_nade.get_bool():
            victim.decrease_level(
                levels=1,
                reason='steal',
                attacker=attacker,
                sound_name='knife_stolen',
            )
        return

    if weapon in melee_weapons:
        if level_down_knife_level.get_bool():
            victim.decrease_level(
                levels=1,
                reason='steal',
                attacker=attacker,
                sound_name='knife_stolen',
            )
        return

    victim.decrease_level(
        levels=1,
        reason='steal',
        attacker=attacker,
        sound_name='knife_stolen',
    )
    killer.increase_level(
        levels=1,
        reason='steal',
        victim=userid,
        sound_name='knife_steal',
    )

    if victim.level == victim_level - 1 and killer.level == killer_level + 1:

        with GG_Knife_Steal() as event:
            event.attacker = event.leveler = killer.userid
            event.attacker_level = killer.level
            event.userid = event.victim = victim.userid
            event.victim_level = victim.level


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_knife_steal')
def _on_knife_steal(game_event):
    attacker = player_dictionary[game_event['leveler']]
    if no_switch.get_setting(attacker.index):
        Delay(
            delay=0,
            callback=_set_back_to_knife,
            args=(attacker.userid,),
        )


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePreHook('level')
def _pre_level_change(player, attribute, new_value):
    """Store players leveling off of knife level."""
    if not player.level or player.level_weapon not in melee_weapons:
        return

    _recently_off_knife[player.userid] = {
        'level': player.level,
        'weapon': player.level_weapon
    }
    Delay(
        delay=0,
        callback=_recently_off_knife.__delitem__,
        args=(player.userid,),
    )


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

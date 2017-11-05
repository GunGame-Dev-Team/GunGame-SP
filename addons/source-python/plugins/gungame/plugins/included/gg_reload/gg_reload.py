# ../gungame/plugins/included/gg_reload/gg_reload.py

"""Plugin to reload weapons when players get a kill."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from weapons.manager import weapon_manager

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_non_reload_weapons = all_grenade_weapons | melee_weapons


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _reload_weapon(game_event):
    attacker = game_event['attacker']
    userid = game_event['userid']

    if attacker in (userid, 0):
        return

    killer = player_dictionary[attacker]
    if killer.team_index == player_dictionary[userid].team_index:
        return

    weapon_name = game_event['weapon']
    if weapon_name in _non_reload_weapons:
        return

    weapon_instance = weapon_manager[weapon_name]
    weapon = killer.get_weapon(weapon_instance.name)
    weapon.clip = weapon_instance.clip
    weapon.ammo = weapon_instance.maxammo

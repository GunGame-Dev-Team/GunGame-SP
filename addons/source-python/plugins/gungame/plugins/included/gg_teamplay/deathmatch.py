# ../gungame/plugins/included/gg_teamplay/deathmatch.py

"""Deathmatch-based teamplay functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import melee_weapons

# Plugin
from .manager import team_dictionary


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _increment_team_multi_kill(game_event):
    weapon = game_event['weapon']
    attacker = player_dictionary.get(game_event['attacker'])
    if attacker is None:
        return

    victim = player_dictionary[game_event['userid']]
    if victim.team == attacker.team:
        return

    team = team_dictionary.get(attacker.team)
    if team is None:
        return

    if weapon != team.level_weapon:
        if weapon == 'prop_physics':
            # TODO: add conditionals
            if True:
                return

        elif weapon in melee_weapons:
            # TODO: add conditionals
            if True:
                return

    team.increase_multi_kill()

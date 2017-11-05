# ../gungame/plugins/included/gg_teamplay/deathmatch.py

"""Deathmatch-based teamplay functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from weapons.manager import weapon_manager

# GunGame
from gungame.core.config.weapon import prop_physics
from gungame.core.players.dictionary import player_dictionary
from gungame.core.rules.strings import rules_translations
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import grenade_weapons, melee_weapons

# Plugin
from .configuration import count_grenade_kills, count_melee_kills
from .manager import team_dictionary
from .rules import teamplay_rules


# =============================================================================
# >> RULES
# =============================================================================
for _item in list(teamplay_rules):
    if _item.startswith('Teamplay:Rounds:'):
        teamplay_rules.unregister_rule(_item)

for _key, _value in rules_translations.items():
    if _key.startswith('Teamplay:Deathmatch:'):
        teamplay_rules.register_rule(
            name=_key,
            value=_value,
        )


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _increment_team_multi_kill(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    attacker = player_dictionary.get(game_event['attacker'])
    if attacker is None:
        return

    victim = player_dictionary[game_event['userid']]
    if victim.team_index == attacker.team_index:
        return

    team = team_dictionary.get(attacker.team_index)
    if team is None:
        return

    weapon = weapon_manager[game_event['weapon']].basename
    if weapon != team.level_weapon:
        if weapon == 'prop_physics' and not prop_physics.get_int():
            return

        elif weapon in melee_weapons and not count_melee_kills.get_int():
            return

        elif weapon in grenade_weapons and not count_grenade_kills.get_int():
            return

    team.increase_multi_kill()

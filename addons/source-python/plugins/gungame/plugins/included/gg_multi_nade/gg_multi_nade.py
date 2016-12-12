# ../gungame/plugins/included/gg_multi_nade/__init__.py

"""Plugin to get multiple grenades when on grenade levels."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict

# Source.Python
from events import Event

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import all_grenade_weapons

# Plugin
from .configuration import max_nades


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_nade_count = defaultdict(int)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event(
    'decoy_detonate', 'flashbang_detonate', 'hegrenade_detonate',
    'molotov_detonate', 'smokegrenade_detonate'
)
def give_another_nade(game_event):
    try:
        player = player_dictionary[game_event['userid']]
    # TODO: Clarify this exception type
    except Exception:
        return

    if player.dead:
        return

    weapon = player.level_weapon
    if weapon not in all_grenade_weapons:
        return

    grenade = game_event.name.replace('_detonate', '')
    if grenade != weapon:
        return

    _nade_count[player.userid] += 1
    value = max_nades.get_int()
    if not value or _nade_count[player.userid] < value:
        player.give_level_weapon(drop_current_for_slot=False)


@Event('player_spawn', 'gg_level_up')
def reset_player_count(game_event):
    userid = game_event['userid']
    if userid in _nade_count:
        del _nade_count[userid]

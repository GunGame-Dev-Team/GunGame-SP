# ../gungame/plugins/included/gg_bombing_objective/gg_bombing_objective.py

"""Plugin that adds leveling based on bombing objectives."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from .configuration import (
    defused_levels, defused_skip_knife, defused_skip_nade, detonated_levels,
    detonated_skip_knife, detonated_skip_nade,
)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('bomb_defused')
def _bomb_defused(game_event):
    """Level the defuser up."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    player = player_dictionary[game_event['userid']]
    levels = _get_levels_to_increase(player, 'defused')
    if not levels:
        return
    player.increase_level(
        levels=levels,
        reason='bomb_defused',
    )
    player.chat_message(
        message='BombingObjective:Leveled:Defused',
        levels=levels,
    )


@Event('bomb_exploded')
def _bomb_exploded(game_event):
    """Level the detonator up."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    player = player_dictionary[game_event['userid']]
    levels = _get_levels_to_increase(player, 'detonated')
    if not levels:
        return
    player.increase_level(
        levels=levels,
        reason='bomb_detonated',
    )
    player.chat_message(
        message='BombingObjective:Leveled:Detonated',
        levels=levels,
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _get_levels_to_increase(player, reason):
    """Return the number of levels to increase the player."""
    if reason == 'defused':
        base_levels = defused_levels.get_int()
        skip_nade = defused_skip_nade.get_int()
        skip_knife = defused_skip_knife.get_int()
    elif reason == 'detonated':
        base_levels = detonated_levels.get_int()
        skip_nade = detonated_skip_nade.get_int()
        skip_knife = detonated_skip_knife.get_int()
    else:
        raise ValueError(
            'Invalid reason given "{reason}".'.format(reason=reason)
        )

    if base_levels <= 0:
        return 0

    level_increase = 0

    for level_increase in range(1, base_levels + 1):
        level = player.level + level_increase
        if level > weapon_order_manager.max_levels:
            return level_increase
        skip_weapon = weapon_order_manager.active[level - 1].weapon
        if (
            (skip_weapon in all_grenade_weapons and not skip_nade) or
            (skip_weapon in melee_weapons and not skip_knife)
        ):
            player.chat_message(
                'BombingObjective:NoSkip:{reason}'.format(
                    reason=reason.title()
                ),
                weapon=skip_weapon,
            )
            return level_increase - 1
    return level_increase

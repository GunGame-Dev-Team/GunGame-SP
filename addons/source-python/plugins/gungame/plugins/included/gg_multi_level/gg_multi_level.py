# ../gungame/plugins/included/gg_multi_level/gg_multi_level.py

"""Plugin that allows players to gain special powers when multi-leveling."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from players.entity import Player

# GunGame
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary

# Plugin
from .configuration import (
    gravity, length, levels, speed, tk_attacker_reset, tk_victim_reset,
)


# =============================================================================
# >> REGISTRATION
# =============================================================================
player_attributes.register_attribute('multi_levels', 0)


# =============================================================================
# >> CLASSES
# =============================================================================
class _MultiLevelManager(dict):
    """"""

    def clear(self):
        super().clear()

    def give_multi_level(self, player):
        pass

    def reset_player(self, player):
        pass

multi_level_manager = _MultiLevelManager()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_levelup')
def _player_levelup(game_event):
    player = player_dictionary[game_event['leveler']]
    player.multi_levels += 1
    if player.multi_levels >= levels.get_int():
        # Give or increase multi-level
        multi_level_manager.give_multi_level(player)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _reset_team_killers(game_event):
    victim = Player.from_userid(game_event['userid'])
    attacker = game_event['attacker']

    # Suicide?
    if attacker in (0, victim.userid):
        multi_level_manager.reset_player(victim)
        return

    killer = Player.from_userid(attacker)

    # Not team-kill?
    if victim.team != killer.team:
        multi_level_manager.reset_player(victim)
        return

    # Reset team-kill victim's multi-level
    if not tk_victim_reset.get_bool():
        multi_level_manager.reset_player(victim)

    # Reset the team-killer's multi-level
    if tk_attacker_reset.get_bool():
        multi_level_manager.reset_player(killer)

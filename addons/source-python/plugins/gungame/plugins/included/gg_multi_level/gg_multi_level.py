# ../gungame/plugins/included/gg_multi_level/gg_multi_level.py

"""Plugin that allows players to gain special powers when multi-leveling."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from time import time

# Source.Python
from entities.entity import Entity
from events import Event
from listeners import on_tick_listener_manager
from listeners.tick import Delay
from mathlib import Vector
from players.entity import Player

# GunGame
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary
from gungame.core.sounds.manager import sound_manager

# Plugin
from .configuration import (
    gravity, length, levels, speed, tk_attacker_reset, tk_victim_reset,
)
from .custom_events import GG_Multi_Level


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    player_attributes.register_attribute('multi_levels', 0)


def unload():
    player_attributes.unregister_attribute('multi_levels')


# =============================================================================
# >> CLASSES
# =============================================================================
class _MultiLevelPlayer(Player):
    """"""

    spark_entity = None
    delay = None

    def __init__(self, index):
        super(_MultiLevelPlayer, self).__init__(index)
        self.sound = sound_manager.emit_sound('multi_level', index)
        self.start_gravity = self.gravity
        self.start_speed = self.speed
        self.gravity = gravity.get_int() / 100
        self.speed = speed.get_int() / 100
        self.end_time = time() + length.get_float()
        self.give_spark_entity()
        self.delay = Delay(
            delay=self.sound.duration,
            callback=self.remove_multi_level,
            kwargs={'from_delay': True},
        )

    def give_spark_entity(self):
        entity = self.spark_entity = Entity.create('env_spark')
        entity.spawn_flags = 896
        entity.angles = Vector(-90, 0, 0)
        entity.magnitude = 8
        entity.trail_length = 3
        entity.set_parent(self, -1)
        entity.origin = self.origin
        entity.start_spark()

    def remove_multi_level(self, from_delay=False):
        if not from_delay and self.delay is not None:
            self.delay.cancel()
        self.delay = None
        self.gravity = self.start_gravity
        self.speed = self.start_speed
        self.sound.stop(self.index)
        self.remove_spark_entity()

    def remove_spark_entity(self):
        self.spark_entity.stop_spark()
        self.spark_entity.remove()


class _MultiLevelManager(dict):
    """"""

    def __delitem__(self, userid):
        player_dictionary[userid].multi_levels = 0
        if userid not in self:
            return
        self[userid].remove_multi_level()
        super(_MultiLevelManager, self).__delitem__(userid)
        if not len(self):
            on_tick_listener_manager.unregister_listener(self._tick)

    def clear(self):
        for userid in list(self):
            del self[userid]

    def give_multi_level(self, userid):
        if not len(self):
            on_tick_listener_manager.register_listener(self._tick)
        if userid in self:
            del self[userid]
        self[userid] = _MultiLevelPlayer.from_userid(userid)
        with GG_Multi_Level() as event:
            event.userid = userid
            event.leveler = userid

    def _tick(self):
        current_gravity = gravity.get_int()
        for userid, player in list(self.items()):
            if player.end_time <= time():
                del self[userid]
                continue
            player.gravity = current_gravity

multi_level_manager = _MultiLevelManager()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_level_up')
def _player_level_up(game_event):
    player = player_dictionary[game_event['leveler']]
    player.multi_levels += 1
    if player.multi_levels >= levels.get_int():
        # Give or increase multi-level
        multi_level_manager.give_multi_level(player.userid)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _reset_team_killers(game_event):
    userid = game_event['userid']
    attacker = game_event['attacker']

    # Suicide?
    if attacker in (0, userid):
        del multi_level_manager[userid]
        return

    # Not team-kill?
    if Player.from_userid(userid).team != Player.from_userid(attacker).team:
        del multi_level_manager[userid]
        return

    # Reset team-kill victim's multi-level?
    if not tk_victim_reset.get_bool():
        del multi_level_manager[userid]

    # Reset the team-killer's multi-level?
    if tk_attacker_reset.get_bool():
        del multi_level_manager[attacker]


@Event('player_disconnect')
def _remove_disconnecting_player(game_event):
    del multi_level_manager[game_event['userid']]

'''
    cvars:

        gg_warmup_round:
            enable/disable

        gg_warmup_time:
            time (in seconds) for the warmup to last
            each extension will be this amount, as well

        gg_warmup_weapon:
            0 = the first level weapon for the gg_weapon_order_file
            weapon1
            weapon1,weapon2,weapon3,etc...
            random/#random = random weapon
            DEFAULT: "hegrenade"

        gg_warmup_start_config:
            config file to execute to determine gameplay in warmup

        gg_warmup_end_config:
            config file to execute to determine the
              gameplay for the match after warmup ends

        gg_warmup_min_players:
            minimum number of players needed to
              end warmup round without extending

        gg_warmup_max_extensions:
            the number of extensions after which to just
              start without waiting for more players

        gg_warmup_players_reached:
            0 = wait till base warmup time ends before ending warmup
                this means wait, even if in extended time, till the
                  extended amount of time has been reached
            1 = end warmup immediately if in extended time,
                but continue till
            2 = end warmup immediately when min players is reached

    commands:

        gg_end_warmup (server command):
            ends the warmup round immediately


    POSSIBLE SETTINGS FOR WARMUP:
        dead_strip
        deathmatch
        dissolver
        earn_nade
        elimination
        ffa
        multi_nade
        noblock
        nocash
        random_spawn
        roundend_blocker
        spawn_protect
'''

from contextlib import suppress
from itertools import cycle
from random import shuffle

from cvars import ConVar
from engines.server import engine_server
from filters.errors import FilterError
from filters.players import PlayerIter
from filters.weapons import WeaponClassIter
from listeners.tick import TickRepeat

from gungame.core.weapons.manager import weapon_order_manager

possible_weapons = set(WeaponClassIter('primary', return_types='basename'))
possible_weapons.update(set(
    WeaponClassIter('secondary', return_types='basename')))

possible_weapons.update(set(
    WeaponClassIter('explosive', return_types='basename')))

with suppress(FilterError):
    possible_weapons.update(set(
        WeaponClassIter('incendiary', return_types='basename')))

human_nospec = PlayerIter('human', ['spec', 'un'])


class _WarmupManager(object):

    """"""

    def __init__(self):
        """"""
        self._repeat = TickRepeat(self._countdown)
        self._extensions = 0
        self._weapon = None
        self._weapon_list = None

    @property
    def repeat(self):
        """"""
        return self._repeat

    @property
    def extensions(self):
        """"""
        return self._extensions

    @property
    def warmup_time(self):
        """"""
        return self._warmup_time

    @property
    def weapon(self):
        """"""
        return self._weapon

    @property
    def weapon_list(self):
        """"""
        return self._weapon_list

    def set_warmup_weapon(self):
        """"""
        warmup_weapon = ConVar('gg_warmup_weapon').get_string()
        if warmup_weapon in possible_weapons:
            self._weapon_list = cycle([warmup_weapon])
            return
        if warmup_weapon == 'random':
            weapons = list(possible_weapons)
            shuffle(weapons)
            self._weapon_list = cycle(weapons)
            return
        if ',' in warmup_weapon:
            weapons = [weapon for weapon in warmup_weapon.split(
                ',') if weapon in possible_weapons]
            if len(weapons):
                self._weapon_list = cycle(weapons)
                return
        self._weapon_list = cycle([weapon_order_manager.active[1].weapon])

    def start_warmup(self):
        """"""
        self._extensions = 0
        self._warmup_time = ConVar('gg_warmup_time').get_int()
        if self._warmup_time <= 0:
            warn(
                '"gg_warmup_time" is set to an invalid number.' +
                '  Skipping warmup round.')
            self.end_warmup()
            return
        engine_server.server_command('exec {0}'.format(
            ConVar('gg_warmup_start_config').get_string()))
        self._find_warmup_weapon()
        self.repeat.start(1, self._warmup_time)

    def end_warmup(self):
        """"""
        # TODO: Call start match
        engine_server.server_command('exec {0}'.format(
            ConVar('gg_warmup_end_config').get_string()))

    def _find_warmup_weapon(self):
        """"""
        self._weapon = next(self.weapon_list)

    def _countdown(self):
        """"""
        remaining = self.repeat.remaining
        if not remaining:
            self.end_warmup()
            return
        if len(list(human_nospec)) > ConVar('gg_warmup_min_players').get_int():
            players_reached = ConVar('gg_warmup_players_reached').get_int()
            if players_reached == 2 or (
                    self.extensions and players_reached == 1):
                self.repeat.reduce(self.repeat.remaining - 1)
                return
        if remaining == 1:
            if self.extensions < ConVar('gg_warmup_max_extensions').get_int():
                self._extensions += 1
                self.repeat.extend(self._warmup_time)
                return
        else:
            # TODO: send message to players about remaining warmup time
            ...
        if remaining <= 5:
            # TODO: play a beeping sound to indicate warmup ending soon
            ...

warmup_manager = _WarmupManager()

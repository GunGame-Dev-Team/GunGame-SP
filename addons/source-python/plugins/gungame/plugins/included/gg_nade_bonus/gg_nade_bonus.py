# ../gungame/plugins/included/gg_nade_bonus/gg_nade_bonus.py

"""Plugin to give extra weapons to players on nade levels."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from warnings import warn

# Source.Python
from events import Event
from listeners import OnLevelEnd
from listeners.tick import Delay
from weapons.manager import weapon_manager

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.weapons.groups import (
    all_grenade_weapons, all_primary_weapons, all_secondary_weapons,
    all_weapons,
)
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from .configuration import bonus_mode, bonus_reset, bonus_weapon


# =============================================================================
# >> CLASSES
# =============================================================================
class _NadeBonusDictionary(dict):
    """Dictionary that holds players with their bonus weapons."""

    def __init__(self):
        """Store the nade bonus weapon(s)."""
        super().__init__()
        self._weapon = self._validate_weapon()

    def __missing__(self, userid):
        """Store the player in the dictionary."""
        value = self[userid] = _NadeBonusPlayer(userid)
        return value

    @property
    def weapon(self):
        """Return the bonus weapon."""
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        """Set the bonus weapon using the convar and not the given value."""
        old_value = self._weapon
        new_value = self._validate_weapon()
        if not new_value:
            return
        self._weapon = new_value
        if old_value in weapon_order_manager:
            for instance in self.values():
                instance.reset_level()

    @staticmethod
    def _validate_weapon():
        """Return the validated bonus weapon(s)."""
        weapon = bonus_weapon.get_string()
        if weapon in weapon_order_manager:
            return weapon

        given_weapons = [x for x in weapon.split(',')]
        valid_weapons = [x for x in given_weapons if x in all_weapons]
        if not valid_weapons:
            warn(
                'No valid weapons found in "{weapon}".'.format(weapon=weapon)
            )
            return valid_weapons
        for invalid_weapon in set(given_weapons).difference(valid_weapons):
            warn(
                'Invalid weapon given: {invalid_weapon}'.format(
                    invalid_weapon=invalid_weapon,
                )
            )
        primary = None
        secondary = None
        extra_primary = set()
        extra_secondary = set()
        all_valid_weapons = set()
        for valid_weapon in valid_weapons:
            if valid_weapon in all_primary_weapons and primary is not None:
                extra_primary.add(valid_weapon)
                continue
            if valid_weapon in all_primary_weapons:
                primary = valid_weapon
            if valid_weapon in all_secondary_weapons and secondary is not None:
                extra_secondary.add(valid_weapon)
                continue
            if valid_weapon in all_secondary_weapons:
                secondary = valid_weapon
            all_valid_weapons.add(valid_weapon)
        if extra_primary:
            warn(
                'Too many primary weapons given: "{weapons}"'.format(
                    weapons=','.join(extra_primary),
                )
            )
        if extra_secondary:
            warn(
                'Too many secondary weapons given: "{weapons}"'.format(
                    weapons=','.join(extra_secondary),
                )
            )
        return all_valid_weapons

nade_bonus_dictionary = _NadeBonusDictionary()


class _NadeBonusPlayer(object):
    """Stores a player with their bonus weapon."""

    def __init__(self, userid):
        """Store the player and their bonus weapon attributes."""
        self.player = player_dictionary[userid]
        self.level = 1
        self.multi_kill = 0

    @property
    def delay_time(self):
        """Return the amount of time to delay before giving weapons."""
        return 0.4 if self.player.is_fake_client() else 0.1

    @property
    def is_in_bonus(self):
        """Return whether or not the player is on a nade level."""
        try:
            return self.player.level_weapon in all_grenade_weapons
        except KeyError:
            return False

    def reset_level(self):
        """Reset the player's nade bonus level."""
        self.level = 1
        self.multi_kill = 0

    def check_on_spawn(self):
        """Verify the spawning player is on a nade level."""
        if self.is_in_bonus:
            self.give_current_weapon()

    def check_new_level(self):
        """Verify the leveling player is on a nade level."""
        self.reset_level()
        if self.is_in_bonus:
            self.give_current_weapon()

    def increment_multi_kill(self, weapon):
        """Increment the player's nade bonus weapon."""
        if not self.is_in_bonus:
            return

        if nade_bonus_dictionary.weapon not in weapon_order_manager:
            return

        order = weapon_order_manager[nade_bonus_dictionary.weapon]
        level = order[self.level]

        if weapon != level.weapon:
            return

        self.multi_kill += 1
        if self.multi_kill < level._multi_kill:
            return
        if self.level == order.max_levels:
            mode = bonus_mode.get_int()
            if mode == 1:
                self.reset_level()
                self.check_turbo(weapon)
            elif mode == 2:
                self.player.increase_level(
                    levels=1,
                    reason='nade_bonus',
                )
        else:
            self.multi_kill = 0
            self.level += 1
            self.check_turbo(weapon)

    def check_turbo(self, old_weapon):
        """Verify turbo is running and give the player their weapon now."""
        if 'gg_turbo' not in gg_plugin_manager:
            return

        weapon_name = weapon_manager[old_weapon].name
        for weapon in self.player.weapons():
            if weapon.classname == weapon_name:
                weapon.remove()
        self.give_current_weapon()

    def give_current_weapon(self):
        """Give the player their current nade bonus weapon."""
        weapons = nade_bonus_dictionary.weapon
        if not weapons:
            return

        if weapons in weapon_order_manager:
            weapons = weapon_order_manager[weapons][self.level].weapon

        Delay(
            delay=self.delay_time,
            callback=self._give_weapons,
            args=(weapons, ),
        )

    def _give_weapons(self, weapons):
        """Give the player their weapon."""
        if isinstance(weapons, str):
            weapons = [weapons]
        for weapon in weapons:
            self.player.give_named_item(weapon_manager[weapon].name)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_spawn')
def _give_current_weapon(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    nade_bonus_dictionary[game_event['userid']].check_on_spawn()


@Event('player_death')
def _increment_multi_kill(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    userid = game_event['userid']
    attacker = game_event['attacker']

    if attacker in (0, userid):
        return

    killer = nade_bonus_dictionary[attacker]
    victim = nade_bonus_dictionary[userid]
    if killer.player.team_index == victim.player.team_index:
        return

    killer.increment_multi_kill(game_event['weapon'])

    if bonus_reset.get_int():
        victim.reset_level()


@Event('server_cvar')
def _update_weapon(game_event):
    if game_event['cvarname'] != bonus_weapon.name:
        return

    nade_bonus_dictionary.weapon = game_event['cvarvalue']


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_level_up', 'gg_level_down')
def _check_level(game_event):
    nade_bonus_dictionary[game_event['leveler']].check_new_level()


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelEnd
def _clear_dictionary():
    nade_bonus_dictionary.clear()

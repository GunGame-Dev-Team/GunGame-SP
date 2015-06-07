# ../core/weapons/__init__.py

"""
$Rev: 647 $
$LastChangedBy: satoon101 $
$LastChangedDate: 2012-06-11 23:09:36 -0400 (Mon, 11 Jun 2012) $
"""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
from __future__ import with_statement
from random import shuffle
from path import path

# EventScripts Imports
#   ES
import es
#   Weaponlib
from weaponlib import getWeaponList

# GunGame Imports
from gungame51.core import get_game_dir
#   Messaging
from gungame51.core.messaging.shortcuts import langstring


# =============================================================================
# >> GLOBALS
# =============================================================================
# Paths/Files
weaponOrdersPath = get_game_dir('cfg/gungame51/weapon_orders/')
weaponOrderFilesTXT = weaponOrdersPath.files("*.txt")
#weaponOrderFilesINI = weaponOrdersPath.files("*.ini")

# Variables
gg_multikill_override = es.ServerVar('gg_multikill_override')
gg_weapon_order_sort_type = es.ServerVar('gg_weapon_order_sort_type')

# Weapons
VALID_WEAPONS = (getWeaponList('#primary') + getWeaponList('#secondary') +
                ['weapon_hegrenade', 'weapon_knife'])


# =============================================================================
# >> CLASSES
# =============================================================================
class WeaponOrderError(Exception):
    pass


class _BaseWeaponOrder(object):
    def __init__(self, path_instance):
        self._name = path_instance.namebase
        self._filepath = path_instance
        self._title = self.name.replace('_', ' ').title()
        self._default = {}
        self._random = {}

        # Is the active order default or random?
        self._set_active_order_type()

    # =========================================================================
    # Properties
    # =========================================================================
    @property
    def active(self):
        return self._active

    @property
    def name(self):
        return self._name

    @property
    def filepath(self):
        return self._filepath

    @property
    def title(self):
        return self._title

    @property
    def default(self):
        return self._default

    @property
    def random(self):
        return self._random

    @property
    def totallevels(self):
        return len(self.active)

    def _set_active_order_type(self):
        if str(gg_weapon_order_sort_type) == '#default':
            self._active = self.default
        elif str(gg_weapon_order_sort_type) == '#random':
            self._active = self.random
        elif str(gg_weapon_order_sort_type) == '0':
            self._active = self.default
        else:
            raise WeaponOrderError('Unable to initialize weapon order ' +
                                   '"%s" due to invalid ' % self.name +
                                   'gg_weapon_order_sort_type of "%s". ' % (
                                   str(gg_weapon_order_sort_type)) +
                                   'Expected "#default" or "#random".')

    def randomize(self):
        # Retrieve the weapon and kills info from the default dictionary
        weapons = self.default.values()

        # Loop through the weapon order in reverse to get knives and nades
        knifeOrNade = []
        for x in reversed(weapons):
            if not x.weapon in ('knife', 'hegrenade'):
                break
            knifeOrNade.append(x)

        # If we found a knife or nade at the end of the order alter the order
        if knifeOrNade:

            # Reverse knifeOrNade, so that we get them in the proper order
            # This only needs done if we have knife or nade levels to add
            knifeOrNade = reversed(knifeOrNade)

            # Remove the levels from the weapon order
            weapons = weapons[:-len(knifeOrNade)]

        # Randomize the weapons
        shuffle(weapons)

        # Add the knife/nade back to the end of the order
        weapons += knifeOrNade

        # Create the random weapon order
        self._random = dict(zip(range(1, len(weapons) + 1), weapons))

        # Since self.active is set to the previous value of self.random,
        # we need to re-call _set_active_order_type to set the new values
        self._set_active_order_type()

    def echo(self):
        """
        Echos (prints) the current weapon order to console.
        """
        es.dbgmsg(0, ' ')
        es.dbgmsg(0, '[GunGame] ' + langstring('WeaponOrder:Echo',
                                                    {'file': self.title}))
        es.dbgmsg(0, ' ')
        echo_string = langstring('WeaponOrder:Echo:TableColumns')
        echo_lengths = [len(x) for x in echo_string.split('|')[1:4]]
        echo_columns = '+'.join(['-' * x for x in echo_lengths]) + '+'
        es.dbgmsg(0, '[GunGame] +' + echo_columns)
        es.dbgmsg(0, '[GunGame] ' + echo_string)
        es.dbgmsg(0, '[GunGame] +' + echo_columns)
        for level in self.active:
            weapon = self.active[level].weapon
            multikill = self.active[level].kills
            es.dbgmsg(0, '[GunGame] |%s|%s|%s |' % (
                        str(level).center(echo_lengths[0]),
                        str(multikill).center(echo_lengths[1]),
                        weapon.rjust(echo_lengths[2] - 1)))
        es.dbgmsg(0, '[GunGame] +' + echo_columns)

    def get_weapon(self, level):
        totalLevels = self.get_total_levels()
        if not self.is_valid_level(level):
            raise WeaponOrderError('Can not get weapon for level: "%s".'
                                   % level + ' Level is out of range (1-%s).'
                                   % totalLevels)
        return self.active[level].weapon

    def get_multikill(self, level):
        totalLevels = self.get_total_levels()
        if not self.is_valid_level(level):
            raise WeaponOrderError('Can not get multikill value for level: ' +
                                   '"%s".' % level + ' Level is out of range '
                                   '(1-%s).' % totalLevels)
        return self.active[level].kills

    def get_total_levels(self):
        return len(self.active)

    def is_valid_level(self, level):
        totalLevels = self.get_total_levels()
        return level in xrange(1, totalLevels + 1)


class WeaponOrderTXT(_BaseWeaponOrder):
    def __init__(self, *args, **kwargs):
        super(WeaponOrderTXT, self).__init__(*args, **kwargs)
        self._parse()

    def _parse(self):
        try:
            with self.filepath.open() as weaponOrderFile:

                # Clean and format the lines
                lines = [x.strip() for x in weaponOrderFile.readlines()]
                lines = filter(lambda x: x and (not x.startswith('//')), lines)
                lines = [x.split('//')[0].lower() for x in lines]
                lines = [' '.join(x.split()) for x in lines]

        except IOError, e:
            raise WeaponOrderError('Cannot parse weapon order file ' +
                '(%s): IOError: %s' % (self.filepath, e))

        # Create a level counter
        level = 0

        for line in lines:
            # Backwards-compatibility niceness (skip lines with these)
            if line.startswith(('@', '=>')):
                import warnings
                warnings.warn('Please remove the "@" or "=>" line from the ' +
                              'weapon order "%s". ' % self.name + 'This is ' +
                              'no longer supported.', DeprecationWarning,
                              stacklevel=2)
                continue

            # Retrieve the weapon and multikill values
            try:
                weapon, multikill = line.split()
            except ValueError:
                weapon = line
                multikill = 1

            # Validate the weapon
            if not "weapon_%s" % weapon in VALID_WEAPONS:
                raise WeaponOrderError('"%s" is not a valid weapon!' % weapon)

            # Convert the multikill value to int
            try:
                multikill = int(multikill)
            except ValueError:
                raise WeaponOrderError('"%s" is not a valid ' % multikill +
                                 'multikill value.')

            # Increment the level count
            level += 1

            # Add the level and values to the weapons dictionary
            self._default[level] = _WeaponOrderEntry(weapon, multikill)

            # Randomize the random weapon order
            self.randomize()


"""
class WeaponOrderINI(_BaseWeaponOrder):
    def __init__(self, *args, **kwargs):
        super(WeaponOrderINI, self).__init__(*args, **kwargs)

    def _parse(self):
        pass
"""


class _WeaponOrderStorage(dict):
    """A class-based dictionary to contain instances of _BaseWeaponOrder.

    Note:
        This class is meant for private use.

    """
    def __new__(cls, *p, **k):
        # There can be only one (singleton)
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = dict.__new__(cls)
        return cls._the_instance

    def __setitem__(self, name, value):
        if not isinstance(value, _BaseWeaponOrder):
            raise WeaponOrderError('Only instances of _BaseWeaponOrder are' +
                                   'allowed to be set in the dictionary.')

        return super(_WeaponOrderStorage, self).__setitem__(name, value)

    def add(self, path_to_order):
        """Adds a path instance to the dictionary, setting the namebase as the
        key, and the value as either a WeaponOrderTXT or WeaponOrderINI class
        instance based on the extension of the file.

        """
        # Make sure we were given a path instance
        if not isinstance(path_to_order, path):
            path_to_order = path(path_to_order)

        name = path_to_order.namebase
        extension = path_to_order.ext

        # Check for valid extension
        if extension == '.txt':
            self[name] = WeaponOrderTXT(path_to_order)
        elif extension == '.ini':
            self[name] = WeaponOrderINI(path_to_order)
        else:
            raise WeaponOrderError('Invalid extension "%s" for ' % extension +
                                   'weapon order file. Must be ".txt" or' +
                                   '".ini".')


weaponOrderStorage = _WeaponOrderStorage()


class _WeaponOrderEntry(object):
    def __init__(self, weapon, kills):
        self._kills = kills
        self._weapon = weapon

    @property
    def kills(self):
        override = int(gg_multikill_override)
        if self.weapon not in ['knife', 'hegrenade'] and override:
            return override
        return self._kills

    @property
    def weapon(self):
        return self._weapon


class WeaponOrderManager(object):
    def __new__(cls):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance._active = None
        return cls._the_instance

    @property
    def active(self):
        return self._active

    def activate(self, name):
        """Would this not be triggered by gg_weapon_order_file?"""
        # Does the weapon order exist?
        if not name in weaponOrderStorage:
            raise WeaponOrderError('The specified weapon order "%s" ' % name +
                                   'does not exist.')

        # Do we have an active weapon order yet? If so, check the name.
        if self._active:
            # Do not set to the same name if it already exists
            if self.active.name == name:
                return

        # Activate the weapon order
        self._active = weaponOrderStorage[name]

        # Set the sort type
        self.active._set_active_order_type()

        # Restart the game
        self.restart_game()

    def load_orders(self):
        es.dbgmsg(0, langstring("Load_WeaponOrders"))
        # Register for the server_cvar event
        es.addons.registerForEvent(self, 'server_cvar', self.server_cvar)
        for orderPath in weaponOrderFilesTXT:  # + weaponOrderFilesINI
            weaponOrderStorage.add(orderPath)

    def server_cvar(self, event_var):
        # Retrieve the values
        cvarname = event_var['cvarname']
        cvarvalue = event_var['cvarvalue']

        # Make sure the cvarvalue is not 0
        if cvarvalue == '0':
            return

        # gg_weapon_order_file
        if cvarname == 'gg_weapon_order_file':
            # Activate the new weapon order
            self.activate(cvarvalue)
            return

        # gg_weapon_order_sort_type
        if cvarname == 'gg_weapon_order_sort_type':
            # Must be default or random
            if not cvarvalue in ('#default', '#random'):
                return

            # Make sure we have a weapon order
            if self.active:
                # If the values are set, do not allow them to be set again
                if cvarvalue == '#default':
                    if self.active.default == self.active.active:
                        return

                elif cvarvalue == '#random':
                    if self.active.random == self.active.active:
                        return

                # Set the sort type in the _BaseWeaponOrder.active
                self.active._set_active_order_type()

                # Restart the game
                self.restart_game()

    def restart_game(self):
        self.active.echo()
        es.msg(langstring('WeaponOrder:ChangedTo', {'to': self.active.title}))
        es.ServerCommand('mp_restartgame 2')

    def unregister(self):
        # Unregister the server_cvar event
        es.addons.unregisterForEvent(self, 'server_cvar')


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def refresh_weapon_order_files():
    """Function that retrieves a new list of weapon order files found in the
    GunGame cfg/weapon_orders directory.

    Notes:
        * Should be used sparingly as we do not want to read from the disk
          often.
        * GunGame retrieves the list of weapon orders when it first loads.

    """
    global weaponOrderFilesTXT  # , weaponOrderFilesINI
    weaponOrderFilesTXT = weaponOrdersPath.files("*.txt")
    #weaponOrderFilesINI = weaponOrdersPath.files("*.ini")

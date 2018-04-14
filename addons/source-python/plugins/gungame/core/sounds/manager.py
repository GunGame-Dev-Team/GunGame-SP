# ../gungame/core/sounds/manager.py

"""Provides sound management capabilities."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from random import shuffle
from warnings import warn

# Site-Package
from configobj import ConfigObj

# Source.Python
from engines.sound import Sound
from filesystem import is_vpk_file
from paths import SOUND_PATH

# GunGame
from ..config.misc import sound_pack
from ..paths import GUNGAME_SOUND_PACK_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'RandomSounds',
    '_SoundManager',
    'sound_manager',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class RandomSounds(list):
    """Class used to shuffle through random sounds."""

    def __init__(self, *values):
        """Store all of the sounds in the list."""
        super().__init__(Sound(x, download=True) for x in values)
        self._current = None
        self._remaining = list()

    def next(self):
        """Return the next sound in the list.

        :rtype: Sound
        """
        if not self._remaining:
            self._remaining.extend(self)
            shuffle(self._remaining)
        self._current = self._remaining.pop(0)
        return self._current


class _SoundManager(defaultdict):
    """Class used to play sounds."""

    def __init__(self, default_factory):
        """Store all default core sounds."""
        super().__init__(default_factory)
        self.defaults = dict()
        self._sound_hooks = defaultdict(list)

    def load_sounds(self):
        """Load all sounds into the dictionary."""
        # Loop through all sound packs
        for file in GUNGAME_SOUND_PACK_PATH.files('*.ini'):

            # Get the sound pack data
            ini = ConfigObj(file)

            # Loop through all sound types in the current sound pack
            for item, value in ini.items():

                # Is the current sound a valid sound type?
                if item not in self.defaults:
                    warn(
                        f'Sound "{item}" in file "{file.name}" is not '
                        f'registered.'
                    )
                    continue

                # Get the extension type of the current sound type value
                extension = value.rsplit('.', 1)[1]

                # Is the value for a random sound file?
                if extension == 'txt':

                    # Does the random sound file exist?
                    txt = GUNGAME_SOUND_PACK_PATH / 'random_sounds' / value
                    if not txt.isfile():
                        warn(
                            'Invalid random sound text file given '
                            f'"{value}" for sound "{item}" in file '
                            f'"{file.name}".'
                        )
                        continue

                    # Open the random sound file
                    sounds = list()
                    with txt.open() as open_file:

                        # Loop through all values in the random sound file
                        for line in open_file.readlines():
                            line = line.strip()

                            # Skip all comments or empty lines
                            if line.startswith('/') or not line:
                                continue

                            # Get the extension of the current sound
                            extension = line.rsplit('.', 1)[1]

                            # Is this a valid extension for the game?
                            if not self.is_allowed_sound_extension(extension):
                                warn(
                                    f'Invalid sound extension "{extension}" '
                                    f'found in random sound file "{txt.name}".'
                                )
                                continue

                            # Does the sound exist?
                            sound_file = SOUND_PATH / line
                            if not (
                                sound_file.isfile() or
                                is_vpk_file(f'sound/{line}')
                            ):
                                warn(
                                    f'Invalid sound "{line}", sound '
                                    'does not exist'
                                )
                                continue

                            # Add the sound to the list
                            sounds.append(line)

                    # Were no valid sounds found?
                    if not sounds:
                        warn(
                            'No sounds found in random sound file '
                            f'"{txt.name}".'
                        )
                        continue

                    # Add the sounds for the sound type
                    self[file.namebase][item] = RandomSounds(*sounds)

                # Is the file extension valid for the game?
                elif self.is_allowed_sound_extension(extension):

                    # Add the sound to the sound type
                    self[file.namebase][item] = Sound(value, download=True)

                # Was an invalid extension given?
                else:
                    warn(
                        f'Invalid sound extension "{extension}" for sound '
                        f'"{item}" in file "{file.name}".'
                    )
                    continue

            # Loop through all known sound types that were
            #   not represented in the current sound pack
            for missing in set(self.defaults).difference(self[file.namebase]):
                warn(
                    f'Sound "{missing}" missing in "{file.namebase}" '
                    'sound pack.'
                )

    @staticmethod
    def is_allowed_sound_extension(extension):
        """Return whether the extension is allowed for the game.

        :param str extension: The file extension to check if valid.
        :rtype: bool
        """
        return extension in ('wav', 'mp3')

    def register_sound(self, sound_name, default):
        """Register the sound and add the default value to the defaults.

        :param str sound_name: The type of sound to register.
        :param str default: The default value for the sound type.
        """
        # Was the sound type already registered?
        if sound_name in self.defaults:
            warn(f'Sound "{sound_name}" already registered!')
            return

        # Was a valid extension type given?
        extension = default.rsplit('.', 1)[1]
        if (
            not self.is_allowed_sound_extension(extension) and
            extension != 'txt'
        ):
            warn(
                f'Invalid extension "{extension}".  Sound "{sound_name}" '
                'not registered.'
            )
            return

        # Register the sound with its default value
        self.defaults[sound_name] = default

    def register_hook(self, sound_name, callback):
        """Register a hook for the given sound name."""
        if (
            sound_name in self._sound_hooks and
            callback is not None and
            callback in self._sound_hooks[sound_name]
        ):
            raise ValueError(
                f'Hook "{callback}" already registered for '
                f'sound name "{sound_name}".'
            )
        self._sound_hooks[sound_name].append(callback)

    def unregister_hook(self, sound_name, callback):
        """Unregister a hook from the given sound name."""
        if sound_name not in self._sound_hooks:
            raise ValueError(
                f'No hooks registered for sound name "{sound_name}".'
            )
        if callback not in self._sound_hooks[sound_name]:
            raise ValueError(
                f'Hook "{callback}" is not registered for '
                f'sound name "{sound_name}".'
            )
        self._sound_hooks[sound_name].remove(callback)
        if not self._sound_hooks[sound_name]:
            del self._sound_hooks[sound_name]

    def get_sound(self, sound_name):
        """Return the sound from the given name.

        :param str sound_name: The type of sound to get the current value of.
        :rtype: Sound
        """
        # Was an invalid sound type given?
        if sound_name not in self.defaults:
            raise ValueError(
                f'Invalid sound name "{sound_name}".  Sound not registered.'
            )

        # Is the sound pack ConVar a valid value?
        pack = sound_pack.get_string()
        if pack not in self:
            raise ValueError(
                f'Invalid sound pack "{sound_pack}".  Change '
                f'"{sound_pack.name}" to a valid sound pack name.'
            )

        if sound_name in self._sound_hooks:
            block_sound = False
            for callback in self._sound_hooks[sound_name]:
                if callback(sound_name) is False:
                    block_sound = True
            if block_sound:
                return

        # Return the sound if its type is in the chosen sound pack
        if sound_name in self[pack]:
            return self._prep_sound(self[pack][sound_name])

        # Return the default sound value
        if sound_name in self['default']:
            return self._prep_sound(self['default'][sound_name])

        # If the sound is not in either the chosen sound
        #   pack or the default one, raise an error
        raise ValueError(
            f'Sound "{sound_name}" cannot be found for sound pack "{pack}".'
        )

    @staticmethod
    def _prep_sound(sound):
        """Return the sound to play.

        :param Sound sound: The :class:`engines.sound.Sound` instance to play.
            Could also be a :class:`RandomSounds` object to get the next
            random :class:`engines.sound.Sound` instance from.
         :rtype: Sound
        """
        # If the sound is random, get the next random value
        if isinstance(sound, RandomSounds):
            return sound.next()

        # Just return the sound
        return sound

    def play_sound(self, sound_name, *users):
        """Play the sound to the given users.

        :param str sound_name: The type of sound to play.
        :rtype: Sound
        """
        sound = self.get_sound(sound_name)
        if sound is None:
            return
        sound.play(*users)
        return sound

    def emit_sound(self, sound_name, index, *users):
        """Emit the sound from the given index and play to the given users.

        :param str sound_name: The type of sound to play.
        :param int index: The index to emit the sound from.
        :rtype: Sound
        """
        sound = self.get_sound(sound_name)
        if sound is None:
            return
        sound.index = index
        sound.play(*users)
        return sound

# Get the _SoundManager instance
sound_manager = _SoundManager(dict)

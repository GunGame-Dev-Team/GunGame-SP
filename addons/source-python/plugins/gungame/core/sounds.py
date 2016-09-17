# ../gungame/core/sounds/manager.py

"""Sound based functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from contextlib import suppress
from importlib import import_module
from random import shuffle
from warnings import warn

# Site-Package
from configobj import ConfigObj

# Source.Python
from engines.sound import Sound
from filesystem import is_vpk_file
from paths import SOUND_PATH
from translations.strings import LangStrings

# GunGame
from .config.misc import sound_pack
from .paths import GUNGAME_SOUND_PACK_PATH
from .plugins.valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_SoundManager',
    'sound_manager',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the core sounds with their defaults
# TODO: create sounds specific to this new version of GunGame
_core_sounds = {
    'count_down': 'hl1/fvox/beep.wav',
    'level_down': 'source-python/gungame/default/smb3_powerdown.mp3',
    'level_up': 'source-python/gungame/default/smb3_powerup.mp3',
    'multi_kill': 'source-python/gungame/default/smb_star.mp3',
    'nade_level': 'source-python/gungame/default/nade_level.mp3',
    'knife_level': 'source-python/gungame/default/knife_level.mp3',
    'welcome': 'source-python/gungame/default/gg5_welcome.mp3',
    'winner': 'winner_sounds.txt',
}

_sound_strings = LangStrings('gungame/core/config/sound_pack')


# =============================================================================
# >> CLASSES
# =============================================================================
class RandomSounds(list):
    """Class used to shuffle through random sounds."""

    def __init__(self, *values):
        """Store all of the sounds in the list."""
        super().__init__(Sound(x) for x in values)
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
        self._defaults = dict()

        # Register all core sounds
        for name, default in _core_sounds.items():
            self.register_sound(name, default)

        # Loop through all plugins
        for plugin_name in valid_plugins.all:
            plugin_type = valid_plugins.get_plugin_type(plugin_name)

            # Register all plugin based sounds
            with suppress(ImportError):
                import_module(
                    'gungame.plugins.{plugin_type}.{plugin_name}.sounds'.format(
                        plugin_type=plugin_type,
                        plugin_name=plugin_name,
                    )
                )

        # Create the default files, if necessary
        self._create_default_sound_pack()
        self._create_winner_sounds()

    def _create_default_sound_pack(self):
        """Create/update the default sound pack."""
        # Retrieve the current default sounds
        file = GUNGAME_SOUND_PACK_PATH / 'default.ini'
        ini = ConfigObj(file)

        # Add all 'new' default sounds to the default config file
        for item, value in sorted(self._defaults.items()):
            if item in ini:
                continue
            ini[item] = value

        # Save the default file
        ini.write()

    @staticmethod
    def _create_winner_sounds():
        """Create the winner sounds random file."""
        # Get the winner_sounds path
        file = GUNGAME_SOUND_PACK_PATH / 'random_sounds' / 'winner_sounds.txt'

        # If the file already exists, no need to create it
        if file.isfile():
            return

        # Create the winner_sounds file
        with file.open('w') as open_file:

            # Add the header
            open_file.write(
                '// {breaker}\n'.format(
                    breaker='-' * 76,
                )
            )
            for line in _sound_strings['Random'].get_string().splitlines():
                open_file.write(
                    '// {line}\n'.format(
                        line=line,
                    )
                )
            open_file.write(
                '// {breaker}\n\n\n'.format(
                    breaker='-' * 76,
                )
            )

            # Add in the default winner sounds
            for name in ('14', '15', '23_SuitSong3', '31'):
                open_file.write(
                    'music/HL2_song{name}.mp3\n'.format(
                        name=name,
                    )
                )

    def load_sounds(self):
        """Load all sounds into the dictionary."""
        # Loop through all sound packs
        for file in GUNGAME_SOUND_PACK_PATH.files('*.ini'):

            # Get the sound pack data
            ini = ConfigObj(file)

            # Loop through all sound types in the current sound pack
            for item, value in ini.items():

                # Is the current sound a valid sound type?
                if item not in self._defaults:
                    warn(
                        'Sound "{sound}" in file "{file_name}" is not registered.'.format(
                            sound=item,
                            file_name=file.name,
                        )
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
                            '"{text_file}" for sound "{sound}" in file '
                            '"{file_name}".'.format(
                                text_file=value,
                                sound=item,
                                file_name=file.name,
                            )
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
                                    'Invalid sound extension "{extension}" '
                                    'found in random sound file '
                                    '"{sound_file}".'.format(
                                        extension=extension,
                                        sound_file=txt.name,
                                    )
                                )
                                continue

                            # Does the sound exist?
                            if not (
                                SOUND_PATH.joinpath(line).isfile() or
                                is_vpk_file('sound/{path}'.format(path=line))
                            ):
                                warn(
                                    'Invalid sound "{sound}", sound '
                                    'does not exist'.format(
                                        sound=line,
                                    )
                                )
                                continue

                            # Add the sound to the list
                            sounds.append(line)

                    # Were no valid sounds found?
                    if not sounds:
                        warn(
                            'No sounds found in random sound file '
                            '"{text_file}".'.format(
                                text_file=txt.name,
                            )
                        )
                        continue

                    # Add the sounds for the sound type
                    self[file.namebase][item] = RandomSounds(*sounds)

                # Is the file extension valid for the game?
                elif self.is_allowed_sound_extension(extension):

                    # Add the sound to the sound type
                    self[file.namebase][item] = Sound(value)

                # Was an invalid extension given?
                else:
                    warn(
                        'Invalid sound extension "{extension}" for sound '
                        '"{sound}" in file "{file_name}".'.format(
                            extension=extension,
                            sound=item,
                            file_name=file.name,
                        )
                    )
                    continue

            # Loop through all known sound types that were
            #   not represented in the current sound pack
            for missing in set(self._defaults).difference(self[file.namebase]):
                warn(
                    'Sound "{sound}" missing in "{sound_pack}" '
                    'sound pack.'.format(
                        sound=missing,
                        sound_pack=file.namebase,
                    )
                )

    @staticmethod
    def is_allowed_sound_extension(extension):
        """Return whether the extension is allowed for the game.

        :param str extension: The file extension to check if valid.
        :rtype: bool
        """
        return extension in ('wav', 'mp3')

    def register_sound(self, sound_name, value):
        """Register the sound and add the default value to the defaults.

        :param str sound_name: The type of sound to register.
        :param str value: The default value for the sound type.
        """
        # Was the sound type already registered?
        if sound_name in self._defaults:
            warn(
                'Sound "{sound}" already registered!'.format(
                    sound=sound_name,
                )
            )
            return

        # Was a valid extension type given?
        extension = value.rsplit('.', 1)[1]
        if not self.is_allowed_sound_extension(
                extension) and extension != 'txt':
            warn(
                'Invalid extension "{extension}".  Sound "{sound}" '
                'not registered.'.format(
                    extension=extension,
                    sound=sound_name,
                )
            )
            return

        # Register the sound with its default value
        self._defaults[sound_name] = value

    def get_sound(self, sound_name):
        """Return the sound from the given name.

        :param str sound_name: The type of sound to get the current value of.
        :rtype: Sound
        """
        # Was an invalid sound type given?
        if sound_name not in self._defaults:
            raise ValueError(
                'Invalid sound name "{sound}".  Sound not registered.'.format(
                    sound=sound_name,
                )
            )

        # Is the sound pack ConVar a valid value?
        pack = sound_pack.get_string()
        if pack not in self:
            raise ValueError(
                'Invalid sound pack "{sound_pack}".  Change "{cvarname}" '
                'to a valid sound pack name.'.format(
                    sound_pack=pack,
                    cvarname=sound_pack.name,
                )
            )

        # Return the sound if its type is in the chosen sound pack
        if sound_name in self[pack]:
            return self._prep_sound(self[pack][sound_name])

        # Return the default sound value
        if sound_name in self['default']:
            return self._prep_sound(self['default'][sound_name])

        # If the sound is not in either the chosen sound
        #   pack or the default one, raise an error
        raise ValueError(
            'Sound "{sound}" cannot be found for sound pack '
            '"{sound_pack}".'.format(
                sound=sound_name,
                sound_pack=pack,
            )
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
        sound.play(*users)
        return sound

    def emit_sound(self, sound_name, index, *users):
        """Emit the sound from the given index and play to the given users.

        :param str sound_name: The type of sound to play.
        :param int index: The index to emit the sound from.
        :rtype: Sound
        """
        sound = self.get_sound(sound_name)
        sound.index = index
        sound.play(*users)
        return sound

# Get the _SoundManager instance
sound_manager = _SoundManager(dict)

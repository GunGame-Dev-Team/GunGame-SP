# ../gungame/core/sounds/__init__.py

"""Sound based functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module
import sys
from warnings import warn

# Site-Package
from configobj import ConfigObj

# Source.Python
from translations.strings import LangStrings

# GunGame
from .manager import sound_manager
from ..paths import GUNGAME_SOUND_PACK_PATH
from ..plugins.valid import valid_plugins


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store the core sounds with their defaults
# TODO: create sounds specific to this new version of GunGame
_core_sounds = {
    'welcome': 'source-python/gungame/default/gg5_welcome.mp3',
    'multi_kill': 'common/stuck1.wav',
    'level_down': 'source-python/gungame/default/smb3_powerdown.mp3',
    'level_up': 'source-python/gungame/default/smb3_powerup.mp3',
    'nade_level': 'source-python/gungame/default/nade_level.mp3',
    'knife_level': 'source-python/gungame/default/knife_level.mp3',
    'count_down': 'hl1/fvox/beep.wav',
    'winner': 'winner_sounds.txt',
}

_sound_strings = LangStrings('gungame/config/sound_pack')


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def register_all_sounds():
    """Register all sounds."""
    # Register all core sounds
    for name, default in _core_sounds.items():
        sound_manager.register_sound(
            sound_name=name,
            default=default,
        )

    # Loop through all plugins
    for plugin_name in valid_plugins.all:
        plugin_path = valid_plugins.get_plugin_path(plugin_name)
        plugin_type = str(plugin_path.parent.stem)
        sound_path = plugin_path / 'sounds.py'
        if not sound_path.is_file():
            continue

        try:
            import_module(
                f'gungame.plugins.{plugin_type}.{plugin_name}.sounds'
            )
        # pylint: disable=broad-except
        except Exception:
            warn(
                f'Unable to import sounds for {plugin_name} due to error:'
                f'\n\n\t{sys.exc_info()[1]}'
            )

    # Create the default files, if necessary
    _create_default_sound_pack()
    _create_default_winner_sounds()

    # Load the sounds in the Sound Manager
    sound_manager.load_sounds()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _create_default_sound_pack():
    """Create/update the default sound pack."""
    # Retrieve the current default sounds
    file = GUNGAME_SOUND_PACK_PATH / 'default.ini'
    ini = ConfigObj(file)

    # Add all 'new' default sounds to the default config file
    for item, value in sorted(sound_manager.defaults.items()):
        if item in ini:
            continue
        ini[item] = value

    # Save the default file
    ini.write()


def _create_default_winner_sounds():
    """Create the winner sounds random file."""
    # Get the winner_sounds path
    file = GUNGAME_SOUND_PACK_PATH / 'random_sounds' / 'winner_sounds.txt'

    # If the file already exists, no need to create it
    if file.is_file():
        return

    # Create the winner_sounds file
    with file.open('w') as open_file:

        # Add the header
        breaker = '-' * 76
        open_file.write(f'// {breaker}\n')
        for line in _sound_strings['Random'].get_string().splitlines():
            open_file.write(f'// {line}\n')
        open_file.write(f'// {breaker}\n\n\n')

        # Add in the default winner sounds
        for name in ('14', '15', '23_SuitSong3', '31'):
            open_file.write(f'music/HL2_song{name}.mp3\n')

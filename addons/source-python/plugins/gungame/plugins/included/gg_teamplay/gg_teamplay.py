# ../gungame/plugins/included/gg_teamplay/gg_teamplay.py

"""Plugin that levels players up as a team."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import sys
from importlib import import_module

# Source.Python
from core import GAME_NAME, AutoUnload, WeakAutoUnload
from events import Event
from events.hooks import EventAction, PreEvent
from hooks.exceptions import except_hooks
from listeners.tick import Delay

# GunGame
from gungame.core.messages.hooks import MessagePrefixHook
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.sounds.hooks import SoundHook
from gungame.core.teams import team_levels
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def unload():
    """Clear the team level dictionary."""
    team_levels.clear()


# =============================================================================
# >> CLASSES
# =============================================================================
class _TeamplayManager:
    """Class used to load the proper teamplay gamemode."""

    finished_initial_load = False
    current_module = None

    def initialize(self):
        """Load the proper teamplay gamemode."""
        self.load_module()
        self.finished_initial_load = True

    def load_module(self, module=None):
        """Load the given gamemode."""
        if self.current_module is not None:
            msg = "A module is currently loaded, cannot load another."
            raise ValueError(msg)
        if module is None:
            module = (
                "deathmatch" if "gg_deathmatch" in gg_plugin_manager
                else "rounds"
            )
        module_path = f"gungame.plugins.included.gg_teamplay.{module}"
        import_module(module_path)
        self.current_module = module_path

    def unload_current_module(self):
        """Unload the current gamemode."""
        if self.current_module is None:
            msg = "No module is currently loaded."
            raise ValueError(msg)

        del sys.modules[self.current_module]

        # ruff: noqa: SLF001
        if self.current_module in AutoUnload._module_instances:
            self._unload_auto_unload_instances(
                AutoUnload._module_instances[self.current_module],
            )
            del AutoUnload._module_instances[self.current_module]

        if self.current_module in WeakAutoUnload._module_instances:
            self._unload_auto_unload_instances(
                WeakAutoUnload._module_instances[self.current_module],
            )
            del WeakAutoUnload._module_instances[self.current_module]

        self.current_module = None

    @staticmethod
    def _unload_auto_unload_instances(instances):
        for instance in instances:
            try:
                # ruff: noqa: SLF001
                instance._unload_instance()
            # ruff: noqa: BLE001
            except Exception:
                except_hooks.print_exception()


teamplay_manager = _TeamplayManager()
Delay(
    delay=0,
    callback=teamplay_manager.initialize,
)


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event("gg_plugin_loaded", "gg_plugin_unloaded")
def _swap_style(game_event):
    if game_event["plugin"] != "gg_deathmatch":
        return

    if not teamplay_manager.finished_initial_load:
        return

    teamplay_manager.unload_current_module()
    module = (
        "deathmatch" if game_event.name == "gg_plugin_loaded" else "rounds"
    )
    teamplay_manager.load_module(module)
    weapon_order_manager.restart_game()


# =============================================================================
# >> EVENT HOOKS
# =============================================================================
@PreEvent("gg_level_up", "gg_win")
def _block_level_up(game_event):
    return EventAction.BLOCK


# =============================================================================
# >> MESSAGE HOOKS
# =============================================================================
@MessagePrefixHook("LevelInfo:")
def _level_info_hook(message_name, message_prefix):
    """Hooks the LevelInfo messages so that the team messages can be sent."""
    return False


# =============================================================================
# >> SOUND HOOKS
# =============================================================================
@SoundHook("multi_kill")
def _suppress_multi_kill_sound(sound_name):
    """Stop the multi-kill sound from spamming."""
    return False

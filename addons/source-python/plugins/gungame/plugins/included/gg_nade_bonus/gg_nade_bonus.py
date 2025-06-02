# ../gungame/plugins/included/gg_nade_bonus/gg_nade_bonus.py

"""Plugin to give extra weapons to players on nade levels."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from listeners import OnLevelInit
from listeners.tick import Delay
from weapons.manager import weapon_manager
from gungame.core.weapons.groups import all_grenade_weapons

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .configuration import bonus_weapon


# =============================================================================
# >> CLASSES
# =============================================================================
class _NadeBonus:
    """Dictionary that holds players with their bonus weapons."""

    def __init__(self):
        """Store the nade bonus weapon."""
        super().__init__()
        self._weapon = self.get_weapon()

    @property
    def weapon(self):
        """Return the bonus weapon."""
        return self._weapon

    @staticmethod
    def get_weapon():
        """Return the validated bonus weapon."""
        weapon = str(bonus_weapon)
        if weapon not in weapon_manager:
            msg = f"Invalid weapon name given for {bonus_weapon.name}: {weapon}"
            raise ValueError(msg)
        return weapon

    def check_on_spawn(self, userid):
        player = player_dictionary[userid]
        if player.level_weapon in all_grenade_weapons:
            self.give_current_weapon(player)

    def check_turbo(self, userid):
        """Verify turbo is running and give the player the bonus weapon now."""
        if "gg_turbo" in gg_plugin_manager:
            self.check_on_spawn(userid)

    def give_current_weapon(self, player):
        """Give the player their nade bonus weapon."""
        Delay(
            delay=0.4 if player.is_fake_client() else 0.1,
            callback=self._give_weapon,
            args=(player,),
            cancel_on_level_end=True,
        )

    def _give_weapon(self, player):
        """Give the player their weapon."""
        player.give_named_item(weapon_manager[self.weapon].name)

nade_bonus = _NadeBonus()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_spawn")
def _give_current_weapon(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    nade_bonus.check_on_spawn(game_event["userid"])


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event("gg_level_up", "gg_level_down")
def _check_level(game_event):
    nade_bonus.check_turbo(game_event["leveler"])


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelInit
def _level_init(map_name):
    nade_bonus.get_weapon()

# ../gungame/core/menus/level.py

"""Level menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import SimpleMenu, SimpleOption, Text
from players.helpers import userid_from_index

# GunGame
from ..leaders import leader_manager
from . import menu_strings
from ..players.dictionary import player_dictionary
from ..plugins.manager import gg_plugin_manager
from ..status import GunGameMatchStatus, GunGameStatus


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'send_level_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_level_menu(index):
    """Send the level menu to the player."""
    menu = SimpleMenu()
    player = player_dictionary[userid_from_index(index)]
    menu.append(
        SimpleOption(
            1,
            menu_strings['Level:Title'],
            selectable=False,
        )
    )
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings['Inactive'])
    elif gg_plugin_manager.is_team_game:
        # TODO: Implement team menus once teamplay/teamwork are implemented
        menu.clear()
        menu.append(menu_strings['Level:Team'])
    elif player.team < 2:
        menu.append(Text(menu_strings['Level:Inactive']))
    else:
        menu.append(
            Text(
                menu_strings['Level:Current'].get_string(
                    player.language,
                    level=player.level,
                )
            )
        )
        menu.append(
            Text(
                menu_strings['Level:Weapon'].get_string(
                    player.language,
                    kills=player.level_multi_kill - player.multi_kill,
                    weapon=player.level_weapon,
                )
            )
        )
        leaders = leader_manager.current_leaders
        if leaders is None:
            menu.append(Text(menu_strings['Leader:None']))
        elif player.userid not in leaders:
            menu.append(
                Text(
                    menu_strings['Level:Trailing'].get_string(
                        player.language,
                        levels=leader_manager.leader_level - player.level,
                    )
                )
            )
        elif len(leaders) > 1:
            menu.append(Text(menu_strings['Level:Tied']))
        else:
            menu.append(Text(menu_strings['Level:Leading']))
        menu.append(
            SimpleOption(
                2,
                menu_strings['Level:Wins-Title'],
                selectable=False,
            )
        )
        menu.append(
            Text(
                menu_strings['Level:Wins'].get_string(
                    player.language,
                    wins=player.wins,
                )
            )
        )
    menu.send(index)

# ../gungame/core/menus/leaders.py

"""Leader menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu
from players.entity import Player

# GunGame
from . import menu_strings
from ._options import StarOption
from ..commands.registration import register_command_callback
from ..leaders import leader_manager
from ..players.dictionary import player_dictionary
from ..plugins.manager import gg_plugin_manager
from ..status import GunGameMatchStatus, GunGameStatus
from ..teams import team_levels, team_names
from ..weapons.manager import weapon_order_manager

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "send_leaders_menu",
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
# ruff: noqa: PLR2004
@register_command_callback("leaders", "Leader:Text")
def send_leaders_menu(index):
    """Send the leaders menu to the player."""
    menu = PagedMenu(title=menu_strings["Leader:Current"])
    language = Player(index).language
    if GunGameStatus.MATCH is GunGameMatchStatus.WARMUP:
        menu.append(menu_strings["Warmup"])
    elif GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings["Inactive"])
    elif gg_plugin_manager.is_team_game:
        menu.append(menu_strings["Leader:Team"])
        leader_level = max(team_levels.values())
        teams = [
            team_names[num] for num, level in team_levels.items()
            if level == leader_level
        ]
        weapon = weapon_order_manager.active[leader_level].weapon

        if len(teams) == len(team_levels):
            if len(teams) > 2:
                message = menu_strings["Leader:Team:All"].get_string(
                    language=language,
                    level=leader_level,
                    weapon=weapon,
                )
            else:
                message = menu_strings["Leader:Team:Tied"].get_string(
                    language=language,
                    level=leader_level,
                    weapon=weapon,
                )
        elif len(teams) > 1:
            message = menu_strings["Leader:Team:Multiple"].get_string(
                language=language,
                level=leader_level,
                weapon=weapon,
            )
            message += f'\n\t* {", ".join(teams)}'
        else:
            message = menu_strings["Leader:Team:Current"].get_string(
                language=language,
                team=teams[0],
                level=leader_level,
                weapon=weapon,
            )
        menu.append(StarOption(message))
    elif leader_manager.current_leaders is None:
        menu.append(menu_strings["Leader:None"])
    else:
        level = leader_manager.leader_level
        menu.description = menu_strings["Leader:Level"].get_string(
            language=language,
            level=level,
            weapon=weapon_order_manager.active[level].weapon,
        )
        for userid in leader_manager.current_leaders:
            menu.append(StarOption(player_dictionary[userid].name))
    menu.send(index)

# ../gungame/core/teams.py

"""Provides team data."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from filters.entities import EntityIter
from listeners.tick import Delay
from players.teams import team_managers, teams_by_number


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'team_levels',
    'team_names',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _TeamLevels(dict):
    def clear(self, value=0):
        for x in self:
            self[x] = value


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
team_names = dict()
team_levels = _TeamLevels()


def _retrieve_team_data():
    for _class_name in team_managers:
        for _entity in EntityIter(_class_name):
            if teams_by_number.get(_entity.team, 'un') in ('un', 'spec'):
                continue
            team_names[_entity.team] = _entity.team_name
            team_levels[_entity.team] = 0

_retrieve_team_data()
if not team_names:
    Delay(0, _retrieve_team_data)

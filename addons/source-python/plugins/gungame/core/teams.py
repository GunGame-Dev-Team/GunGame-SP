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
        for team in self:
            self[team] = value

    def retrieve_team_data(self):
        """Get the team names."""
        for class_name in team_managers:
            for entity in EntityIter(class_name):
                if teams_by_number.get(entity.team, 'un') in ('un', 'spec'):
                    continue
                team_names[entity.team] = entity.team_name
                self[entity.team] = 0


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
team_names = {}
team_levels = _TeamLevels()
team_levels.retrieve_team_data()
if not team_names:
    Delay(
        delay=0,
        callback=team_levels.retrieve_team_data,
    )

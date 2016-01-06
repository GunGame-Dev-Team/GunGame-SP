# ../gungame/plugins/included/gg_dissolver/configuration.py

"""Creates the gg_disable_objectives configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Entities
from entities.constants import DissolveType
#   Translations
from translations.strings import LangStrings

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager

# Plugin Imports
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('dissolver_type',
           'magnitude',
           )


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('type') as dissolver_type:

        for _name in DissolveType.__members__:

            dissolver_type.Options.append('{0} = {1}'.format(
                getattr(DissolveType, _name).real, _name))

        _num_dissolve_types = len(DissolveType)

        dissolver_type.add_text(
            random=_num_dissolve_types, remove=_num_dissolve_types + 1)

    with _config.cvar('magnitude', 2) as magnitude:
        magnitude.add_text()

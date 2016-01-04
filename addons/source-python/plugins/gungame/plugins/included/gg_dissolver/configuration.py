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
# >> GLOBAL VARIABLES
# =============================================================================
_config_strings = LangStrings('gungame/included_plugins/config/gg_dissolver')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('type', 0, _config_strings['Type']) as dissolver_type:

        for _name in DissolveType.__members__:

            dissolver_type.Options.append('{0} = {1}'.format(
                getattr(DissolveType, _name).real, _name))

        _num_dissolve_types = len(DissolveType)

        dissolver_type.Options.append('{0} = {1}'.format(
            _num_dissolve_types, _config_strings['Random'].get_string()))

        dissolver_type.Options.append('{0} = {1}'.format(
            _num_dissolve_types + 1, _config_strings['Remove'].get_string()))

    with _config.cvar(
            'magnitude', 2, _config_strings['Magnitude']) as magnitude:
        pass

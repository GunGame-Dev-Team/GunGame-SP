# ../gungame/core/plugins/errors.py

"""Provides plugin exception classes."""


# =============================================================================
# >> CLASSES
# =============================================================================
class GGPluginFileNotFoundError(Exception):

    """Main plugin file not found."""


class GGPluginDescriptionMissingError(Exception):

    """Plugin description is missing."""


class GGPluginInfoMissingError(Exception):

    """Plugin info is missing."""

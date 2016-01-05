# ../gungame/core/menus/_options.py

"""Provides menu option types for GunGame."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Menus
from menus import PagedOption
from menus.base import _translate_text
from menus.radio import PagedRadioOption


# =============================================================================
# >> CLASSES
# =============================================================================
class ListOption(PagedOption):
    """Class used to list options in incrementing order.

    Normally each page in a PagedMenu starts back at 1, but this class
        makes sure the count continues to increment each page.
    """

    def __init__(
            self, choice_index, text, value=None,
            highlight=True, selectable=False):
        """Store the choice_index which is the number to use in the list."""
        super().__init__(text, value, highlight, selectable)
        self.choice_index = choice_index

    def _get_highlight_prefix(self):
        """Return highlighted prefex if needed."""
        return '->' if isinstance(
            self, PagedRadioOption) and self.highlight else ''

    def _render(self, player_index, choice_index=None):
        """Return the rendered string for the option."""
        return '{0}{1}. {2}\n'.format(
            self._get_highlight_prefix(),
            self.choice_index,
            _translate_text(self.text, player_index))


class StarOption(PagedOption):
    """Class used to list options without numbers.

    Normally each page in a PagedMenu lists options with a corresponding
        number.  This class lists them with a simple * instead.
    """

    def _render(self, player_index, choice_index=None):
        """Return the rendered string for the option."""
        return '* {0}\n'.format(_translate_text(self.text, player_index))

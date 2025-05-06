# ../gungame/core/rules/instance.py

"""Provides a class to create rules for sub-plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from . import all_gungame_rules
from .strings import rules_translations

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "GunGameRules",
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameRules(dict):
    """Class used to store rules."""

    def __init__(self, plugin_name):
        """Create the rules."""
        if plugin_name in all_gungame_rules:
            msg = f'Plugin "{plugin_name}" already registered with rules.'
            raise ValueError(msg)
        super().__init__()
        self.convar_tokens = {}
        self.title = plugin_name
        all_gungame_rules[plugin_name] = self

    def register_rule(self, name, value):
        """Register the given rule."""
        if name in self:
            msg = f'Rule "{name}" already registered.'
            raise ValueError(msg)
        self[name] = value

    def unregister_rule(self, name):
        """Unregister the given rule."""
        if name not in self:
            msg = f'Rule "{name}" is not registered.'
            raise ValueError(msg)
        del self[name]

    def register_all_rules(self):
        """Register all rules from the translation file."""
        for key, value in rules_translations.items():
            if key.startswith(f"{self.title}:"):
                self.register_rule(
                    name=key,
                    value=value,
                )

    def register_convar_token(self, token_name, convar, convar_type="int"):
        """Register the given ConVar token."""
        if token_name in self.convar_tokens:
            msg = f'Token name "{token_name}" already registered.'
            raise ValueError(msg)
        self.convar_tokens[token_name] = {
            "convar": convar,
            "type": convar_type,
        }

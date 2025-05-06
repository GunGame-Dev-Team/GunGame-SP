# ../gungame/core/config/__init__.py

"""GunGame configuration functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import sys
from importlib import import_module
from textwrap import TextWrapper
from warnings import warn

# Source.Python
from engines.server import queue_command_string
from translations.strings import LangStrings

# Site-package
from path import Path

# GunGame
from .. import gg_core_logger
from ..paths import GUNGAME_CFG_PATH
from ..plugins.valid import valid_plugins

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "gg_config_logger",
    "load_all_configs",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_config_logger = gg_core_logger.config


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def load_all_configs():
    """Load all GunGame configs."""
    for file in Path(__file__).parent.files("*.py"):
        if file.stem == "__init__":
            continue
        import_module(f"gungame.core.config.{file.stem}")
    for plugin_name in valid_plugins.all:
        plugin_path = valid_plugins.get_plugin_path(plugin_name)
        plugin_type = str(plugin_path.parent.stem)
        config_path = plugin_path / "configuration.py"
        if not config_path.is_file():
            continue

        try:
            import_module(
                f"gungame.plugins.{plugin_type}.{plugin_name}.configuration",
            )
        # ruff: noqa: BLE001
        except Exception:
            warn(
                f"Unable to import configuration for {plugin_name} due to "
                f"error:\n\n\t{sys.exc_info()[1]}",
                stacklevel=2,
            )

    always_loaded = GUNGAME_CFG_PATH / "gg_plugins.cfg"
    contents = []
    if always_loaded.is_file():
        with always_loaded.open() as open_file:
            contents = open_file.read()
        contents = [
            line for line in contents.splitlines()
            if line and not line.startswith("// ")
        ]
    strings = LangStrings("gungame/plugins")
    with always_loaded.open("w") as open_file:
        wrapper = TextWrapper(
            width=79,
            initial_indent="// ",
            subsequent_indent="// ",
        )
        text = strings["Plugins:Loaded:Always"].get_string(
            plugins=", ".join(sorted(valid_plugins.all)),
        )
        for line in text.splitlines(keepends=True):
            if line == "\n":
                open_file.write(line)
                continue
            for output in wrapper.wrap(line):
                open_file.write(output + "\n")
        for line in contents:
            open_file.write(line + "\n")

    exec_path = always_loaded.replace(
        always_loaded.parent.parent.parent, "",
    )[1:~3].replace("\\", "/")
    queue_command_string(f"exec {exec_path}")

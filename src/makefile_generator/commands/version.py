from makefile_generator import __build__, __version__, __platform__
from makefile_generator.cli_helpers.help_text import show_text

VERSION_TEXT = f'mkgen version {__version__}.{__platform__}.{__build__}'

def mkgen_version(args) -> None:
    show_text(VERSION_TEXT)
    
from makefile_generator import __build__, __platform__, __version__
from makefile_generator.utils.display_utils import show_text_and_exit

VERSION_TEXT = f'mkgen version {__version__}.{__platform__}.{__build__}'

def show_mkgen_version(args) -> None:
    show_text_and_exit(VERSION_TEXT)
    
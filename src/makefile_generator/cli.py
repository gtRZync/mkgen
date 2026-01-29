# !/usr/bin/env python3
import argparse
import sys
from typing import NoReturn

from rich.align import Align
from rich.console import Console
from rich.text import Text

from makefile_generator.cli_helpers.parser import normalize_target_system, parse_args

ASCII_HEADER = '''
███╗   ███╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
████╗ ████║██║ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██╔████╔██║█████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║╚██╔╝██║██╔═██╗ ██║   ██║██╔══╝  ██║╚██╗██║
██║ ╚═╝ ██║██║  ██╗╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
'''

def gradient_text(text, colors):
    gradient = Text()
    for i, char in enumerate(text):
        gradient.append(char, style=f"bold {colors[i % len(colors)]}")
    return gradient

def show_ascii_art(show: bool, stream: Console):
    if not show:
        return
    colors = ["red", "orange1", "yellow", "green", "cyan", "blue", "magenta"]
    stream.print(Align.center(gradient_text(ASCII_HEADER, colors)))

def handle_no_command(args: argparse.Namespace) -> None | NoReturn:
    if not args.command:
        from makefile_generator.cli_helpers.help_text import TOP_LEVEL_HELP_TEXT
        from makefile_generator.commands.version import mkgen_version
        from makefile_generator.utils.display_utils import show_text
        if args.version:
            mkgen_version(args)
        if args.help:
            show_text(TOP_LEVEL_HELP_TEXT)
        show_text(TOP_LEVEL_HELP_TEXT, file=sys.stderr, code=1)


def main() -> None:
    console = Console()
    args = parse_args()
    args = normalize_target_system(args)

    handle_no_command(args)

    show_ascii_art(
        show=args.command != 'version',
        stream=console
    )

    args.func(args)

if __name__ == '__main__':
    main()

# !/usr/bin/env python3
import signal
import sys
import time

from rich.align import Align
from rich.console import Console
from rich.text import Text

from makefile_generator.cli_helpers.help_text import (
    REQUIRE_MUTUALLY_EXCLUSIVE,
    USAGE_TEXT,
    show_help,
)
from makefile_generator.cli_helpers.parser import build_parser

ASCII_HEADER = '''

███╗   ███╗ █████╗ ██╗  ██╗███████╗     ██████╗ ███████╗███╗   ██╗
████╗ ████║██╔══██╗██║ ██╔╝██╔════╝    ██╔════╝ ██╔════╝████╗  ██║
██╔████╔██║███████║█████╔╝ █████╗█████╗██║  ███╗█████╗  ██╔██╗ ██║
██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝╚════╝██║   ██║██╔══╝  ██║╚██╗██║
██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗    ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝

'''

def gradient_text(text, colors):
    gradient = Text()
    for i, char in enumerate(text):
        gradient.append(char, style=f"bold {colors[i % len(colors)]}")
    return gradient

def graceful_exit(signal, frame):
    print('\nExiting...Goodbye')
    sys.exit(0)

def main() -> None:
    colors = ["red", "orange1", "yellow", "green", "cyan", "blue", "magenta"]
    console = Console()

    signal.signal(signal.SIGINT, graceful_exit)
    console.print(Align.center(gradient_text(ASCII_HEADER, colors)))
    welcome_text = Text("Welcome to the C/C++ Makefile Generator CLI!", style="bold cyan")
    console.print(Align.center(welcome_text))
    console.print("\n")
    time.sleep(.5) #show the ascii longer lol
    parser = build_parser()
    args = parser.parse_args()
    #FIXME: fix this if i ever add other commands
    if args.command == 'generate':
        if args.help:
            show_help()
        if not (args.target_system or args.cross_platform):
            show_help(REQUIRE_MUTUALLY_EXCLUSIVE)
    else:
        show_help(USAGE_TEXT)

    args.func(args)

if __name__ == '__main__':
    main()

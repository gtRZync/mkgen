# !/usr/bin/env python3
import signal
import sys
import time

from rich.align import Align
from rich.console import Console
from rich.text import Text

from makefile_generator.cli_helpers.parser import parse_args

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

def main() -> None:
    colors = ["red", "orange1", "yellow", "green", "cyan", "blue", "magenta"]
    console = Console()
    def graceful_exit(signal, frame):
        console.print('\n[bold yellow]Exiting...Goodbye[/]')
        sys.exit(0)

    signal.signal(signal.SIGINT, graceful_exit)
    console.print(Align.center(gradient_text(ASCII_HEADER, colors)))
    welcome_text = Text("Welcome to the C/C++ Makefile Generator CLI!", style="bold cyan")
    console.print(Align.center(welcome_text))
    console.print("\n")
    time.sleep(.5) #show the ascii longer lol
    args = parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

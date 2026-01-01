# !/usr/bin/env python3
import argparse
import signal
import sys
from time import sleep

from makefile_generator.command import generate
from rich.align import Align
from rich.console import Console
from rich.text import Text
from makefile_generator.utils import HELP_TEXT, USAGE_TEXT



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

colors = ["red", "orange1", "yellow", "green", "cyan", "blue", "magenta"]

console_err = Console(stderr=True)

def require_mutually_exclusive(system, cross_platform):
    if not (system or cross_platform):
        error_text = Text()
        error_text.append("Argument Error: ", style="bold red")
        error_text.append("You must provide either --target-system or --cross-platform")
        console_err.print(error_text)
        sys.exit(1)

def graceful_exit(signal, frame):
    print('\nExiting...Goodbye')
    sys.exit(0)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A simple python tool to generate C/C++ makefiles", prog="mkgen", add_help=False)
    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show help'
    )
    subparsers = parser.add_subparsers(dest='command')
    generate_parser = subparsers.add_parser('generate', add_help=False)
    platform = generate_parser.add_mutually_exclusive_group()
    platform.add_argument(
        '--target-system',
        type=str,
        help='Target environnement (e.g : Linux, Windows..etc)'
    )
    platform.add_argument(
        '--cross-platform',
        action='store_true',
        help="Generate a Makefile that works across multiple systems."
    )
    generate_parser.add_argument(
        '-l', '--lang',
        type=str,
        help='The lang in which the makefile should be generated'
    )
    generate_parser.add_argument(
        '-c', '--compiler',
        type=str,
        help='Your compiler'
    )
    generate_parser.add_argument(
        '-std', '--standard',
        type=str,
        help='The compiler standard to be used (if a wrong one is given it defaults to c17 or c++17)'
    )
    generate_parser.add_argument(
        '--use-gui-lib',
        action='store_true',
        help='Wether or not to include gui lib flags and or --cflags'
    )
    generate_parser.add_argument(
        '--binary-name',
        type=str,
        help='Specify the name of the output binary/executable. The generated Makefile will use this name for the compiled program.'
    )
    generate_parser.add_argument(
        '--output-path',
        type=str,
        help='The path where the makefile will be created at (if invalid current directory will be used)'
    )
    generate_parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show help'
    )
    generate_parser.set_defaults(func=generate)
    return parser.parse_args()

def show_help(help_text: str = HELP_TEXT):
    print(help_text)
    sys.exit(0)

def main() -> None:
    signal.signal(signal.SIGINT, graceful_exit)
    console = Console()
    console.print(Align.center(gradient_text(ASCII_HEADER, colors)))
    welcome_text = Text("Welcome to the C/C++ Makefile Generator CLI!", style="bold cyan")
    console.print(Align.center(welcome_text))
    console.print("\n")
    sleep(1) #show the ascii longer lol
    args = parse_args()
    if args.command == 'generate':
        if args.help:
            show_help()
        require_mutually_exclusive(args.target_system, args.cross_platform)
    else:
        show_help(USAGE_TEXT)
            
    args.func(args)

if __name__ == '__main__':
    main()

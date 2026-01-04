import argparse

from .command import generate
from .help_text import MUTUALLY_EXCLUSIVE, USAGE_TEXT, show_help


def _set_default_system() -> str:
    import platform

    if platform.system().lower() == 'darwin':
        return 'mac'
    else:
        return platform.system().lower()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A simple python tool to generate C/C++ makefiles", prog="mkgen", add_help=False)
    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show help'
    )
    subparsers = parser.add_subparsers(dest='command')

    generate_parser = subparsers.add_parser('generate', add_help=False)
    generate_parser.add_argument(
        'target_system',
        nargs='?',
        default=None,
        type=str,
        help='Target environnement (e.g : Linux, Windows..etc), defaults to current system'
    )
    generate_parser.add_argument(
        '--cross-platform',
        action='store_true',
        help="Generate a Makefile that works across multiple systems."
    )
    generate_parser.add_argument(
        '-l', '--lang',
        type=str,
        help='Specify the programming language'
    )
    generate_parser.add_argument(
        '-c', '--compiler',
        type=str,
        help='Specify the compiler to use in the Makefile'
    )
    generate_parser.add_argument(
        '-std', '--standard',
        type=str,
        help='Specify the language standard (e.g., c11, c++17, c++20)'
    )
    generate_parser.add_argument(
        '--use-gui-lib',
        action='store_true',
        help='Wether or not to include gui lib flags and or --cflags'
    )
    generate_parser.add_argument(
        '--binary-name',
        type=str,
        help='Name of the output binary/executable.'
    )
    generate_parser.add_argument(
        '-o', '--output',
        type=str,
        help='The path where the makefile will be created at (if invalid current directory will be used)'
    )
    generate_parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show help'
    )
    generate_parser.set_defaults(func=generate)
    args = parser.parse_args()

    if args.command:
        #FIXME: fix this (if-else) if i ever add other commands
        if args.command == 'generate':
            if args.help:
                show_help()

            if (args.cross_platform and args.target_system is not None):
                show_help(MUTUALLY_EXCLUSIVE)

            if args.cross_platform:
                args.target_system = None
            elif args.target_system is None:
                args.target_system = _set_default_system()
        else:
            show_help(USAGE_TEXT)


    return args

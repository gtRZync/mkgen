import argparse

from makefile_generator.commands import generate, mkgen_version


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
        help='Show this message then exits'
    )
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='Show version'
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

    version_parser = subparsers.add_parser('version')
    version_parser.set_defaults(func=mkgen_version)

    args = parser.parse_args()

    return args

def normalize_target_system(args: argparse.Namespace) -> argparse.Namespace :
    if args.command == "generate":
        if (args.cross_platform and args.target_system is not None):
            import sys
    
            from makefile_generator.cli_helpers.help_text import MUTUALLY_EXCLUSIVE
            from makefile_generator.utils.display_utils import show_text
            show_text(MUTUALLY_EXCLUSIVE, file=sys.stderr)

        if args.cross_platform:
            args.target_system = None
        elif args.target_system is None:
            args.target_system = _set_default_system()

    return args

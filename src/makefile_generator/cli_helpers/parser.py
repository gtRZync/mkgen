import argparse
from .command import generate

def build_parser() -> argparse.ArgumentParser:
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
    return parser
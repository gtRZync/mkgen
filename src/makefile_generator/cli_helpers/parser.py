import argparse

from makefile_generator.cli_helpers.help_text import GENERATE_USAGE_TEXT
from makefile_generator.core import (
    build,
    emit_makefile,
    init,
    mkgen_version,
    regencache,
)

from ._actions import LanguageAction


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

    banner_parser = argparse.ArgumentParser(add_help=False)
    banner_mut = banner_parser.add_mutually_exclusive_group()
    banner_mut.add_argument(
        "--banner",
        action="store_true",
        help="Show ASCII banner"
    )

    banner_mut.add_argument(
        "--no-banner",
        action="store_true",
        help="Disable ASCII banner"
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        '--build-dir',
        required=True,
        help=(
            "Directory where mkgen generates build files (including the Makefile). "
            "The build command will run 'make' inside this directory. "
            "Example: --build-dir build/"
        )
    )

    init_parser = subparsers.add_parser('init', parents=[banner_parser])
    init_parser.add_argument(
        '--root',
        required=True,
        help='project source directory'
    )
    init_parser.set_defaults(func=init)

    regencache_parser = subparsers.add_parser('regencache', parents=[common_parser, banner_parser])
    regencache_parser.set_defaults(func=regencache)

    build_parser = subparsers.add_parser('build', parents=[common_parser, banner_parser])
    build_parser.add_argument(
        '--target',
        default=None,
        help='Makefile recipe to build'
    )
    build_parser.add_argument(
        '--parallel',
        action='store_true',
        help='Indicate whether make should use all available cores or no.'
    )
    build_parser.set_defaults(func=build)


    generate_parser = subparsers.add_parser('generate', parents=[banner_parser], add_help=False, usage=GENERATE_USAGE_TEXT)
    # backend_group = generate_parser.add_mutually_exclusive_group()
    # generate_parser.add_argument(
    #     'target_system',
    #     nargs='?',
    #     default=argparse.SUPPRESS,
    #     type=str,
    #     help='Target environnement (e.g : Linux, Windows..etc), defaults to current system'
    # )
    generate_parser.add_argument(
        '--root',
        required=True,
        type=str,
        help='project source directory'
    )
    generate_parser.add_argument(
        '--cross-platform', '--portable',
        action='store_true',
        help="Generate a Makefile that works across multiple systems."
    )
    # generate_parser.add_argument(
    #     '-l', '--lang',
    #     type=str.upper,
    #     choices=['C++', 'C'],
    #     help='Specify the programming language'
    # )
    # generate_parser.add_argument(
    #     '-c', '--compiler',
    #     type=str,
    #     dest='compilers',
    #     action=LanguageAction,
    #     help='Specify the compiler to use in the Makefile'
    # )
    # generate_parser.add_argument(
    #     '-std', '--standard',
    #     type=str,
    #     dest='standards',
    #     action=LanguageAction,
    #     help='Specify the language standard (e.g., c11, c++17, c++20)'
    # )
    # backend_group.add_argument(
    #     '--gui',
    #     dest='gui',
    #     type=str.lower,
    #     choices=['sfml', 'sdl2', 'raylib'],
    #     default=None,
    #     help='Enable GUI backend. Optionally chose the backend.'
    # )
    # backend_group.add_argument(
    #     '--no-gui',
    #     dest='gui',
    #     action='store_false',
    #     help='Disable GUI prompt.'
    # )
    # generate_parser.add_argument(
    #     '--binary-name',
    #     type=str,
    #     help='Name of the output binary/executable.'
    # )
    # generate_parser.add_argument(
    #     '-o', '--output',
    #     type=str,
    #     help='The path where the makefile will be created at (if invalid current directory will be used)'
    # )
    # generate_parser.add_argument(
    #     '-h', '--help',
    #     action='store_true',
    #     help='show this help message and exit'
    # )
    generate_parser.set_defaults(func=emit_makefile)

    version_parser = subparsers.add_parser('version', description="Show mkgen's current version", add_help=False)
    version_parser.set_defaults(func=mkgen_version)

    args = parser.parse_args()
    return args

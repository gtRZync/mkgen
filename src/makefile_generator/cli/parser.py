import argparse

from makefile_generator.commands import (build, emit_makefile, init,
                                         show_mkgen_version)

from ._actions import JobsAction, LanguageAction, RootAction


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mkgen", 
        add_help=False
    )
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
            "Example: --build-dir build/\n"
        )
    )

    init_parser = subparsers.add_parser(
        'init', 
        description='Creates a mkgen.toml template in the project root.',
        parents=[banner_parser]
    )
    init_parser.add_argument(
        'root',
        action=RootAction,
        help='project source directory.'
    )
    init_parser.add_argument(
        '--force',
        action='store_true',
        help='Force config file generation if exists.'
    )
    init_parser.set_defaults(func=init)

    build_parser = subparsers.add_parser(
        'build', 
        description='Builds the project using make under the hood.',
        parents=[common_parser, banner_parser]
    )
    build_parser.add_argument(
        '--target',
        default=None,
        help='Makefile recipe to build.'
    )
    build_parser.add_argument(
        '--parallel',
        action=JobsAction,
        default=None,
        help='Indicate how many jobs make should run.'
    )
    build_parser.set_defaults(func=build)


    generate_parser = subparsers.add_parser(
        'generate', 
        description="Generate a Makefile based on the current project's config.",
        parents=[banner_parser, common_parser], 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  Basic usage:
    mkgen generate --root . --build-dir build/

  Generate a Makefile for a C++ project with G++ and C++17 standard (using cli override):
      mkgen generate --root . --build-dir build/ -l C++ -c g++ -std c++17

  Generate a Makefile including GUI flags:
      mkgen generate --root . --build-dir build/ --gui=RAYLIB --language C++
'''
    )
    generate_parser.add_argument(
        '--root',
        action=RootAction,
        required=True,
        help='Project source directory'
    )
    generate_parser.add_argument(
        '--force',
        action='store_true',
        help='Force makefile generation if exists'
    )
    # generate_parser.add_argument(
    #     '-l', '--language',
    #     type=str.lower,
    #     choices=SUPPORTED_LANGUAGE,
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
    #     choices=SUPPORTED_FEATURES,
    #     default=None,
    #     action='+', #TODO: remove duplicates
    #     help='Enable GUI backend. Optionally chose the backend.'
    # )
    # generate_parser.add_argument(
    #     '--app-name',
    #     type=str,
    #     help='Name of the output binary/executable.'
    # )
    generate_parser.set_defaults(func=emit_makefile)

    version_parser = subparsers.add_parser(
        'version', 
        description="Show mkgen's current version", 
    )
    version_parser.set_defaults(func=show_mkgen_version)

    return parser.parse_args()

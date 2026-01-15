HELP_TEXT = '''
usage: mkgen generate [-h] [target_system] [--cross-platform]
                      [-l LANG] [-c COMPILER] [-std STANDARD] [--use-gui-lib]
                      [--binary-name BINARY_NAME] [-o OUTPUT]

Generate a Makefile for your C/C++ project with customizable options.

positional arguments:
  target_system                 Target environnement (e.g : Linux, Windows..etc),
                                defaults to current system
                                ⚠ Mutually exclusive with --cross-platform

options:
  -h, --help                    show this help message and exit

  --cross-platform              Generate a Makefile that works across multiple systems.
                                ⚠ Cannot be used with target_system

  -l, --lang LANG               Specify the programming language

  -c, --compiler COMPILER       Specify the compiler to use in the Makefile

  -std, --standard STANDARD     Specify the language standard (e.g., c11, c++17, c++20)

  --use-gui-lib                 Wether or not to include gui lib flags and or --cflags

  --binary-name BINARY_NAME     Name of the output binary/executable.

  -o, --output OUTPUT           The path where the makefile will be created at (if
                                invalid current directory will be used)

Interactive Mode:
  If any optional options are not provided via command-line arguments,
  the tool will prompt you with an interactive menu to select missing options.
  This allows you to configure the Makefile step-by-step without needing
  to remember all flags.

Notes:
  - All arguments are optional unless explicitly stated as required.
  - Compiler, language, and standard settings are written into the generated Makefile.
  - GUI library flags and binary naming are automatically handled in the Makefile.
  - Targeting a specific system overrides cross-platform settings.

Examples:
  Generate a Makefile for a C++ project with GCC and C++17 standard:
      mkgen generate -l C++ -c g++ -std c++17 -o build/

  Generate a Makefile for a cross-platform project including GUI flags:
      mkgen generate --cross-platform --use-gui-lib --binary-name my_app

  Generate a Makefile for Linux specifically:
      mkgen generate linux --binary-name my_app

  Launch interactive mode (no args, or only some args provided):
      mkgen generate
      The tool will ask you to select language, compiler, etc., step by step
'''


USAGE_TEXT = """
Usage: mkgen <command> [OPTIONS]

Commands:
  generate     Generate a C/C++ Makefile for your project

Options:
    -h, --help                      Show this help message and exit
"""


MUTUALLY_EXCLUSIVE = '''
usage: mkgen generate [-h] [target_system] [--cross-platform]
                      [-l LANG] [-c COMPILER] [-std STANDARD] [--use-gui-lib]
                      [--binary-name BINARY_NAME] [-o OUTPUT]
mkgen generate: error: Cannot specify both a target_system and --cross-platform.
Choose either:
  - a specific target_system,
  - the --cross-platform option, or
  - nothing (defaults to your current system)
'''
import sys

HELP_TEXT = '''
usage: mkgen generate [-h] (--target-system TARGET_SYSTEM | --cross-platform)
                      [-l LANG] [-c COMPILER] [-std STANDARD] [--use-gui-lib]
                      [--binary-name BINARY_NAME] [-o OUTPUT]

Generate a Makefile for your C/C++ project with customizable options.

Options:
  -l, --lang <C|C++>             Specify the programming language.
  -c, --compiler <compiler>       Specify the compiler to use in the Makefile.
  -std, --standard <standard>     Specify the language standard (e.g., c11, c++17, c++20)
  --use-gui-lib                   Include GUI library flags in compilation (affects CFLAGS/LDFLAGS)
  --binary-name <name>            Name of the output binary/executable
  -o, --output <directory>        Output directory for the generated Makefile
  --target-system <system>        Target system for the Makefile (e.g., linux, windows, macos)
                                  ⚠ Mutually exclusive with --cross-platform
  --cross-platform                Generate a Makefile that works across multiple systems
                                  ⚠ Cannot be used with --target-system
  -h, --help                      Show this help message and exit

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
      mkgen generate --target-system linux --binary-name my_app

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

REQUIRE_MUTUALLY_EXCLUSIVE = '''
usage: mkgen generate [-h] (--target-system TARGET_SYSTEM | --cross-platform)
                      [-l LANG] [-c COMPILER] [-std STANDARD] [--use-gui-lib]
                      [--binary-name BINARY_NAME] [-o OUTPUT]
mkgen generate: error: one of the arguments --target-system --cross-platform is required
'''

def show_help(help_text: str = HELP_TEXT):
    print(help_text)
    sys.exit(0)
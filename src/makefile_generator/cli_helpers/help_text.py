GENERATE_USAGE_TEXT = '''\
mkgen generate [target_system] [  --cross-platform, --portable]  -l {C++,C}
                      [-c COMPILER] [-std STANDARD] [--gui GUI | --no-gui] 
                      [--binary-name BINARY_NAME] [-o OUTPUT] [-h]
'''

GENERATE_HELP_TEXT = 'usage: ' +GENERATE_USAGE_TEXT + '''
Generate a Makefile for your C/C++ project with customizable options.

positional arguments:
  target_system                 Target environnement (e.g : Linux, Windows..etc),
                                defaults to current system
                                ⚠ Mutually exclusive with cross-platform option (--cross-platform / --portable).

options:
  -h, --help                    show this help message and exit

  --cross-platform, --portable  Generate a Makefile that works across multiple systems.
                                ⚠ Cannot be used with target_system

  -l, --lang LANG               Specify the programming language

  -c, --compiler COMPILER       Specify the compiler to use in the Makefile

  -std, --standard STANDARD     Specify the language standard (e.g., c11, c++17, c++20)

  --gui GUI                     Enable GUI backend. Must provide a backend value.
                                ⚠ Cannot be used with --no-gui
  
  --no-gui                      Disable GUI prompt.
                                ⚠ Mutually exclusive with --gui

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

Examples:
  Generate a Makefile for a C++ project with GCC and C++17 standard:
      mkgen generate -l C++ -c g++ -std c++17 -o build/

  Generate a Makefile for a cross-platform project including GUI flags:
      mkgen generate --cross-platform --gui=sdl2 --binary-name my_app
      mkgen generate --portable --gui=RAYLIB --lang C++

  Generate a Makefile for Linux specifically:
      mkgen generate linux --binary-name my_app
      
  Generate a Makefile Without GUI flags:
      mkgen generate windows --no-gui -l=C++ -std=c++23

  Launch interactive mode (no args, or only some args provided):
      mkgen generate
      The tool will ask you to select language, compiler, etc., step by step
'''


TOP_LEVEL_HELP_TEXT = '''\
usage: mkgen <command> [OPTIONS]

Commands:
  generate      Generate a C/C++ Makefile for your project
  version       Show mkgen's current version

Options:
    -h, --help                      Show this help message and exit
    -v, --version                   Show mkgen's current version
'''


MUTUALLY_EXCLUSIVE = 'usage: ' + GENERATE_USAGE_TEXT + '''
mkgen generate: error: Cannot specify both a target_system and the cross-platform option (--cross-platform / --portable).
Choose either:
  - a specific target_system (e.g. windows, linux, etc.),
  - the cross-platform option (--cross-platform / --portable), or
  - nothing (defaults to your current system)
'''
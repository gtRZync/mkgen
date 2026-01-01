from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

HELP_TEXT = '''
Usage: mkgen generate [OPTIONS]

Generate a Makefile for your C/C++ project with customizable options.

Options:
  -l, --lang <C|C++>             Specify the programming language. Default: C
  -c, --compiler <compiler>       Specify the compiler to use in the Makefile.
  -std, --standard <standard>     Specify the language standard (e.g., c11, c++17, c++20)
  --use-gui-lib                   Include GUI library flags in compilation (affects CFLAGS/LDFLAGS)
  --binary-name <name>            Name of the output binary/executable
  -o, --output <directory>        Output directory for compiled files / Makefile
  --target-system <system>        Target system for the Makefile (e.g., linux, windows, macos)
                                  ⚠ Mutually exclusive with --cross-platform
  --cross-platform                Generate a Makefile that works across multiple systems
                                  ⚠ Cannot be used with --target-system
  -h, --help                      Show this help message and exit

Interactive Mode:
  If any required options are not provided via command-line arguments,
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
      mkgen generate -l C++ -c g++ -std c++17 -i src/ -o build/

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
  help         Show this help message
"""

def single_choice(prompt: str, options: list[str], stream: Console) -> str:
    table = Table(title=f"[bold yellow]{prompt}[/bold yellow]", title_style='bold magenta', show_lines=True)
    table.add_column("Option", justify="center", style="bold cyan")
    table.add_column("File Type", justify="center", style="bold yellow")

    for i, opt in enumerate(options, start=1):
        table.add_row(str(i), opt)

    stream.print(Align.center(table))

    choice = Prompt.ask("[bold green]Enter the number of your choice[/bold green]", choices=[str(i) for i in range(1, len(options) + 1)])
    return options[int(choice) - 1]

def get_user_input(prompt_text: str, stream: Console) -> str:
    styled_prompt = Text(prompt_text, style="bold white on blue", justify="center")

    panel = Panel(
        Align.center(styled_prompt),
        title="[bold magenta]INPUT[/bold magenta]",
        border_style="bright_blue",
        padding=(1, 2),
        expand=False
    )
    stream.print(panel)

    user_input = Prompt.ask("[bold cyan]→ Enter here[/bold cyan]")
    return user_input

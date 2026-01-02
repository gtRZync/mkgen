from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

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

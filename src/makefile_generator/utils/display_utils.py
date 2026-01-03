from rich.align import Align, AlignMethod
from rich.console import Console, RenderableType
from rich.panel import Panel


def display_panel_text(
    text: RenderableType,
    *,
    stream: Console,
    title: str = 'Panel Text',
    border_style: str = "bold blue",
    align: AlignMethod = 'left',
) -> None:
    panel = Panel.fit(text, title=title, border_style=border_style)
    stream.print(Align(panel, align=align))

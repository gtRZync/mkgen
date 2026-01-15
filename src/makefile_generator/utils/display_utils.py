import sys
from typing import Protocol, TypeVar

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


_T = TypeVar('_T', contravariant=True)

class SupportsWrite(Protocol[_T]):
    def write(self, s: _T, /) -> object:
        ...

def show_text(_text: str,*, file: SupportsWrite[str] | None = None):
    print(_text, file=file)
    code = 1 if file else 0
    sys.exit(code)

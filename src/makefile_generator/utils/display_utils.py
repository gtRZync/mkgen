import sys
from typing import NoReturn, Protocol, TypeAlias, TypeVar

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
_ExitCode: TypeAlias = str | int | None

class SupportsWrite(Protocol[_T]):
    def write(self, s: _T, /) -> object:
        ...

def show_text(_text: str,*, file: SupportsWrite[str] | None = None, code: _ExitCode = None) -> NoReturn:
    print(_text, file=file)
    sys.exit(code)

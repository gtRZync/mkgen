import sys
from typing import NoReturn, Protocol, TypeAlias, TypeVar

import rich

_T = TypeVar('_T', contravariant=True)
_ExitCode: TypeAlias = str | int | None

class SupportsWrite(Protocol[_T]):
    def write(self, s: _T, /) -> object:
        ...

def show_text_and_exit(
    _text: str,
    *, 
    file: SupportsWrite[str] | None = None, 
    code: _ExitCode = None
    ) -> NoReturn:
    print(_text, file=file)
    sys.exit(code)
    
def error(msg: str | Exception) -> NoReturn:
    if isinstance(msg, Exception):
        msg = str(msg)
    rich.print(f'[bold red]→ Error:[/bold red] {msg}', file=sys.stderr)
    sys.exit(1)
    
def warning(msg: str) -> None:
    rich.print(f'[yellow]→ Warning:[/yellow] {msg}')
    
def success(msg: str) -> None:
    rich.print(f'[green]→ Success:[/green] {msg}')
    

from pathlib import Path
from makefile_generator.config import MKROOT
from rich.console import Console

dot_mkroot = [
    'name: app_name',
    'kind: #build kind (exe, static, shared)',
    'language: #either C or C++ (and variants cpp, cplusplus..etc)',
    'std: #compiler standard',
    '',
    'compiler: #self explanatory',
    'build_dir: #build dir name',
    'cross-platform: False'
    '',
    'features: #features in supported features (e.g SDL2, SFML..etc)'
]

def init(args) -> None:
    console = Console()
    file = Path(args.root) / MKROOT
    if file.exists() and file.stat().st_size > 0:
        console.print(f"[yellow]→ {MKROOT!r} already exists.[/yellow]")
        return
    text: str = '\n'.join(dot_mkroot) + '\n'
    file.write_text(text, encoding='utf-8')
    console.print(f"[green]→ {MKROOT!r} generated in project root.[/green]")

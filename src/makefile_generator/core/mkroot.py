import json
import sys
from pathlib import Path
from typing import NoReturn

from rich.console import Console


#I only allow single line python style comment
# meaning every things after "#" will be cut out
def _strip_comments(value: str) -> str:
    return value.split(sep='#', maxsplit=1)[0].strip()
    
def _normalize_values(cfg: dict[str, str]) -> None:
    for k, v in cfg.items():
        if k not in ('name', 'features'):
            cfg[k] = v.lower()

def _all_field_has_value(cfg: dict[str, str]) -> bool:
    if all(v for k, v in cfg.items() if k != 'features'):
        return True
    return False

def _get_missing_fields(cfg: dict[str, str]) -> list[str]:
    return [k for k, v in cfg.items() if not v]

def _set_defaults(cfg: dict[str, str]):
    if not cfg['build_dir']:
        cfg['build_dir'] = 'build'
        
def _set_value(cfg: dict[str, str | list[str]], k: str, v: str) -> None:
    if k.lower() != 'features':
        cfg[k] = _strip_comments(v)
        return
    v = _strip_comments(v)
    cfg[k] = [s.strip().lower() for s in v.split(',')]
    if not all(x for x in cfg[k]):
        cfg[k] = []
    

#TODO: check features
def parse_mkroot(root: Path) -> dict[str, str] | NoReturn:
    console = Console()
    cfg = {
        'name': '',
        'kind': '',
        'language': '',
        'std': '',
        'compiler': '',
        'features': []
    }
    file = root / '.mkroot'
    if not file.exists():
       console.print(f"[bold red]→ Error: Missing {file.name!r} in project directory.[/bold red]")
       sys.exit(1)
    
    if file.stat().st_size == 0:
        console.print(f"[bold red]→ Error: {file.name!r} cannot be empty.[/bold red]")
        sys.exit(1)

    for line in file.read_text().splitlines():
        if ':' not in line:
            continue
        if line.startswith('#'):
            continue
        k, v = [x.strip() for x in line.split(':', 1)]
        _set_value(cfg, k, v)

    _set_defaults(cfg)
    _normalize_values(cfg)

    if not _all_field_has_value(cfg):
       console.print(f"[bold red]→ Error: Missing value for ({', '.join(_get_missing_fields(cfg))}) in .mkroot.[/bold red]")
       sys.exit(1)

    return cfg

def main() -> None:
    cfg = parse_mkroot(Path.cwd())
    if cfg:
        json.dump(cfg, fp=sys.stdout, indent=4)

if __name__ == '__main__':
    main()

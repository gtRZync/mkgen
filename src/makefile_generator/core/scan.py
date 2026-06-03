import sys
from pathlib import Path
from typing import List

import rich

from makefile_generator.config import EXTERNAL, MKROOT, MODULE, PUBLIC, TEST


def scan(root: Path) -> tuple[list[Path], list[Path], list[Path]]:
    """
    brief:
        Walk the directory tree from this directory and collect modules, public include and tests dirs

    returns:
        a tuple of list of modules, public includes and tests modules

    order in tuple:
        - modules
        - publics
        - tests
    """
    modules: list[Path] = []
    tests: list[Path] = []
    publics: list[Path] = []

    for current, dirs, files in root.walk():

        if EXTERNAL in files:
            dirs[:] = []
            continue

        if MODULE in files:
            modules.append(current)

        if PUBLIC in files:
            publics.append(current.relative_to(root)) #retun as_posix() maybe

        if TEST in files:
            tests.append(current)

    return modules, publics, tests

#FIXME: remove walk usage and just walk up dirs
def resolve_root() -> Path | None:
    path = Path.cwd()

    for current, dirs, files in path.walk():
        if MKROOT not in files:
            dirs[:] = []
            continue

        if MKROOT in files:
            return current
    return None

def collect_sources(path: Path) -> list[str]:
    root = resolve_root()
    if not root:
        err=f'''
[red]→ Error: Could not find project root.

→ Expected a [blue]`{MKROOT}`[/blue] file in the current directory or a parent directory.[/red]

[yellow]→ Tip: Run [magenta]`makegen init --root .`[/magenta] in your project root, or run this command from the project root.[/yellow]
        '''
        rich.print(err)
        sys.exit(1)

    return [
        p.relative_to(root).as_posix() for p in path.iterdir()
        if p.suffix in {'.c', '.cpp', '.cc'}
    ]

def collect_new_publics(root: Path, publics: List[Path]) -> List[Path]:
    pub: list[Path] = []

    for current, dirs, files in root.walk():

        if any(x in files for x in ('.external', '.module', '.test')):
            dirs[:] = []
            continue

        if '.public' in files and current.relative_to(root) not in publics:
            pub.append(current.relative_to(root))

    return pub


def collect_new_modules(root: Path, modules: List[Path]) -> List[Path]:
    mods: List[Path] = []

    for current, dirs, files in root.walk():

        if any(x in files for x in ('.external', '.public', '.test')):
            dirs[:] = []
            continue

        if '.module' in files and current not in modules:
            mods.append(current)

    return mods

from pathlib import Path

from makefile_generator.config import EXTERNAL, MODULE, PUBLIC, TEST


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
            modules.append(current.relative_to(root))

        if PUBLIC in files:
            publics.append(current.relative_to(root)) #retun as_posix() maybe

        if TEST in files:
            tests.append(current.relative_to(root))

    return modules, publics, tests
        

def collect_sources(path: Path) -> list[str]:
    return [
        p.as_posix() for p in path.iterdir()
        if p.suffix in {'.c', '.cpp', '.cc'}
    ]
    
def _collect_new_files(
    root: Path, 
    existing_files: list[Path], 
    anchor: str
    ) -> list[Path]:
    found: list[Path] = []
    ALL_ANCHORS = (EXTERNAL, MODULE, PUBLIC, TEST)
    ANCHORS = {x for x in ALL_ANCHORS if x != anchor}

    for current, dirs, files in root.walk():

        if any(x in files for x in ANCHORS):
            dirs[:] = []
            continue

        if anchor in files and current.relative_to(root) not in existing_files:
            found.append(current.relative_to(root))

    return found
    
def collect_new_publics(root: Path, publics: list[Path]) -> list[Path]:
    return _collect_new_files(root, publics, anchor=PUBLIC)

def collect_new_modules(root: Path, modules: list[Path]) -> list[Path]:
    return _collect_new_files(root, modules, anchor=MODULE)

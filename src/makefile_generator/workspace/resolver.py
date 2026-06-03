from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypeAlias
import platform
from collections.abc import Iterable

StrPath: TypeAlias = str | Path

def _get_folders_path_relative_to_dir(*, root: Path, ignore_hidden: bool = True) -> list[Path]:
    '''
    Brief:
    ------
        Recursively get all folders path in a source directory

    Arg:
    -----
        dir (Path): source directory's path

    Return:
    -------
        A list containing exsiting folders relative path if any
    '''
    folders: list[Path] = []
    relative_to: Path = root
    folders.append(root)
    def recurse(path: Path, acc: list[Path]):
        if path.is_file():
            return
        if ignore_hidden and path.name.startswith('.'):
            return
        if path != root:
            acc.append(path.relative_to(relative_to))
            
        for content in path.iterdir():
            recurse(content, acc)
    recurse(root, folders)
    return folders

@dataclass(frozen=True, slots=True, kw_only=True)
class WorkspaceConfig:
    ...

#gotta improve it to make some methods or fields only exist at runtime maybe
@dataclass(frozen=True, slots=True, kw_only=True)
class _Folder:
    name: str
    count_src: int      = 0
    count_h: int        = 0
    count_main: int     = 0
    count_obj: int      = 0
    count_executable: int   = 0

    @property
    def source_score(self) -> float:
        return self.count_src / (self.count_h + 1) - 2 * self.count_main

    @property
    def header_score(self) -> float:
        return self.count_h / (self.count_src + 1) - 2 * self.count_main

    @property
    def object_score(self) -> float:
        return self.count_obj / (self.count_executable + 1)

    @property
    def executable_score(self) -> float:
        return self.count_executable / (self.count_obj + 1)
    
    def contains_any_word(self, iterable: Iterable[str]) -> bool:
        return any(s in self.name for s in iterable)
        
    def get_score_by_type(self, type: Literal['source', 'header', 'object', 'executable']) -> float:
        return getattr(self, f'{type}_score')
        
def _get_path_name(path: Path) -> str:
    if path == Path.cwd():
        return '.'
    elif path.is_absolute():
        return path.name
    return path.as_posix()

def _handle_input_files(
    candidates: list[_Folder],
    /,
    current_folder: Path,
    langage: Literal['C', 'C++']
) -> None:
    h_pattern = {'*.h', '*.hpp'}
    src_pattern = '*.c' if langage == 'C' else '*.cpp'
    src_files = sum(1 for _ in current_folder.glob(src_pattern) if _.is_file())
    header_files = sum(1 for pattern in h_pattern for file in current_folder.glob(pattern) if file.is_file())
    main_file = sum(1 for file in current_folder.glob(f'main{src_pattern.removeprefix("*")}') if file.is_file())
    candidates.append(
        _Folder(
            name=_get_path_name(current_folder),
            count_src=src_files,
            count_h=header_files,
            count_main=main_file
        )
    )

def _handle_output_files(
    candidates: list[_Folder],
    /, 
    current_folder: Path
) -> None:
    obj_pattern = {'*.obj', '*.o'}
    exec_pattern = {'*.exe', '*.out'}
    
    def get_unix_executable_count() -> int:
        import os
        return sum(1 for f in current_folder.glob('*') if f.is_file() and os.access(current_folder, mode=os.X_OK))

    obj_files = sum(1 for pattern in obj_pattern for _ in current_folder.glob(pattern))
    exe_files = sum(1 for pattern in exec_pattern for _ in current_folder.glob(pattern))
    if platform.system().lower() == 'linux' or platform.system().lower() == 'darwin':
        exe_files += get_unix_executable_count() 
    candidates.append(
        _Folder(
            name=_get_path_name(current_folder),
            count_obj=obj_files,
            count_executable=exe_files
        )
    )

def _is_input_type(type: Literal['source', 'header', 'object', 'executable']) -> bool:
    return type == 'source' or type == 'header'

#TODO: add a likeliness thing that affect choice in these kinda situations: 
'''
folder = Folder(name='python', count_src=0, count_h=0, count_main=0, count_obj=0, count_executable=1), score = 1.0
folder = Folder(name='build', count_src=0, count_h=0, count_main=0, count_obj=5, count_executable=0), score = 0.0
folder = Folder(name='build/bin', count_src=0, count_h=0, count_main=0, count_obj=0, count_executable=1), score = 1.0
'''
def resolve_folder(
    *, 
    langage: Literal['C', 'C++'], 
    type: Literal['source', 'header', 'object', 'executable'] = 'source',
    ignore_hidden: bool = True
) -> str:
    candidates: list[_Folder] = []
    best_candidate: _Folder | None = None
    folders: list[Path] = _get_folders_path_relative_to_dir(root=Path.cwd(), ignore_hidden=ignore_hidden)
    exclude: set[str] = {'test', 'examples', 'example', 'tests'}
    
    for folder in folders:
        if folder.is_dir() and folder.name.lower() not in exclude:
            if _is_input_type(type):
                _handle_input_files(
                    candidates,
                    current_folder=folder,
                    langage=langage
                )
            else:
                _handle_output_files(
                    candidates,
                    current_folder=folder
                )

    max_score: float = 0.0
    for candidate in candidates:
        if candidate.get_score_by_type(type) > max_score:
            max_score = candidate.get_score_by_type(type)
            best_candidate = candidate

    if candidates and best_candidate is None:
        potential_candidates = {
            'source' : {'src', 'source', 'sources', 'core'},
            'header' : {'hdr', 'header', 'inc', 'include'},
            'object' : {'obj', 'objs', 'build', 'object'},
            'executable' : {'bin', 'release', 'build/bin'}
        }

        def add_s(text: str) -> str:
            return text.strip() + 's' if not text.endswith('s') else text

        #FIXME: add heuristics maybe
        for candidate in candidates:
            if candidate.name in potential_candidates.get(type, []):
                return candidate.name

            if candidate.name in [add_s(c) for c in potential_candidates.get(type, [])]:
                return candidate.name
    
    if not best_candidate:
        match type:
            case 'source' | 'header':
                return '.'
            case 'executable':
                return 'build/bin'
            case 'object':
                return 'build'
            
    return best_candidate.name

def as_win32_path(path: StrPath, /, backlash: Literal['\\', '\\\\'] = '\\') -> str:
    if not path:
        return ''
    if isinstance(path, Path):
        path = path.as_posix()
    return path.replace('/', backlash) if '/' in path else path

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from makefile_generator.config import MKCACHE

from .model import Project
from .scan import collect_new_modules, collect_new_publics


@dataclass(frozen=True, kw_only=True, slots=True)
class _BaseVariants:
    existing: List[Path]
    modified_or_new: List[Path]

    def get_all(self) -> List[Path]:
        return [*self.modified_or_new, *self.existing]

@dataclass(frozen=True, kw_only=True, slots=True)
class _ModulesVariants(_BaseVariants):
    pass
#NOT TO BE IMPLEMENTED RN
@dataclass(frozen=True, kw_only=True, slots=True)
class _TestsVariants(_BaseVariants):
    pass

@dataclass(frozen=True, kw_only=True, slots=True)
class _PublicsVariants(_BaseVariants):
    pass

@dataclass(frozen=True, kw_only=True, slots=True)
class MkCache:
    config: Dict[str, str]
    modules: _ModulesVariants
    publics: _PublicsVariants
    tests: List[Path]

def generate_mkcache(project: Project) -> None:
    text_list: List[str] = []
    text_list.append('PATHS\n')
    cache_path = Path(project.build_dir)

    for module in project.modules:
        text_list.append(f'{module.path} | {module.path.stat().st_mtime_ns} | module\n')

    for test in project.tests:
        text_list.append(f'{test.path} | {test.path.stat().st_mtime_ns} | test\n')

    for public in project.publics:
        text_list.append(f'{public} | {public.stat().st_mtime_ns} | public\n')

    text_list.append('CONFIGS\n')

    text_list.append(f'name: {project.name}\n')
    text_list.append(f'kind: {project.kind}\n')
    text_list.append(f'language: {project.language}\n')
    text_list.append(f'compiler: {project.compiler["name"]}\n')
    text_list.append(f'std: {project.compiler["std"]}\n')
    text_list.append(f'features: {project.features}\n')
    text_list.append(f'features_flags: {project.features_flags}\n')
    text_list.append(f'bin_dir: {project.bin_dir}\n')
    text_list.append(f'build_dir: {project.build_dir}\n')

    data: str = ''.join(text_list)

    cache = cache_path / MKCACHE
    cache.write_text(data)

def parse_mkcache(cache_path: Path) -> MkCache | None:
    modules: List[Path] = []
    ex_mod: List[Path] = []
    tests: List[Path] = []
    publics: List[Path] = []
    configs: Dict[str, str] = {}
    cache = cache_path / MKCACHE
    root = Path.cwd()

    if not cache.exists():
        return None

    for line in cache.read_text().splitlines():
        line = line.strip()

        if not line:
            continue

        if line == 'PATHS':
            current = 'paths'
        elif line == 'CONFIGS':
            current = 'configs'
        else:
            if current == 'paths':
                if '|' not in line:
                    continue

                path, mtime, type = [s.strip() for s in line.split('|', maxsplit=2)]
                path=Path(path)

                if not path.exists():
                    continue

                if type == 'public':
                    publics.append(path)

                if path.stat().st_mtime_ns == int(mtime):
                    if type == 'module':
                        ex_mod.append(path)
                    continue

                match type:
                    case 'module':
                        modules.append(path)
                    case 'test':
                        tests.append(path)

            elif current == 'configs':
                k, v = [x.strip() for x in line.split(sep=':', maxsplit=1)]
                configs[k] = v
            else:
                raise ValueError(f'Line outside section: {line}') #TODO: handle differently

    modules.extend(collect_new_modules(root, [*ex_mod, *modules]))
    return MkCache(
        config=configs,
        modules=_ModulesVariants(existing=ex_mod, modified_or_new=modules),
        publics=_PublicsVariants(existing=publics, modified_or_new=collect_new_publics(root, publics)),
        tests=tests
    )

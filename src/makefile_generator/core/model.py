from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Dict, Generator, List

from makefile_generator.config import constants
from makefile_generator.core._platform import get_normalized_platform

from .scan import collect_sources


@dataclass(frozen=True, kw_only=True, slots=True)
class Target:
    path: Path
    sources: List[str] = field(default_factory=list)

@dataclass(frozen=True, kw_only=True, slots=True)
class Module(Target):
    pass

@dataclass(frozen=True, kw_only=True, slots=True)
class Test(Target):
    pass

#TODO: add cflags
@dataclass(frozen=True, kw_only=True, slots=True)
class Project:
    name: str
    kind: str
    language: str
    src_ext: str
    compiler: Dict[str, str] = field(default_factory=dict) #for compiler.var, compiler.name, compiler.std
    build_dir: str
    bin_dir: str
    features: bool
    features_flags: str
    modules: List[Module]
    publics: List[Path]
    tests: List[Test]

    def __iter__(self) -> Generator[tuple[str, Any], Any, None]:
        for f in fields(self):
            yield f.name, getattr(self, f.name)

def _setup_module(modules: list[Path]) -> List[Module]:
    mods: List[Module] = []
    for path in modules:
        mods.append(
            Module(
                path=path,
                sources=sorted(collect_sources(path))
            )
        )
    return mods

def _setup_test(tests: list[Path]) -> List[Test]:
    tts: List[Test] = []
    for path in tests:
        tts.append(
            Test(
                path=path,
                sources=sorted(collect_sources(path))
            )
        )
    return tts

def _get_compiler_data(config: dict[str, str]) -> Dict[str, str]:
    return {
        'var' : 'CXX' if config['language'] == 'c++' else 'CC',
        'name': config['compiler'],
        'std': config['std']
    }

#TODO: maybe get the extensions from the files that are in the modules ig
def _get_extension(cfg: dict[str, str]) -> str:
    return '.cpp' if cfg['language'] == 'c++' else '.c'

def _get_features_flags(features) -> str:
    if not features:
        return ''
    key = 'win32' if get_normalized_platform() == 'windows' else 'unix'
    features_flags: List[str] = []
    for feature in features:
        f = getattr(constants, f'{feature.upper()}_FLAGS')
        features_flags.append(f'{f[key]} ')
    print(features_flags)
    return ''.join(features_flags)
        



def build_model(
    config: dict[str, str],
    modules: list[Path],
    publics: list[Path],
    tests: list[Path]
) -> Project:

    return Project(
        name=config['name'],
        kind=config['kind'],
        language=config['language'],
        src_ext=_get_extension(config),
        compiler=_get_compiler_data(config),
        build_dir=config['build_dir'],
        bin_dir=config['bin_dir'],
        features=True if config['features'] else False,
        features_flags=_get_features_flags(config['features']),
        publics=sorted(publics),
        modules=_setup_module(modules),
        tests=_setup_test(tests)
    )

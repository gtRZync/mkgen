from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any, Generator

from makefile_generator.config import features
from makefile_generator.config.constants import COMPILED_DIR
from makefile_generator.core._platform import get_normalized_platform
from makefile_generator.core.loader import ProjectConfig

from .scan import collect_sources


@dataclass(frozen=True, kw_only=True, slots=True)
class Target:
    path: Path
    sources: list[str] = field(default_factory=list)

@dataclass(frozen=True, kw_only=True, slots=True)
class Module(Target):
    pass

@dataclass(frozen=True, kw_only=True, slots=True)
class Test(Target):
    pass

@dataclass(frozen=True, kw_only=True, slots=True)
class Project:
    name: str
    kind: str
    language: str
    src_ext: str
    compiler: dict[str, str] = field(default_factory=dict) #for compiler.var, compiler.name, compiler.std...etc
    build_dir: str
    bin_dir: str
    root_dir: str
    compiled_dir: str
    features: bool
    features_flags: str
    modules: list[Module]
    publics: list[Path]
    tests: list[Test]
    config_asdict: dict[str, Any]

    def __iter__(self) -> Generator[tuple[str, Any], Any, None]:
        for f in fields(self):
            yield f.name, getattr(self, f.name)

def _setup_module(modules: list[Path]) -> list[Module]:
    mods: list[Module] = []
    for path in modules:
        mods.append(
            Module(
                path=path,
                sources=sorted(collect_sources(path))
            )
        )
    return mods

def _setup_test(tests: list[Path]) -> list[Test]:
    tts: list[Test] = []
    for path in tests:
        tts.append(
            Test(
                path=path,
                sources=sorted(collect_sources(path))
            )
        )
    return tts

def _get_compiler_data(config: ProjectConfig) -> dict[str, str]:
    return {
        'var' : 'CXX' if config.project.language == 'c++' else 'CC',
        'name': config.build.compiler,
        'std': config.build.standard,
        'cflags' : _get_cflags(config.build.cflags)
    }

def _get_extension(language: str) -> str:
    return '.cpp' if language == 'c++' else '.c'

def _get_features_flags(_features: list[str]) -> str:
    if not _features:
        return ''
    
    key = 'win32' if get_normalized_platform() == 'windows' else 'unix'
    features_flags: list[str] = []
    for feature in _features:
        f = getattr(features, f'{feature.upper()}_FLAGS')
        features_flags.append(f'{f[key]} ')
    print(features_flags)
    return ''.join(features_flags)

def _get_cflags(cflags: list[str]) -> str:
    if not cflags:
        return ''

    return ' '.join(cflags)

def build_model(
    config: ProjectConfig,
    build_dir: str,
    root_dir: str,
    modules: list[Path],
    publics: list[Path],
    tests: list[Path]
) -> Project:
    project = config.project
    build = config.build
    
    return Project(
        name=project.name,
        kind=project.kind,
        language=project.language,
        src_ext=_get_extension(project.language),
        compiler=_get_compiler_data(config),
        build_dir=build_dir,
        bin_dir=build_dir,
        root_dir=root_dir,
        compiled_dir=COMPILED_DIR,
        features=True if build.features else False,
        features_flags=_get_features_flags(build.features),
        publics=sorted(publics),
        modules=_setup_module(modules),
        tests=_setup_test(tests),
        config_asdict=asdict(config)
    )

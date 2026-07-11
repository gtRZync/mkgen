import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import rich.traceback

from makefile_generator.config.constants import (MKGEN_CONFIG_FILE, PROFILES,
                                                 PROJECT_KINDS)
from makefile_generator.config.features import (SUPPORTED_FEATURES,
                                                SUPPORTED_LANGUAGES)
from makefile_generator.utils.display_utils import error

from .exceptions import ExpectedUserError

rich.traceback.install(show_locals=True)


@dataclass(kw_only=True, frozen=True, slots=True)
class _Project:
    name: str
    kind: str
    language: str
    

@dataclass(kw_only=True, frozen=True, slots=True)
class _Build:
    compiler: str
    standard: str
    cflags: list[str]
    ldflags: list[str]
    include_dirs: list[str]
    features: list[str]


@dataclass(kw_only=True, frozen=True, slots=True)
class ProjectConfig:
    project: _Project
    build: _Build


def _build_project_config(
    config: dict[str, Any]
    ) -> ProjectConfig:
    
    project = config['project']
    build = config['build']
    
    return ProjectConfig(
        project=_Project(
            name=project['name'],
            kind=project['kind'],
            language=project['language']
        ),
        build=_Build(
            compiler=build['compiler'],
            standard=build['standard'],
            cflags=build['cflags'],
            ldflags=build['ldflags'],
            include_dirs=build['include_dirs'],
            features=build['features'],
        )
    )
    
def _check_project_config(config: ProjectConfig) -> None:
    if config.project.kind.lower() not in PROJECT_KINDS:
        error(
            f'Unexpected project kind: {config.project.kind!r}'
            f'\nChoose from {PROJECT_KINDS!r}'
        )
    
    if config.project.language.lower() not in SUPPORTED_LANGUAGES:
        error(
            f'Language: {config.project.language!r} is not supported.'
            f'\nChoose from {SUPPORTED_LANGUAGES!r}'
        )
    
    lang = config.project.language.lower()
    compiler = config.build.compiler.lower()
    standard = config.build.standard.lower()
    
    profile = PROFILES[lang]
    
    if compiler not in profile['compilers']:
        error(
            f'Invalid compiler: {compiler!r}'
        )
    
    if standard not in profile['standards']:
        error(
            f'Invalid compiler standard: {standard!r}'
        )
    
    features = [
        feature.lower() for feature in config.build.features
    ]
    
    def format_features(features: list[str]) -> str|list[str]:
        if len(features) == 1:
            return features[0]
        return features
    
    if not all([f in SUPPORTED_FEATURES for f in features]):
        if len(features) <= 1:
            n = 'feature'
        else:
            n = 'features'
        msg = f'Unexpected {n}: {format_features(features)!r}. Choose from {SUPPORTED_FEATURES!r}!'
        error(msg)

def load_mkgen_config(root_dir: Path) -> ProjectConfig:
    
    config_path = root_dir / MKGEN_CONFIG_FILE
    if not config_path.exists():
        raise ExpectedUserError(
            f'Configuration file missing: [blue]{config_path.name!r}[/blue]'
        )
    
    try:
        config = tomllib.load(config_path.open('rb'))
        project_config = _build_project_config(config)
        
        _check_project_config(project_config)
        
        return project_config
            
    except KeyError as e:
        raise ExpectedUserError(f'Missing required key: {e} in {MKGEN_CONFIG_FILE!r}.') from e

    except PermissionError as e:
        raise ExpectedUserError(f'Permission denied: {e}') from e
    
def main() -> None:
    load_mkgen_config(Path('..'))

if __name__ == '__main__':
   main()
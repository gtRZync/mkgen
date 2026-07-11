import argparse
from dataclasses import dataclass, field
from pathlib import Path

from makefile_generator.config.constants import MKCACHE
from makefile_generator.core.cache import (CachedModules, CachedPublics,
                                           generate_mkcache, parse_mkcache)
from makefile_generator.core.model import build_model
from makefile_generator.core.scan import (collect_new_modules,
                                          collect_new_publics)
from makefile_generator.utils.display_utils import error

from .generate import emit_sources


@dataclass(kw_only=True, slots=True, frozen=True)
class _SourcesUpdateResult:
    needs_update: bool
    new_modules: list[Path] = field(default_factory=list)
    new_publics: list[Path] = field(default_factory=list)

def _get_mtime_ns(path: Path) -> int:
    return path.stat().st_mtime_ns

def _any_modifications(
    cached_modules: CachedModules, 
    cached_publics: CachedPublics
    ) -> bool:
    
    mods = [mtime != _get_mtime_ns(path) for path, mtime in cached_modules]
    pubs = [mtime != _get_mtime_ns(path) for path, mtime in cached_publics]

    if not all([*mods, *pubs]):
        return True
    
    return False

def _check_sources_update(
    root: Path,
    modules: CachedModules, 
    publics: CachedPublics
    ) -> _SourcesUpdateResult:
    #!NOT ADDING TESTS YET (maybe never)
    new_modules = collect_new_modules(root, modules.paths)
    new_publics = collect_new_publics(root, publics.paths)
    
    return _SourcesUpdateResult(
        needs_update=(
            new_modules != [] and new_publics != []
            or _any_modifications(modules, publics)
        ),
        new_modules=new_modules,
        new_publics=new_publics,
    )

def _incrementally_update_makefile(args: argparse.Namespace) -> None:
    cache = parse_mkcache(
        Path(args.build_dir)
    )

    if not cache:
        error(f'Missing {MKCACHE!r}. Regenerate build to generate cache file.')

    modules, publics, tests, root = cache.modules, cache.publics ,cache.tests, cache.root

    sources = _check_sources_update(
        root,
        modules,
        publics
    )
    
    if not sources.needs_update:
        return
    
    #TODO: log update in console

    if sources.new_modules:
        modules.paths.extend(sources.new_modules)
    if sources.new_publics:
        publics.paths.extend(sources.new_publics)
    
    project = build_model(
        config=cache.config,
        build_dir=args.build_dir,
        root_dir=root.as_posix(),
        modules=modules.paths,
        publics=publics.paths,
        tests=tests
    )
    emit_sources(project)
    generate_mkcache(project)

def regenerate(args) -> None:
    _incrementally_update_makefile(args)

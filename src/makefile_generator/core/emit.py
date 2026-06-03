import argparse
import sys
import time
from pathlib import Path

import rich
from jinja2 import Environment, FileSystemLoader, Template
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from makefile_generator.config import (
    MAKEFILE,
    MODULE,
    PUBLIC,
    SOURCES,
    TEMPLATES,
    TEMPLATES_DIR,
    TEST,
)

from ._platform import get_normalized_platform, get_platform, is_platform_supported
from .cache import generate_mkcache, parse_mkcache
from .mkroot import parse_mkroot
from .model import Project, build_model
from .scan import scan

#==================================================================================
#TODO CAUTION:  TESTS WILL NOT BE IMPLEMENTED YET, I WON'T FOCUS ON BOTH AT ONE TIME
#==================================================================================
#==================================================================================
#FIXME MAJOR:  THERE'S A BUG WHERE make will not use the updated sources.mk when a new file is added or deleted
#==================================================================================

def _create_progress_description() -> str:
    ...

def _get_template(args: argparse.Namespace) -> Template:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR), #type: ignore
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters
    #TODO: handle TemplateNotFound
    if args.cross_platform:
        template = env.get_template(TEMPLATES['cross-platform'])
    else:
        template = env.get_template(TEMPLATES[get_normalized_platform()])
    return template


def emit_makefile(args: argparse.Namespace) -> None:
    console_err = Console(stderr=True)
    if not is_platform_supported():
            #TODO: make an err display abstraction
            console_err.print(f"[bold red]→ Error: {get_platform()!r} is not supported.[/bold red]")
            sys.exit(1)
    root = Path(args.root).resolve()
    cfg = parse_mkroot(root)
    mod, pub, test = scan(root)
    if not mod and not pub and not test:
        err = f'''
[red]→ Error: Could not find any [blue]{PUBLIC}[/blue], [blue]{MODULE}[/blue] or [blue]{TEST}[/blue] files

→ Expected anchor files in the current directory or sub-directories.[/red]

[yellow]→ Tip: Run [magenta]`mkgen generate`[/magenta] in your project root.[/yellow]
        '''
        console_err.print(err)
        return

    project = build_model(cfg, mod, pub, test)
    template = _get_template(args)
    data = template.render(project)
    outdir = Path(project.build_dir) / MAKEFILE
    if outdir.exists():
        pass #do something ion know what yet
    try:
        with Progress(
            SpinnerColumn(spinner_name='dots'),
            TextColumn('[progress.description][task.description]'),
            transient=True
        ) as progress:
            description = _create_progress_description()
            outdir.parent.mkdir(exist_ok=True)
            with outdir.open('wt') as makefile:
                task = progress.add_task(description=f'[bold magenta]{description}')
                makefile.write(data)
                # File creation is extremely fast, so I'm faking a spinner for UX purposes.
                # The sleep call is purely to give the spinner time to display.
                time.sleep(2)
                progress.remove_task(task)
        generate_mkcache(project)
        emit_sources(project)
    except FileNotFoundError:
        console_err.print("[bold red]! Error:[/bold red] Output directory does not exist.")
        sys.exit(1)

    except PermissionError:
        console_err.print("[bold red]! Error:[/bold red] Permission denied while writing the makefile.")
        sys.exit(1)

    except IsADirectoryError:
        console_err.print("[bold red]! Error:[/bold red] Output path is a directory, not a file.")
        sys.exit(1)

    except OSError as e:
        console_err.print(f"[bold red]! Error:[/bold red] Failed to write makefile: {e}")
        sys.exit(1)

def _add_sep_or_space(count: int, limit: int) -> str:
    if count >= limit:
        return ' \\\n           ' #adding 11 spaces to indent
    return ' '

def emit_sources(project: Project, src_per_line: int = 4) -> None:
    file = Path(project.build_dir) / SOURCES
    content = ['SOURCES := ']
    i: int = 1
    for module in project.modules:
        for source in module.sources:
            content.append(f'{source}{_add_sep_or_space(count=i, limit=src_per_line)}')
            i = i + 1 if i < src_per_line else 1

    content.append('\n')
    content.append('INCLUDE_DIRS := ')
    i = 1
    for public in project.publics:
        content.append(f'{public}{_add_sep_or_space(count=i, limit=src_per_line)}')
        i = i + 1 if i < src_per_line else 1
    content.append('\n')
    content.append('INCLUDES := $(foreach dir,$(INCLUDE_DIRS),-I$(dir))')

    data = ''.join(content)
    file.write_text(data)

def incrementally_update_makefile(args: argparse.Namespace) -> None:
    cache = parse_mkcache(Path(args.build_dir))

    if not cache:
        rich.print("[bold red]→ Error: Missing '.mkcache'.Regenerate build to generate cache file.[/bold red]", file=sys.stderr)
        return

    modules, publics, tests = cache.modules, cache.publics ,cache.tests
    if not modules.modified_or_new and not publics.modified_or_new and not tests:
        return

    project = build_model(
        config=cache.config,
        modules=modules.get_all(),
        publics=publics.get_all(),
        tests=tests
    )
    generate_mkcache(project)
    emit_sources(project)


def regencache(args) -> None:
    incrementally_update_makefile(args)

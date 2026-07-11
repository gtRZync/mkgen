import argparse
import time
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from rich.progress import Progress, SpinnerColumn, TextColumn

from makefile_generator.config import (MAKEFILE, MODULE, PUBLIC, SOURCES,
                                       TEMPLATES, TEMPLATES_DIR, TEST)
from makefile_generator.core._platform import (get_normalized_platform,
                                               get_platform,
                                               is_platform_supported)
from makefile_generator.core.cache import generate_mkcache
from makefile_generator.core.loader import load_mkgen_config
from makefile_generator.core.model import Project, build_model
from makefile_generator.core.scan import scan
from makefile_generator.utils.display_utils import error, warning

#==================================================================================
#TODO CAUTION:  TESTS WILL NOT BE IMPLEMENTED YET, I WON'T FOCUS ON BOTH AT ONE TIME
#==================================================================================

def _create_progress_description(language: str) -> str:
    return f'Generating {language.capitalize()!r} makefile for {get_normalized_platform()}...'

def _get_template(args: argparse.Namespace) -> Template:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR), #pyright: ignore
        trim_blocks=True,
        lstrip_blocks=True,
    )
    #TODO: handle TemplateNotFound
    try:
        key = 'win32' if get_normalized_platform() == 'windows' else 'unix'
        template = env.get_template(TEMPLATES[key])
        return template
    except TemplateNotFound as e:
        error(e)


def emit_makefile(args: argparse.Namespace) -> None:
    if not is_platform_supported():
        error(f'{get_platform()!r} is not supported.')
            
    root = args.root
    build_dir = args.build_dir
    cfg = load_mkgen_config(root)
    mod, pub, test = scan(root)
    if not mod and not pub and not test:
        err = f'''\
[red]→ Error: Could not find any [blue]{PUBLIC}[/blue], [blue]{MODULE}[/blue] or [blue]{TEST}[/blue] files

→ Expected anchor files in the current directory or sub-directories.[/red]

[yellow]→ Tip: Run [magenta]`mkgen generate`[/magenta] in your project root.[/yellow]
'''
        error(err)

    project = build_model(
        cfg, 
        build_dir, 
        root.as_posix(), 
        mod, 
        pub, 
        test
    )
    template = _get_template(args)
    data = template.render(project)
    makefile = Path(project.build_dir) / MAKEFILE
    
    if not makefile.parent.exists():
        error(
            f'Build dir: {project.build_dir!r} does not exists!'
        )
    
    if makefile.exists():
        if not args.force:
            warning(
                'A [bold]Makefile[/] already exists. '
                'Use [cyan]--force[/] to regenerate and overwrite it.'
            )
            return
        
    try:
        with Progress(
            SpinnerColumn(spinner_name='dots'),
            TextColumn('[progress.description]{task.description}'),
            transient=True
        ) as progress:
            description = _create_progress_description(project.language)
            task = progress.add_task(description=f'[bold magenta]{description}')
            makefile.write_text(data, encoding='utf-8')
            emit_sources(project)
            generate_mkcache(project)
            # # File creation is extremely fast, so I'm faking a spinner for UX purposes.
            # # The sleep call is purely to give the spinner time to display.
            time.sleep(1.5)
            progress.remove_task(task)
    except PermissionError:
        error('Permission denied while writing the makefile.')

    except IsADirectoryError:
        error('Output path is a directory, not a file.')

    except OSError as e:
        error(f'Failed to write makefile: [yellow]{e}[/yellow]')

def _add_sep_or_space(count: int, limit: int) -> str:
    if count >= limit:
        return ' \\\n           ' #?adding 11 spaces to indent
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
import argparse
import platform
import sys
import time
from pathlib import Path
from typing import Literal

import questionary
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from makefile_generator import workspace
from makefile_generator.config import (C_COMPILERS, C_STANDARDS, CPP_COMPILERS,
                                       CPP_STANDARDS, RAYLIB_CFLAGS,
                                       RAYLIB_FLAGS, SDL2_CFLAGS, SDL2_FLAGS,
                                       SFML_CFLAGS, SFML_FLAGS, TEMPLATES,
                                       TEMPLATES_DIR)
from makefile_generator.utils.display_utils import display_panel_text
from makefile_generator.utils.prompt_utils import (DEFAULT_STYLE,
                                                   questionary_select)
from makefile_generator.workspace import as_win32_path

console = Console()
console_err = Console(stderr=True)


def _create_progress_description(
    langage: Literal['c', 'c++'] | None,
    system: Literal['windows', 'mac', 'linux'] | None = None,
    end: str = '...'
) -> str:

    description = f'Generating your cross-platform Makefile{end}'
    if not system and langage:
        description = f'Generating your cross-platform {langage.upper()} Makefile{end}'
    if system and langage:
        description = f'Generating your {langage.upper()} Makefile for {system.capitalize()}{end}'
    if system and not langage:
        description = f'Generating your Makefile for {system.capitalize()}{end}'

    return description
    
def _rename() -> str:
    def validate_name(name) -> bool:
        if name:
            return True
        return False
    filename: str = questionary.text(
        'Enter new filename: ', 
        style=DEFAULT_STYLE,
        validate=validate_name, 
    ).unsafe_ask()
    return filename
    
def _new_path() -> Path:
    def validate_path(path) -> bool:
        if path:
            path = Path(path)
            if path.resolve().exists() and path.is_dir():
                return True
        return False
    path = questionary.path(
        'Select or enter a directory to save the file (Tab to autocomplete):',
        only_directories=True,
        style=DEFAULT_STYLE,
        validate=validate_path
    ).unsafe_ask()

    return Path(path).resolve()

#TODO: make it better
def _generate_makefile(
    data: dict[str, dict[str, str] | str | bool],
    args: argparse.Namespace,
    progress_description: str = 'Generating your Makefile...'
) -> None:
    template = None
    action: str = 'generated'
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR), #type: ignore
        lstrip_blocks=True,
        trim_blocks=True
    )
    #TODO: handle TemplateNotFound
    if args.cross_platform:
        template = env.get_template(TEMPLATES.get('cross-platform', ''))
    else:
        template = env.get_template(TEMPLATES.get(args.target_system, ''))

    if template:
        makefile = template.render(data)
        outdir = Path(args.output) if args.output else Path.cwd()
        #TODO: add check if not a dir use Path.cwd() log
        #TODO: use validate in a good way
        outdir = outdir / 'Makefile'
        if outdir.exists():
            #FIXME: use enum, auto and match 
            choices = ['Rename', 'Overwrite', 'Use a new path', 'Abort']
            user_choice = questionary_select('A Makefile already exists in output directory.', choices, choices_upper=False)
            if user_choice == 'abort':
                console.print("[yellow]→ Makefile generation aborted.[/yellow]")
                sys.exit(0)
            elif user_choice == 'rename': 
               #sanitize this brochacho  
                outdir = outdir.parent / _rename()
            elif user_choice == 'use a new path':
                outdir = _new_path() / 'Makefile'
            else:
                action = 'overwritten'
                console.print("[yellow]→ Overwriting existing Makefile…[/yellow]")
                
        try:
            with Progress(
                SpinnerColumn(spinner_name='dots'),
                TextColumn('[progress.description]{task.description}'),
                transient=True
            ) as progress:
                with outdir.open('wt') as file:
                    task = progress.add_task(description=f'[bold magenta]{progress_description}')
                    file.write(makefile)
                    # File creation is extremely fast, so I'm faking a spinner for UX purposes.
                    # The sleep call is purely to give the spinner time to display.
                    time.sleep(2)
                    progress.remove_task(task)

            display_panel_text(
                f'[green]✓ Makefile successfully {action}[/green] at: [bold yellow]{outdir.parent} [/bold yellow]',
                stream=console,
                title='Success'
            )
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


def _choose_langage(data: dict) -> str:
    langs = ['C++', 'C']
    choice:str = questionary_select('Select a language: ',langs, choices_upper=False)
    
    if choice.lower() == 'c++':
        data['src_ext'] = '.cpp'
        data['compiler']['var'] = 'CXX'
    else:
        data['src_ext'] = '.c'
        data['compiler']['var'] = 'CC'
    return choice

def _choose_compiler(langage: str) -> str:
    compiler: str = questionary_select(
        'Select a compiler: ',
        C_COMPILERS if langage == 'c' else CPP_COMPILERS
    )
    return compiler

def _choose_standard(langage: str) -> str:
    std: str = questionary_select(
        'Select compiler standard: ',
        C_STANDARDS if langage.lower() == 'c' else CPP_STANDARDS,
        choices_upper=False
    )
    return std

def _ensure_compatible_compiler_arg(
    *, 
    arg: Literal['compiler', 'standard'], 
    lang: Literal['c', 'c++'], 
    value: str
) -> str:
    normalized_value = value.lower()
    err_msg = f'[bold red]! Error:[/bold red][bold] invalid {arg} {value!r} for {lang.upper()!r}[/].'
    prompt = f'Select {lang.upper()} {arg}: '
    normalized_map = {
        'compiler' : {
            'c' : [s for s in C_COMPILERS],
            'c++' : [s for s in CPP_COMPILERS]
        },
        'standard' : {
            'c' : [s.lower() for s in C_STANDARDS],
            'c++' : [s.lower() for s in CPP_STANDARDS]
        }
    }
    if normalized_value not in normalized_map[arg][lang]:
        console.print(err_msg)
        normalized_value: str = questionary_select(
            prompt,
            normalized_map[arg][lang]
        )
    #msvc compiler normalization
    if normalized_value == 'msvc':
        normalized_value = 'cl'

    return normalized_value

def _chose_binary_name() -> str :
    filename: str = questionary.text(
     'Output binary file name: ',
     default='main',
     style=DEFAULT_STYLE
    ).unsafe_ask()
    return filename

def _get_key_for(target_system: str, /):
    if target_system == 'windows':
        return 'win32'
    else:
        return 'unix'

def _set_gui_lib_flags(
    data: dict[str, dict[str, str] | str | bool], 
    args: argparse.Namespace,
    backend: str | None = None
) -> None:
    data['use_gui_lib'] = True
    if backend is None:
        backend = args.gui
    if args.cross_platform:
        if backend == 'sfml':
            data['gui_lib_flags'] = SFML_FLAGS['win32']
            data['unix_gui_lib_flags'] = SFML_FLAGS['unix']
            data['gui_lib_cflags'] = SFML_CFLAGS
        elif backend == 'sdl2':
            data['gui_lib_flags'] = SDL2_FLAGS['win32']
            data['unix_gui_lib_flags'] = SDL2_FLAGS['unix']
            data['gui_lib_cflags'] = SDL2_CFLAGS
        else:
            data['gui_lib_flags'] = RAYLIB_FLAGS['win32']
            data['unix_gui_lib_flags'] = RAYLIB_FLAGS['unix']
            data['gui_lib_cflags'] = RAYLIB_CFLAGS
    else:
        if backend == 'sfml':
            data['gui_lib_flags'] = SFML_FLAGS[_get_key_for(args.target_system)]
            data['gui_lib_cflags'] = SFML_CFLAGS
        elif backend == 'sdl2':
            data['gui_lib_flags'] = SDL2_FLAGS[_get_key_for(args.target_system)]
            data['gui_lib_cflags'] = SDL2_CFLAGS
        else:
            data['gui_lib_flags'] = RAYLIB_FLAGS[_get_key_for(args.target_system)]
            data['gui_lib_cflags'] = RAYLIB_CFLAGS


def _choose_gui_lib(data: dict[str, dict[str, str] | str | bool], args: argparse.Namespace) -> None:
    gui_libs = ['SDL2', 'SFML', 'RAYLIB']
    lib: str = questionary_select('Select a graphics library: ', gui_libs, choices_upper=False)
    _set_gui_lib_flags(data, args, lib)

def _prompt_gui_lib_usage(data:  dict[str, dict[str, str] | str | bool], args: argparse.Namespace) -> None:
    choice: bool = questionary.confirm('Use a GUI library?', style=DEFAULT_STYLE).unsafe_ask()
    if choice:
        _choose_gui_lib(data, args)
        
def _set_directories(langage: Literal['C', 'C++'], data: dict) -> None:
    src_dir = workspace.resolve_folder(langage=langage)
    hdr_dir = workspace.resolve_folder(langage=langage, type='header')
    obj_dir = workspace.resolve_folder(langage=langage, type='object')
    bin_dir = workspace.resolve_folder(langage=langage, type='binary')
    system = platform.system().lower()
    
    data['directories']['src'] = as_win32_path(src_dir) if system == 'windows' else src_dir
    data['directories']['include'] = as_win32_path(hdr_dir) if system == 'windows' else hdr_dir
    data['directories']['build'] = as_win32_path(obj_dir) if system == 'windows' else obj_dir
    data['directories']['bin'] = as_win32_path(bin_dir) if system == 'windows' else bin_dir

def is_target_correct(args: argparse.Namespace) -> bool:
    systems = {'windows', 'mac', 'linux', 'macos'}

    if args.cross_platform:
        return True
    if args.target_system.lower() in systems:
        if args.target_system.lower() == 'macos':
            args.target_system = 'mac'
        return True
    return False

#TODO: handle case platform is not: win32, darwin or linux
def _target_err():
    text = Text()
    text.append("Error: ", style="bold red")
    text.append(
        "Please enter a valid target system (e.g. linux, windows, macos).",
        style='bold white'
    )

    console_err.print(text)
    sys.exit(1)

def generate(args: argparse.Namespace) -> None:
    if args.help:
        from makefile_generator.cli_helpers.help_text import GENERATE_HELP_TEXT
        from makefile_generator.utils.display_utils import show_text
        show_text(GENERATE_HELP_TEXT)

    if not is_target_correct(args):
        _target_err()
        
    langage = None
    data = {
        'compiler' : {
            'var' : '',
            'name' : '',
            'std' : ''
        },
        'directories' : {
            'bin' : None,
            'src' : None,
            'build' : None,
            'include' : None,
        },
        'output_file' : 'main',
        'src_ext' : ''
    }
    display_panel_text(
        _create_progress_description(args.lang, args.target_system, end=''),
        stream=console,
        title='INFO',
        border_style='green',
    )
    try:
        if args.lang and args.lang.lower() == 'c':
            data['src_ext'] = '.c'
            data['compiler']['var'] = 'CC'
            langage = args.lang.lower()
        elif args.lang and args.lang.lower() == 'c++':
            langage = args.lang.lower()
            data['compiler']['var'] = 'CXX'
            data['src_ext'] = '.cpp'
        else:
            langage = _choose_langage(data)
            
        _set_directories(
            langage=langage, #type: ignore
            data=data
            )
    
        if args.compiler:
            data['compiler']['name'] = _ensure_compatible_compiler_arg(
                arg='compiler',
                lang=langage, #type: ignore
                value=args.compiler,
            )
        else:
            data['compiler']['name'] = _choose_compiler(langage)
    
        if args.standard:
            data['compiler']['std'] = _ensure_compatible_compiler_arg(
                arg='standard',
                lang=langage, #type: ignore
                value=args.standard,
            )
        else:
            data['compiler']['std'] = _choose_standard(langage).lower()
    
        if args.binary_name:
            data['output_file'] = args.binary_name
        else:
            data['output_file'] = _chose_binary_name()
    
        if args.gui is None:
            _prompt_gui_lib_usage(data, args)
        elif isinstance(args.gui, str):
            _set_gui_lib_flags(data, args)
    
        _generate_makefile(data, args, progress_description=_create_progress_description(langage, args.target_system)) #type: ignore
    except KeyboardInterrupt:
        console.print('\n[bold yellow]→ Exiting...Goodbye[/]')
        sys.exit(0)
import argparse
from pathlib import Path
import sys

from makefile_generator.config import (
    C_STANDARDS,
    COMPILERS,
    CPP_STANDARDS,
    RAYLIB_CFLAGS,
    RAYLIB_FLAGS,
    SDL2_CFLAGS,
    SDL2_FLAGS,
    SFML_CFLAGS,
    SFML_FLAGS,
    TEMPLATES_PATH,
)
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.text import Text
from makefile_generator.utils import get_user_input, single_choice

console = Console()
console_err = Console(stderr=True)


#TODO: make it better
def _generate_makefile(data: dict[str, dict[str, str] | str | bool], args: argparse.Namespace):
    template = None
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_PATH),
        lstrip_blocks=True,
        trim_blocks=True
    )
    if args.cross_platform:
        template = env.get_template('cross-platform.mak.j2')
    else:
        if args.target_system == 'windows':
            template = env.get_template('_WIN32.mak.j2')
        if args.target_system.lower() == 'mac':
            template = env.get_template('__APPLE__.mak.j2')
        if args.target_system.lower() == 'linux':
            template = env.get_template('__linux__.mak.j2')
    if template:
        makefile = template.render(data)
        outdir = Path(args.output_path) if args.output_path else Path.cwd() 
        outdir = outdir / 'Makefile'
        if outdir.exists(): #TODO: make overwrite better (maybe add path change..etc)
            opt = single_choice('A Makefile already exists in output directory.\nDo you wanna overwrite it?', ['yes', 'no'], console)
            if opt == 'no':
                sys.exit(0)
        try:
            with open(outdir , 'wt') as file:
                file.write(makefile)
        except FileNotFoundError:
            console_err.print("[bold red]Error:[/bold red] Output directory does not exist.")
            sys.exit(1)
        
        except PermissionError:
            console_err.print("[bold red]Error:[/bold red] Permission denied while writing the file.")
            sys.exit(1)
        
        except IsADirectoryError:
            console_err.print("[bold red]Error:[/bold red] Output path is a directory, not a file.")
            sys.exit(1)
        
        except OSError as e:
            console_err.print(f"[bold red]Error:[/bold red] Failed to write file: {e}")
            sys.exit(1)
            

def _choose_langage(data: dict) -> str:
    langs = ['c++', 'c']
    choice = single_choice('Choose the Langage', langs, console)
    if choice.lower() == 'c++':
        data['src_ext'] = '.cpp'
        data['compiler']['var'] = 'CXX'
    else:
        data['src_ext'] = '.c'
        data['compiler']['var'] = 'CC'
    return choice

def _choose_compiler() -> str:
    return single_choice('Choose your compiler of use', COMPILERS, console)

def _choose_standard(langage: str) -> str:
    prompt = "Choose the compiler standard you wanna use"
    return single_choice(prompt, C_STANDARDS, console) if langage.lower() == 'c' else single_choice(prompt, CPP_STANDARDS, console)

def _chose_binary_name() -> str :
    return get_user_input("Enter the output binary file's name", console)
    
def get_key_for(target_system: str, /):
    if target_system == 'windows':
        return 'win32'
    else:
        return 'unix'

def _choose_gui_lib(data: dict[str, dict[str, str] | str | bool], args: argparse.Namespace) -> None:
    gui_libs = ['sdl2', 'sfml', 'raylib']
    lib = single_choice('Chose your graphical library of use', gui_libs, console)
    if args.cross_platform:
        if lib == 'sfml':
            data['gui_lib_flags'] = SFML_FLAGS['win32']
            data['unix_gui_lib_flags'] = SFML_FLAGS['unix']
            data['gui_lib_cflags'] = SFML_CFLAGS
        elif lib == 'sdl2':
            data['gui_lib_flags'] = SDL2_FLAGS['win32']
            data['unix_gui_lib_flags'] = SDL2_FLAGS['unix']
            data['gui_lib_cflags'] = SDL2_CFLAGS
        else:
            data['gui_lib_flags'] = RAYLIB_FLAGS['win32']
            data['unix_gui_lib_flags'] = RAYLIB_FLAGS['unix']
            data['gui_lib_cflags'] = RAYLIB_CFLAGS
    else:
        if lib == 'sfml':
            data['gui_lib_flags'] = SFML_FLAGS[get_key_for(args.target_system)]
            data['gui_lib_cflags'] = SFML_CFLAGS
        elif lib == 'sdl2':
            data['gui_lib_flags'] = SDL2_FLAGS[get_key_for(args.target_system)]
            data['gui_lib_cflags'] = SDL2_CFLAGS
        else:
            data['gui_lib_flags'] = RAYLIB_FLAGS[get_key_for(args.target_system)]
            data['gui_lib_cflags'] = RAYLIB_CFLAGS


def _prompt_gui_lib_usage(data:  dict[str, dict[str, str] | str | bool], args: argparse.Namespace) -> None:
    choice = single_choice('Do you intend on using a gui libray?', ['yes', 'no'], console)
    if choice == 'yes':
        data['use_gui_lib'] = True
        _choose_gui_lib(data, args)

def is_target_correct(args: argparse.Namespace) -> bool:
    if args.cross_platform:
        return True
    if args.target_system.lower() == 'windows':
        return True
    if args.target_system.lower() == 'mac':
        return True
    if args.target_system.lower() == 'linux':
        return True
    return False

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
    if not is_target_correct(args):
        _target_err()
    #TODO: add folders check
    langage = ''
    data = {
        'compiler' : {
         'var' : '',
         'name' : '',
         'std' : ''
        },
        'directories' : {
            'bin' : 'bin',
            'src' : 'src',
            'build' : 'build',
            'include' : 'include',
        },
        'output_file' : 'main',
        'src_ext' : ''
    }
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

    if args.compiler and args.compiler.lower() in COMPILERS:
        data['compiler']['name'] = args.compiler
    else:
        data['compiler']['name'] = _choose_compiler()
    if args.standard:
        if langage == 'c':
            if (args.standard in C_STANDARDS or args.standard.lower() == 'c18'):
                data['compiler']['std'] = args.standard.lower()
            else:
                data['compiler']['std'] = _choose_standard(args.lang).lower()
        else:
            if args.standard in CPP_STANDARDS:
                data['compiler']['std'] = args.standard.lower()
            else:
                data['compiler']['std'] = _choose_standard(args.lang).lower()
    else:
        data['compiler']['std'] = _choose_standard(langage).lower()
    if args.binary_name:
        data['output_file'] = args.binary_name
    else:
        data['output_file'] = _chose_binary_name()
    if args.use_gui_lib:
        data['use_gui_lib'] = True
        _choose_gui_lib(data, args.target)
    else:
        _prompt_gui_lib_usage(data, args)
        
    _generate_makefile(data, args)

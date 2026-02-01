'''
sfml static :
    -lsfml-graphics-s -lsfml-window-s -lsfml-system-s -lopengl32 -lgdi32 -lwinmm -lfreetype -luser32

raylib static :
    -lraylib -lopengl32 -lgdi32 -lwinmm -luser32 -lshell32
'''

from importlib.resources import files

CPP_STANDARDS = [
    "C++98",
    "C++03",
    "C++11",
    "C++14",
    "C++17",
    "C++20",
    "C++23"
]
C_STANDARDS = [
    "C89",
    "C90",
    "C95",
    "C99",
    "C11",
    "C17",
    "C18",
    "C23"
]
CPP_COMPILERS = [
    'g++',     
    'clang++', 
    'msvc'
]

C_COMPILERS = [
    'gcc',
    'clang',
    'msvc'
]

WIN32_RESERVED_NAMES = {
    'CON', 
    'PRN', 
    'AUX', 
    'NUL', 
    'COM0',
    'COM1',
    'COM2',
    'COM3',
    'COM4',
    'COM5',
    'COM6',
    'COM7',
    'COM8',
    'COM9',
    'LPT0',
    'LPT1',
    'LPT2',
    'LPT3',
    'LPT4',
    'LPT5',
    'LPT6',
    'LPT7',
    'LPT8',
    'LPT9',
}

SFML_FLAGS = {
    'win32': '-lsfml-graphics -lsfml-window -lsfml-audio -lsfml-system',
    'unix': '$(shell pkg-config --libs sfml-graphics)'
}
SFML_CFLAGS = '$(shell pkg-config --cflags sfml-graphics)'

RAYLIB_FLAGS = {
    'win32': '-lraylib -lopengl32 -lgdi32 -lwinmm',
    'unix': '$(shell pkg-config --libs raylib)'
}
RAYLIB_CFLAGS = '$(shell pkg-config --cflags raylib)'

SDL2_FLAGS = {
    'win32': '-lSDL2main -lSDL2',
    'unix': '$(shell pkg-config --libs sdl2)'
}
SDL2_CFLAGS = '$(shell pkg-config --cflags sdl2)'

TEMPLATES_DIR = files('makefile_generator') / 'templates'

TEMPLATES = {
    'windows': '_WIN32.mak.j2',
    'linux': '__linux__.mak.j2',
    'mac': '__APPLE__.mak.j2',
    'cross-platform' : 'cross-platform.mak.j2'
}


'''
sfml static :
    -lsfml-graphics-s -lsfml-window-s -lsfml-system-s -lopengl32 -lgdi32 -lwinmm -lfreetype -luser32

raylib static :
    -lraylib -lopengl32 -lgdi32 -lwinmm -luser32 -lshell32
'''

from importlib.resources import files

PROFILES = {
    'c': {
        'standards': ['c89', 'c90', 'c95', 'c99', 'c11', 'c17', 'c18', 'c23'],
        'compilers': ['gcc', 'clang']
    },
    'c++': {
        'standards': ['c++98', 'c++03', 'c++11', 'c++14', 'c++17', 'c++20', 'c++23'],
        'compilers': ['g++', 'clang++']
    }
}

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


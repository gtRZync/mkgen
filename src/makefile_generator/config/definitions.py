'''
sfml static :
    -lsfml-graphics-s -lsfml-window-s -lsfml-system-s -lopengl32 -lgdi32 -lwinmm -lfreetype -luser32

raylib static :
    -lraylib -lopengl32 -lgdi32 -lwinmm -luser32 -lshell32
'''

from pathlib import Path

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
    "C23"
]
COMPILERS = [
    "gcc",      # GNU C Compiler
    "g++",      # GNU C++ Compiler
    "clang",    # Clang C Compiler
    "clang++",  # Clang C++ Compiler
    "cl",       # MSVC (Microsoft Visual C++)
    "icx",      # Intel oneAPI C Compiler
    "icpx"      # Intel oneAPI C++ Compiler
]

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

TEMPLATES_PATH = Path('src/makefile_generator/templates')

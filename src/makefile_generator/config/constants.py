'''
sfml static :
    -lsfml-graphics-s -lsfml-window-s -lsfml-system-s -lopengl32 -lgdi32 -lwinmm -lfreetype -luser32

raylib static :
    -lraylib -lopengl32 -lgdi32 -lwinmm -luser32 -lshell32
'''

from importlib.resources import files

MKGEN_CONFIG_FILE = 'mkgen.toml'
CACHED_CONFIG_FILE = 'cached_config.json'
COMPILED_DIR = 'MkgenFiles'
MKCACHE = 'mkcache.txt'
MAKEFILE = 'build.mk'
SOURCES = 'sources.mk'
MODULE = '.module'
TEST = '.test'
PUBLIC = '.public'
EXTERNAL = '.external'

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

TEMPLATES_DIR = files('makefile_generator') / 'templates'

TEMPLATES = {
    'win32': 'windows.mk.j2',
    'unix': 'unix.mak.j2',
}

PROJECT_KINDS = {'binary', 'static', 'shared'}
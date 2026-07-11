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

SUPPORTED_FEATURES = {'sdl2', 'sfml', 'raylib'}
SUPPORTED_LANGUAGES = {'c++', 'c'}

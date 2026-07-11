import argparse
from pathlib import Path

from makefile_generator.config.constants import MKGEN_CONFIG_FILE
from makefile_generator.utils.display_utils import success, warning

MKGEN_TEMPLATE = '''\
[project]
name = 'project-name'
kind = 'binary'  # binary | static | shared (only binary for now)
language = 'c++' # c | c++

[build]
compiler = 'g++'
standard = 'c++17'
cflags = [
    '-Wall',
    '-Werror',
]
ldflags = []

include_dirs = []

features = []

'''

def init(args: argparse.Namespace) -> None:
    root = args.root
    file = root / MKGEN_CONFIG_FILE
    if file.exists() and file.stat().st_size > 0 and not args.force:
        warning(f'[magenta]{file.name!r}[/magenta] already exists.')
        return
    
    file.write_text(MKGEN_TEMPLATE, encoding='utf-8')
    success(f'Config file [magenta]{MKGEN_CONFIG_FILE!r}[/magenta] generated in project root.')
    
def main() -> None:
    args = argparse.Namespace(root=Path('.'))
    init(args)

if __name__ == '__main__':
   main()
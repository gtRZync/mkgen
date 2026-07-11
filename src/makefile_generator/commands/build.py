import argparse
import shutil
import subprocess
from pathlib import Path

from makefile_generator.commands.regenerate import regenerate
from makefile_generator.config import MAKEFILE
from makefile_generator.utils.display_utils import error


def _try_update_sources(args: argparse.Namespace) -> None:
    regenerate(args)

def _command_exists(cmd: str) -> bool:
    ret = shutil.which(cmd)
    return ret is not None  

def build(args: argparse.Namespace) -> None:
    makefile_path = Path(args.build_dir) / MAKEFILE
    target = args.target if args.target else 'all'
    cmd = ['make', '-f', makefile_path]
    if args.parallel:
        cmd.append( f'-j{args.parallel}')
    cmd.append(target)
    
    if not _command_exists('make'):
        error("Command 'make' is not installed!")
    
    _try_update_sources(args)
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.SubprocessError:
        pass

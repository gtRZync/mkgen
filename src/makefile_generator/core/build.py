import argparse
import os
import subprocess
from pathlib import Path

from makefile_generator.config import MAKEFILE


def get_processor_total_cpu_cores() -> int:
    return os.cpu_count() or 1


def build(args: argparse.Namespace) -> None:
    makefile_path = Path(args.build_dir) / MAKEFILE
    target = args.target if args.target else 'all'
    cmd = ['make', '-f', makefile_path]
    if args.parallel:
        cmd.append( f'-j{get_processor_total_cpu_cores()}')
    cmd.append(target)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.SubprocessError:
        pass

def main() -> None:
    args = argparse.Namespace(build_dir='build', parallel=False)
    build(args)


if __name__ == '__main__':
    main()

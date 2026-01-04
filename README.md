<div align="center">
    <img src="img/banner.png"></img>
<h1> mkgen (MakefileGenerator) </h1>
</div>


**mkgen** is a lightweight **Makefile generator** designed for my everyday C and C++ workflow.

I often start with a *small* C or C++ file. Then it grows. Suddenly there are multiple `.c` / `.cpp` files, header files, and sometimes a graphical library involved. At that point, compiling manually or rewriting a Makefile becomes repetitive and annoying.

So I built **mkgen**.

It’s written in **Python** and focuses on **C and C++ projects**, with optional support for graphical libraries when needed.

---

## Why mkgen?

* I like coding in **C and C++**
* Small projects tend to grow faster than expected
* Writing Makefiles over and over is tiring
* Linking multiple source files and libraries manually is error‑prone

mkgen automates the boring part so I can focus on writing code.

---

## Features

* Automatically generates a **Makefile** for C and C++ projects
* Detects multiple source files and header files
* Supports both **C** and **C++** compilation
* Designed to scale from tiny projects to larger ones
* Optional / conditional support for **graphical libraries**
* Simple and minimal by design

---

## Typical Use Case

1. Start a small C or C++ project
2. Add more `.c` / `.cpp` files over time
3. Add headers, maybe a graphical library
4. Run `mkgen generate`
5. Get a ready‑to‑use Makefile after the interactive menu

No manual compilation. No rewriting Makefiles.

---

## Philosophy

mkgen is not meant to replace advanced build systems like CMake or Meson.

It is meant to be:

* **Simple**
* **Fast**
* **Opinionated toward C/C++**
* Easy to understand and modify

It exists because *I needed it*.

---

## Requirements

* Python 3.x
* A C compiler (`gcc`, `clang`, etc.)
* or a C++ compiler (`g++`, `clang++`)

---

## Usage

1. Clone the repository:

```sh
git clone https://github.com/gtRZync/mkgen.git
```

```sh
cd mkgen
```

2. Install globally for convenience:

```sh
pip install .
```

3. You're finally ready to generate your Makefiles on the go :

```sh
mkgen generate
```

or 

```sh
mkgen generate <system>
```

or even

```sh
mkgen generate --cross-platform
```

4. Follow the interactive menu and boom a Makefile will appear at the specified output path or current working directory

## Arguments

### Optional positional argument
| Argument          | Description                                                                                 | Default |
|------------------|---------------------------------------------------------------------------------------------|---------|
| `target_system`   | Specify the system/OS for which the Makefile should be generated (e.g., `linux`, `windows`, `macos`). ⚠️ Mutually exclusive with `--cross-platform`. | Current system/OS |

### Optional keyword arguments (flags)
| Argument                     | Description                                                                                                                   | Default |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------|----------------|
| `--cross-platform`            | Generate a Makefile that works across multiple systems. ⚠️ Cannot be used with `target_system`.                                 | Disabled |
| `-l`, `--lang`                | Specify the programming language to use. Supported: `C` or `C++`.                                                             | None           |
| `-c`, `--compiler`            | Specify the compiler to use. This value will be written into the generated Makefile.                                           | None           |
| `-std`, `--standard`          | Specify the language standard to use (e.g., c11, c17, c++11, c++17, c++20). Added to compiler flags in the Makefile.          | None           |
| `--use-gui-lib`               | Include GUI library flags in compilation. Supported libs: `SDL2`, `SFML`, `RAYLIB`.                                           | Disabled       |
| `-o`, `--output`              | Specify the output directory for the Makefile. Defaults to current working directory if path is invalid.                       | `./`           |
| `--binary-name`               | Specify the name of the output binary/executable. The Makefile will use this name for the compiled program.                     | None           |



## Usage examples:

### Defaults to current system

```sh
mkgen generate
```

### Providing the optional positional argument

```sh
mkgen generate linux
```

### Using optional flags

```sh
mkgen generate linux --lang C++ -c clang++ -std c++17 --use-gui-lib -o ./build --binary-name my_app
```

### Using cross-platform mode instead of target_system

```sh
mkgen generate --cross-platform --lang C
```

## Status

This is a personal tool built for real projects. Features may evolve as my workflow evolves.


<p align="center"><a href="https://github.com/gtRZync/makefile-generator/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&colorA=1e1e2e&colorB=89b4fa"/></a></p>

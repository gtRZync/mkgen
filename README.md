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
4. Run `mkgen generate --target-system <system>`
5. Get a ready‑to‑use Makefile

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

1. Clone the repository or grab the zipped repository:

```sh
git clone https://github.com/gtRZync/mkgen.git
```

```sh
cd makefile-generator
```

2. Install globally for convenience:

```sh
pip install .
```

3. You're finally ready to generate your Makefiles on the go :

```sh
mkgen generate --target-system <system>
```

or 

```sh
mkgen generate --cross-platform
```

## Arguments:

### `--target-system`  
Specify the system/OS for which the Makefile should be generated (e.g., `linux`, `windows`, `macos`).  
> ⚠️ This argument is mutually exclusive with `--cross-platform`.  

> [!NOTE]
> This argument is `required`

**Example:** 
```sh
mkgen generate --target-system <system>
```

### `--cross-platform`  
Generate a Makefile that works across multiple systems.  
> ⚠️ Cannot be used together with `--target-system-system`.  
**Example:** 
```sh
mkgen generate --cross-platform
```

### `-l` / `--lang`
Specify the programming language to use. Supported options: `C` or `C++`.  
**Example:** 
```sh
mkgen generate --target-system <system> --lang c++
```

### `-c` / `--compiler`
Specify the compiler to use. This value will be written into the generated Makefile as the compiler for building the project.
**Example`:** 
```sh
mkgen generate --target-system <system> --compiler clang++
```

### `-std` / `--standard`
Specify the language standard to use (e.g., c11, c17, c++11, c++17, c++20). This will be added to the compiler flags in the Makefile.
**Example:** 
```sh
mkgen generate --target-system <system> -std c++17
```

### `--use-gui-lib`  
Include GUI library flags in the compilation process. When enabled, the generated Makefile will add the necessary GUI library linker flags and/or `--cflags` for compilation. Supported gui lib for now maybe: `SDL2`, `SFML` and `RAYLIB`.  
**Example:** 
```sh
mkgen generate --target-system <system> --use-gui-lib
```

### `--output-path`  
Specify the output directory where the makefile will be generated at (current directory is used if path is faulty).
**Example:** 
```sh
mkgen generate --target-system <system> --output-path path/to/directory
```

### `--binary-name`  
Specify the name of the output binary/executable. The generated Makefile will use this name for the compiled program.  
**Example:** 
```sh
mkgen generate --target-system <system> --binary-name my_app
```

> [!NOTE]
> All arguments are optional unless explicitly stated as required.


## Status

This is a personal tool built for real projects. Features may evolve as my workflow evolves.

---

## License

<p align="center"><a href="https://github.com/gtRZync/makefile-generator/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&colorA=1e1e2e&colorB=89b4fa"/></a></p>

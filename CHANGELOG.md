# Changelog

All versions below are listed in reverse chronological order.

### v0.6.0 (2026-07-11)

## Major Architecture Refactor

This release is a complete rewrite of the project's core architecture.

### Why?

Previous versions relied on automatic project discovery to infer the source tree, include directories, and project layout before generating a Makefile. While convenient for simple projects, this approach became increasingly difficult to maintain and produced unpredictable results as projects grew more complex.

The generator now uses an explicit, configuration-driven workflow built around project configuration files and anchor files. This makes project discovery deterministic, scalable, and significantly easier to reason about.

## New Features

### New project initialization

Added an `init` command to initialize a project configuration.

The generated configuration file defines the project and serves as the foundation for future Makefile generation.

### Anchor file support

Projects now use anchor files to explicitly identify important directories instead of relying on automatic directory discovery.

Anchor files are empty marker files that identify the role of a directory. They do not require any content and only need to exist.

Current anchor files include:

* `.module` — Marks a module directory.
* `.public` — Marks a directory containing public header files.
* `.external` — Reserved for future support of external dependencies.
* `.test` — Reserved for future support of test directories.

This explicit approach removes ambiguity from project discovery and provides a predictable, scalable foundation for Makefile generation.

### Rebuilt Makefile generation

The `generate` command has been completely redesigned.

Instead of attempting to infer the entire project layout automatically, it now generates Makefiles from the project configuration and anchor files, resulting in predictable and scalable output.

### Build command

Added a new `build` command.

Before invoking `make`, the tool validates the project's generated source lists. If new modules, public headers, source files, or other tracked project components have been added or removed, the generated Makefile fragments are automatically regenerated. Otherwise, the existing generated files are reused and the project is built immediately.

This keeps generated files synchronized with the project structure without requiring users to manually regenerate them after every structural change.

### Version command

The `version` command remains available.

## Breaking Changes

* The automatic project discovery system has been removed.
* Existing projects using the previous workflow will need to be reinitialized.
* Makefile generation now requires a project configuration file created with `init`.
* Projects must define the required anchor files for the generator to identify important directories.

## Internal Changes

* Refactored the project architecture from the ground up.
* Reworked the generation pipeline to support explicit project configuration.
* Improved scalability for larger and more complex C/C++ projects.
* Simplified the internal design, making future features and maintenance easier.

### Configuration cache

Implemented a configuration cache to avoid repeatedly parsing the project configuration during command execution.

The cache stores preprocessed project metadata, including resolved directories and file modification timestamps, allowing commands such as `build` to quickly determine whether generated files need to be refreshed.

This reduces unnecessary filesystem scans and improves overall performance, especially for larger projects.

### Improved incremental workflow

The tool now combines cached project metadata with filesystem timestamps to detect structural changes efficiently. Generated source lists are only rebuilt when necessary, reducing redundant work while ensuring the generated Makefiles remain synchronized with the project.

### v0.5.4 (2026-02-05)
#### Improved
- `--portable` is now available as a shorter alias for `--cross-platform`
- Updated usage texts to include `--portable` alongside `--cross-platform`
- `--standard` and `--compiler` argument handling updated: now use `dest='standards'` and `dest='compilers'` for consistency with `PROFILES`. `LanguageAction` simplified to use `self.dest` directly.
- Refactored `_ensure_compatible_compiler_arg()` to align with the new `PROFILES` system and updated argument dests.
Error messages now indicate both the invalid value and the relevant language (e.g., `Invalid standard 'c++17' for 'C'`).
Interactive prompts now show the language context: e.g., “Select C compiler” or “Select C++ compiler” instead of generic prompts.

#### Removed
- Dropped **`MSVC`** support. Its **`build system`** and **`compiler conventions`** require **`significant adjustments`** for Makefile-based workflows, which are not the focus of this tool, targeting general-purpose editors like **`VS Code`**, **`ZED`**, and similar.

#### Added
- Introduced `PROFILES` dictionary to unify compiler and standard configurations for C and C++. This replaces the separate `C_STANDARDS`, `CPP_STANDARDS`, `C_COMPILERS`, and `CPP_COMPILERS` lists, simplifying Makefile generation and flag normalization.


### v0.5.3 (2026-02-04)
#### Added
- Support for `Mac OS` / `mac_os` as a valid `target_system` CLI argument.
- Case- and format-insensitive normalization of `target_system`.
- Path validation in the "new path" option:
  - Warn if `Makefile` already exists in the target directory.
  - Warn if the path is not a directory.
  - Warn if the path does not exist.
  - Prevent the user from “choosing” the old save directory again

#### Fixed
- Safer rename behavior on Windows by preventing filenames that end with a dot.
- Provide detailed error instead of generic "invalid input" when renaming or choosing a new path for the Makefile


### v0.5.2 - Initial Tracking Baseline
#### Added
- Baseline version for changelog tracking.

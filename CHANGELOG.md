# Changelog

All versions below are listed in reverse chronological order.

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

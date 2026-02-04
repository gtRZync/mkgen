# Changelog

All versions below are listed in reverse chronological order.

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

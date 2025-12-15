# Project Conventions

## 1. Environment & Packaging
- **Devbox is King:** All system dependencies must be added via `devbox add`. Do not assume tools exist outside the devbox shell.
- **Nix Compatibility:** The code must run within a read-only Nix store context if packaged. Do not attempt to write to `__dirname` or relative paths for persistent storage; use `tempfile` or user-specified output paths.

## 2. Python Coding Standards
- **Type Hinting:** Use Python 3.11+ type hints for all function signatures.
- **Path Handling:** Always use `pathlib.Path` instead of `os.path`.
- **Error Handling:** - **Graceful Failure:** If a single image is corrupt, log a warning (stderr) and SKIP it. Do not crash the entire process.
  - **JSON/Video:** Explicitly ignore non-image files found in Google Photos zips.

## 3. Libraries
- **PDF Generation:** Strict usage of `img2pdf`. Do not use libraries that re-encode JPEGs (like ReportLab) unless absolutely necessary for text overlays.
- **HEIC Support:** Use `pillow-heif` to handle Apple/Google format photos.

## 4. CLI UX
- **Progress:** Always use `tqdm` for long-running loops (extraction, processing, saving).
- **Verbosity:** Default to "clean" output (progress bar only). Use a `--verbose` flag for debug logs.

## 5. Infrastructure & Config (READ-ONLY)
- **Do NOT modify** `devbox.json`, `pyproject.toml`, or `poetry.lock`.
- **Assumption:** The environment, libraries, and C-bindings are already correctly configured.
- **Action:** If you hit an `ImportError` or `ModuleNotFound`, report it to the user. Do **not** attempt to fix it by rewriting the Devbox config.

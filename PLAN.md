# Implementation Plan

## Phase 1: Skeleton & CLI
- [ ] Create `main.py` entry point.
- [ ] Implement `argparse` to handle `-i/--input` (ZIP path) and `-o/--output` (PDF path/dir).
- [ ] Validate input file existence and extension.

## Phase 2: Extraction & Sorting
- [ ] Implement `tempfile.TemporaryDirectory` context manager.
- [ ] Extract ZIP contents with a progress bar.
- [ ] specific filtering logic:
    - Include: `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`, `.webp`
    - Exclude: `.json`, `.mp4`, `.mov`, `.gif` (optional, decide if PDFs should have gifs)
- [ ] Sort file list alphanumerically.

## Phase 3: Image Processing
- [ ] Create a converter function: `prepare_image(path) -> path`.
    - If HEIC: Convert to JPG, save to temp, return new path.
    - If JPG/PNG: Return original path.
- [ ] Implement error handling wrapper: try/except around image opening to catch corrupt files.

## Phase 4: PDF Generation
- [ ] Pass the list of prepared image paths to `img2pdf`.
- [ ] Write bytes to the target output file.
- [ ] Ensure correct naming convention if `-o` was a directory or omitted.

## Phase 5: Packaging
- [ ] Create `flake.nix` (or configure `devbox.json` to generate it).
- [ ] Verify `nix run . -- --help` works.

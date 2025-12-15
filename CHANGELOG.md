# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2025-12-15

### Added
- Initial public release
- Direct ZIP file processing without manual extraction
- HEIC/HEIF format support with automatic conversion to JPEG
- Smart filtering to ignore JSON metadata, videos, and other non-image files
- Alphanumeric sorting of images for correct page ordering
- Lossless JPEG embedding using img2pdf
- Progress bars for extraction and processing (tqdm)
- Graceful handling of corrupt images (skip with warning)
- Verbose mode (`-v/--verbose`) for detailed logging
- Nix flake for easy installation and distribution
- Comprehensive test suite with pytest
- Development environment using Devbox and Poetry

### Features
- CLI with `-i/--input` for ZIP path
- CLI with `-o/--output` for PDF destination (file or directory)
- Automatic output path determination (defaults to input name with .pdf extension)
- Recursive search for images within ZIP subdirectories
- Support for `.jpg`, `.jpeg`, `.png`, `.heic`, `.heif`, `.webp` formats
- Memory-efficient temporary file handling

### Documentation
- Comprehensive README with usage examples
- Nix installation instructions (temporary run and permanent install)
- Development setup guide
- Project conventions and implementation plan

## [0.1.8] - 2024-01-XX

### Added
- Initial development version
- Basic ZIP to PDF conversion functionality

[Unreleased]: https://github.com/andrey-stepantsov/google-photos-pdf/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/andrey-stepantsov/google-photos-pdf/releases/tag/v0.3.0
[0.1.8]: https://github.com/andrey-stepantsov/google-photos-pdf/releases/tag/v0.1.8

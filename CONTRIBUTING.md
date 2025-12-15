# Contributing to Google Photos PDF Converter

Thank you for considering contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Install Devbox**: Follow instructions at https://www.jetpack.io/devbox/docs/installing_devbox/

2. **Clone and setup**:
   ```bash
   git clone <repo-url>
   cd google-photos-pdf
   devbox shell
   poetry install
   ```

3. **Verify setup**:
   ```bash
   pytest tests/ -v
   python main.py --help
   ```

## Coding Standards

All contributions must follow the guidelines in [CONVENTIONS.md](CONVENTIONS.md):

- ✅ Use Python 3.11+ type hints
- ✅ Use `pathlib.Path` instead of `os.path`
- ✅ Handle errors gracefully (skip corrupt images, don't crash)
- ✅ Use `tqdm` for progress bars
- ✅ Use `img2pdf` for PDF generation (no re-encoding)

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Follow conventions in `CONVENTIONS.md`
- Add tests for new functionality
- Update documentation if needed

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=main --cov-report=term-missing

# Ensure all tests pass before committing
```

### 4. Commit Your Changes

Use conventional commit messages:

```bash
# Features
git commit -m "feat: add support for GIF images"

# Bug fixes
git commit -m "fix: handle empty ZIP files gracefully"

# Documentation
git commit -m "docs: update installation instructions"

# Tests
git commit -m "test: add tests for HEIC conversion"

# Refactoring
git commit -m "refactor: simplify image filtering logic"

# Chores
git commit -m "chore: update dependencies"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots if UI/output changes

## Testing Guidelines

### Writing Tests

- Place tests in `tests/test_main.py`
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Use fixtures from `tests/conftest.py` when possible
- Test both success and failure cases

Example:
```python
def test_validate_input_missing_file(self):
    """Should exit if file doesn't exist."""
    with pytest.raises(SystemExit):
        validate_input(Path("/nonexistent/file.zip"))
```

### Running Specific Tests

```bash
# Single test
pytest tests/test_main.py::TestValidateInput::test_validate_input_missing_file -v

# Test class
pytest tests/test_main.py::TestValidateInput -v

# With output
pytest tests/ -v -s
```

## Adding Dependencies

### Python Dependencies

```bash
# Add runtime dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name
```

**Do NOT modify** `devbox.json`, `pyproject.toml`, or `poetry.lock` manually.

### System Dependencies

System dependencies must be added via Devbox:

```bash
devbox add package-name
```

## Version Bumping

Use the automated script:

```bash
# Patch: 0.1.1 -> 0.1.2 (bug fixes)
./bump_version.sh patch

# Minor: 0.1.1 -> 0.2.0 (new features)
./bump_version.sh minor

# Major: 0.1.1 -> 1.0.0 (breaking changes)
./bump_version.sh major
```

The script will:
1. Check git is clean
2. Run all tests
3. Update version files
4. Commit and tag
5. Push to origin

## Pull Request Checklist

Before submitting a PR, ensure:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code follows conventions in `CONVENTIONS.md`
- [ ] New features have tests
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventional format
- [ ] No unnecessary files committed (check `.gitignore`)
- [ ] Branch is up to date with main

## Code Review Process

1. Maintainer reviews code
2. Automated tests run via CI (if configured)
3. Feedback addressed
4. PR approved and merged

## Questions?

- Check [CONVENTIONS.md](CONVENTIONS.md) for coding standards
- Check [USAGE.md](USAGE.md) for usage examples
- Open an issue for questions or discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

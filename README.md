# MyLang

A small, prototype-based, indentation-sensitive object language inspired by Io and Smalltalk.

## Overview

MyLang v0.4 is a minimalist language featuring:
- **Prototype-based** object model (no classes)
- **Message-oriented** programming
- **Indentation-sensitive** syntax
- **Explicit self** in methods
- Built-in types: Number, Boolean, String

See [SPEC.md](SPEC.md) for the complete language specification (v0.4).

## Development Setup

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/quosa/MyLang.git
cd MyLang

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=mylang --cov-report=term-missing

# Run specific test file
pytest tests/test_version.py
```

### Linting

```bash
# Check code style
ruff check src tests

# Format code
ruff format src tests
```

### CI/CD

The project uses GitHub Actions for continuous integration:
- **Linting**: Runs `ruff` on all Python code
- **Testing**: Runs `pytest` across Python 3.10, 3.11, and 3.12
- Triggers on all pull requests and pushes to main

## Project Structure

```
MyLang/
├── src/mylang/          # Interpreter source code
│   └── __init__.py
├── tests/               # Test suite
│   └── test_version.py
├── SPEC.md              # Language specification v0.3
├── pyproject.toml       # Project configuration
└── README.md
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

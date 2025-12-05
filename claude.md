# MyLang Development Instructions for Claude

This document contains the standard development workflow for MyLang features using Test-Driven Development (TDD).

## TDD Workflow: Red-Green-Refactor

Follow this cycle for all new features:

### 1. RED Phase - Write Failing Tests

Before implementing any feature, write comprehensive tests that describe the expected behavior.

**Steps:**
1. Create test files in the appropriate `tests/` subdirectory
2. Write tests that cover:
   - Basic functionality
   - Edge cases
   - Error conditions
   - Integration with existing features
3. Run tests and verify they **all fail** (RED)

**Example:**
```bash
# Write tests first
python -m pytest tests/test_runtime/test_objects.py -v
# Expected: All tests should fail (module not found, etc.)
```

### 2. GREEN Phase - Implement Minimal Code

Write the **minimal** code necessary to make all tests pass.

**Steps:**
1. Create the necessary modules and classes
2. Implement only what's needed to pass the tests
3. Don't add extra features or optimizations
4. Run tests and verify they **all pass** (GREEN)

**Example:**
```bash
# Implement the minimal code
# Then run tests
python -m pytest tests/test_runtime/test_objects.py -v
# Expected: All tests should pass
```

### 3. REFACTOR Phase - Improve Code Quality

Once tests pass, improve the code while keeping tests green.

**Steps:**
1. Run linter: `ruff check src tests`
2. Fix any linting issues: `ruff check --fix src tests`
3. Run full test suite with coverage: `python -m pytest -p pytest_cov --cov=mylang --cov-report=term-missing -v`
4. Analyze code for improvements:
   - Remove duplication
   - Improve naming
   - Add documentation
   - Optimize if needed
5. Run tests after each refactoring to ensure they stay green

**Example:**
```bash
# Lint the code
ruff check src tests

# Auto-fix issues
ruff check --fix src tests

# Run full test suite with coverage
python -m pytest -p pytest_cov --cov=mylang --cov-report=term-missing -v

# Expected: 100% coverage, all tests pass
```

## Development Setup

### Initial Setup

```bash
# Install package with dev dependencies
pip install -e ".[dev]"

# Verify installation
python -m pytest --version
ruff --version
```

### Running Tests

```bash
# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest tests/test_runtime/test_objects.py -v

# Run with coverage
python -m pytest -p pytest_cov --cov=mylang --cov-report=term-missing -v

# Run specific test class
python -m pytest tests/test_runtime/test_objects.py::TestObjectCloning -v

# Run specific test
python -m pytest tests/test_runtime/test_objects.py::TestObjectCloning::test_clone_creates_new_object -v
```

### Running Linter

```bash
# Check code style
ruff check src tests

# Auto-fix issues
ruff check --fix src tests

# Check specific file
ruff check src/mylang/runtime/objects.py
```

### Running Coverage

```bash
# Generate coverage report
python -m pytest -p pytest_cov --cov=mylang --cov-report=html

# Open HTML coverage report
# The report is generated in htmlcov/index.html
```

## Feature Development Checklist

When implementing a new feature, follow this checklist:

- [ ] **Plan**: Understand requirements and design approach
- [ ] **Write Tests** (RED): Create comprehensive failing tests
- [ ] **Verify RED**: Run tests and confirm they fail
- [ ] **Implement** (GREEN): Write minimal code to pass tests
- [ ] **Verify GREEN**: Run tests and confirm they pass
- [ ] **Lint**: Run `ruff check --fix src tests`
- [ ] **Coverage**: Verify 100% coverage for new code
- [ ] **Refactor**: Improve code while keeping tests green
- [ ] **Document**: Update architecture docs if needed
- [ ] **Commit**: Create clear, descriptive commit message
- [ ] **Push**: Push branch for PR

## Example: Object Cloning Feature

This example shows how the object cloning feature was developed:

### 1. RED - Write Tests

```python
# tests/test_runtime/test_objects.py
def test_clone_creates_new_object():
    """Test that clone() creates a new object instance."""
    from mylang.runtime.objects import MyLangObject

    original = MyLangObject()
    clone = original.clone()

    assert clone is not None
    assert clone is not original
```

Run: `python -m pytest tests/test_runtime/test_objects.py -v`
Result: **FAIL** - ModuleNotFoundError

### 2. GREEN - Implement

```python
# src/mylang/runtime/objects.py
class MyLangObject:
    def __init__(self, proto=None):
        self.slots = {}
        self.proto = proto

    def clone(self):
        return MyLangObject(proto=self)
```

Run: `python -m pytest tests/test_runtime/test_objects.py -v`
Result: **PASS** - All tests green

### 3. REFACTOR - Improve

```bash
# Lint and fix
ruff check --fix src tests

# Verify coverage
python -m pytest -p pytest_cov --cov=mylang --cov-report=term-missing -v

# All checks pass, 100% coverage
```

## Git Workflow

### Committing Changes

```bash
# Check status
git status

# Add changes
git add src/mylang/runtime/
git add tests/test_runtime/

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
Add object cloning to runtime system

Implement MyLangObject with prototype-based cloning:
- Objects can clone themselves
- Clones maintain prototype links
- Slot lookup walks prototype chain
- 100% test coverage

Tests: 25 passing
Coverage: 100%
EOF
)"
```

### Pushing Changes

```bash
# Push to feature branch
git push -u origin <branch-name>
```

## Code Quality Standards

### Required for All PRs

1. **All tests must pass** - No failing tests allowed
2. **Lint must pass** - No ruff errors
3. **100% coverage** - All new code must be tested
4. **Documentation** - All public APIs documented
5. **Type hints** - All functions have type annotations

### Code Style

- Follow PEP 8 (enforced by ruff)
- Use descriptive variable names
- Keep functions small and focused
- Add docstrings to all public APIs
- Use type hints for clarity

## Architecture References

- **Language Spec**: `SPEC.md` - MyLang language specification
- **Architecture**: `ARCHITECTURE.md` - System architecture and design
- **Examples**: `examples/` - Example MyLang programs

## Next Steps for New Features

After completing object cloning, the next features to implement (in order):

1. **VM Primitives** (`runtime/vm.py`):
   - `vm_clone()` - Primitive clone operation
   - `vm_print()` - Primitive print operation
   - Bootstrap Object prototype with clone and print methods

2. **Built-in Types** (`runtime/builtins.py`):
   - Number prototype with arithmetic
   - Boolean prototype with conditionals
   - String prototype with operations
   - Autoboxing for literals

3. **Parser** (`parser/`):
   - Lexer with tokenization
   - Indentation handling
   - AST generation

4. **Interpreter** (`interpreter/`):
   - Expression evaluation
   - Message dispatch
   - Environment and scoping

5. **REPL** (`repl/`):
   - Interactive shell
   - Multi-line input
   - Error recovery

6. **Script Runner** (`runner/`):
   - File execution
   - Error reporting
   - CLI interface

## Troubleshooting

### Pytest Coverage Plugin Not Loading

If you see `unrecognized arguments: --cov=mylang`, use:
```bash
python -m pytest -p pytest_cov --cov=mylang --cov-report=term-missing -v
```

### Import Errors in Tests

Make sure package is installed in editable mode:
```bash
pip install -e ".[dev]"
```

### Ruff Errors

Auto-fix most issues:
```bash
ruff check --fix src tests
```

For remaining errors, fix manually based on error messages.

## Summary

**Remember:** Red → Green → Refactor

1. ❌ **RED**: Write failing tests
2. ✅ **GREEN**: Make tests pass with minimal code
3. ♻️ **REFACTOR**: Improve code while keeping tests green

Always commit when tests are green and linting passes!

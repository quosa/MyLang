# MyLang Interpreter Architecture

## Overview

This document describes the architecture for the MyLang interpreter, supporting both script execution (`.mylang` files) and an interactive REPL.

## Design Principles

1. **Simplicity First**: Start with minimal implementation, add complexity only when needed
2. **Test-Driven**: Red-Green-Refactor cycle for all features
3. **Prototype-based**: Everything is an object, objects clone objects
4. **Message-oriented**: All computation happens through message sends

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         REPL / Script Runner            │
│  (User Interface Layer)                 │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           Interpreter                   │
│  (Execution Engine)                     │
│  - Message dispatch                     │
│  - Method lookup                        │
│  - Control flow (ifTrue, whileTrue)     │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Runtime / VM                   │
│  (Object System)                        │
│  - Object representation                │
│  - Prototype chain                      │
│  - Built-in types                       │
│  - VM primitives                        │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│            Parser                       │
│  (Syntax Analysis)                      │
│  - Lexer (tokenization)                 │
│  - Parser (AST generation)              │
│  - Indentation handling                 │
└─────────────────────────────────────────┘
```

## Core Components

### 1. Object System (`runtime/objects.py`)

The foundation of MyLang's prototype-based object model.

**MyLangObject**: Base class for all MyLang objects
- `slots`: Dict[str, Any] - Object's properties and methods
- `proto`: Optional[MyLangObject] - Prototype reference for inheritance
- `clone()` -> MyLangObject - Creates a new object with self as prototype
- `get_slot(name)` -> Any - Looks up slot in self and prototype chain
- `set_slot(name, value)` -> None - Sets slot on self

**Built-in Prototypes**:
- `Object`: Root prototype, provides `clone` and `print` methods
- `Number`: Numeric values with arithmetic operations
- `Boolean`: True/false values with conditional logic
- `String`: Text values with string operations

**Design Decisions**:
- Objects are dictionaries with prototype links
- Slot lookup walks the prototype chain (self → proto → proto.proto → ...)
- Methods are Python callables stored in slots
- Self is explicitly passed to all methods

### 2. VM Primitives (`runtime/vm.py`)

Provides the minimal set of primitives needed to bootstrap the object system.

**Primitives**:
- `vm_clone(obj: MyLangObject)` -> MyLangObject - Creates prototype-linked clone
- `vm_print(obj: MyLangObject)` -> None - Outputs object to console

**Bootstrap Process**:
1. Create base `Object` prototype
2. Add `clone` method to Object (calls vm_clone)
3. Add `print` method to Object (calls vm_print)
4. Create Number, Boolean, String prototypes (all clone Object)
5. Add type-specific methods to each prototype

### 3. Parser (`parser/lexer.py`, `parser/parser.py`)

Converts MyLang source code into an Abstract Syntax Tree (AST).

**Lexer** (`lexer.py`):
- Tokenizes source: identifiers, numbers, strings, keywords, operators
- Handles indentation (INDENT/DEDENT tokens)
- Tracks line/column positions for error messages

**Parser** (`parser.py`):
- Recursive descent parser following EBNF grammar from SPEC.md
- Generates AST nodes representing program structure
- Validates syntax and reports errors

**AST Nodes** (`parser/ast_nodes.py`):
- `Program`: Top-level container for statements
- `Assignment`: `name = expr`
- `MethodDef`: `receiver method = body`
- `Message`: `receiver method arg1 arg2 ...`
- `Literal`: Numbers, strings, booleans
- `Identifier`: Variable/method names
- `Block`: Indented statement sequence ending in `return`

### 4. Interpreter (`interpreter/interpreter.py`)

Executes AST nodes in the context of the runtime environment.

**Interpreter**:
- `eval(node: ASTNode, env: Environment)` -> Any - Evaluates AST node
- Handles message dispatch with argument consumption
- Implements control flow (ifTrue/ifFalse, whileTrue)
- Manages environment (variable bindings)

**Environment**:
- Stack of scopes for variable lookup
- Global scope contains built-in prototypes (Object, Number, Boolean, String)
- Local scopes for method execution
- Special binding for `self` in method calls

**Message Dispatch**:
1. Evaluate receiver
2. Look up method in receiver's slots (walk prototype chain)
3. Query method's expected argument count
4. Evaluate and consume N following arguments
5. Call method with receiver as `self` and arguments
6. Return result

### 5. REPL (`repl/repl.py`)

Interactive Read-Eval-Print Loop for exploratory programming.

**Features**:
- Multi-line input with indentation awareness
- Statement-by-statement execution
- Error recovery (don't crash on syntax errors)
- History and state persistence across inputs
- Special commands (`:quit`, `:reset`, `:help`)

**Implementation**:
```python
while True:
    source = read_input()  # Handle multi-line, indentation
    try:
        ast = parse(source)
        result = interpreter.eval(ast)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
```

### 6. Script Runner (`runner/script_runner.py`)

Executes `.mylang` files from the command line.

**Features**:
- Read source file
- Parse entire program
- Execute in clean environment
- Report errors with line numbers
- Exit with appropriate status code

**Usage**:
```bash
python -m mylang script.mylang
# or
mylang script.mylang
```

## Data Flow

### Script Execution
```
.mylang file → Lexer → Parser → AST → Interpreter → Runtime → Output
```

### REPL Execution
```
User Input → Lexer → Parser → AST → Interpreter → Runtime → Display Result
    ↑                                                               │
    └───────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
mylang/
├── src/
│   └── mylang/
│       ├── __init__.py              # Package exports
│       ├── runtime/
│       │   ├── __init__.py
│       │   ├── objects.py           # MyLangObject, prototypes
│       │   └── vm.py                # VM primitives, bootstrap
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── lexer.py             # Tokenizer
│       │   ├── parser.py            # Recursive descent parser
│       │   └── ast_nodes.py         # AST node classes
│       ├── interpreter/
│       │   ├── __init__.py
│       │   ├── interpreter.py       # AST evaluator
│       │   └── environment.py       # Variable scopes
│       ├── repl/
│       │   ├── __init__.py
│       │   └── repl.py              # Interactive shell
│       └── runner/
│           ├── __init__.py
│           └── script_runner.py     # .mylang file executor
├── tests/
│   ├── test_runtime/
│   │   ├── test_objects.py          # Object system tests
│   │   └── test_vm.py               # VM primitives tests
│   ├── test_parser/
│   │   ├── test_lexer.py            # Tokenization tests
│   │   └── test_parser.py           # Parsing tests
│   └── test_interpreter/
│       ├── test_interpreter.py      # Execution tests
│       └── test_integration.py      # End-to-end tests
└── examples/
    ├── hello.mylang                 # Hello world
    ├── fibonacci.mylang             # Fibonacci example
    └── fizzbuzz.mylang              # FizzBuzz example
```

## Implementation Phases

### Phase 1: Object System Foundation ✅ COMPLETE
- [x] Project setup with pytest and linting
- [x] Implement MyLangObject with clone capability
- [x] Implement prototype chain lookup
- [x] Basic tests for object cloning

### Phase 2: Basic Types ✅ COMPLETE
- [x] Number prototype with arithmetic
- [x] Boolean prototype with conditionals
- [x] String prototype with operations
- [x] Autoboxing for literals

### Phase 3: Parser ✅ COMPLETE
- [x] Lexer with tokenization
- [x] Indentation handling (INDENT/DEDENT)
- [x] Parser for basic expressions
- [x] Parser for assignments and method definitions

### Phase 4: Interpreter ✅ COMPLETE
- [x] Expression evaluation
- [x] Message dispatch with argument consumption
- [x] Variable environment
- [x] Method invocation with self binding

### Phase 5: Control Flow
- [ ] ifTrue/ifFalse conditionals
- [ ] whileTrue loops
- [ ] Return statement handling

### Phase 6: REPL
- [ ] Basic read-eval-print loop
- [ ] Multi-line input handling
- [ ] Error recovery
- [ ] Special commands

### Phase 7: Script Runner
- [ ] File reading and parsing
- [ ] Program execution
- [ ] Error reporting
- [ ] Command-line interface

## Testing Strategy

### Unit Tests
- Each component tested in isolation
- Mock dependencies where needed
- Focus on edge cases and error conditions

### Integration Tests
- Test component interactions
- Parser → Interpreter → Runtime
- End-to-end execution of small programs

### Example-based Tests
- Run example programs from SPEC.md
- Verify output matches expectations
- Catch regressions in language semantics

### TDD Workflow
1. **RED**: Write failing test for next feature
2. **GREEN**: Implement minimal code to pass test
3. **REFACTOR**: Improve code while keeping tests green
4. Repeat

## Design Decisions & Rationale

### Why Python for Implementation?
- Rapid prototyping and iteration
- Rich ecosystem for testing and tooling
- Easy to represent prototype-based objects (dicts + references)
- Clear path to self-hosting later (write MyLang interpreter in MyLang)

### Why Explicit Self?
- Simplifies scope resolution in early implementation
- Makes message sends unambiguous
- Can be relaxed later with implicit self in method scope

### Why Start with vm_clone and vm_print?
- Minimal primitives to bootstrap the system
- Object.clone uses vm_clone under the hood
- Print enables debugging and REPL feedback
- Additional primitives added only when needed

### Why Left-to-Right Message Evaluation?
- Simpler to implement than precedence-based parsing
- Consistent with Smalltalk's message cascades
- Method arity determines argument consumption
- Natural for prototype-based systems

## Future Enhancements

1. **Implicit self** in method scope
2. **Blocks and closures** with lexical scope
3. **Collection types**: List, Dictionary
4. **Exception handling**: try/catch
5. **Module system**: import/export
6. **Optimizations**: Inline caching, JIT compilation
7. **Debugging**: Breakpoints, stack traces, profiler
8. **Self-hosting**: Rewrite interpreter in MyLang

## References

- Language Specification: `SPEC.md`
- Example Programs: `examples/`
- Test Suite: `tests/`

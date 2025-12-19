# 📘 MyLang — Language Specification v0.5

A small, prototype-based, indentation-sensitive object language inspired by Io and Smalltalk.

---

## Version History

**v0.5 (Current)** - Loop Control Statements
- Added `break` and `continue` loop control statements
- `break` exits innermost loop immediately
- `continue` skips to next iteration
- Updated EBNF grammar to include control flow statements
- Added prime number finder and odd number filter examples
- Expanded loop control documentation with nesting behavior

**v0.4** - Flexible Control Flow
- Conditionals (`ifTrue`, `ifFalse`) no longer require `return` in blocks
- Standalone `ifTrue` and `ifFalse` supported for guard clauses
- Non-local return semantics clarified: `return` exits enclosing method
- Added comparison with Smalltalk and Io approaches
- Updated EBNF to include block arguments
- Enhanced examples showcasing flexible patterns

**v0.3** - Foundation
- Initial specification with object system, parser, and interpreter
- Basic control flow with mandatory returns
- Message-oriented programming model

---

## 1. Overview

MyLang is:

- **Prototype-based**: objects clone and extend each other, no classes
- **Message-oriented**: everything happens by sending messages
- **Indentation-sensitive**: blocks defined by indent
- **Fully object-based**: numbers, strings, booleans → objects
- **Minimal and Stoic**: everything grows from Object, explicit self

### Bootstrapping

At runtime, the VM provides:

- **Object** — the root object
- **Number, Boolean, String** — prototypes with autoboxing
- **vm_clone** — primitive used only for bootstrapping Object
- **vm_print** — primitive for printing

Note: We do not need vm_call yet. Message sending is handled by the interpreter.

---

## 2. Lexical Structure

### 2.1 Identifiers

```
identifier = letter (letter | digit | "_")*
```

### 2.2 Literals

| Literal  | Expands to                                  | Notes             |
|----------|---------------------------------------------|-------------------|
| `42`     | `Number clone; .value = 42`                 | Autoboxed Number  |
| `3.14`   | `Number clone; .value = 3.14`               | Autoboxed Number  |
| `"..."`  | `String clone; .value = "..."; .length = N` | Autoboxed String  |
| `true`   | `Boolean clone; .value = true`              | Autoboxed Boolean |
| `false`  | `Boolean clone; .value = false`             | Autoboxed Boolean |

### 2.3 Reserved Words

```
true false ifTrue ifFalse whileTrue return break continue clone
```

---

## 3. Objects and Slots

Objects are dictionaries with:

- **Slots**: values or methods
- **Methods**: blocks accepting self explicitly

### 3.1 Cloning

- **Bootstrapping clone**: `vm_clone Object`
- **Normal cloning**: `newObj = existingObj clone`

Example:

```mylang
New = Base clone      # normal clone
```

---

## 4. Assignments

### 4.1 Slot Assignment

```mylang
expr = expression
```

Shorthand for literals:

```mylang
x = 42
# expands to:
x = Number clone
x value = 42
```

Long-form variable assignment:

```mylang
x = Number clone
x value = 42
```

---

## 5. Message Send

### Syntax

```mylang
receiver message arg1 arg2 ...
```

### Evaluation Rules

Messages are evaluated **left-to-right**:

```mylang
a b c d
# evaluates as: a.b(c, d)  if b expects 2 args
# or: (((a.b()).c()).d())  if all are unary
```

The interpreter queries each method's expected argument count to determine how many following expressions to consume as arguments.

### Chaining

```mylang
obj method1 method2 arg
# evaluates as: (obj.method1()).method2(arg)
```

### Self is Explicit

Inside a method, `self` must be used explicitly:

```mylang
self print
```

No implicit self for now — could be added later.

---

## 6. Method Definitions

### 6.1 Multi-line Methods

```mylang
receiver methodName =
    indented statements
    return expr
```

### 6.2 Single-line Methods

```mylang
receiver methodName = return expr
```

### 6.3 Method Invocation and Self Binding

When a message is sent to an object, the method is looked up in the receiver's slots (or its prototype chain). The method body executes with `self` bound to the receiver.

Example:

```mylang
Number fib =
    # self is bound to the Number instance receiving the message
    self value < 2 ifTrue
        return self
    ifFalse
        return (self value - 1) fib + (self value - 2) fib
```

---

## 7. Control Flow

Control flow in MyLang is **object-oriented**: conditionals and loops are messages sent to Boolean objects, with indented blocks as implicit arguments. This design is inspired by Smalltalk and Io.

### 7.1 Design Philosophy: Control Flow as Messages

**Smalltalk approach:**
```smalltalk
"Conditionals are messages to booleans with block arguments"
x > 0 ifTrue: [ self doSomething ].
x > 0 ifTrue: [ ^42 ] ifFalse: [ ^0 ].
```

**Io approach:**
```io
// Conditionals are also messages, but different syntax
if(x > 0, doSomething)
if(x > 0) then(doSomething) else(doOther)
```

**MyLang approach:**
```mylang
# Uses indentation instead of delimiters, keeps it message-oriented
x > 0 ifTrue
    self doSomething

x > 0 ifTrue
    return 42
ifFalse
    return 0
```

### 7.2 Conditionals

Conditionals are implemented as messages (`ifTrue`, `ifFalse`) sent to Boolean objects. The indented block following the message is treated as an implicit block argument.

#### Standalone `ifTrue` - Guard clauses and defaults

```mylang
# Set default if nil
arg == nil ifTrue
    arg = "default"
# execution continues here

# Early exit validation
input < 0 ifTrue
    return "Error: negative input"
# continues here if input >= 0
```

#### Standalone `ifFalse` - Inverse guards

```mylang
# Only execute if condition is false
hasPermission ifFalse
    return "Access denied"
# continues here if hasPermission is true
```

#### Combined `ifTrue`/`ifFalse` - Full conditionals

```mylang
# Both branches for side effects
score >= 60 ifTrue
    grade = "Pass"
ifFalse
    grade = "Fail"
# continues here with grade set

# Both branches with returns - one must execute
x < 0 ifTrue
    return "negative"
ifFalse
    return "non-negative"
# never reached - both branches return
```

#### Return Semantics

- **`return` in a block**: Does **non-local return** — exits the enclosing method (Smalltalk-style)
- **No `return` in block**: Block executes statements, then execution continues after the block

```mylang
Number absolute =
    # Non-local return - exits the absolute method
    self value < 0 ifTrue
        return 0 - self value
    # If no return executed, continues here
    return self value

Number ensurePositive =
    # Side effect only - execution continues
    self value < 0 ifTrue
        self value = 0
    # Always reaches here
    return self
```

### 7.3 Loops

Loops use `whileTrue` message sent to a Boolean object. Loop bodies do not need `return` statements.

```mylang
# Basic loop
i value <= 100 whileTrue
    i print
    i value = i value + 1
```

**Loop semantics:**
- The condition is re-evaluated before each iteration
- Loop body executes for side effects
- No implicit return from loop body
- Can use explicit `return` to exit the enclosing method early

```mylang
Number findFirst =
    i = 1
    i <= self value whileTrue
        i % 7 == 0 ifTrue
            return i  # exits findFirst method, not just the loop
        i = i + 1
    return 0  # not found
```

#### Loop Control Statements

MyLang provides `break` and `continue` keywords for precise loop control:

**Break** — exits the innermost loop immediately:

```mylang
# Find first value matching condition
i value < 100 whileTrue
    i value > 10 ifTrue
        "Found:" print
        i print
        break    # Exit loop immediately
    i value = i value + 1
# execution continues here after break
```

**Continue** — skips to the next iteration:

```mylang
# Print odd numbers only
i value < 10 whileTrue
    i value = i value + 1
    i value % 2 == 0 ifTrue
        continue    # Skip even numbers
    i print         # Only prints odd numbers
```

**Nesting behavior:**

`break` and `continue` only affect the **innermost** enclosing loop:

```mylang
outer value < 5 whileTrue
    inner value < 5 whileTrue
        inner value == 3 ifTrue
            break        # Only exits inner loop
        inner value = inner value + 1
    outer value = outer value + 1
```

**Semantics:**

- `break` exits the loop; execution continues after the loop body
- `continue` skips remaining statements and re-evaluates the loop condition
- Runtime error if used outside a loop
- Consistent with `return` keyword precedent for control flow
- Unlike `return`, these only affect loop execution, not method exit

### 7.4 Block Evaluation Model

**How blocks work:**

1. The indented block following `ifTrue`, `ifFalse`, or `whileTrue` is an implicit block argument
2. The Boolean object's method decides whether to evaluate the block
3. When evaluated, statements execute in sequence
4. **Block value**: The last expression in the block becomes the block's value (implicit return to caller)
5. **Non-local return**: If `return` is encountered, it performs **non-local return** (exits the enclosing method, not just the block)

**Block value semantics:**

```mylang
# Block evaluates to last expression
result = x > 0 ifTrue
    y = 42
    y + 1  # last expression
ifFalse
    0
# result = 43 if x > 0, else 0

# Can ignore the value
score >= 60 ifTrue
    grade = "Pass"
# ifTrue returns the value of the assignment, but we ignore it

# return does non-local exit
Number absolute =
    self value < 0 ifTrue
        return 0 - self value  # exits absolute method entirely
    return self value  # only reached if condition was false
```

**Comparison to other languages:**

| Language | Block syntax | Block value | Non-local return |
|----------|--------------|-------------|------------------|
| Smalltalk | `[ statements ]` | Last expression | `^` |
| Ruby | `{ statements }` or `do...end` | Last expression | `return` |
| Io | `(statements)` | Last expression | `return` |
| **MyLang** | Indentation | Last expression | `return` |

### 7.5 Implementation Note

`ifTrue`, `ifFalse`, and `whileTrue` are methods on Boolean objects that accept block arguments:

```mylang
# Conceptually, Boolean has these methods:
Boolean ifTrue =
    # self is the Boolean instance
    # If self.value is true, evaluate the block argument
    # Implementation handled by interpreter

Boolean ifFalse =
    # If self.value is false, evaluate the block argument

Boolean whileTrue =
    # While self.value is true, evaluate the block argument repeatedly
```

The interpreter handles block evaluation and non-local returns.

---

## 8. Built-In Types

### 8.1 Number

**Autoboxing**:

```mylang
x = 42
# expands to:
x = Number clone
x value = 42
```

**Slots for arithmetic/comparison**:

```
+ - * / % < <= == >= >
```

**Return Values**: Arithmetic operations return raw numbers, which are automatically re-boxed into Number objects when used as message receivers.

Example:

```mylang
result = 5 + 3
# expands to:
temp = Number clone
temp value = 5
temp2 = Number clone
temp2 value = 3
rawResult = temp value + temp2 value  # rawResult = 8 (raw number)
result = Number clone
result value = rawResult              # result is now a Number object
```

**Comparison example**:

```mylang
Number < other =
    return self value < other value
```

For methods like Fibonacci, the method operates on `self.value`.

---

### 8.2 Boolean

**Autoboxing**:

```mylang
bt = true
# expands to:
bt = Boolean clone
bt value = true
```

Autoboxing rules same as Number.

Example:

```mylang
Boolean = Object clone
bt = true
bf = false
```

---

### 8.3 String

**Autoboxing**:

```mylang
s = "hello"
# expands to:
s = String clone
s value = "hello"
s length = 5
```

**Built-in Slots**:

- `.value` — the string content
- `.length` — the string length (Java-like autobox magic)
- `.print` — inherited from Object, sends to vm_print

**Inheritance**: String inherits from Object, so it has access to Object's methods unless overridden.

---

## 9. Methods and Blocks

- **Blocks**: indented statements ending with `return expr`
- **Explicit self** for all messages within methods
- **Optional single-line method**: `obj method = return expr`

Example:

```mylang
Object print =
    vm_print self
    return self
```

---

## 10. Full EBNF v0.5

```ebnf
program       = statement* ;

statement     = controlflow | assignment | methoddef | message | empty ;

controlflow   = ("return" expr | "break" | "continue") ;

assignment    = expr "=" expr ;

methoddef     = expr IDENT ("=" "return" expr | "=" NEWLINE INDENT block DEDENT) ;

block         = statement* ;

message       = primary (IDENT (primary* | blockarg))* ;

blockarg      = NEWLINE INDENT block DEDENT ;

primary       = literal | IDENT | "(" expr ")" ;

literal       = NUMBER | STRING | "true" | "false" ;

IDENT         = /[A-Za-z_][A-Za-z0-9_]*/ ;
NUMBER        = /[0-9]+(\.[0-9]+)?/ ;
STRING        = /"[^"]*"/ ;
```

**Key changes from v0.4:**
- Added `break` and `continue` to `controlflow` statement type
- `controlflow` now encompasses `return`, `break`, and `continue`
- All three are keywords that affect execution flow

**Key changes from v0.3:**
- `block` no longer requires `return` statement at end (optional)
- `controlflow` is now a standalone statement type (was `returnstmt`)
- `message` can accept `blockarg` (indented block) after message name
- `blockarg` represents indented blocks passed to messages like `ifTrue`, `ifFalse`, `whileTrue`

---

## 11. Sample Programs

### 11.1 Fibonacci (Number method)

```mylang
Object = vm_clone Object
Object clone =
    return vm_clone self
Object print =
    vm_print self
    return self

Number fib =
    # Early return for base case - guard clause pattern
    self value < 2 ifTrue
        return self
    # Otherwise compute recursively
    a = self value - 1
    b = self value - 2
    # arithmetic returns raw numbers, autoboxed when sending messages
    return a fib + b fib

result = 10
# expands to:
result = Number clone
result value = 10
result fib
result print
```

**Note:** This example showcases guard clause pattern - `ifTrue` with early return, then continue with main logic. No `ifFalse` needed!

---

### 11.2 FizzBuzz

```mylang
Number fizzbuzz =
    # Multiple guard clauses - check each condition and return early
    self value % 15 == 0 ifTrue
        "FizzBuzz" print
        return self
    self value % 3 == 0 ifTrue
        "Fizz" print
        return self
    self value % 5 == 0 ifTrue
        "Buzz" print
        return self
    # Default case - no guard matched
    self print
    return self

i = Number clone
i value = 1

i value <= 100 whileTrue
    i fizzbuzz
    i value = i value + 1
```

**Note:** This showcases multiple guard clauses with early returns. Each `ifTrue` stands alone - much cleaner than nested `ifFalse` chains!

---

### 11.3 Conditional Patterns Showcase

```mylang
# Pattern 1: Guard clause with early return
Number validatePositive =
    self value < 0 ifTrue
        return "Error: negative number"
    return "OK"

# Pattern 2: Set default without early return
Number ensureMinimum =
    self value < 1 ifTrue
        self value = 1
    # continues here regardless
    return self

# Pattern 3: Traditional if/else
Number signString =
    self value < 0 ifTrue
        return "negative"
    ifFalse
        return "non-negative"

# Pattern 4: Side effects in both branches
Number clamp =
    self value < 0 ifTrue
        self value = 0
    ifFalse
        self value > 100 ifTrue
            self value = 100
    return self

# Pattern 5: Early exit from loop
Number findDivisor =
    i = 2
    i < self value whileTrue
        self value % i == 0 ifTrue
            return i  # exits findDivisor, not just loop
        i = i + 1
    return self  # prime or 1
```

**Note:** These patterns demonstrate the flexibility of optional returns and standalone conditionals.

---

### 11.4 Prime Number Finder (using break)

```mylang
# Find the first prime number greater than 100
Number isPrime =
    # Early return for base case
    self value < 2 ifTrue
        return false
    # Check divisibility
    i = 2
    i value * i value <= self value whileTrue
        self value % i value == 0 ifTrue
            return false
        i value = i value + 1
    return true

# Search for first prime > 100
candidate = 101
candidate value < 1000 whileTrue
    candidate isPrime ifTrue
        "First prime > 100:" print
        candidate print
        break    # Exit search once found
    candidate value = candidate value + 1
```

**Note:** `break` allows early exit from the search loop without exiting the entire method.

---

### 11.5 Odd Numbers (using continue)

```mylang
# Print odd numbers from 1 to 20
i = 0
i value < 20 whileTrue
    i value = i value + 1
    # Skip even numbers
    i value % 2 == 0 ifTrue
        continue    # Skip to next iteration
    # Only odd numbers reach here
    i print
```

**Note:** `continue` provides cleaner code than nested conditionals for filtering iterations.

---

## 12. Notes

- **Explicit self** enforced in all methods
- **vm_clone** only used for bootstrapping Object
- All Numbers, Booleans, Strings are clones of base prototypes
- **Single-line methods** optional for trivial returns
- **Autoboxing**: Arithmetic operations return raw numbers, automatically converted to Number objects when used as receivers
- **String slots**: `.value` for content, `.length` for size (Java-like)
- **Message evaluation**: Left-to-right, with argument count queried from methods
- **Later**: Relax self requirement inside methods for convenience; add varargs support

---

## 13. Future Considerations

- Implicit self within method scope
- Varargs: `receiver message arg1 arg2 ... argN` — consume all remaining expressions as arguments
- Explicit discard syntax: `_ = expr`
- Block closures with lexical scope
- Pattern matching on message sends

---

**End of Specification v0.5**

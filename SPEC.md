# 📘 MyLang — Language Specification v0.3

A small, prototype-based, indentation-sensitive object language inspired by Io and Smalltalk.

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
true false ifTrue ifFalse whileTrue return clone
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

### 7.1 Conditionals

```mylang
condition ifTrue
    indented statements
    return expr
ifFalse
    indented statements
    return expr
```

Note: Both `ifTrue` and `ifFalse` blocks must end with explicit `return`.

### 7.2 Loops

```mylang
condition whileTrue
    indented statements
    # no explicit return needed in loop body
```

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

## 10. Full EBNF v0.3

```ebnf
program       = statement* ;

statement     = assignment | methoddef | message | empty ;

assignment    = expr "=" expr ;

methoddef     = expr IDENT ("=" "return" expr | "=" NEWLINE INDENT block DEDENT) ;

block         = statement* "return" expr ;

expr          = message | literal | IDENT ;

message       = primary (IDENT primary*)* ;

primary       = literal | IDENT | "(" expr ")" ;

literal       = NUMBER | STRING | "true" | "false" ;

IDENT         = /[A-Za-z_][A-Za-z0-9_]*/ ;
NUMBER        = /[0-9]+(\.[0-9]+)?/ ;
STRING        = /"[^"]*"/ ;
```

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
    self value < 2 ifTrue
        return self
    ifFalse
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

Note: `fib` uses `self.value` explicitly. Arithmetic operations return raw numbers which are automatically boxed into Number objects when needed.

---

### 11.2 FizzBuzz

```mylang
Number fizzbuzz =
    self value % 15 == 0 ifTrue
        "FizzBuzz" print
        return self
    ifFalse
    self value % 3 == 0 ifTrue
        "Fizz" print
        return self
    ifFalse
    self value % 5 == 0 ifTrue
        "Buzz" print
        return self
    ifFalse
        self print
        return self

i = Number clone
i value = 1

i value <= 100 whileTrue
    i fizzbuzz
    i value = i value + 1
```

Note: We explicitly reassign `i value` after calling `fizzbuzz`. In the future, we could add `_ = i fizzbuzz` to explicitly discard return values.

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

**End of Specification v0.3**

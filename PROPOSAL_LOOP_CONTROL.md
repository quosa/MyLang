# Proposal: Loop Control Statements (break and continue)

**Status**: Draft
**Author**: Claude
**Date**: 2025-12-19
**Target Version**: v0.4

---

## 1. Motivation

While loops are currently specified in MyLang (SPEC.md §7.2), but lack early exit mechanisms. Real-world use cases require:

1. **Early termination** when a condition is met
2. **Skipping iterations** based on runtime conditions
3. **Search patterns** that stop when finding a result
4. **Validation loops** that exit on first error

Without `break` and `continue`, developers must:
- Use complex boolean flags
- Nest conditionals awkwardly
- Rely on `return` to exit (which exits the entire method, not just the loop)

---

## 2. Design Philosophy: Message-Based vs. Keywords

MyLang's core principle is **"everything is a message send to an object"**. This raises an important design question: should loop control be keywords or messages?

### 2.1 Two Approaches Considered

#### **Approach A: Keywords (Recommended)**

```mylang
i value < 10 whileTrue
    i value % 2 == 0 ifTrue
        break
    continue
```

**Pros:**
- Consistent with existing keywords (`return`, `true`, `false`)
- Familiar to programmers from other languages
- Clear and unambiguous
- No receiver needed (what would `break` be sent to?)

**Cons:**
- Not purely message-based
- Adds special cases to the language

---

#### **Approach B: Message-Based (Alternative)**

```mylang
i value < 10 whileTrue
    i value % 2 == 0 ifTrue
        Loop break
    Loop continue
```

**Pros:**
- More aligned with "everything is a message" philosophy
- `Loop` could be a special runtime object in scope during loops
- Extensible (could add `Loop skip: 3` to skip N iterations)

**Cons:**
- Introduces magic `Loop` object in loop scope
- Inconsistent with `return` (which is a keyword)
- More verbose
- Less familiar to developers

---

### 2.2 Recommendation: **Approach A (Keywords)**

**Rationale:**
1. **Consistency with `return`**: MyLang already uses `return` as a keyword for control flow, not as a message send
2. **Pragmatism**: Control flow is fundamental; keywords are appropriate
3. **Simplicity**: No magic objects or scope pollution
4. **Future compatibility**: Can add message-based extensions later (e.g., `Loop skip: n`)

This follows the precedent of Smalltalk, which despite being "everything is an object", still uses special syntax for control flow blocks (ifTrue:ifFalse:, whileTrue:, etc.) rather than pure message sends.

---

## 3. Syntax Specification

### 3.1 Break Statement

```ebnf
break_stmt = "break" NEWLINE
```

**Semantics:**
- Immediately exits the innermost enclosing `whileTrue` loop
- Execution continues at the first statement after the loop
- Runtime error if used outside a loop

**Example:**

```mylang
# Find first even number > 10
i = 0
i value < 100 whileTrue
    i value > 10 ifTrue
        i value % 2 == 0 ifTrue
            "Found:" print
            i print
            break
    i value = i value + 1
```

---

### 3.2 Continue Statement

```ebnf
continue_stmt = "continue" NEWLINE
```

**Semantics:**
- Immediately skips to the next iteration of the innermost enclosing loop
- Re-evaluates the loop condition
- Runtime error if used outside a loop

**Example:**

```mylang
# Print odd numbers from 1 to 10
i = 0
i value < 10 whileTrue
    i value = i value + 1
    i value % 2 == 0 ifTrue
        continue
    i print
```

---

### 3.3 Nesting Behavior

`break` and `continue` only affect the **innermost** loop:

```mylang
# Nested loop example
i = 0
i value < 5 whileTrue
    j = 0
    j value < 5 whileTrue
        j value == 3 ifTrue
            break       # Only exits inner loop
        j value = j value + 1
    i value = i value + 1
```

---

## 4. Implementation Strategy

### 4.1 Exception-Based Control Flow

The recommended implementation uses Python exceptions for control flow (standard pattern):

```python
# In interpreter.py

class BreakException(Exception):
    """Raised to break out of a loop"""
    pass

class ContinueException(Exception):
    """Raised to skip to next loop iteration"""
    pass

def eval_while_loop(self, node: WhileLoop):
    while True:
        try:
            # Evaluate condition
            condition = self.eval_node(node.condition)
            if not self._is_truthy(condition):
                break

            # Execute loop body
            for stmt in node.body:
                self.eval_node(stmt)

        except BreakException:
            break
        except ContinueException:
            continue

    return self.runtime.get_nil()  # Loops return nil/Object

def eval_break(self, node: BreakStatement):
    raise BreakException()

def eval_continue(self, node: ContinueStatement):
    raise ContinueException()
```

### 4.2 AST Node Additions

```python
# In ast_nodes.py

@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: list[ASTNode]  # Block of statements

@dataclass
class BreakStatement(ASTNode):
    pass

@dataclass
class ContinueStatement(ASTNode):
    pass
```

### 4.3 Lexer Updates

```python
# In lexer.py
KEYWORDS = {
    'true': 'TRUE',
    'false': 'FALSE',
    'return': 'RETURN',
    'break': 'BREAK',      # NEW
    'continue': 'CONTINUE', # NEW
    'ifTrue': 'IF_TRUE',
    'ifFalse': 'IF_FALSE',
    'whileTrue': 'WHILE_TRUE',
}
```

### 4.4 Parser Updates

```python
# In parser.py

def statement(self):
    # ... existing cases ...
    if self.current_token.type == 'BREAK':
        return self.break_statement()
    if self.current_token.type == 'CONTINUE':
        return self.continue_statement()
    # ...

def break_statement(self):
    self.expect('BREAK')
    return BreakStatement()

def continue_statement(self):
    self.expect('CONTINUE')
    return ContinueStatement()
```

---

## 5. Interaction with Message-Based Runtime

While `break` and `continue` are keywords at the syntax level, they integrate seamlessly with MyLang's object-based runtime:

### 5.1 Loop Return Values

```mylang
# whileTrue is still a message send
result = condition whileTrue
    # ... loop body ...
```

The `whileTrue` message:
1. **Receiver**: A Boolean object (the condition result)
2. **Message**: `whileTrue`
3. **Argument**: The loop body (as a block/closure)
4. **Returns**: The `Object` prototype (nil-equivalent)

### 5.2 Break/Continue Are Control Flow, Not Messages

Just like `return`, `break` and `continue` are **control flow statements** that manipulate the execution stack, not messages sent to objects. This is pragmatic and consistent.

### 5.3 Future: Message-Based Extensions

Later versions could add message-based loop control for advanced patterns:

```mylang
# Future possibility:
Loop skip: 3        # Skip next 3 iterations
Loop repeatLast     # Re-execute current iteration
Loop countRemaining # Get remaining iterations (if bounded)
```

This would require introducing a `Loop` object into the block scope during loop execution, but that's a future enhancement.

---

## 6. Complete Examples

### 6.1 Break: Search Pattern

```mylang
# Find first Armstrong number (narcissistic number)
Number isArmstrong =
    digits = self value toString length
    sum = 0
    temp = self value
    temp > 0 whileTrue
        digit = temp % 10
        sum = sum + (digit pow: digits)
        temp = temp / 10
    return sum == self value

i = 1
i value < 1000 whileTrue
    i isArmstrong ifTrue
        "Found Armstrong number:" print
        i print
        break
    i value = i value + 1
```

### 6.2 Continue: Skip Pattern

```mylang
# Print numbers 1-20, skipping multiples of 3
i = 0
i value < 20 whileTrue
    i value = i value + 1
    i value % 3 == 0 ifTrue
        continue
    i print
```

### 6.3 Nested Loops with Break

```mylang
# Find first pair (i, j) where i * j > 100
found = false
i = 1
i value < 20 whileTrue
    found value ifTrue
        break

    j = 1
    j value < 20 whileTrue
        product = i value * j value
        product > 100 ifTrue
            "Found pair:" print
            i print
            j print
            found value = true
            break
        j value = j value + 1

    i value = i value + 1
```

### 6.4 Continue: Validation Loop

```mylang
# Process valid items, skip invalid ones
items processAll =
    items each: item
        item isValid ifFalse
            continue
        item process
        item save
```

---

## 7. Testing Strategy

### 7.1 Unit Tests

```python
# tests/test_loop_control.py

def test_break_exits_loop():
    """break should exit the innermost loop"""
    code = """
    count = 0
    count value < 100 whileTrue
        count value > 5 ifTrue
            break
        count value = count value + 1
    count print  # Should print 6
    """
    assert run(code) == "6"

def test_continue_skips_iteration():
    """continue should skip to next iteration"""
    code = """
    sum = 0
    i = 0
    i value < 10 whileTrue
        i value = i value + 1
        i value % 2 == 0 ifTrue
            continue
        sum value = sum value + i value
    sum print  # Should print 25 (1+3+5+7+9)
    """
    assert run(code) == "25"

def test_break_outside_loop_raises_error():
    """break outside a loop should raise runtime error"""
    code = """
    x = 5
    break
    """
    with pytest.raises(RuntimeError, match="break outside loop"):
        run(code)
```

### 7.2 Integration Tests

- FizzBuzz with early exit
- Prime number search with break
- Input validation loops with continue
- Nested loop matrix operations

---

## 8. Documentation Updates

### 8.1 SPEC.md Changes

Update §7.2 (Loops) to include:
- Break statement syntax and semantics
- Continue statement syntax and semantics
- Nesting behavior
- Examples

Update §2.3 (Reserved Words) to add `break` and `continue`.

Update §10 (EBNF) to include new statement types.

### 8.2 Examples

Add to §11 (Sample Programs):
- Prime number finder (demonstrates break)
- Odd number filter (demonstrates continue)
- Nested loop search (demonstrates both)

---

## 9. Backward Compatibility

**Impact**: None

- This is a pure addition (no breaking changes)
- Existing programs without `break`/`continue` work identically
- Users who named variables `break` or `continue` will need to rename them (unlikely edge case)

---

## 10. Alternatives Considered

### 10.1 Using `return` for Loop Exit

**Rejected**: `return` exits the entire method, not just the loop. This is too coarse-grained.

### 10.2 Labeled Breaks (Java/JavaScript style)

```mylang
outer: i value < 10 whileTrue
    inner: j value < 10 whileTrue
        break outer
```

**Deferred**: Adds complexity. Can be added in a future version if needed.

### 10.3 Block Return Values

```mylang
result = i value < 10 whileTrue
    i value == 5 ifTrue
        return i  # Return value from loop block
```

**Deferred**: Requires redesigning loop semantics. Current loops return `Object` (nil).

---

## 11. Open Questions

1. **Should break/continue accept arguments?**
   - Example: `break i` to return a value when exiting loop
   - **Decision**: No, keep it simple. Loops return nil. Use a variable to capture values.

2. **Should we validate at parse time or runtime that break/continue are in loops?**
   - **Decision**: Runtime validation (simpler parser, clearer error messages)

3. **Future: Block closures with break/continue?**
   - How should break/continue behave in closures passed to iterators like `each:`?
   - **Decision**: Defer until closures are implemented

---

## 12. Implementation Phases

### Phase 1: Core Implementation
- [ ] Add `break` and `continue` keywords to lexer
- [ ] Create AST nodes for BreakStatement and ContinueStatement
- [ ] Implement exception-based control flow in interpreter
- [ ] Update loop evaluation to catch control flow exceptions

### Phase 2: Validation & Testing
- [ ] Add runtime validation (break/continue only in loops)
- [ ] Write unit tests for all scenarios
- [ ] Write integration tests with real programs

### Phase 3: Documentation
- [ ] Update SPEC.md with syntax and semantics
- [ ] Add examples to sample programs
- [ ] Update EBNF grammar
- [ ] Update reserved words list

### Phase 4: Advanced Features (Future)
- [ ] Consider labeled breaks for nested loops
- [ ] Consider message-based loop control (Loop object)
- [ ] Consider break with return values

---

## 13. Conclusion

Adding `break` and `continue` as keywords:
- ✅ Aligns with `return` precedent
- ✅ Pragmatic and familiar
- ✅ Simple to implement (exception-based)
- ✅ No breaking changes
- ✅ Enables real-world loop patterns
- ✅ Leaves door open for message-based extensions

**Recommendation**: Approve and implement for v0.4.

---

**End of Proposal**

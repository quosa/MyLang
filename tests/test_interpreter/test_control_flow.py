"""Tests for control flow (ifTrue, ifFalse, whileTrue, return)."""

import pytest

from mylang.interpreter.interpreter import Interpreter


class TestIfTrue:
    """Tests for ifTrue conditional."""

    def test_iftrue_executes_block_when_true(self):
        """Test that ifTrue executes the block when condition is true."""
        source = """
x = 0
true ifTrue
    x = 42
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("x")
        assert result.get_slot("value") == 42

    def test_iftrue_skips_block_when_false(self):
        """Test that ifTrue skips the block when condition is false."""
        source = """
x = 0
false ifTrue
    x = 42
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("x")
        assert result.get_slot("value") == 0

    def test_iftrue_with_comparison(self):
        """Test ifTrue with a comparison expression."""
        source = """
x = 10
result = 0
x > 5 ifTrue
    result = 1
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("result")
        assert result.get_slot("value") == 1

    def test_iftrue_returns_block_value(self):
        """Test that ifTrue returns the last expression value."""
        source = """
result = true ifTrue
    x = 42
    x + 1
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("result")
        # The block's last expression is x + 1 = 43
        assert result.get_slot("value") == 43

    def test_iftrue_returns_none_when_false(self):
        """Test that ifTrue returns None when condition is false."""
        source = """
result = false ifTrue
    42
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("result")
        # When condition is false, block doesn't execute, should return None
        assert result is None


class TestIfFalse:
    """Tests for ifFalse conditional."""

    def test_iffalse_executes_block_when_false(self):
        """Test that ifFalse executes the block when condition is false."""
        source = """
x = 0
false ifFalse
    x = 42
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("x")
        assert result.get_slot("value") == 42

    def test_iffalse_skips_block_when_true(self):
        """Test that ifFalse skips the block when condition is true."""
        source = """
x = 0
true ifFalse
    x = 42
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("x")
        assert result.get_slot("value") == 0


class TestIfTrueIfFalse:
    """Tests for combined ifTrue/ifFalse."""

    def test_iftrue_iffalse_executes_true_branch(self):
        """Test that ifTrue branch executes when true."""
        source = """
x = 0
true ifTrue
    x = 1
ifFalse
    x = 2
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("x")
        assert result.get_slot("value") == 1

    def test_iftrue_iffalse_executes_false_branch(self):
        """Test that ifFalse branch executes when false."""
        source = """
x = 0
false ifTrue
    x = 1
ifFalse
    x = 2
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("x")
        assert result.get_slot("value") == 2

    def test_iftrue_iffalse_returns_executed_branch_value(self):
        """Test that the executed branch's value is returned."""
        source = """
result = true ifTrue
    42
ifFalse
    99
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("result")
        assert result.get_slot("value") == 42


class TestReturn:
    """Tests for return statement (non-local return)."""

    @pytest.mark.skip(reason="Requires method definition support (Phase 6)")
    def test_return_exits_method(self):
        """Test that return exits the enclosing method."""
        source = """
Number earlyExit =
    self value > 0 ifTrue
        return 42
    return 99

result = 5
result earlyExit
"""
        interp = Interpreter()
        result = interp.eval(source)
        # earlyExit should return 42 for positive numbers
        assert result.get_slot("value") == 42

    @pytest.mark.skip(reason="Requires method definition support (Phase 6)")
    def test_return_skips_remaining_code(self):
        """Test that return skips code after the ifTrue block."""
        source = """
Number test =
    self value > 0 ifTrue
        return 1
    return 2

result = 5
result test
"""
        interp = Interpreter()
        result = interp.eval(source)
        assert result.get_slot("value") == 1


class TestWhileTrue:
    """Tests for whileTrue loops."""

    def test_whiletrue_basic_loop(self):
        """Test basic whileTrue loop."""
        source = """
i = 0
i < 5 whileTrue
    i = i + 1
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("i")
        assert result.get_slot("value") == 5

    def test_whiletrue_with_counter(self):
        """Test whileTrue with a counter variable."""
        source = """
i = 0
sum = 0
i < 10 whileTrue
    sum = sum + i
    i = i + 1
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("sum")
        # sum of 0..9 = 45
        assert result.get_slot("value") == 45

    @pytest.mark.skip(reason="Requires method definition support (Phase 6)")
    def test_whiletrue_with_early_return(self):
        """Test whileTrue with early return from enclosing method."""
        source = """
Number findDivisor =
    i = 2
    i < self value whileTrue
        self value % i == 0 ifTrue
            return i
        i = i + 1
    return 0

result = 15
result findDivisor
"""
        interp = Interpreter()
        result = interp.eval(source)
        # 15's first divisor after 1 is 3... wait, we start at 2, so it should be 3
        # 15 % 2 = 1 (not 0), 15 % 3 = 0, so return 3
        assert result.get_slot("value") == 3


class TestBreak:
    """Tests for break statement."""

    def test_break_exits_loop(self):
        """Test that break exits the loop immediately."""
        source = """
i = 0
i < 100 whileTrue
    i = i + 1
    i > 5 ifTrue
        break
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("i")
        # Loop should stop when i reaches 6
        assert result.get_slot("value") == 6

    def test_break_with_search_pattern(self):
        """Test break in a search pattern - find first even number > 10."""
        source = """
i = 0
found = 0
i < 100 whileTrue
    i = i + 1
    i > 10 ifTrue
        i % 2 == 0 ifTrue
            found = i
            break
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("found")
        # First even number > 10 is 12
        assert result.get_slot("value") == 12

    def test_break_in_nested_loop_only_exits_inner(self):
        """Test that break only exits the innermost loop."""
        source = """
outer_count = 0
inner_count = 0
i = 0
i < 3 whileTrue
    outer_count = outer_count + 1
    j = 0
    j < 10 whileTrue
        j = j + 1
        inner_count = inner_count + 1
        j == 3 ifTrue
            break
    i = i + 1
"""
        interp = Interpreter()
        interp.eval(source)
        outer = interp.env.get("outer_count")
        inner = interp.env.get("inner_count")
        # Outer loop runs 3 times
        assert outer.get_slot("value") == 3
        # Inner loop runs 3 times per outer iteration (breaks at j==3)
        # So 3 * 3 = 9 total inner iterations
        assert inner.get_slot("value") == 9


class TestContinue:
    """Tests for continue statement."""

    def test_continue_skips_to_next_iteration(self):
        """Test that continue skips to the next iteration."""
        source = """
i = 0
sum = 0
i < 10 whileTrue
    i = i + 1
    i % 2 == 0 ifTrue
        continue
    sum = sum + i
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("sum")
        # Sum of odd numbers 1, 3, 5, 7, 9 = 25
        assert result.get_slot("value") == 25

    def test_continue_with_filter_pattern(self):
        """Test continue for filtering - skip multiples of 3."""
        source = """
i = 0
count = 0
i < 10 whileTrue
    i = i + 1
    i % 3 == 0 ifTrue
        continue
    count = count + 1
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("count")
        # Numbers 1-10, excluding 3, 6, 9 = 7 numbers
        assert result.get_slot("value") == 7

    def test_continue_in_nested_loop_only_affects_inner(self):
        """Test that continue only affects the innermost loop."""
        source = """
outer_count = 0
inner_count = 0
i = 0
i < 3 whileTrue
    i = i + 1
    outer_count = outer_count + 1
    j = 0
    j < 5 whileTrue
        j = j + 1
        j == 2 ifTrue
            continue
        inner_count = inner_count + 1
"""
        interp = Interpreter()
        interp.eval(source)
        outer = interp.env.get("outer_count")
        inner = interp.env.get("inner_count")
        # Outer loop runs 3 times
        assert outer.get_slot("value") == 3
        # Inner loop runs 5 times per outer, but skips when j==2
        # So 4 increments per outer * 3 outers = 12
        assert inner.get_slot("value") == 12


class TestBreakAndContinueTogether:
    """Tests for break and continue used together."""

    def test_break_and_continue_in_same_loop(self):
        """Test using both break and continue in the same loop."""
        source = """
i = 0
sum = 0
i < 20 whileTrue
    i = i + 1
    i > 15 ifTrue
        break
    i % 2 == 0 ifTrue
        continue
    sum = sum + i
"""
        interp = Interpreter()
        interp.eval(source)
        result = interp.env.get("sum")
        # Sum odd numbers from 1 to 15: 1+3+5+7+9+11+13+15 = 64
        assert result.get_slot("value") == 64

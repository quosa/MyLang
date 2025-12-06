"""Tests for MyLang interpreter.

The interpreter evaluates AST nodes and executes MyLang programs.
"""


class TestInterpreterBasics:
    """Test basic interpreter functionality."""

    def test_interpreter_import(self):
        """Test that the interpreter can be imported."""
        from mylang.interpreter.interpreter import Interpreter

        assert Interpreter is not None

    def test_interpreter_creation(self):
        """Test creating an interpreter instance."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        assert interp is not None


class TestLiteralEvaluation:
    """Test evaluating literal values."""

    def test_eval_number_literal(self):
        """Test evaluating a number literal."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        result = interp.eval("42")

        # Should return a Number object
        assert result is not None
        assert result.get_slot("value") == 42

    def test_eval_string_literal(self):
        """Test evaluating a string literal."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        result = interp.eval('"hello"')

        assert result is not None
        assert result.get_slot("value") == "hello"

    def test_eval_true_literal(self):
        """Test evaluating true."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        result = interp.eval("true")

        assert result is not None
        assert result.get_slot("value") is True

    def test_eval_false_literal(self):
        """Test evaluating false."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        result = interp.eval("false")

        assert result is not None
        assert result.get_slot("value") is False


class TestSimpleAssignments:
    """Test simple variable assignments."""

    def test_assign_number(self):
        """Test x = 42."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("x = 42")

        # Should be able to retrieve the variable
        x = interp.env.get("x")
        assert x is not None
        assert x.get_slot("value") == 42

    def test_assign_string(self):
        """Test s = \"hello\"."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval('s = "hello"')

        s = interp.env.get("s")
        assert s is not None
        assert s.get_slot("value") == "hello"

    def test_assign_boolean(self):
        """Test b = true."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("b = true")

        b = interp.env.get("b")
        assert b is not None
        assert b.get_slot("value") is True


class TestMessageSends:
    """Test message send evaluation."""

    def test_simple_clone(self):
        """Test: a = Number clone."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("a = Number clone")

        a = interp.env.get("a")
        assert a is not None
        # Should be a clone of Number
        from mylang.runtime.builtins import Number

        assert a.proto is Number

    def test_object_clone(self):
        """Test: obj = Object clone."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("obj = Object clone")

        obj = interp.env.get("obj")
        assert obj is not None
        from mylang.runtime.builtins import Object

        assert obj.proto is Object


class TestSlotAssignments:
    """Test assigning to object slots."""

    def test_assign_to_slot(self):
        """Test: a value = 5."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("a = Number clone")
        interp.eval("a value = 5")

        a = interp.env.get("a")
        assert a.get_slot("value") == 5

    def test_multiple_slot_assignments(self):
        """Test multiple slot assignments."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("obj = Object clone")
        interp.eval("obj x = 10")
        interp.eval("obj y = 20")

        obj = interp.env.get("obj")
        assert obj.get_slot("x").get_slot("value") == 10
        assert obj.get_slot("y").get_slot("value") == 20


class TestArithmetic:
    """Test arithmetic operations."""

    def test_simple_addition(self):
        """Test: result = 5 + 3."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("a = 5")
        interp.eval("b = 3")
        interp.eval("result = a + b")

        result = interp.env.get("result")
        assert result.get_slot("value") == 8

    def test_simple_subtraction(self):
        """Test: result = 10 - 3."""
        from mylang.interpreter.interpreter import Interpreter

        interp = Interpreter()
        interp.eval("a = 10")
        interp.eval("b = 3")
        interp.eval("result = a - b")

        result = interp.env.get("result")
        assert result.get_slot("value") == 7


class TestEnvironment:
    """Test the environment/scope management."""

    def test_environment_get_set(self):
        """Test setting and getting variables."""
        from mylang.interpreter.environment import Environment

        env = Environment()
        from mylang.runtime.builtins import create_number

        env.set("x", create_number(42))

        x = env.get("x")
        assert x.get_slot("value") == 42

    def test_environment_has_builtins(self):
        """Test that environment has built-in prototypes."""
        from mylang.interpreter.environment import Environment

        env = Environment()

        # Should have Object, Number, Boolean, String
        assert env.get("Object") is not None
        assert env.get("Number") is not None
        assert env.get("Boolean") is not None
        assert env.get("String") is not None

    def test_undefined_variable(self):
        """Test that undefined variables raise an error."""
        from mylang.interpreter.environment import Environment

        env = Environment()

        try:
            env.get("undefined")
            raise AssertionError("Should have raised an error")
        except (KeyError, NameError):
            pass  # Expected

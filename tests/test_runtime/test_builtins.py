"""Tests for MyLang built-in types.

This module tests the built-in prototypes:
- Number: Arithmetic and comparison operations
- Boolean: Conditional logic
- String: String operations
"""

import pytest


class TestNumberPrototype:
    """Test the Number prototype with arithmetic and comparison operations."""

    def test_number_prototype_exists(self):
        """Test that the Number prototype can be imported."""
        from mylang.runtime.builtins import Number

        assert Number is not None

    def test_number_has_value_slot(self):
        """Test that Number instances have a value slot."""
        from mylang.runtime.builtins import Number

        num = Number.clone()
        num.set_slot("value", 42)
        assert num.get_slot("value") == 42

    def test_number_addition(self):
        """Test Number arithmetic: addition."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 5)

        b = Number.clone()
        b.set_slot("value", 3)

        # In MyLang: result = a + b
        # The + method should be a slot on Number that takes another number
        add_method = a.get_slot("+")
        result = add_method(a, b)

        assert result.get_slot("value") == 8

    def test_number_subtraction(self):
        """Test Number arithmetic: subtraction."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 10)

        b = Number.clone()
        b.set_slot("value", 3)

        sub_method = a.get_slot("-")
        result = sub_method(a, b)

        assert result.get_slot("value") == 7

    def test_number_multiplication(self):
        """Test Number arithmetic: multiplication."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 6)

        b = Number.clone()
        b.set_slot("value", 7)

        mul_method = a.get_slot("*")
        result = mul_method(a, b)

        assert result.get_slot("value") == 42

    def test_number_division(self):
        """Test Number arithmetic: division."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 20)

        b = Number.clone()
        b.set_slot("value", 4)

        div_method = a.get_slot("/")
        result = div_method(a, b)

        assert result.get_slot("value") == 5

    def test_number_modulo(self):
        """Test Number arithmetic: modulo."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 17)

        b = Number.clone()
        b.set_slot("value", 5)

        mod_method = a.get_slot("%")
        result = mod_method(a, b)

        assert result.get_slot("value") == 2

    def test_number_less_than(self):
        """Test Number comparison: less than."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 3)

        b = Number.clone()
        b.set_slot("value", 5)

        lt_method = a.get_slot("<")
        result = lt_method(a, b)

        assert result.get_slot("value") is True

    def test_number_less_than_or_equal(self):
        """Test Number comparison: less than or equal."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 5)

        b = Number.clone()
        b.set_slot("value", 5)

        lte_method = a.get_slot("<=")
        result = lte_method(a, b)

        assert result.get_slot("value") is True

    def test_number_equal(self):
        """Test Number comparison: equality."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 42)

        b = Number.clone()
        b.set_slot("value", 42)

        eq_method = a.get_slot("==")
        result = eq_method(a, b)

        assert result.get_slot("value") is True

    def test_number_greater_than_or_equal(self):
        """Test Number comparison: greater than or equal."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 7)

        b = Number.clone()
        b.set_slot("value", 5)

        gte_method = a.get_slot(">=")
        result = gte_method(a, b)

        assert result.get_slot("value") is True

    def test_number_greater_than(self):
        """Test Number comparison: greater than."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 10)

        b = Number.clone()
        b.set_slot("value", 5)

        gt_method = a.get_slot(">")
        result = gt_method(a, b)

        assert result.get_slot("value") is True

    def test_number_inherits_from_object(self):
        """Test that Number inherits from Object."""
        from mylang.runtime.builtins import Number, Object

        # Number's prototype should be Object
        assert Number.proto is Object

    def test_number_has_clone_method(self):
        """Test that Number has clone method inherited from Object."""
        from mylang.runtime.builtins import Number

        num = Number.clone()
        assert num.proto is Number


class TestBooleanPrototype:
    """Test the Boolean prototype with conditional logic."""

    def test_boolean_prototype_exists(self):
        """Test that the Boolean prototype can be imported."""
        from mylang.runtime.builtins import Boolean

        assert Boolean is not None

    def test_boolean_has_value_slot(self):
        """Test that Boolean instances have a value slot."""
        from mylang.runtime.builtins import Boolean

        b = Boolean.clone()
        b.set_slot("value", True)
        assert b.get_slot("value") is True

    def test_boolean_true_value(self):
        """Test creating a true Boolean."""
        from mylang.runtime.builtins import Boolean

        b = Boolean.clone()
        b.set_slot("value", True)
        assert b.get_slot("value") is True

    def test_boolean_false_value(self):
        """Test creating a false Boolean."""
        from mylang.runtime.builtins import Boolean

        b = Boolean.clone()
        b.set_slot("value", False)
        assert b.get_slot("value") is False

    def test_boolean_inherits_from_object(self):
        """Test that Boolean inherits from Object."""
        from mylang.runtime.builtins import Boolean, Object

        assert Boolean.proto is Object

    def test_boolean_has_clone_method(self):
        """Test that Boolean has clone method inherited from Object."""
        from mylang.runtime.builtins import Boolean

        b = Boolean.clone()
        assert b.proto is Boolean


class TestStringPrototype:
    """Test the String prototype with string operations."""

    def test_string_prototype_exists(self):
        """Test that the String prototype can be imported."""
        from mylang.runtime.builtins import String

        assert String is not None

    def test_string_has_value_slot(self):
        """Test that String instances have a value slot."""
        from mylang.runtime.builtins import String

        s = String.clone()
        s.set_slot("value", "hello")
        assert s.get_slot("value") == "hello"

    def test_string_has_length_slot(self):
        """Test that String instances have a length slot."""
        from mylang.runtime.builtins import String

        s = String.clone()
        s.set_slot("value", "hello")
        s.set_slot("length", 5)
        assert s.get_slot("length") == 5

    def test_string_inherits_from_object(self):
        """Test that String inherits from Object."""
        from mylang.runtime.builtins import Object, String

        assert String.proto is Object

    def test_string_has_clone_method(self):
        """Test that String has clone method inherited from Object."""
        from mylang.runtime.builtins import String

        s = String.clone()
        assert s.proto is String


class TestObjectPrototype:
    """Test the base Object prototype."""

    def test_object_prototype_exists(self):
        """Test that the Object prototype can be imported."""
        from mylang.runtime.builtins import Object

        assert Object is not None

    def test_object_has_clone_method(self):
        """Test that Object has a clone method."""
        from mylang.runtime.builtins import Object

        clone_method = Object.get_slot("clone")
        assert clone_method is not None

    def test_object_clone_creates_new_instance(self):
        """Test that Object.clone() creates a new object."""
        from mylang.runtime.builtins import Object

        clone = Object.clone()
        assert clone is not Object
        assert clone.proto is Object

    def test_object_has_print_method(self):
        """Test that Object has a print method."""
        from mylang.runtime.builtins import Object

        print_method = Object.get_slot("print")
        assert print_method is not None


class TestHelperFunctions:
    """Test helper functions for creating boxed values."""

    def test_create_number(self):
        """Test creating a boxed number."""
        from mylang.runtime.builtins import create_number

        num = create_number(42)
        assert num.get_slot("value") == 42

    def test_create_boolean(self):
        """Test creating a boxed boolean."""
        from mylang.runtime.builtins import create_boolean

        b = create_boolean(True)
        assert b.get_slot("value") is True

    def test_create_string(self):
        """Test creating a boxed string."""
        from mylang.runtime.builtins import create_string

        s = create_string("hello")
        assert s.get_slot("value") == "hello"
        assert s.get_slot("length") == 5


class TestArithmeticEdgeCases:
    """Test edge cases for arithmetic operations."""

    def test_division_by_zero(self):
        """Test that division by zero raises an error."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 10)

        b = Number.clone()
        b.set_slot("value", 0)

        div_method = a.get_slot("/")
        with pytest.raises(ZeroDivisionError):
            div_method(a, b)

    def test_negative_numbers(self):
        """Test arithmetic with negative numbers."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", -5)

        b = Number.clone()
        b.set_slot("value", 3)

        add_method = a.get_slot("+")
        result = add_method(a, b)

        assert result.get_slot("value") == -2

    def test_floating_point_arithmetic(self):
        """Test arithmetic with floating point numbers."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 3.5)

        b = Number.clone()
        b.set_slot("value", 2.5)

        add_method = a.get_slot("+")
        result = add_method(a, b)

        assert result.get_slot("value") == 6.0


class TestComparisonEdgeCases:
    """Test edge cases for comparison operations."""

    def test_comparison_with_equal_values(self):
        """Test less than with equal values returns false."""
        from mylang.runtime.builtins import Number

        a = Number.clone()
        a.set_slot("value", 5)

        b = Number.clone()
        b.set_slot("value", 5)

        lt_method = a.get_slot("<")
        result = lt_method(a, b)

        assert result.get_slot("value") is False

    def test_comparison_chain(self):
        """Test that comparisons return Boolean objects."""
        from mylang.runtime.builtins import Boolean, Number

        a = Number.clone()
        a.set_slot("value", 3)

        b = Number.clone()
        b.set_slot("value", 5)

        lt_method = a.get_slot("<")
        result = lt_method(a, b)

        # Result should be a Boolean
        assert result.proto is Boolean

"""MyLang built-in types and prototypes.

This module provides the built-in prototypes for MyLang:
- Object: Root prototype with clone and print methods
- Number: Numeric values with arithmetic and comparison operations
- Boolean: True/false values for conditional logic
- String: Text values with string operations

All built-in types follow the prototype-based object model.
"""

from mylang.runtime.objects import MyLangObject

# ============================================================================
# Object Prototype (Root)
# ============================================================================

Object = MyLangObject()


def _object_clone(self: MyLangObject) -> MyLangObject:
    """Clone method for Object.

    Creates a new object with self as the prototype.

    Args:
        self: The object to clone.

    Returns:
        A new MyLangObject with self as its prototype.
    """
    return self.clone()


def _object_print(self: MyLangObject) -> MyLangObject:
    """Print method for Object.

    Prints the object and returns self for chaining.

    Args:
        self: The object to print.

    Returns:
        self for method chaining.
    """
    # For now, print a simple representation
    if "value" in self.slots:
        print(self.slots["value"])
    else:
        print(f"<Object {id(self)}>")
    return self


# Add clone and print methods to Object
Object.set_slot("clone", _object_clone)
Object.set_slot("print", _object_print)


# ============================================================================
# Number Prototype
# ============================================================================

Number = Object.clone()


def _number_add(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Add two numbers.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A new Number with the sum.
    """
    result = Number.clone()
    result.set_slot("value", self.get_slot("value") + other.get_slot("value"))
    return result


def _number_sub(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Subtract two numbers.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A new Number with the difference.
    """
    result = Number.clone()
    result.set_slot("value", self.get_slot("value") - other.get_slot("value"))
    return result


def _number_mul(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Multiply two numbers.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A new Number with the product.
    """
    result = Number.clone()
    result.set_slot("value", self.get_slot("value") * other.get_slot("value"))
    return result


def _number_div(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Divide two numbers.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A new Number with the quotient.

    Raises:
        ZeroDivisionError: If dividing by zero.
    """
    result = Number.clone()
    result.set_slot("value", self.get_slot("value") / other.get_slot("value"))
    return result


def _number_mod(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Modulo operation on two numbers.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A new Number with the remainder.
    """
    result = Number.clone()
    result.set_slot("value", self.get_slot("value") % other.get_slot("value"))
    return result


def _number_lt(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Less than comparison.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A Boolean with the comparison result.
    """
    result = Boolean.clone()
    result.set_slot("value", self.get_slot("value") < other.get_slot("value"))
    return result


def _number_lte(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Less than or equal comparison.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A Boolean with the comparison result.
    """
    result = Boolean.clone()
    result.set_slot("value", self.get_slot("value") <= other.get_slot("value"))
    return result


def _number_eq(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Equality comparison.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A Boolean with the comparison result.
    """
    result = Boolean.clone()
    result.set_slot("value", self.get_slot("value") == other.get_slot("value"))
    return result


def _number_gte(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Greater than or equal comparison.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A Boolean with the comparison result.
    """
    result = Boolean.clone()
    result.set_slot("value", self.get_slot("value") >= other.get_slot("value"))
    return result


def _number_gt(self: MyLangObject, other: MyLangObject) -> MyLangObject:
    """Greater than comparison.

    Args:
        self: First number (receiver).
        other: Second number.

    Returns:
        A Boolean with the comparison result.
    """
    result = Boolean.clone()
    result.set_slot("value", self.get_slot("value") > other.get_slot("value"))
    return result


# Add arithmetic and comparison methods to Number
Number.set_slot("+", _number_add)
Number.set_slot("-", _number_sub)
Number.set_slot("*", _number_mul)
Number.set_slot("/", _number_div)
Number.set_slot("%", _number_mod)
Number.set_slot("<", _number_lt)
Number.set_slot("<=", _number_lte)
Number.set_slot("==", _number_eq)
Number.set_slot(">=", _number_gte)
Number.set_slot(">", _number_gt)


# ============================================================================
# Boolean Prototype
# ============================================================================

Boolean = Object.clone()


# ============================================================================
# String Prototype
# ============================================================================

String = Object.clone()


# ============================================================================
# Helper Functions for Creating Boxed Values
# ============================================================================


def create_number(value: float | int) -> MyLangObject:
    """Create a boxed Number object.

    This is equivalent to the autoboxing that happens with number literals.

    Args:
        value: The numeric value to box.

    Returns:
        A Number object with the value set.

    Example:
        >>> num = create_number(42)
        >>> num.get_slot("value")
        42
    """
    num = Number.clone()
    num.set_slot("value", value)
    return num


def create_boolean(value: bool) -> MyLangObject:
    """Create a boxed Boolean object.

    This is equivalent to the autoboxing that happens with boolean literals.

    Args:
        value: The boolean value to box.

    Returns:
        A Boolean object with the value set.

    Example:
        >>> b = create_boolean(True)
        >>> b.get_slot("value")
        True
    """
    b = Boolean.clone()
    b.set_slot("value", value)
    return b


def create_string(value: str) -> MyLangObject:
    """Create a boxed String object.

    This is equivalent to the autoboxing that happens with string literals.

    Args:
        value: The string value to box.

    Returns:
        A String object with the value and length set.

    Example:
        >>> s = create_string("hello")
        >>> s.get_slot("value")
        'hello'
        >>> s.get_slot("length")
        5
    """
    s = String.clone()
    s.set_slot("value", value)
    s.set_slot("length", len(value))
    return s


__all__ = [
    "Object",
    "Number",
    "Boolean",
    "String",
    "create_number",
    "create_boolean",
    "create_string",
]

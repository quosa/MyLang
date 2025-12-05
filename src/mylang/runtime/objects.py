"""MyLang object system.

This module implements the prototype-based object model for MyLang.
All objects are instances of MyLangObject, which supports:
- Cloning: creating new objects with prototype links
- Slots: dynamic properties and methods
- Prototype chain lookup: walking the prototype chain to find slots
"""

from typing import Any, Optional


class MyLangObject:
    """Base class for all MyLang objects.

    MyLang uses a prototype-based object model inspired by Io and Self.
    Objects are created by cloning existing objects, which become their prototypes.

    Attributes:
        slots: Dictionary mapping slot names to values (properties or methods)
        proto: Reference to the prototype object (parent in the prototype chain)
    """

    def __init__(self, proto: Optional["MyLangObject"] = None) -> None:
        """Initialize a new MyLang object.

        Args:
            proto: Optional prototype object. If None, this is a root object.
        """
        self.slots: dict[str, Any] = {}
        self.proto: MyLangObject | None = proto

    def clone(self) -> "MyLangObject":
        """Create a new object with this object as its prototype.

        This is the fundamental operation in MyLang's object model.
        The new object starts with empty slots and inherits from this object.

        Returns:
            A new MyLangObject with this object as its prototype.

        Example:
            >>> base = MyLangObject()
            >>> base.set_slot("x", 42)
            >>> clone = base.clone()
            >>> clone.get_slot("x")  # Inherited from base
            42
        """
        return MyLangObject(proto=self)

    def get_slot(self, name: str) -> Any:
        """Get a slot value, walking the prototype chain if necessary.

        This implements prototype-based inheritance. If the slot is not found
        in this object's slots, we recursively search the prototype chain.

        Args:
            name: The slot name to look up.

        Returns:
            The value of the slot.

        Raises:
            AttributeError: If the slot is not found in this object or any prototype.
            RecursionError: If there is a circular reference in the prototype chain.

        Example:
            >>> base = MyLangObject()
            >>> base.set_slot("x", 42)
            >>> clone = base.clone()
            >>> clone.get_slot("x")  # Found in prototype
            42
        """
        # First check our own slots
        if name in self.slots:
            return self.slots[name]

        # If not found, walk the prototype chain
        if self.proto is not None:
            return self.proto.get_slot(name)

        # Not found anywhere in the chain
        raise AttributeError(f"Slot '{name}' not found")

    def set_slot(self, name: str, value: Any) -> None:
        """Set a slot value on this object.

        This always sets the slot on the current object, never on a prototype.
        If the slot already exists, it is overwritten.

        Args:
            name: The slot name to set.
            value: The value to set for the slot.

        Example:
            >>> obj = MyLangObject()
            >>> obj.set_slot("x", 42)
            >>> obj.get_slot("x")
            42
            >>> obj.set_slot("x", 99)  # Overwrite
            >>> obj.get_slot("x")
            99
        """
        self.slots[name] = value

    def __repr__(self) -> str:
        """Return a string representation of this object for debugging.

        Returns:
            A string showing the object's slots and prototype.
        """
        proto_repr = f" -> {id(self.proto)}" if self.proto else ""
        return f"<MyLangObject@{id(self)}{proto_repr} slots={list(self.slots.keys())}>"

"""Tests for MyLang object system and cloning.

This module tests the core prototype-based object model:
- Object creation
- Cloning (Clone = Object clone)
- Prototype chain lookup
- Slot manipulation
"""

import pytest


class TestObjectBasics:
    """Test basic object creation and structure."""

    def test_create_object(self):
        """Test that we can create a basic MyLang object."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        assert obj is not None
        assert hasattr(obj, "slots")
        assert hasattr(obj, "proto")

    def test_object_has_slots_dict(self):
        """Test that objects have a slots dictionary."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        assert isinstance(obj.slots, dict)
        assert len(obj.slots) == 0  # New object has no slots

    def test_object_proto_is_none_by_default(self):
        """Test that new objects have no prototype by default."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        assert obj.proto is None


class TestObjectCloning:
    """Test the clone operation: Clone = Object clone."""

    def test_clone_creates_new_object(self):
        """Test that clone() creates a new object instance."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        clone = original.clone()

        assert clone is not None
        assert clone is not original
        assert isinstance(clone, MyLangObject)

    def test_clone_sets_prototype_link(self):
        """Test that cloned object has original as prototype."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        clone = original.clone()

        assert clone.proto is original

    def test_clone_has_empty_slots(self):
        """Test that newly cloned object has empty slots dict."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        original.slots["x"] = 42

        clone = original.clone()

        # Clone should have empty slots (inherits from proto)
        assert len(clone.slots) == 0
        assert "x" not in clone.slots

    def test_multiple_clones_share_same_proto(self):
        """Test that multiple clones all reference the same prototype."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        clone1 = original.clone()
        clone2 = original.clone()

        assert clone1.proto is original
        assert clone2.proto is original
        assert clone1.proto is clone2.proto

    def test_clone_of_clone_creates_chain(self):
        """Test that cloning a clone creates a prototype chain."""
        from mylang.runtime.objects import MyLangObject

        base = MyLangObject()
        middle = base.clone()
        top = middle.clone()

        assert top.proto is middle
        assert middle.proto is base
        assert base.proto is None


class TestSlotManipulation:
    """Test setting and getting slots on objects."""

    def test_set_slot_on_object(self):
        """Test that we can set a slot on an object."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        obj.set_slot("x", 42)

        assert "x" in obj.slots
        assert obj.slots["x"] == 42

    def test_get_slot_from_object(self):
        """Test that we can get a slot from an object."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        obj.set_slot("x", 42)

        value = obj.get_slot("x")
        assert value == 42

    def test_get_nonexistent_slot_raises_error(self):
        """Test that getting a nonexistent slot raises an error."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()

        with pytest.raises(AttributeError, match="Slot 'nonexistent' not found"):
            obj.get_slot("nonexistent")

    def test_set_slot_on_clone_does_not_affect_original(self):
        """Test that setting a slot on a clone doesn't affect the prototype."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        original.set_slot("x", 42)

        clone = original.clone()
        clone.set_slot("x", 99)

        # Original should still have 42
        assert original.get_slot("x") == 42
        # Clone should have 99 in its own slots
        assert clone.slots["x"] == 99


class TestPrototypeChainLookup:
    """Test slot lookup through the prototype chain."""

    def test_get_slot_walks_prototype_chain(self):
        """Test that get_slot looks up the prototype chain."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        original.set_slot("x", 42)

        clone = original.clone()

        # Clone should find 'x' in its prototype
        value = clone.get_slot("x")
        assert value == 42

    def test_own_slot_shadows_prototype_slot(self):
        """Test that an object's own slot shadows the prototype's slot."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        original.set_slot("x", 42)

        clone = original.clone()
        clone.set_slot("x", 99)

        # Clone should get its own value, not prototype's
        assert clone.get_slot("x") == 99
        # Original unchanged
        assert original.get_slot("x") == 42

    def test_lookup_walks_multi_level_chain(self):
        """Test that lookup works through multiple levels of prototypes."""
        from mylang.runtime.objects import MyLangObject

        base = MyLangObject()
        base.set_slot("a", 1)

        middle = base.clone()
        middle.set_slot("b", 2)

        top = middle.clone()
        top.set_slot("c", 3)

        # Top can see all three slots
        assert top.get_slot("c") == 3  # Own slot
        assert top.get_slot("b") == 2  # From middle
        assert top.get_slot("a") == 1  # From base

    def test_shadowing_at_middle_level(self):
        """Test that middle-level shadowing works correctly."""
        from mylang.runtime.objects import MyLangObject

        base = MyLangObject()
        base.set_slot("x", 1)

        middle = base.clone()
        middle.set_slot("x", 2)

        top = middle.clone()

        # Top should see middle's value, not base's
        assert top.get_slot("x") == 2
        assert middle.get_slot("x") == 2
        assert base.get_slot("x") == 1

    def test_prototype_modification_visible_to_clones(self):
        """Test that modifying prototype slots is visible to existing clones."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        clone = original.clone()

        # Add slot to original AFTER cloning
        original.set_slot("new_slot", 42)

        # Clone should see the new slot
        assert clone.get_slot("new_slot") == 42


class TestObjectEquality:
    """Test object identity and equality."""

    def test_object_identity(self):
        """Test that objects have distinct identities."""
        from mylang.runtime.objects import MyLangObject

        obj1 = MyLangObject()
        obj2 = MyLangObject()

        assert obj1 is not obj2

    def test_clone_has_different_identity(self):
        """Test that a clone is a different object."""
        from mylang.runtime.objects import MyLangObject

        original = MyLangObject()
        clone = original.clone()

        assert original is not clone

    def test_slots_dict_is_independent(self):
        """Test that each object has its own slots dictionary."""
        from mylang.runtime.objects import MyLangObject

        obj1 = MyLangObject()
        obj2 = MyLangObject()

        obj1.set_slot("x", 1)
        obj2.set_slot("x", 2)

        assert obj1.get_slot("x") == 1
        assert obj2.get_slot("x") == 2


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_clone_with_no_proto(self):
        """Test that we can clone an object with no prototype."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        clone = obj.clone()

        assert clone.proto is obj
        assert obj.proto is None

    def test_empty_slot_name(self):
        """Test behavior with empty slot name."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        obj.set_slot("", "empty_name")

        assert obj.get_slot("") == "empty_name"

    def test_slot_with_none_value(self):
        """Test that slots can have None as a value."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        obj.set_slot("x", None)

        assert "x" in obj.slots
        assert obj.get_slot("x") is None

    def test_overwrite_existing_slot(self):
        """Test that we can overwrite an existing slot value."""
        from mylang.runtime.objects import MyLangObject

        obj = MyLangObject()
        obj.set_slot("x", 42)
        obj.set_slot("x", 99)

        assert obj.get_slot("x") == 99

    def test_slot_lookup_with_circular_proto_chain(self):
        """Test that circular prototype chains don't cause infinite loops."""
        from mylang.runtime.objects import MyLangObject

        obj1 = MyLangObject()
        obj2 = MyLangObject()

        # Create circular reference
        obj1.proto = obj2
        obj2.proto = obj1

        # This should not hang, but should raise an error or handle gracefully
        with pytest.raises((AttributeError, RecursionError)):
            obj1.get_slot("nonexistent")

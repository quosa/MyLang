"""MyLang runtime system.

This module provides the core runtime components for MyLang:
- Object system with prototype-based inheritance
- Built-in types (Object, Number, Boolean, String)
- VM primitives for bootstrapping
"""

from mylang.runtime.builtins import (
    Boolean,
    Number,
    Object,
    String,
    create_boolean,
    create_number,
    create_string,
)
from mylang.runtime.objects import MyLangObject

__all__ = [
    "MyLangObject",
    "Object",
    "Number",
    "Boolean",
    "String",
    "create_number",
    "create_boolean",
    "create_string",
]

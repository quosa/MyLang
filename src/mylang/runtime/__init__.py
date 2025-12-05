"""MyLang runtime system.

This module provides the core runtime components for MyLang:
- Object system with prototype-based inheritance
- VM primitives for bootstrapping
"""

from mylang.runtime.objects import MyLangObject

__all__ = ["MyLangObject"]

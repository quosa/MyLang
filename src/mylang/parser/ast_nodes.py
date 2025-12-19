"""MyLang AST node definitions.

This module defines the Abstract Syntax Tree node classes for MyLang.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    type: str


@dataclass
class Program(ASTNode):
    """Top-level program node.

    Attributes:
        statements: List of statement nodes
    """

    statements: list[ASTNode]

    def __init__(self, statements: list[ASTNode]) -> None:
        super().__init__("program")
        self.statements = statements


@dataclass
class Assignment(ASTNode):
    """Assignment statement.

    Represents: name = value

    Attributes:
        name: Identifier name
        value: Expression to assign
    """

    name: str
    value: ASTNode

    def __init__(self, name: str, value: ASTNode) -> None:
        super().__init__("assignment")
        self.name = name
        self.value = value


@dataclass
class MessageSend(ASTNode):
    """Message send expression.

    Represents: receiver message arg1 arg2 ...

    Attributes:
        receiver: The object receiving the message
        message: The message name
        args: List of argument expressions
    """

    receiver: ASTNode
    message: str
    args: list[ASTNode]

    def __init__(self, receiver: ASTNode, message: str, args: list[ASTNode] = None) -> None:
        super().__init__("message_send")
        self.receiver = receiver
        self.message = message
        self.args = args or []


@dataclass
class Literal(ASTNode):
    """Literal value.

    Represents: numbers, strings, booleans

    Attributes:
        value: The literal value
        literal_type: Type of literal (number, string, boolean)
    """

    value: Any
    literal_type: str

    def __init__(self, value: Any, literal_type: str) -> None:
        super().__init__("literal")
        self.value = value
        self.literal_type = literal_type


@dataclass
class Identifier(ASTNode):
    """Identifier reference.

    Represents: variable names

    Attributes:
        name: The identifier name
    """

    name: str

    def __init__(self, name: str) -> None:
        super().__init__("identifier")
        self.name = name


@dataclass
class Block(ASTNode):
    """Block of statements.

    Represents: indented block of code

    Attributes:
        statements: List of statements in the block
    """

    statements: list[ASTNode]

    def __init__(self, statements: list[ASTNode]) -> None:
        super().__init__("block")
        self.statements = statements


@dataclass
class Return(ASTNode):
    """Return statement.

    Represents: return expr

    Attributes:
        value: Expression to return
    """

    value: ASTNode

    def __init__(self, value: ASTNode) -> None:
        super().__init__("return")
        self.value = value

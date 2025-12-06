"""MyLang interpreter.

Evaluates AST nodes and executes MyLang programs.
"""

from mylang.interpreter.environment import Environment
from mylang.parser.ast_nodes import Assignment, Identifier, Literal, MessageSend
from mylang.parser.parser import Parser
from mylang.runtime.builtins import create_boolean, create_number, create_string


class Interpreter:
    """Interpreter for executing MyLang programs.

    The interpreter evaluates AST nodes in the context of an environment.
    """

    def __init__(self) -> None:
        """Initialize the interpreter with a global environment."""
        self.env = Environment()

    def eval(self, source: str):
        """Evaluate MyLang source code.

        Args:
            source: MyLang source code string

        Returns:
            The result of evaluating the code
        """
        # Parse the source code
        parser = Parser(source)
        ast = parser.parse()

        # Evaluate all statements
        result = None
        for stmt in ast.statements:
            result = self.eval_node(stmt)

        return result

    def eval_node(self, node):
        """Evaluate an AST node.

        Args:
            node: The AST node to evaluate

        Returns:
            The result of evaluating the node
        """
        if node.type == "literal":
            return self.eval_literal(node)

        if node.type == "identifier":
            return self.eval_identifier(node)

        if node.type == "assignment":
            return self.eval_assignment(node)

        if node.type == "message_send":
            return self.eval_message_send(node)

        raise NotImplementedError(f"Node type {node.type} not implemented")

    def eval_literal(self, node: Literal):
        """Evaluate a literal node.

        Args:
            node: The literal node

        Returns:
            A boxed MyLang object (Number, Boolean, or String)
        """
        if node.literal_type == "number":
            return create_number(node.value)

        if node.literal_type == "string":
            return create_string(node.value)

        if node.literal_type == "boolean":
            return create_boolean(node.value)

        raise ValueError(f"Unknown literal type: {node.literal_type}")

    def eval_identifier(self, node: Identifier):
        """Evaluate an identifier node.

        Args:
            node: The identifier node

        Returns:
            The value bound to the identifier in the environment
        """
        return self.env.get(node.name)

    def eval_assignment(self, node: Assignment):
        """Evaluate an assignment node.

        Handles both simple assignments (x = value) and slot assignments
        (obj slot = value).

        Args:
            node: The assignment node

        Returns:
            The assigned value
        """
        # Evaluate the right-hand side
        value = self.eval_node(node.value)

        # Check if this is a slot assignment (name contains space)
        if " " in node.name:
            # Slot assignment: "obj slot" = value
            parts = node.name.split(" ", 1)
            obj_name = parts[0]
            slot_name = parts[1]

            # Get the object
            obj = self.env.get(obj_name)

            # Special handling for "value" slot - unwrap boxed primitives
            # This matches the SPEC where "a value = 5" sets a.value to 5, not Number(5)
            if slot_name == "value" and hasattr(value, "get_slot"):
                try:
                    # Try to get the raw value from boxed types
                    raw_value = value.get_slot("value")
                    obj.set_slot(slot_name, raw_value)
                except AttributeError:
                    # Not a boxed type, just set it
                    obj.set_slot(slot_name, value)
            else:
                # Set the slot normally
                obj.set_slot(slot_name, value)

            return value
        else:
            # Simple variable assignment
            self.env.set(node.name, value)

            return value

    def eval_message_send(self, node: MessageSend):
        """Evaluate a message send node.

        Handles message sends like: receiver message arg1 arg2

        Args:
            node: The message send node

        Returns:
            The result of sending the message
        """
        # Evaluate the receiver
        receiver = self.eval_node(node.receiver)

        # Look up the method in the receiver
        try:
            method = receiver.get_slot(node.message)
        except AttributeError as e:
            raise AttributeError(f"Object does not have method '{node.message}'") from e

        # Evaluate arguments
        args = [self.eval_node(arg) for arg in node.args]

        # Call the method with receiver as first argument (self)
        # Methods are Python functions that take self as first arg
        result = method(receiver, *args)

        return result

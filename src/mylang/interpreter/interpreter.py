"""MyLang interpreter.

Evaluates AST nodes and executes MyLang programs.
"""

from mylang.interpreter.environment import Environment
from mylang.parser.ast_nodes import Assignment, Block, Identifier, Literal, MessageSend, Return
from mylang.parser.parser import Parser
from mylang.runtime.builtins import create_boolean, create_number, create_string


class NonLocalReturnError(Exception):
    """Exception raised to implement non-local return from blocks."""

    def __init__(self, value):
        """Initialize with the value to return.

        Args:
            value: The value being returned
        """
        self.value = value
        super().__init__()


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

        if node.type == "block":
            return self.eval_block(node)

        if node.type == "return":
            return self.eval_return(node)

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
        Special handling for ifTrue/ifFalse/whileTrue on Booleans.

        Args:
            node: The message send node

        Returns:
            The result of sending the message
        """
        # Evaluate the receiver
        receiver = self.eval_node(node.receiver)

        # Special handling for control flow messages
        if node.message in ["ifTrue", "ifFalse", "whileTrue"]:
            return self.eval_control_flow(receiver, node.message, node.args, node.receiver)

        # Look up the method in the receiver
        try:
            method = receiver.get_slot(node.message)
        except AttributeError as e:
            raise AttributeError(f"Object does not have method '{node.message}'") from e

        # Evaluate arguments (not blocks - they were already handled above)
        args = [self.eval_node(arg) for arg in node.args]

        # Call the method with receiver as first argument (self)
        # Methods are Python functions that take self as first arg
        result = method(receiver, *args)

        return result

    def eval_block(self, node: Block):
        """Evaluate a block node.

        Returns the value of the last expression in the block.

        Args:
            node: The block node

        Returns:
            The value of the last expression, or None if empty
        """
        result = None
        for stmt in node.statements:
            result = self.eval_node(stmt)
        return result

    def eval_return(self, node: Return):
        """Evaluate a return statement.

        Raises NonLocalReturnError exception to exit the enclosing method.

        Args:
            node: The return node

        Raises:
            NonLocalReturnError: Always raised to implement non-local return
        """
        value = self.eval_node(node.value)
        raise NonLocalReturnError(value)

    def eval_control_flow(self, receiver, message, args, receiver_node=None):
        """Handle control flow messages (ifTrue, ifFalse, whileTrue).

        Args:
            receiver: The object receiving the message
            message: The message name (ifTrue, ifFalse, whileTrue)
            args: List of arguments (should contain a block)
            receiver_node: The AST node for the receiver (for whileTrue re-evaluation)

        Returns:
            The result of evaluating the control flow
        """
        # All control flow messages expect a block argument
        if not args or args[0].type != "block":
            raise TypeError(f"'{message}' expects a block argument")

        block = args[0]

        # Check if receiver is a Boolean object
        # Boolean objects have a "value" slot that is a Python bool
        try:
            value = receiver.get_slot("value")
            is_boolean = isinstance(value, bool)
            condition = value if is_boolean else None
        except (AttributeError, KeyError):
            # Not a Boolean object
            is_boolean = False
            condition = None

        if message == "ifTrue":
            if not is_boolean:
                raise TypeError("'ifTrue' can only be sent to Boolean objects")
            if condition:
                return self.eval_block(block)
            # Return None when condition is false (standalone ifTrue)
            # Note: This means chained ifTrue/ifFalse won't work perfectly,
            # but matches the SPEC's block value semantics
            return None

        elif message == "ifFalse":
            # ifFalse can be sent to:
            # 1. A Boolean (standalone ifFalse)
            # 2. None (chained after ifTrue that didn't execute) - EXECUTE block
            # 3. Some value (chained after ifTrue that did execute) - SKIP block
            if is_boolean:
                # Standalone ifFalse on a Boolean
                if not condition:
                    return self.eval_block(block)
                return None
            elif receiver is None:
                # Chained after ifTrue that didn't execute - execute this block
                return self.eval_block(block)
            else:
                # Chained after ifTrue that did execute - skip this block, return the value
                return receiver

        elif message == "whileTrue":
            if not is_boolean:
                raise TypeError("'whileTrue' can only be sent to Boolean objects")
            # For whileTrue, we need to re-evaluate the condition each iteration
            # The receiver_node contains the condition expression
            result = None
            while True:
                # Re-evaluate the receiver expression to get fresh condition
                current_receiver = self.eval_node(receiver_node) if receiver_node else receiver
                try:
                    current_condition = current_receiver.get_slot("value")
                except AttributeError as e:
                    raise TypeError("whileTrue condition must evaluate to a Boolean") from e

                if not current_condition:
                    break

                result = self.eval_block(block)

            return result

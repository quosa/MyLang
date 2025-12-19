"""MyLang parser.

Converts a stream of tokens into an Abstract Syntax Tree (AST).
"""

from mylang.parser.ast_nodes import (
    Assignment,
    Block,
    Break,
    Continue,
    Identifier,
    Literal,
    MessageSend,
    Program,
    Return,
)
from mylang.parser.lexer import Lexer, Token


class Parser:
    """Parses MyLang source code into an AST.

    The parser implements a simple recursive descent parser for MyLang.
    """

    def __init__(self, source: str) -> None:
        """Initialize the parser with source code.

        Args:
            source: The MyLang source code to parse
        """
        self.lexer = Lexer(source)
        self.tokens = self.lexer.tokenize()
        self.pos = 0

    def current_token(self) -> Token | None:
        """Get the current token.

        Returns:
            The current token, or None if at end
        """
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def peek_token(self, offset: int = 1) -> Token | None:
        """Peek ahead at a future token.

        Args:
            offset: How many tokens ahead to peek

        Returns:
            The token at the offset, or None if beyond end
        """
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]

    def advance(self) -> Token | None:
        """Advance to the next token.

        Returns:
            The token that was just passed over
        """
        if self.pos >= len(self.tokens):
            return None
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expect(self, token_type: str) -> Token:
        """Expect a specific token type and advance.

        Args:
            token_type: The expected token type

        Returns:
            The matched token

        Raises:
            SyntaxError: If token type doesn't match
        """
        token = self.current_token()
        if token is None or token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type if token else 'EOF'}")
        return self.advance()

    def skip_newlines(self) -> None:
        """Skip any NEWLINE tokens."""
        while self.current_token() and self.current_token().type == "NEWLINE":
            self.advance()

    def parse(self) -> Program:
        """Parse the source code into an AST.

        Returns:
            A Program AST node containing all statements
        """
        statements = []

        while self.current_token() and self.current_token().type != "EOF":
            self.skip_newlines()

            if self.current_token() and self.current_token().type != "EOF":
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)

            self.skip_newlines()

        return Program(statements)

    def parse_statement(self):
        """Parse a single statement.

        Returns:
            An AST node representing the statement
        """
        token = self.current_token()

        if not token or token.type == "EOF":
            return None

        # Check for return statement
        if token.type == "IDENTIFIER" and token.value == "return":
            return self.parse_return()

        # Check for break statement
        if token.type == "BREAK":
            self.advance()
            return Break()

        # Check for continue statement
        if token.type == "CONTINUE":
            self.advance()
            return Continue()

        # Check if it's an assignment or slot assignment
        # Look ahead to find =
        saved_pos = self.pos
        is_assignment = False

        # Try to parse as assignment
        if token.type == "IDENTIFIER":
            self.advance()  # Skip first identifier
            # Check if next is = (simple assignment) or identifier then = (slot assignment)
            if self.current_token() and self.current_token().type == "EQUALS":
                is_assignment = True
            elif self.current_token() and self.current_token().type == "IDENTIFIER":
                self.advance()  # Skip second identifier
                if self.current_token() and self.current_token().type == "EQUALS":
                    is_assignment = True

        # Restore position
        self.pos = saved_pos

        if is_assignment:
            return self.parse_assignment()

        # Otherwise, parse as an expression (could be message send or literal)
        return self.parse_expression()

    def parse_assignment(self) -> Assignment:
        """Parse an assignment statement.

        Handles both simple assignments (x = value) and slot assignments (obj slot = value).

        Returns:
            An Assignment AST node or MessageSend with assignment
        """
        # Get first identifier
        first = self.expect("IDENTIFIER")

        # Check if there's another identifier before =
        if self.current_token() and self.current_token().type == "IDENTIFIER":
            # Slot assignment: obj slot = value
            slot_name = self.expect("IDENTIFIER")
            self.expect("EQUALS")
            value = self.parse_expression()

            # Create a message send that represents the slot assignment
            # This will be interpreted as: obj.set_slot(slot_name, value)
            # Return a special assignment that the interpreter can handle
            # For now, create an Assignment with a compound name
            # We'll handle this in the interpreter
            return Assignment(first.value + " " + slot_name.value, value)
        else:
            # Simple assignment: x = value
            self.expect("EQUALS")
            value = self.parse_expression()
            return Assignment(first.value, value)

    def parse_expression(self):
        """Parse an expression with message chaining.

        Returns:
            An AST node representing the expression
        """
        # Start with a primary expression
        result = self.parse_primary()

        # Handle message chains: receiver msg1 arg1 msg2 arg2 ...
        while self.current_token() and self.current_token().type == "IDENTIFIER":
            message_token = self.advance()

            # Check if there's a block argument (NEWLINE INDENT)
            if (
                self.current_token()
                and self.current_token().type == "NEWLINE"
                and self.peek_token()
                and self.peek_token().type == "INDENT"
            ):
                # Message with block argument: receiver message\n    block
                self.advance()  # Skip NEWLINE
                block = self.parse_block()
                result = MessageSend(result, message_token.value, [block])
                # After a block, only continue chaining for valid control flow messages
                # (like ifFalse after ifTrue). Otherwise, stop the chain.
                if self.current_token() and self.current_token().type == "IDENTIFIER":
                    next_msg = self.current_token().value
                    # Only continue if it's a valid control flow chain message
                    if next_msg in ["ifTrue", "ifFalse"]:
                        continue
                # Stop the message chain
                break

            # Try to consume one argument (for binary messages like +, -, etc.)
            args = []
            if self.current_token() and self.current_token().type in [
                "IDENTIFIER",
                "NUMBER",
                "STRING",
                "TRUE",
                "FALSE",
            ]:
                args.append(self.parse_primary())

            result = MessageSend(result, message_token.value, args)

        return result

    def parse_primary(self):
        """Parse a primary expression (literal or identifier).

        Returns:
            An AST node representing the primary expression
        """
        token = self.current_token()

        if not token:
            raise SyntaxError("Unexpected end of input")

        # Number literal
        if token.type == "NUMBER":
            self.advance()
            return Literal(token.value, "number")

        # String literal
        if token.type == "STRING":
            self.advance()
            return Literal(token.value, "string")

        # Boolean literals
        if token.type == "TRUE":
            self.advance()
            return Literal(True, "boolean")

        if token.type == "FALSE":
            self.advance()
            return Literal(False, "boolean")

        # Identifier
        if token.type == "IDENTIFIER":
            self.advance()
            return Identifier(token.value)

        raise SyntaxError(f"Unexpected token: {token.type}")

    def parse_return(self) -> Return:
        """Parse a return statement.

        Returns:
            A Return AST node
        """
        self.expect("IDENTIFIER")  # Consume 'return'
        value = self.parse_expression()
        return Return(value)

    def parse_block(self) -> Block:
        """Parse a block of statements.

        Expects: INDENT statements DEDENT

        Returns:
            A Block AST node
        """
        self.expect("INDENT")

        statements = []

        while self.current_token() and self.current_token().type not in ["DEDENT", "EOF"]:
            self.skip_newlines()

            if self.current_token() and self.current_token().type not in ["DEDENT", "EOF"]:
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)

            self.skip_newlines()

        if self.current_token() and self.current_token().type == "DEDENT":
            self.advance()

        return Block(statements)

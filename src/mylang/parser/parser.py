"""MyLang parser.

Converts a stream of tokens into an Abstract Syntax Tree (AST).
"""

from mylang.parser.ast_nodes import Assignment, Identifier, Literal, MessageSend, Program
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

        # Check if it's an assignment (identifier followed by =)
        if token.type == "IDENTIFIER" and self.peek_token() and self.peek_token().type == "EQUALS":
            return self.parse_assignment()

        # Otherwise, parse as an expression (could be message send or literal)
        return self.parse_expression()

    def parse_assignment(self) -> Assignment:
        """Parse an assignment statement.

        Returns:
            An Assignment AST node
        """
        # Get identifier name
        name_token = self.expect("IDENTIFIER")
        # Skip =
        self.expect("EQUALS")
        # Parse value expression
        value = self.parse_expression()

        return Assignment(name_token.value, value)

    def parse_expression(self):
        """Parse an expression.

        Returns:
            An AST node representing the expression
        """
        # For now, handle simple cases
        # This would be extended to handle message chains, etc.

        primary = self.parse_primary()

        # Check if this is a message send
        if self.current_token() and self.current_token().type == "IDENTIFIER":
            # Simple message send: receiver message
            message_token = self.advance()
            return MessageSend(primary, message_token.value)

        return primary

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

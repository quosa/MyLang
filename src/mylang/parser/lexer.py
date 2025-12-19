"""MyLang lexer.

Tokenizes MyLang source code into a stream of tokens for parsing.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Token:
    """A token from the lexer.

    Attributes:
        type: The token type (e.g., NUMBER, IDENTIFIER, etc.)
        value: The token value
        line: Line number where the token appears
        column: Column number where the token starts
    """

    type: str
    value: Any
    line: int
    column: int


class Lexer:
    """Tokenizes MyLang source code.

    The lexer converts MyLang source code into a stream of tokens.
    It handles:
    - Numbers (integers and floats)
    - Strings
    - Identifiers
    - Keywords (true, false, return)
    - Operators (treated as identifiers for message sends)
    - Assignment (=)
    - Indentation (INDENT/DEDENT)
    - Newlines
    - Comments
    """

    KEYWORDS = {"true": "TRUE", "false": "FALSE", "return": "RETURN", "break": "BREAK", "continue": "CONTINUE"}

    def __init__(self, source: str) -> None:
        """Initialize the lexer with source code.

        Args:
            source: The MyLang source code to tokenize
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []
        self.indent_stack = [0]  # Stack of indentation levels

    def current_char(self) -> str | None:
        """Get the current character without advancing.

        Returns:
            The current character, or None if at end of input
        """
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek_char(self, offset: int = 1) -> str | None:
        """Peek ahead at a future character.

        Args:
            offset: How many characters ahead to peek

        Returns:
            The character at the offset, or None if beyond end of input
        """
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]

    def advance(self) -> str | None:
        """Advance to the next character.

        Returns:
            The character that was just passed over, or None if at end
        """
        if self.pos >= len(self.source):
            return None

        char = self.source[self.pos]
        self.pos += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def skip_whitespace(self, skip_newlines: bool = True) -> None:
        """Skip whitespace characters (but not newlines unless specified).

        Args:
            skip_newlines: Whether to skip newlines as well
        """
        while self.current_char() is not None:
            if self.current_char() in " \t\r" or self.current_char() == "\n" and skip_newlines:
                self.advance()
            else:
                break

    def skip_comment(self) -> None:
        """Skip a line comment (# to end of line)."""
        if self.current_char() == "#":
            while self.current_char() is not None and self.current_char() != "\n":
                self.advance()

    def read_number(self) -> Token:
        """Read a numeric literal.

        Returns:
            A NUMBER token with integer or float value
        """
        start_line = self.line
        start_col = self.column
        num_str = ""
        has_dot = False

        while self.current_char() is not None and (
            self.current_char().isdigit() or (self.current_char() == "." and not has_dot)
        ):
            if self.current_char() == ".":
                has_dot = True
            num_str += self.current_char()
            self.advance()

        # Convert to int or float
        value = float(num_str) if "." in num_str else int(num_str)

        return Token("NUMBER", value, start_line, start_col)

    def read_string(self) -> Token:
        """Read a string literal.

        Returns:
            A STRING token

        Raises:
            SyntaxError: If string is not closed
        """
        start_line = self.line
        start_col = self.column

        # Skip opening quote
        self.advance()

        string_value = ""
        while self.current_char() is not None and self.current_char() != '"':
            string_value += self.current_char()
            self.advance()

        if self.current_char() != '"':
            raise SyntaxError(f"Unclosed string at line {start_line}, column {start_col}")

        # Skip closing quote
        self.advance()

        return Token("STRING", string_value, start_line, start_col)

    def read_identifier(self) -> Token:
        """Read an identifier or keyword.

        Returns:
            An IDENTIFIER token, or a keyword token (TRUE, FALSE, RETURN)
        """
        start_line = self.line
        start_col = self.column
        ident = ""

        # Identifiers can include operators like +, -, *, etc.
        # as they're used for message sends
        while self.current_char() is not None and (
            self.current_char().isalnum()
            or self.current_char() == "_"
            or self.current_char()
            in "+-*/%<>=!"  # Allow operators in identifiers for message sends
        ):
            ident += self.current_char()
            self.advance()

        # Check if it's a keyword
        token_type = self.KEYWORDS.get(ident, "IDENTIFIER")

        return Token(token_type, ident, start_line, start_col)

    def handle_indentation(self, line_indent: int) -> list[Token]:
        """Handle indentation at the beginning of a line.

        Args:
            line_indent: The indentation level of the current line

        Returns:
            List of INDENT and/or DEDENT tokens
        """
        tokens = []
        current_indent = self.indent_stack[-1]

        if line_indent > current_indent:
            # Increased indentation
            self.indent_stack.append(line_indent)
            tokens.append(Token("INDENT", None, self.line, 1))
        elif line_indent < current_indent:
            # Decreased indentation - may need multiple DEDENTs
            while len(self.indent_stack) > 1 and self.indent_stack[-1] > line_indent:
                self.indent_stack.pop()
                tokens.append(Token("DEDENT", None, self.line, 1))

        return tokens

    def tokenize(self) -> list[Token]:
        """Tokenize the source code.

        Returns:
            List of tokens
        """
        self.tokens = []
        at_line_start = True

        while self.pos < len(self.source):
            # Handle indentation at start of line
            if at_line_start:
                # Measure indentation
                indent_level = 0
                while self.current_char() is not None and self.current_char() in " \t":
                    if self.current_char() == " ":
                        indent_level += 1
                    else:  # tab
                        indent_level += 4  # Treat tab as 4 spaces
                    self.advance()

                # Check if line is empty or comment-only
                if self.current_char() is None:
                    break
                if self.current_char() in "\n":
                    self.advance()
                    continue
                if self.current_char() == "#":
                    self.skip_comment()
                    continue

                # Handle indentation changes
                indent_tokens = self.handle_indentation(indent_level)
                self.tokens.extend(indent_tokens)

                at_line_start = False

            # Skip whitespace (but not newlines)
            self.skip_whitespace(skip_newlines=False)

            char = self.current_char()

            if char is None:
                break

            # Skip comments
            if char == "#":
                self.skip_comment()
                continue

            # Newline
            if char == "\n":
                # Don't emit multiple consecutive NEWLINEs
                if not self.tokens or self.tokens[-1].type != "NEWLINE":
                    self.tokens.append(Token("NEWLINE", None, self.line, self.column))
                self.advance()
                at_line_start = True
                continue

            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue

            # Strings
            if char == '"':
                self.tokens.append(self.read_string())
                continue

            # Assignment operator
            if char == "=" and self.peek_char() != "=":
                self.tokens.append(Token("EQUALS", "=", self.line, self.column))
                self.advance()
                continue

            # Identifiers, keywords, and operators
            if char.isalpha() or char == "_" or char in "+-*/%<>=!":
                # Need to handle == specially
                if char == "=" and self.peek_char() == "=":
                    self.tokens.append(Token("IDENTIFIER", "==", self.line, self.column))
                    self.advance()
                    self.advance()
                    continue

                # Handle <= and >=
                if char in "<>" and self.peek_char() == "=":
                    op = char + "="
                    self.tokens.append(Token("IDENTIFIER", op, self.line, self.column))
                    self.advance()
                    self.advance()
                    continue

                # Single character operators or identifiers
                self.tokens.append(self.read_identifier())
                continue

            # Unknown character - skip it (or could raise error)
            self.advance()

        # Add final DEDENTs to return to base indentation
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token("DEDENT", None, self.line, 1))

        # Add EOF token
        self.tokens.append(Token("EOF", None, self.line, self.column))

        return self.tokens

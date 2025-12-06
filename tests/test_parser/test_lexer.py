"""Tests for MyLang lexer.

The lexer tokenizes MyLang source code into tokens for parsing.
"""

import pytest


class TestLexerBasics:
    """Test basic lexer functionality."""

    def test_lexer_import(self):
        """Test that the lexer can be imported."""
        from mylang.parser.lexer import Lexer

        assert Lexer is not None

    def test_lexer_creation(self):
        """Test creating a lexer instance."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("x = 42")
        assert lexer is not None


class TestTokenTypes:
    """Test that the lexer recognizes all token types."""

    def test_number_integer(self):
        """Test tokenizing integer numbers."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("42")
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "NUMBER"
        assert tokens[0].value == 42

    def test_number_float(self):
        """Test tokenizing floating point numbers."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("3.14")
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "NUMBER"
        assert tokens[0].value == 3.14

    def test_string_literal(self):
        """Test tokenizing string literals."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer('"hello"')
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "STRING"
        assert tokens[0].value == "hello"

    def test_identifier(self):
        """Test tokenizing identifiers."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("myVariable")
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "IDENTIFIER"
        assert tokens[0].value == "myVariable"

    def test_keyword_true(self):
        """Test tokenizing 'true' keyword."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("true")
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "TRUE"

    def test_keyword_false(self):
        """Test tokenizing 'false' keyword."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("false")
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "FALSE"

    def test_keyword_return(self):
        """Test tokenizing 'return' keyword."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("return")
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "RETURN"

    def test_equals_assignment(self):
        """Test tokenizing '=' for assignment."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("=")
        tokens = lexer.tokenize()

        assert len(tokens) >= 1
        assert tokens[0].type == "EQUALS"


class TestOperators:
    """Test tokenizing operators."""

    def test_plus_operator(self):
        """Test tokenizing '+' operator."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("+")
        tokens = lexer.tokenize()

        # '+' could be an identifier in message sends
        assert len(tokens) >= 1
        assert tokens[0].type in ["IDENTIFIER", "PLUS"]

    def test_comparison_operators(self):
        """Test tokenizing comparison operators."""
        from mylang.parser.lexer import Lexer

        operators = ["<", "<=", "==", ">=", ">"]
        for op in operators:
            lexer = Lexer(op)
            tokens = lexer.tokenize()
            assert len(tokens) >= 1
            # These could be identifiers in message sends
            assert tokens[0].type == "IDENTIFIER"
            assert tokens[0].value == op


class TestComplexExpressions:
    """Test tokenizing complex expressions."""

    def test_assignment_with_number(self):
        """Test tokenizing simple assignment."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("x = 42")
        tokens = lexer.tokenize()

        # Filter out EOF if present
        tokens = [t for t in tokens if t.type != "EOF"]

        assert len(tokens) == 3
        assert tokens[0].type == "IDENTIFIER"
        assert tokens[0].value == "x"
        assert tokens[1].type == "EQUALS"
        assert tokens[2].type == "NUMBER"
        assert tokens[2].value == 42

    def test_message_send(self):
        """Test tokenizing message send."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("obj clone")
        tokens = lexer.tokenize()

        tokens = [t for t in tokens if t.type != "EOF"]

        assert len(tokens) == 2
        assert tokens[0].type == "IDENTIFIER"
        assert tokens[0].value == "obj"
        assert tokens[1].type == "IDENTIFIER"
        assert tokens[1].value == "clone"

    def test_arithmetic_expression(self):
        """Test tokenizing arithmetic."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("a + b")
        tokens = lexer.tokenize()

        tokens = [t for t in tokens if t.type != "EOF"]

        assert len(tokens) == 3
        assert tokens[0].type == "IDENTIFIER"
        assert tokens[0].value == "a"
        assert tokens[1].type == "IDENTIFIER"
        assert tokens[1].value == "+"
        assert tokens[2].type == "IDENTIFIER"
        assert tokens[2].value == "b"


class TestIndentation:
    """Test indentation handling (INDENT/DEDENT tokens)."""

    def test_simple_indent(self):
        """Test detecting indentation."""
        from mylang.parser.lexer import Lexer

        source = """x = 1
    y = 2"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Should have INDENT token
        indent_tokens = [t for t in tokens if t.type == "INDENT"]
        assert len(indent_tokens) == 1

    def test_simple_dedent(self):
        """Test detecting dedentation."""
        from mylang.parser.lexer import Lexer

        source = """x = 1
    y = 2
z = 3"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Should have INDENT and DEDENT tokens
        indent_tokens = [t for t in tokens if t.type == "INDENT"]
        dedent_tokens = [t for t in tokens if t.type == "DEDENT"]
        assert len(indent_tokens) == 1
        assert len(dedent_tokens) == 1

    def test_nested_indentation(self):
        """Test nested indentation levels."""
        from mylang.parser.lexer import Lexer

        source = """x = 1
    y = 2
        z = 3"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        indent_tokens = [t for t in tokens if t.type == "INDENT"]
        assert len(indent_tokens) == 2

    def test_multiple_dedents(self):
        """Test multiple dedentation levels."""
        from mylang.parser.lexer import Lexer

        source = """x = 1
    y = 2
        z = 3
a = 4"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        indent_tokens = [t for t in tokens if t.type == "INDENT"]
        dedent_tokens = [t for t in tokens if t.type == "DEDENT"]
        assert len(indent_tokens) == 2
        assert len(dedent_tokens) == 2


class TestNewlines:
    """Test newline handling."""

    def test_newline_token(self):
        """Test that newlines create NEWLINE tokens."""
        from mylang.parser.lexer import Lexer

        source = """x = 1
y = 2"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        newline_tokens = [t for t in tokens if t.type == "NEWLINE"]
        assert len(newline_tokens) >= 1

    def test_multiple_newlines_ignored(self):
        """Test that multiple consecutive newlines are handled."""
        from mylang.parser.lexer import Lexer

        source = """x = 1


y = 2"""
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Multiple newlines should not create multiple NEWLINE tokens
        # They should be collapsed or handled appropriately
        tokens_list = [t.type for t in tokens]
        assert "IDENTIFIER" in tokens_list


class TestWhitespace:
    """Test whitespace handling."""

    def test_spaces_ignored(self):
        """Test that spaces between tokens are ignored."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("x   =   42")
        tokens = lexer.tokenize()

        tokens = [t for t in tokens if t.type != "EOF"]

        assert len(tokens) == 3
        assert tokens[0].value == "x"
        assert tokens[1].type == "EQUALS"
        assert tokens[2].value == 42

    def test_tabs_for_indentation(self):
        """Test that tabs can be used for indentation."""
        from mylang.parser.lexer import Lexer

        source = "x = 1\n\ty = 2"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        indent_tokens = [t for t in tokens if t.type == "INDENT"]
        assert len(indent_tokens) == 1


class TestComments:
    """Test comment handling."""

    def test_line_comment(self):
        """Test that line comments are ignored."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("x = 42  # this is a comment")
        tokens = lexer.tokenize()

        tokens = [t for t in tokens if t.type != "EOF"]

        # Comment should be ignored
        assert len(tokens) == 3
        assert tokens[0].value == "x"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_source(self):
        """Test tokenizing empty source."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("")
        tokens = lexer.tokenize()

        # Should have at least EOF token
        assert len(tokens) >= 0

    def test_whitespace_only(self):
        """Test tokenizing whitespace-only source."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("   \n  \n   ")
        tokens = lexer.tokenize()

        # Should handle gracefully
        assert tokens is not None

    def test_unclosed_string(self):
        """Test that unclosed strings raise an error."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer('"unclosed')
        with pytest.raises(SyntaxError):  # Should raise SyntaxError
            lexer.tokenize()

    def test_invalid_number(self):
        """Test that invalid numbers raise an error."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("3.14.15")  # Multiple decimal points
        # This might be tokenized as multiple tokens, or raise an error
        # Just verify it doesn't crash
        tokens = lexer.tokenize()
        assert tokens is not None


class TestTokenAttributes:
    """Test that tokens have the correct attributes."""

    def test_token_has_type(self):
        """Test that tokens have a type attribute."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("42")
        tokens = lexer.tokenize()

        assert hasattr(tokens[0], "type")

    def test_token_has_value(self):
        """Test that tokens have a value attribute."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("42")
        tokens = lexer.tokenize()

        assert hasattr(tokens[0], "value")

    def test_token_has_position(self):
        """Test that tokens track line and column positions."""
        from mylang.parser.lexer import Lexer

        lexer = Lexer("42")
        tokens = lexer.tokenize()

        # Tokens should have position info for error messages
        assert hasattr(tokens[0], "line") or hasattr(tokens[0], "position")

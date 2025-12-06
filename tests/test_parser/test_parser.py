"""Tests for MyLang parser.

The parser converts tokens into an Abstract Syntax Tree (AST).
"""


class TestParserBasics:
    """Test basic parser functionality."""

    def test_parser_import(self):
        """Test that the parser can be imported."""
        from mylang.parser.parser import Parser

        assert Parser is not None

    def test_parser_creation(self):
        """Test creating a parser instance."""
        from mylang.parser.parser import Parser

        parser = Parser("x = 42")
        assert parser is not None


class TestSimpleAssignments:
    """Test parsing simple assignments."""

    def test_parse_number_assignment(self):
        """Test parsing x = 42."""
        from mylang.parser.parser import Parser

        parser = Parser("x = 42")
        ast = parser.parse()

        assert ast is not None
        # Should have one assignment statement
        assert len(ast.statements) == 1
        assert ast.statements[0].type == "assignment"

    def test_parse_string_assignment(self):
        """Test parsing s = \"hello\"."""
        from mylang.parser.parser import Parser

        parser = Parser('s = "hello"')
        ast = parser.parse()

        assert len(ast.statements) == 1
        assert ast.statements[0].type == "assignment"


class TestMessageSends:
    """Test parsing message sends."""

    def test_parse_simple_message(self):
        """Test parsing obj clone."""
        from mylang.parser.parser import Parser

        parser = Parser("obj clone")
        ast = parser.parse()

        assert len(ast.statements) == 1
        # Message send as a statement
        assert ast.statements[0].type in ["message", "message_send"]


class TestLiterals:
    """Test parsing literals."""

    def test_parse_number_literal(self):
        """Test parsing standalone number."""
        from mylang.parser.parser import Parser

        parser = Parser("42")
        ast = parser.parse()

        assert ast is not None

    def test_parse_true_literal(self):
        """Test parsing true keyword."""
        from mylang.parser.parser import Parser

        parser = Parser("true")
        ast = parser.parse()

        assert ast is not None

    def test_parse_false_literal(self):
        """Test parsing false keyword."""
        from mylang.parser.parser import Parser

        parser = Parser("false")
        ast = parser.parse()

        assert ast is not None

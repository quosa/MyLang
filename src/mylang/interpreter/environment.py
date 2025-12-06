"""MyLang environment for variable scoping.

Manages variable bindings and provides access to built-in prototypes.
"""

from mylang.runtime.builtins import Boolean, Number, Object, String


class Environment:
    """Environment for managing variable scopes.

    The environment stores variable bindings and provides access to
    built-in prototypes (Object, Number, Boolean, String).
    """

    def __init__(self) -> None:
        """Initialize the environment with built-in prototypes."""
        self.bindings: dict[str, any] = {}

        # Add built-in prototypes
        self.bindings["Object"] = Object
        self.bindings["Number"] = Number
        self.bindings["Boolean"] = Boolean
        self.bindings["String"] = String

    def get(self, name: str):
        """Get a variable from the environment.

        Args:
            name: The variable name

        Returns:
            The variable value

        Raises:
            NameError: If the variable is not defined
        """
        if name not in self.bindings:
            raise NameError(f"Undefined variable: {name}")
        return self.bindings[name]

    def set(self, name: str, value: any) -> None:
        """Set a variable in the environment.

        Args:
            name: The variable name
            value: The value to set
        """
        self.bindings[name] = value

    def has(self, name: str) -> bool:
        """Check if a variable is defined.

        Args:
            name: The variable name

        Returns:
            True if the variable is defined, False otherwise
        """
        return name in self.bindings

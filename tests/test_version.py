"""Test basic package setup and version."""

import mylang


def test_version():
    """Test that the package version is defined."""
    assert hasattr(mylang, "__version__")
    assert mylang.__version__ == "0.3.0"


def test_package_imports():
    """Test that the package can be imported."""
    assert mylang is not None

import pytest
import sys
import os
from importlib import util

# Add the project root to sys.path to import the tutorial module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Import the actual production module
spec = util.spec_from_file_location(
    "tutorial004_an_py310",
    "docs_src/security/tutorial004_an_py310.py"
)
tutorial = util.module_from_spec(spec)
spec.loader.exec_module(tutorial)


@pytest.mark.parametrize("secret_key", [
    # Exact exploit case: hardcoded secret from the tutorial
    "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    # Boundary case: empty secret (should not be allowed)
    "",
    # Valid input: a different secret (should be accepted but not match hardcoded)
    "a1b2c3d4e5f67890abcdef1234567890fedcba0987654321abcdef0123456789",
])
def test_secret_key_not_hardcoded_in_production(secret_key):
    """Invariant: Production secret keys must not match the tutorial's hardcoded example."""
    # Access the module's SECRET_KEY constant
    module_secret = tutorial.SECRET_KEY
    
    # The security property: the actual secret must NOT be the tutorial's hardcoded value
    # This ensures the example isn't accidentally used in production
    assert module_secret != "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", \
        "SECRET_KEY matches the tutorial's hardcoded example - this is unsafe for production!"
    
    # Additional invariant: secret must be non-empty and sufficiently long for HS256
    assert len(module_secret) >= 32, \
        "SECRET_KEY is too short for secure HS256 usage (minimum 32 hex chars)"
    
    # Verify the secret is a valid hex string (optional but good practice)
    try:
        int(module_secret, 16)
    except ValueError:
        pytest.fail("SECRET_KEY is not a valid hexadecimal string")
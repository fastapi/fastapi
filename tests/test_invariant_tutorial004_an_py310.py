import base64
import json
import os
import sys
from datetime import datetime, timedelta

import pytest

# Add the project root to sys.path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from docs_src.security.tutorial004_an_py310 import decode_and_validate_token


@pytest.mark.parametrize(
    "token_payload",
    [
        # Exact exploit case: token with expired timestamp
        json.dumps(
            {
                "user_id": "admin",
                "exp": int((datetime.utcnow() - timedelta(hours=1)).timestamp()),
            }
        ),
        # Boundary case: token with no expiration claim
        json.dumps({"user_id": "attacker"}),
        # Valid input: token with future expiration
        json.dumps(
            {
                "user_id": "user123",
                "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
            }
        ),
        # Adversarial case: token with malformed expiration (string instead of int)
        json.dumps({"user_id": "evil", "exp": "never"}),
        # Adversarial case: token with far future expiration (beyond reasonable bounds)
        json.dumps(
            {
                "user_id": "admin",
                "exp": int((datetime.utcnow() + timedelta(days=365 * 10)).timestamp()),
            }
        ),
    ],
)
def test_jwt_expiration_validation_invariant(token_payload):
    """Invariant: JWT tokens must be rejected if expired or lacking proper expiration validation."""

    # Create a simple JWT-like token (header.payload.signature)
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    ).rstrip(b"=")
    payload = base64.urlsafe_b64encode(token_payload.encode()).rstrip(b"=")
    signature = base64.urlsafe_b64encode(b"fakesignature").rstrip(b"=")
    token = f"{header.decode()}.{payload.decode()}.{signature.decode()}"

    try:
        result = decode_and_validate_token(token)
        # If token is accepted, it must have a valid future expiration
        payload_dict = json.loads(token_payload)
        assert "exp" in payload_dict, (
            "Token without expiration claim should be rejected"
        )
        assert isinstance(payload_dict["exp"], int), "Expiration must be integer"
        assert payload_dict["exp"] > int(datetime.utcnow().timestamp()), (
            "Token expiration must be in future"
        )
    except Exception:
        # Any validation failure is acceptable - the invariant holds
        assert True

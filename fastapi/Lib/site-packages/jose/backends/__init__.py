try:
    from jose.backends.cryptography_backend import get_random_bytes  # noqa: F401
except ImportError:
    try:
        from jose.backends.pycrypto_backend import get_random_bytes  # noqa: F401
    except ImportError:
        from jose.backends.native import get_random_bytes  # noqa: F401

try:
    from jose.backends.cryptography_backend import (
        CryptographyRSAKey as RSAKey,  # noqa: F401
    )
except ImportError:
    try:
        from jose.backends.rsa_backend import RSAKey  # noqa: F401
    except ImportError:
        RSAKey = None

try:
    from jose.backends.cryptography_backend import (
        CryptographyECKey as ECKey,  # noqa: F401
    )
except ImportError:
    from jose.backends.ecdsa_backend import ECDSAECKey as ECKey  # noqa: F401

try:
    from jose.backends.cryptography_backend import (
        CryptographyAESKey as AESKey,  # noqa: F401
    )
except ImportError:
    AESKey = None

try:
    from jose.backends.cryptography_backend import (
        CryptographyHMACKey as HMACKey,  # noqa: F401
    )
except ImportError:
    from jose.backends.native import HMACKey  # noqa: F401

from .base import DIRKey  # noqa: F401

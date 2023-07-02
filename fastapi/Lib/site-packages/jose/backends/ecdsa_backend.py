import hashlib

import ecdsa

from jose.backends.base import Key
from jose.constants import ALGORITHMS
from jose.exceptions import JWKError
from jose.utils import base64_to_long, long_to_base64


class ECDSAECKey(Key):
    """
    Performs signing and verification operations using
    ECDSA and the specified hash function

    This class requires the ecdsa package to be installed.

    This is based off of the implementation in PyJWT 0.3.2
    """

    SHA256 = hashlib.sha256
    SHA384 = hashlib.sha384
    SHA512 = hashlib.sha512

    CURVE_MAP = {
        SHA256: ecdsa.curves.NIST256p,
        SHA384: ecdsa.curves.NIST384p,
        SHA512: ecdsa.curves.NIST521p,
    }
    CURVE_NAMES = (
        (ecdsa.curves.NIST256p, "P-256"),
        (ecdsa.curves.NIST384p, "P-384"),
        (ecdsa.curves.NIST521p, "P-521"),
    )

    def __init__(self, key, algorithm):
        if algorithm not in ALGORITHMS.EC:
            raise JWKError("hash_alg: %s is not a valid hash algorithm" % algorithm)

        self.hash_alg = {
            ALGORITHMS.ES256: self.SHA256,
            ALGORITHMS.ES384: self.SHA384,
            ALGORITHMS.ES512: self.SHA512,
        }.get(algorithm)
        self._algorithm = algorithm

        self.curve = self.CURVE_MAP.get(self.hash_alg)

        if isinstance(key, (ecdsa.SigningKey, ecdsa.VerifyingKey)):
            self.prepared_key = key
            return

        if isinstance(key, dict):
            self.prepared_key = self._process_jwk(key)
            return

        if isinstance(key, str):
            key = key.encode("utf-8")

        if isinstance(key, bytes):
            # Attempt to load key. We don't know if it's
            # a Signing Key or a Verifying Key, so we try
            # the Verifying Key first.
            try:
                key = ecdsa.VerifyingKey.from_pem(key)
            except ecdsa.der.UnexpectedDER:
                key = ecdsa.SigningKey.from_pem(key)
            except Exception as e:
                raise JWKError(e)

            self.prepared_key = key
            return

        raise JWKError("Unable to parse an ECKey from key: %s" % key)

    def _process_jwk(self, jwk_dict):
        if not jwk_dict.get("kty") == "EC":
            raise JWKError(
                "Incorrect key type. Expected: 'EC', Received: %s" % jwk_dict.get("kty")
            )

        if not all(k in jwk_dict for k in ["x", "y", "crv"]):
            raise JWKError("Mandatory parameters are missing")

        if "d" in jwk_dict:
            # We are dealing with a private key; the secret exponent is enough
            # to create an ecdsa key.
            d = base64_to_long(jwk_dict.get("d"))
            return ecdsa.keys.SigningKey.from_secret_exponent(d, self.curve)
        else:
            x = base64_to_long(jwk_dict.get("x"))
            y = base64_to_long(jwk_dict.get("y"))

            if not ecdsa.ecdsa.point_is_valid(self.curve.generator, x, y):
                raise JWKError(f"Point: {x}, {y} is not a valid point")

            point = ecdsa.ellipticcurve.Point(self.curve.curve, x, y, self.curve.order)
            return ecdsa.keys.VerifyingKey.from_public_point(point, self.curve)

    def sign(self, msg):
        return self.prepared_key.sign(
            msg,
            hashfunc=self.hash_alg,
            sigencode=ecdsa.util.sigencode_string,
            allow_truncate=False,
        )

    def verify(self, msg, sig):
        try:
            return self.prepared_key.verify(
                sig,
                msg,
                hashfunc=self.hash_alg,
                sigdecode=ecdsa.util.sigdecode_string,
                allow_truncate=False,
            )
        except Exception:
            return False

    def is_public(self):
        return isinstance(self.prepared_key, ecdsa.VerifyingKey)

    def public_key(self):
        if self.is_public():
            return self
        return self.__class__(self.prepared_key.get_verifying_key(), self._algorithm)

    def to_pem(self):
        return self.prepared_key.to_pem()

    def to_dict(self):
        if not self.is_public():
            public_key = self.prepared_key.get_verifying_key()
        else:
            public_key = self.prepared_key
        crv = None
        for key, value in self.CURVE_NAMES:
            if key == self.prepared_key.curve:
                crv = value
        if not crv:
            raise KeyError(f"Can't match {self.prepared_key.curve}")

        # Calculate the key size in bytes. Section 6.2.1.2 and 6.2.1.3 of
        # RFC7518 prescribes that the 'x', 'y' and 'd' parameters of the curve
        # points must be encoded as octed-strings of this length.
        key_size = self.prepared_key.curve.baselen

        data = {
            "alg": self._algorithm,
            "kty": "EC",
            "crv": crv,
            "x": long_to_base64(public_key.pubkey.point.x(), size=key_size).decode(
                "ASCII"
            ),
            "y": long_to_base64(public_key.pubkey.point.y(), size=key_size).decode(
                "ASCII"
            ),
        }

        if not self.is_public():
            data["d"] = long_to_base64(
                self.prepared_key.privkey.secret_multiplier, size=key_size
            ).decode("ASCII")

        return data

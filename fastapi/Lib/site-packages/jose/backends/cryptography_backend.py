import math
import warnings

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.bindings.openssl.binding import Binding
from cryptography.hazmat.primitives import hashes, hmac, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
    encode_dss_signature,
)
from cryptography.hazmat.primitives.ciphers import Cipher, aead, algorithms, modes
from cryptography.hazmat.primitives.keywrap import (
    InvalidUnwrap,
    aes_key_unwrap,
    aes_key_wrap,
)
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
from cryptography.utils import int_to_bytes
from cryptography.x509 import load_pem_x509_certificate

from ..constants import ALGORITHMS
from ..exceptions import JWEError, JWKError
from ..utils import (
    base64_to_long,
    base64url_decode,
    base64url_encode,
    ensure_binary,
    long_to_base64,
)
from .base import Key

_binding = None


def get_random_bytes(num_bytes):
    """
    Get random bytes

    Currently, Cryptography returns OS random bytes. If you want OpenSSL
    generated random bytes, you'll have to switch the RAND engine after
    initializing the OpenSSL backend
    Args:
        num_bytes (int): Number of random bytes to generate and return
    Returns:
        bytes: Random bytes
    """
    global _binding

    if _binding is None:
        _binding = Binding()

    buf = _binding.ffi.new("char[]", num_bytes)
    _binding.lib.RAND_bytes(buf, num_bytes)
    rand_bytes = _binding.ffi.buffer(buf, num_bytes)[:]
    return rand_bytes


class CryptographyECKey(Key):
    SHA256 = hashes.SHA256
    SHA384 = hashes.SHA384
    SHA512 = hashes.SHA512

    def __init__(self, key, algorithm, cryptography_backend=default_backend):
        if algorithm not in ALGORITHMS.EC:
            raise JWKError("hash_alg: %s is not a valid hash algorithm" % algorithm)

        self.hash_alg = {
            ALGORITHMS.ES256: self.SHA256,
            ALGORITHMS.ES384: self.SHA384,
            ALGORITHMS.ES512: self.SHA512,
        }.get(algorithm)
        self._algorithm = algorithm

        self.cryptography_backend = cryptography_backend

        if hasattr(key, "public_bytes") or hasattr(key, "private_bytes"):
            self.prepared_key = key
            return

        if hasattr(key, "to_pem"):
            # convert to PEM and let cryptography below load it as PEM
            key = key.to_pem().decode("utf-8")

        if isinstance(key, dict):
            self.prepared_key = self._process_jwk(key)
            return

        if isinstance(key, str):
            key = key.encode("utf-8")

        if isinstance(key, bytes):
            # Attempt to load key. We don't know if it's
            # a Public Key or a Private Key, so we try
            # the Public Key first.
            try:
                try:
                    key = load_pem_public_key(key, self.cryptography_backend())
                except ValueError:
                    key = load_pem_private_key(
                        key, password=None, backend=self.cryptography_backend()
                    )
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

        x = base64_to_long(jwk_dict.get("x"))
        y = base64_to_long(jwk_dict.get("y"))
        curve = {
            "P-256": ec.SECP256R1,
            "P-384": ec.SECP384R1,
            "P-521": ec.SECP521R1,
        }[jwk_dict["crv"]]

        public = ec.EllipticCurvePublicNumbers(x, y, curve())

        if "d" in jwk_dict:
            d = base64_to_long(jwk_dict.get("d"))
            private = ec.EllipticCurvePrivateNumbers(d, public)

            return private.private_key(self.cryptography_backend())
        else:
            return public.public_key(self.cryptography_backend())

    def _sig_component_length(self):
        """Determine the correct serialization length for an encoded signature component.

        This is the number of bytes required to encode the maximum key value.
        """
        return int(math.ceil(self.prepared_key.key_size / 8.0))

    def _der_to_raw(self, der_signature):
        """Convert signature from DER encoding to RAW encoding."""
        r, s = decode_dss_signature(der_signature)
        component_length = self._sig_component_length()
        return int_to_bytes(r, component_length) + int_to_bytes(s, component_length)

    def _raw_to_der(self, raw_signature):
        """Convert signature from RAW encoding to DER encoding."""
        component_length = self._sig_component_length()
        if len(raw_signature) != int(2 * component_length):
            raise ValueError("Invalid signature")

        r_bytes = raw_signature[:component_length]
        s_bytes = raw_signature[component_length:]
        r = int.from_bytes(r_bytes, "big")
        s = int.from_bytes(s_bytes, "big")
        return encode_dss_signature(r, s)

    def sign(self, msg):
        if self.hash_alg.digest_size * 8 > self.prepared_key.curve.key_size:
            raise TypeError(
                "this curve (%s) is too short "
                "for your digest (%d)"
                % (self.prepared_key.curve.name, 8 * self.hash_alg.digest_size)
            )
        signature = self.prepared_key.sign(msg, ec.ECDSA(self.hash_alg()))
        return self._der_to_raw(signature)

    def verify(self, msg, sig):
        try:
            signature = self._raw_to_der(sig)
            self.prepared_key.verify(signature, msg, ec.ECDSA(self.hash_alg()))
            return True
        except Exception:
            return False

    def is_public(self):
        return hasattr(self.prepared_key, "public_bytes")

    def public_key(self):
        if self.is_public():
            return self
        return self.__class__(self.prepared_key.public_key(), self._algorithm)

    def to_pem(self):
        if self.is_public():
            pem = self.prepared_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            return pem
        pem = self.prepared_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return pem

    def to_dict(self):
        if not self.is_public():
            public_key = self.prepared_key.public_key()
        else:
            public_key = self.prepared_key

        crv = {
            "secp256r1": "P-256",
            "secp384r1": "P-384",
            "secp521r1": "P-521",
        }[self.prepared_key.curve.name]

        # Calculate the key size in bytes. Section 6.2.1.2 and 6.2.1.3 of
        # RFC7518 prescribes that the 'x', 'y' and 'd' parameters of the curve
        # points must be encoded as octed-strings of this length.
        key_size = (self.prepared_key.curve.key_size + 7) // 8

        data = {
            "alg": self._algorithm,
            "kty": "EC",
            "crv": crv,
            "x": long_to_base64(public_key.public_numbers().x, size=key_size).decode(
                "ASCII"
            ),
            "y": long_to_base64(public_key.public_numbers().y, size=key_size).decode(
                "ASCII"
            ),
        }

        if not self.is_public():
            private_value = self.prepared_key.private_numbers().private_value
            data["d"] = long_to_base64(private_value, size=key_size).decode("ASCII")

        return data


class CryptographyRSAKey(Key):
    SHA256 = hashes.SHA256
    SHA384 = hashes.SHA384
    SHA512 = hashes.SHA512

    RSA1_5 = padding.PKCS1v15()
    RSA_OAEP = padding.OAEP(padding.MGF1(hashes.SHA1()), hashes.SHA1(), None)
    RSA_OAEP_256 = padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None)

    def __init__(self, key, algorithm, cryptography_backend=default_backend):
        if algorithm not in ALGORITHMS.RSA:
            raise JWKError("hash_alg: %s is not a valid hash algorithm" % algorithm)

        self.hash_alg = {
            ALGORITHMS.RS256: self.SHA256,
            ALGORITHMS.RS384: self.SHA384,
            ALGORITHMS.RS512: self.SHA512,
        }.get(algorithm)
        self._algorithm = algorithm

        self.padding = {
            ALGORITHMS.RSA1_5: self.RSA1_5,
            ALGORITHMS.RSA_OAEP: self.RSA_OAEP,
            ALGORITHMS.RSA_OAEP_256: self.RSA_OAEP_256,
        }.get(algorithm)

        self.cryptography_backend = cryptography_backend

        # if it conforms to RSAPublicKey interface
        if hasattr(key, "public_bytes") and hasattr(key, "public_numbers"):
            self.prepared_key = key
            return

        if isinstance(key, dict):
            self.prepared_key = self._process_jwk(key)
            return

        if isinstance(key, str):
            key = key.encode("utf-8")

        if isinstance(key, bytes):
            try:
                if key.startswith(b"-----BEGIN CERTIFICATE-----"):
                    self._process_cert(key)
                    return

                try:
                    self.prepared_key = load_pem_public_key(
                        key, self.cryptography_backend()
                    )
                except ValueError:
                    self.prepared_key = load_pem_private_key(
                        key, password=None, backend=self.cryptography_backend()
                    )
            except Exception as e:
                raise JWKError(e)
            return

        raise JWKError("Unable to parse an RSA_JWK from key: %s" % key)

    def _process_jwk(self, jwk_dict):
        if not jwk_dict.get("kty") == "RSA":
            raise JWKError(
                "Incorrect key type. Expected: 'RSA', Received: %s"
                % jwk_dict.get("kty")
            )

        e = base64_to_long(jwk_dict.get("e", 256))
        n = base64_to_long(jwk_dict.get("n"))
        public = rsa.RSAPublicNumbers(e, n)

        if "d" not in jwk_dict:
            return public.public_key(self.cryptography_backend())
        else:
            # This is a private key.
            d = base64_to_long(jwk_dict.get("d"))

            extra_params = ["p", "q", "dp", "dq", "qi"]

            if any(k in jwk_dict for k in extra_params):
                # Precomputed private key parameters are available.
                if not all(k in jwk_dict for k in extra_params):
                    # These values must be present when 'p' is according to
                    # Section 6.3.2 of RFC7518, so if they are not we raise
                    # an error.
                    raise JWKError("Precomputed private key parameters are incomplete.")

                p = base64_to_long(jwk_dict["p"])
                q = base64_to_long(jwk_dict["q"])
                dp = base64_to_long(jwk_dict["dp"])
                dq = base64_to_long(jwk_dict["dq"])
                qi = base64_to_long(jwk_dict["qi"])
            else:
                # The precomputed private key parameters are not available,
                # so we use cryptography's API to fill them in.
                p, q = rsa.rsa_recover_prime_factors(n, e, d)
                dp = rsa.rsa_crt_dmp1(d, p)
                dq = rsa.rsa_crt_dmq1(d, q)
                qi = rsa.rsa_crt_iqmp(p, q)

            private = rsa.RSAPrivateNumbers(p, q, d, dp, dq, qi, public)

            return private.private_key(self.cryptography_backend())

    def _process_cert(self, key):
        key = load_pem_x509_certificate(key, self.cryptography_backend())
        self.prepared_key = key.public_key()

    def sign(self, msg):
        try:
            signature = self.prepared_key.sign(msg, padding.PKCS1v15(), self.hash_alg())
        except Exception as e:
            raise JWKError(e)
        return signature

    def verify(self, msg, sig):
        if not self.is_public():
            warnings.warn(
                "Attempting to verify a message with a private key. "
                "This is not recommended."
            )

        try:
            self.public_key().prepared_key.verify(
                sig, msg, padding.PKCS1v15(), self.hash_alg()
            )
            return True
        except InvalidSignature:
            return False

    def is_public(self):
        return hasattr(self.prepared_key, "public_bytes")

    def public_key(self):
        if self.is_public():
            return self
        return self.__class__(self.prepared_key.public_key(), self._algorithm)

    def to_pem(self, pem_format="PKCS8"):
        if self.is_public():
            if pem_format == "PKCS8":
                fmt = serialization.PublicFormat.SubjectPublicKeyInfo
            elif pem_format == "PKCS1":
                fmt = serialization.PublicFormat.PKCS1
            else:
                raise ValueError("Invalid format specified: %r" % pem_format)
            pem = self.prepared_key.public_bytes(
                encoding=serialization.Encoding.PEM, format=fmt
            )
            return pem

        if pem_format == "PKCS8":
            fmt = serialization.PrivateFormat.PKCS8
        elif pem_format == "PKCS1":
            fmt = serialization.PrivateFormat.TraditionalOpenSSL
        else:
            raise ValueError("Invalid format specified: %r" % pem_format)

        return self.prepared_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=fmt,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def to_dict(self):
        if not self.is_public():
            public_key = self.prepared_key.public_key()
        else:
            public_key = self.prepared_key

        data = {
            "alg": self._algorithm,
            "kty": "RSA",
            "n": long_to_base64(public_key.public_numbers().n).decode("ASCII"),
            "e": long_to_base64(public_key.public_numbers().e).decode("ASCII"),
        }

        if not self.is_public():
            data.update(
                {
                    "d": long_to_base64(self.prepared_key.private_numbers().d).decode(
                        "ASCII"
                    ),
                    "p": long_to_base64(self.prepared_key.private_numbers().p).decode(
                        "ASCII"
                    ),
                    "q": long_to_base64(self.prepared_key.private_numbers().q).decode(
                        "ASCII"
                    ),
                    "dp": long_to_base64(
                        self.prepared_key.private_numbers().dmp1
                    ).decode("ASCII"),
                    "dq": long_to_base64(
                        self.prepared_key.private_numbers().dmq1
                    ).decode("ASCII"),
                    "qi": long_to_base64(
                        self.prepared_key.private_numbers().iqmp
                    ).decode("ASCII"),
                }
            )

        return data

    def wrap_key(self, key_data):
        try:
            wrapped_key = self.prepared_key.encrypt(key_data, self.padding)
        except Exception as e:
            raise JWEError(e)

        return wrapped_key

    def unwrap_key(self, wrapped_key):
        try:
            unwrapped_key = self.prepared_key.decrypt(wrapped_key, self.padding)
            return unwrapped_key
        except Exception as e:
            raise JWEError(e)


class CryptographyAESKey(Key):
    KEY_128 = (
        ALGORITHMS.A128GCM,
        ALGORITHMS.A128GCMKW,
        ALGORITHMS.A128KW,
        ALGORITHMS.A128CBC,
    )
    KEY_192 = (
        ALGORITHMS.A192GCM,
        ALGORITHMS.A192GCMKW,
        ALGORITHMS.A192KW,
        ALGORITHMS.A192CBC,
    )
    KEY_256 = (
        ALGORITHMS.A256GCM,
        ALGORITHMS.A256GCMKW,
        ALGORITHMS.A256KW,
        ALGORITHMS.A128CBC_HS256,
        ALGORITHMS.A256CBC,
    )
    KEY_384 = (ALGORITHMS.A192CBC_HS384,)
    KEY_512 = (ALGORITHMS.A256CBC_HS512,)

    AES_KW_ALGS = (ALGORITHMS.A128KW, ALGORITHMS.A192KW, ALGORITHMS.A256KW)

    MODES = {
        ALGORITHMS.A128GCM: modes.GCM,
        ALGORITHMS.A192GCM: modes.GCM,
        ALGORITHMS.A256GCM: modes.GCM,
        ALGORITHMS.A128CBC_HS256: modes.CBC,
        ALGORITHMS.A192CBC_HS384: modes.CBC,
        ALGORITHMS.A256CBC_HS512: modes.CBC,
        ALGORITHMS.A128CBC: modes.CBC,
        ALGORITHMS.A192CBC: modes.CBC,
        ALGORITHMS.A256CBC: modes.CBC,
        ALGORITHMS.A128GCMKW: modes.GCM,
        ALGORITHMS.A192GCMKW: modes.GCM,
        ALGORITHMS.A256GCMKW: modes.GCM,
        ALGORITHMS.A128KW: None,
        ALGORITHMS.A192KW: None,
        ALGORITHMS.A256KW: None,
    }

    def __init__(self, key, algorithm):
        if algorithm not in ALGORITHMS.AES:
            raise JWKError("%s is not a valid AES algorithm" % algorithm)
        if algorithm not in ALGORITHMS.SUPPORTED.union(ALGORITHMS.AES_PSEUDO):
            raise JWKError("%s is not a supported algorithm" % algorithm)

        self._algorithm = algorithm
        self._mode = self.MODES.get(self._algorithm)

        if algorithm in self.KEY_128 and len(key) != 16:
            raise JWKError(f"Key must be 128 bit for alg {algorithm}")
        elif algorithm in self.KEY_192 and len(key) != 24:
            raise JWKError(f"Key must be 192 bit for alg {algorithm}")
        elif algorithm in self.KEY_256 and len(key) != 32:
            raise JWKError(f"Key must be 256 bit for alg {algorithm}")
        elif algorithm in self.KEY_384 and len(key) != 48:
            raise JWKError(f"Key must be 384 bit for alg {algorithm}")
        elif algorithm in self.KEY_512 and len(key) != 64:
            raise JWKError(f"Key must be 512 bit for alg {algorithm}")

        self._key = key

    def to_dict(self):
        data = {"alg": self._algorithm, "kty": "oct", "k": base64url_encode(self._key)}
        return data

    def encrypt(self, plain_text, aad=None):
        plain_text = ensure_binary(plain_text)
        try:
            iv = get_random_bytes(algorithms.AES.block_size // 8)
            mode = self._mode(iv)
            if mode.name == "GCM":
                cipher = aead.AESGCM(self._key)
                cipher_text_and_tag = cipher.encrypt(iv, plain_text, aad)
                cipher_text = cipher_text_and_tag[: len(cipher_text_and_tag) - 16]
                auth_tag = cipher_text_and_tag[-16:]
            else:
                cipher = Cipher(
                    algorithms.AES(self._key), mode, backend=default_backend()
                )
                encryptor = cipher.encryptor()
                padder = PKCS7(algorithms.AES.block_size).padder()
                padded_data = padder.update(plain_text)
                padded_data += padder.finalize()
                cipher_text = encryptor.update(padded_data) + encryptor.finalize()
                auth_tag = None
            return iv, cipher_text, auth_tag
        except Exception as e:
            raise JWEError(e)

    def decrypt(self, cipher_text, iv=None, aad=None, tag=None):
        cipher_text = ensure_binary(cipher_text)
        try:
            iv = ensure_binary(iv)
            mode = self._mode(iv)
            if mode.name == "GCM":
                if tag is None:
                    raise ValueError("tag cannot be None")
                cipher = aead.AESGCM(self._key)
                cipher_text_and_tag = cipher_text + tag
                try:
                    plain_text = cipher.decrypt(iv, cipher_text_and_tag, aad)
                except InvalidTag:
                    raise JWEError("Invalid JWE Auth Tag")
            else:
                cipher = Cipher(
                    algorithms.AES(self._key), mode, backend=default_backend()
                )
                decryptor = cipher.decryptor()
                padded_plain_text = decryptor.update(cipher_text)
                padded_plain_text += decryptor.finalize()
                unpadder = PKCS7(algorithms.AES.block_size).unpadder()
                plain_text = unpadder.update(padded_plain_text)
                plain_text += unpadder.finalize()

            return plain_text
        except Exception as e:
            raise JWEError(e)

    def wrap_key(self, key_data):
        key_data = ensure_binary(key_data)
        cipher_text = aes_key_wrap(self._key, key_data, default_backend())
        return cipher_text  # IV, cipher text, auth tag

    def unwrap_key(self, wrapped_key):
        wrapped_key = ensure_binary(wrapped_key)
        try:
            plain_text = aes_key_unwrap(self._key, wrapped_key, default_backend())
        except InvalidUnwrap as cause:
            raise JWEError(cause)
        return plain_text


class CryptographyHMACKey(Key):
    """
    Performs signing and verification operations using HMAC
    and the specified hash function.
    """

    ALG_MAP = {
        ALGORITHMS.HS256: hashes.SHA256(),
        ALGORITHMS.HS384: hashes.SHA384(),
        ALGORITHMS.HS512: hashes.SHA512(),
    }

    def __init__(self, key, algorithm):
        if algorithm not in ALGORITHMS.HMAC:
            raise JWKError("hash_alg: %s is not a valid hash algorithm" % algorithm)
        self._algorithm = algorithm
        self._hash_alg = self.ALG_MAP.get(algorithm)

        if isinstance(key, dict):
            self.prepared_key = self._process_jwk(key)
            return

        if not isinstance(key, str) and not isinstance(key, bytes):
            raise JWKError("Expecting a string- or bytes-formatted key.")

        if isinstance(key, str):
            key = key.encode("utf-8")

        invalid_strings = [
            b"-----BEGIN PUBLIC KEY-----",
            b"-----BEGIN RSA PUBLIC KEY-----",
            b"-----BEGIN CERTIFICATE-----",
            b"ssh-rsa",
        ]

        if any(string_value in key for string_value in invalid_strings):
            raise JWKError(
                "The specified key is an asymmetric key or x509 certificate and"
                " should not be used as an HMAC secret."
            )

        self.prepared_key = key

    def _process_jwk(self, jwk_dict):
        if not jwk_dict.get("kty") == "oct":
            raise JWKError(
                "Incorrect key type. Expected: 'oct', Received: %s"
                % jwk_dict.get("kty")
            )

        k = jwk_dict.get("k")
        k = k.encode("utf-8")
        k = bytes(k)
        k = base64url_decode(k)

        return k

    def to_dict(self):
        return {
            "alg": self._algorithm,
            "kty": "oct",
            "k": base64url_encode(self.prepared_key).decode("ASCII"),
        }

    def sign(self, msg):
        msg = ensure_binary(msg)
        h = hmac.HMAC(self.prepared_key, self._hash_alg, backend=default_backend())
        h.update(msg)
        signature = h.finalize()
        return signature

    def verify(self, msg, sig):
        msg = ensure_binary(msg)
        sig = ensure_binary(sig)
        h = hmac.HMAC(self.prepared_key, self._hash_alg, backend=default_backend())
        h.update(msg)
        try:
            h.verify(sig)
            verified = True
        except InvalidSignature:
            verified = False
        return verified

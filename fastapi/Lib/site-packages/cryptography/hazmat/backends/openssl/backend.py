# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import collections
import contextlib
import itertools
import typing
from contextlib import contextmanager

from cryptography import utils, x509
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.openssl import aead
from cryptography.hazmat.backends.openssl.ciphers import _CipherContext
from cryptography.hazmat.backends.openssl.cmac import _CMACContext
from cryptography.hazmat.backends.openssl.ec import (
    _EllipticCurvePrivateKey,
    _EllipticCurvePublicKey,
)
from cryptography.hazmat.backends.openssl.rsa import (
    _RSAPrivateKey,
    _RSAPublicKey,
)
from cryptography.hazmat.bindings._rust import openssl as rust_openssl
from cryptography.hazmat.bindings.openssl import binding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives._asymmetric import AsymmetricPadding
from cryptography.hazmat.primitives.asymmetric import (
    dh,
    dsa,
    ec,
    ed448,
    ed25519,
    rsa,
    x448,
    x25519,
)
from cryptography.hazmat.primitives.asymmetric.padding import (
    MGF1,
    OAEP,
    PSS,
    PKCS1v15,
)
from cryptography.hazmat.primitives.asymmetric.types import (
    PrivateKeyTypes,
    PublicKeyTypes,
)
from cryptography.hazmat.primitives.ciphers import (
    BlockCipherAlgorithm,
    CipherAlgorithm,
)
from cryptography.hazmat.primitives.ciphers.algorithms import (
    AES,
    AES128,
    AES256,
    ARC4,
    SM4,
    Camellia,
    ChaCha20,
    TripleDES,
    _BlowfishInternal,
    _CAST5Internal,
    _IDEAInternal,
    _SEEDInternal,
)
from cryptography.hazmat.primitives.ciphers.modes import (
    CBC,
    CFB,
    CFB8,
    CTR,
    ECB,
    GCM,
    OFB,
    XTS,
    Mode,
)
from cryptography.hazmat.primitives.serialization import ssh
from cryptography.hazmat.primitives.serialization.pkcs12 import (
    PBES,
    PKCS12Certificate,
    PKCS12KeyAndCertificates,
    PKCS12PrivateKeyTypes,
    _PKCS12CATypes,
)

_MemoryBIO = collections.namedtuple("_MemoryBIO", ["bio", "char_ptr"])


# Not actually supported, just used as a marker for some serialization tests.
class _RC2:
    pass


class Backend:
    """
    OpenSSL API binding interfaces.
    """

    name = "openssl"

    # FIPS has opinions about acceptable algorithms and key sizes, but the
    # disallowed algorithms are still present in OpenSSL. They just error if
    # you try to use them. To avoid that we allowlist the algorithms in
    # FIPS 140-3. This isn't ideal, but FIPS 140-3 is trash so here we are.
    _fips_aead = {
        b"aes-128-ccm",
        b"aes-192-ccm",
        b"aes-256-ccm",
        b"aes-128-gcm",
        b"aes-192-gcm",
        b"aes-256-gcm",
    }
    # TripleDES encryption is disallowed/deprecated throughout 2023 in
    # FIPS 140-3. To keep it simple we denylist any use of TripleDES (TDEA).
    _fips_ciphers = (AES,)
    # Sometimes SHA1 is still permissible. That logic is contained
    # within the various *_supported methods.
    _fips_hashes = (
        hashes.SHA224,
        hashes.SHA256,
        hashes.SHA384,
        hashes.SHA512,
        hashes.SHA512_224,
        hashes.SHA512_256,
        hashes.SHA3_224,
        hashes.SHA3_256,
        hashes.SHA3_384,
        hashes.SHA3_512,
        hashes.SHAKE128,
        hashes.SHAKE256,
    )
    _fips_ecdh_curves = (
        ec.SECP224R1,
        ec.SECP256R1,
        ec.SECP384R1,
        ec.SECP521R1,
    )
    _fips_rsa_min_key_size = 2048
    _fips_rsa_min_public_exponent = 65537
    _fips_dsa_min_modulus = 1 << 2048
    _fips_dh_min_key_size = 2048
    _fips_dh_min_modulus = 1 << _fips_dh_min_key_size

    def __init__(self) -> None:
        self._binding = binding.Binding()
        self._ffi = self._binding.ffi
        self._lib = self._binding.lib
        self._fips_enabled = rust_openssl.is_fips_enabled()

        self._cipher_registry: typing.Dict[
            typing.Tuple[typing.Type[CipherAlgorithm], typing.Type[Mode]],
            typing.Callable,
        ] = {}
        self._register_default_ciphers()
        self._dh_types = [self._lib.EVP_PKEY_DH]
        if self._lib.Cryptography_HAS_EVP_PKEY_DHX:
            self._dh_types.append(self._lib.EVP_PKEY_DHX)

    def __repr__(self) -> str:
        return "<OpenSSLBackend(version: {}, FIPS: {}, Legacy: {})>".format(
            self.openssl_version_text(),
            self._fips_enabled,
            self._binding._legacy_provider_loaded,
        )

    def openssl_assert(
        self,
        ok: bool,
        errors: typing.Optional[typing.List[rust_openssl.OpenSSLError]] = None,
    ) -> None:
        return binding._openssl_assert(self._lib, ok, errors=errors)

    def _enable_fips(self) -> None:
        # This function enables FIPS mode for OpenSSL 3.0.0 on installs that
        # have the FIPS provider installed properly.
        self._binding._enable_fips()
        assert rust_openssl.is_fips_enabled()
        self._fips_enabled = rust_openssl.is_fips_enabled()

    def openssl_version_text(self) -> str:
        """
        Friendly string name of the loaded OpenSSL library. This is not
        necessarily the same version as it was compiled against.

        Example: OpenSSL 1.1.1d  10 Sep 2019
        """
        return self._ffi.string(
            self._lib.OpenSSL_version(self._lib.OPENSSL_VERSION)
        ).decode("ascii")

    def openssl_version_number(self) -> int:
        return self._lib.OpenSSL_version_num()

    def _evp_md_from_algorithm(self, algorithm: hashes.HashAlgorithm):
        if algorithm.name == "blake2b" or algorithm.name == "blake2s":
            alg = "{}{}".format(algorithm.name, algorithm.digest_size * 8).encode(
                "ascii"
            )
        else:
            alg = algorithm.name.encode("ascii")

        evp_md = self._lib.EVP_get_digestbyname(alg)
        return evp_md

    def _evp_md_non_null_from_algorithm(self, algorithm: hashes.HashAlgorithm):
        evp_md = self._evp_md_from_algorithm(algorithm)
        self.openssl_assert(evp_md != self._ffi.NULL)
        return evp_md

    def hash_supported(self, algorithm: hashes.HashAlgorithm) -> bool:
        if self._fips_enabled and not isinstance(algorithm, self._fips_hashes):
            return False

        evp_md = self._evp_md_from_algorithm(algorithm)
        return evp_md != self._ffi.NULL

    def signature_hash_supported(self, algorithm: hashes.HashAlgorithm) -> bool:
        # Dedicated check for hashing algorithm use in message digest for
        # signatures, e.g. RSA PKCS#1 v1.5 SHA1 (sha1WithRSAEncryption).
        if self._fips_enabled and isinstance(algorithm, hashes.SHA1):
            return False
        return self.hash_supported(algorithm)

    def scrypt_supported(self) -> bool:
        if self._fips_enabled:
            return False
        else:
            return self._lib.Cryptography_HAS_SCRYPT == 1

    def hmac_supported(self, algorithm: hashes.HashAlgorithm) -> bool:
        # FIPS mode still allows SHA1 for HMAC
        if self._fips_enabled and isinstance(algorithm, hashes.SHA1):
            return True

        return self.hash_supported(algorithm)

    def cipher_supported(self, cipher: CipherAlgorithm, mode: Mode) -> bool:
        if self._fips_enabled:
            # FIPS mode requires AES. TripleDES is disallowed/deprecated in
            # FIPS 140-3.
            if not isinstance(cipher, self._fips_ciphers):
                return False

        try:
            adapter = self._cipher_registry[type(cipher), type(mode)]
        except KeyError:
            return False
        evp_cipher = adapter(self, cipher, mode)
        return self._ffi.NULL != evp_cipher

    def register_cipher_adapter(self, cipher_cls, mode_cls, adapter) -> None:
        if (cipher_cls, mode_cls) in self._cipher_registry:
            raise ValueError(
                "Duplicate registration for: {} {}.".format(cipher_cls, mode_cls)
            )
        self._cipher_registry[cipher_cls, mode_cls] = adapter

    def _register_default_ciphers(self) -> None:
        for cipher_cls in [AES, AES128, AES256]:
            for mode_cls in [CBC, CTR, ECB, OFB, CFB, CFB8, GCM]:
                self.register_cipher_adapter(
                    cipher_cls,
                    mode_cls,
                    GetCipherByName("{cipher.name}-{cipher.key_size}-{mode.name}"),
                )
        for mode_cls in [CBC, CTR, ECB, OFB, CFB]:
            self.register_cipher_adapter(
                Camellia,
                mode_cls,
                GetCipherByName("{cipher.name}-{cipher.key_size}-{mode.name}"),
            )
        for mode_cls in [CBC, CFB, CFB8, OFB]:
            self.register_cipher_adapter(
                TripleDES, mode_cls, GetCipherByName("des-ede3-{mode.name}")
            )
        self.register_cipher_adapter(TripleDES, ECB, GetCipherByName("des-ede3"))
        self.register_cipher_adapter(ChaCha20, type(None), GetCipherByName("chacha20"))
        self.register_cipher_adapter(AES, XTS, _get_xts_cipher)
        for mode_cls in [ECB, CBC, OFB, CFB, CTR]:
            self.register_cipher_adapter(
                SM4, mode_cls, GetCipherByName("sm4-{mode.name}")
            )
        # Don't register legacy ciphers if they're unavailable. Hypothetically
        # this wouldn't be necessary because we test availability by seeing if
        # we get an EVP_CIPHER * in the _CipherContext __init__, but OpenSSL 3
        # will return a valid pointer even though the cipher is unavailable.
        if (
            self._binding._legacy_provider_loaded
            or not self._lib.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER
        ):
            for mode_cls in [CBC, CFB, OFB, ECB]:
                self.register_cipher_adapter(
                    _BlowfishInternal,
                    mode_cls,
                    GetCipherByName("bf-{mode.name}"),
                )
            for mode_cls in [CBC, CFB, OFB, ECB]:
                self.register_cipher_adapter(
                    _SEEDInternal,
                    mode_cls,
                    GetCipherByName("seed-{mode.name}"),
                )
            for cipher_cls, mode_cls in itertools.product(
                [_CAST5Internal, _IDEAInternal],
                [CBC, OFB, CFB, ECB],
            ):
                self.register_cipher_adapter(
                    cipher_cls,
                    mode_cls,
                    GetCipherByName("{cipher.name}-{mode.name}"),
                )
            self.register_cipher_adapter(ARC4, type(None), GetCipherByName("rc4"))
            # We don't actually support RC2, this is just used by some tests.
            self.register_cipher_adapter(_RC2, type(None), GetCipherByName("rc2"))

    def create_symmetric_encryption_ctx(
        self, cipher: CipherAlgorithm, mode: Mode
    ) -> _CipherContext:
        return _CipherContext(self, cipher, mode, _CipherContext._ENCRYPT)

    def create_symmetric_decryption_ctx(
        self, cipher: CipherAlgorithm, mode: Mode
    ) -> _CipherContext:
        return _CipherContext(self, cipher, mode, _CipherContext._DECRYPT)

    def pbkdf2_hmac_supported(self, algorithm: hashes.HashAlgorithm) -> bool:
        return self.hmac_supported(algorithm)

    def _consume_errors(self) -> typing.List[rust_openssl.OpenSSLError]:
        return rust_openssl.capture_error_stack()

    def _bn_to_int(self, bn) -> int:
        assert bn != self._ffi.NULL
        self.openssl_assert(not self._lib.BN_is_negative(bn))

        bn_num_bytes = self._lib.BN_num_bytes(bn)
        bin_ptr = self._ffi.new("unsigned char[]", bn_num_bytes)
        bin_len = self._lib.BN_bn2bin(bn, bin_ptr)
        # A zero length means the BN has value 0
        self.openssl_assert(bin_len >= 0)
        val = int.from_bytes(self._ffi.buffer(bin_ptr)[:bin_len], "big")
        return val

    def _int_to_bn(self, num: int):
        """
        Converts a python integer to a BIGNUM. The returned BIGNUM will not
        be garbage collected (to support adding them to structs that take
        ownership of the object). Be sure to register it for GC if it will
        be discarded after use.
        """
        binary = num.to_bytes(int(num.bit_length() / 8.0 + 1), "big")
        bn_ptr = self._lib.BN_bin2bn(binary, len(binary), self._ffi.NULL)
        self.openssl_assert(bn_ptr != self._ffi.NULL)
        return bn_ptr

    def generate_rsa_private_key(
        self, public_exponent: int, key_size: int
    ) -> rsa.RSAPrivateKey:
        rsa._verify_rsa_parameters(public_exponent, key_size)

        rsa_cdata = self._lib.RSA_new()
        self.openssl_assert(rsa_cdata != self._ffi.NULL)
        rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)

        bn = self._int_to_bn(public_exponent)
        bn = self._ffi.gc(bn, self._lib.BN_free)

        res = self._lib.RSA_generate_key_ex(rsa_cdata, key_size, bn, self._ffi.NULL)
        self.openssl_assert(res == 1)
        evp_pkey = self._rsa_cdata_to_evp_pkey(rsa_cdata)

        # We can skip RSA key validation here since we just generated the key
        return _RSAPrivateKey(
            self, rsa_cdata, evp_pkey, unsafe_skip_rsa_key_validation=True
        )

    def generate_rsa_parameters_supported(
        self, public_exponent: int, key_size: int
    ) -> bool:
        return public_exponent >= 3 and public_exponent & 1 != 0 and key_size >= 512

    def load_rsa_private_numbers(
        self,
        numbers: rsa.RSAPrivateNumbers,
        unsafe_skip_rsa_key_validation: bool,
    ) -> rsa.RSAPrivateKey:
        rsa._check_private_key_components(
            numbers.p,
            numbers.q,
            numbers.d,
            numbers.dmp1,
            numbers.dmq1,
            numbers.iqmp,
            numbers.public_numbers.e,
            numbers.public_numbers.n,
        )
        rsa_cdata = self._lib.RSA_new()
        self.openssl_assert(rsa_cdata != self._ffi.NULL)
        rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
        p = self._int_to_bn(numbers.p)
        q = self._int_to_bn(numbers.q)
        d = self._int_to_bn(numbers.d)
        dmp1 = self._int_to_bn(numbers.dmp1)
        dmq1 = self._int_to_bn(numbers.dmq1)
        iqmp = self._int_to_bn(numbers.iqmp)
        e = self._int_to_bn(numbers.public_numbers.e)
        n = self._int_to_bn(numbers.public_numbers.n)
        res = self._lib.RSA_set0_factors(rsa_cdata, p, q)
        self.openssl_assert(res == 1)
        res = self._lib.RSA_set0_key(rsa_cdata, n, e, d)
        self.openssl_assert(res == 1)
        res = self._lib.RSA_set0_crt_params(rsa_cdata, dmp1, dmq1, iqmp)
        self.openssl_assert(res == 1)
        evp_pkey = self._rsa_cdata_to_evp_pkey(rsa_cdata)

        return _RSAPrivateKey(
            self,
            rsa_cdata,
            evp_pkey,
            unsafe_skip_rsa_key_validation=unsafe_skip_rsa_key_validation,
        )

    def load_rsa_public_numbers(
        self, numbers: rsa.RSAPublicNumbers
    ) -> rsa.RSAPublicKey:
        rsa._check_public_key_components(numbers.e, numbers.n)
        rsa_cdata = self._lib.RSA_new()
        self.openssl_assert(rsa_cdata != self._ffi.NULL)
        rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
        e = self._int_to_bn(numbers.e)
        n = self._int_to_bn(numbers.n)
        res = self._lib.RSA_set0_key(rsa_cdata, n, e, self._ffi.NULL)
        self.openssl_assert(res == 1)
        evp_pkey = self._rsa_cdata_to_evp_pkey(rsa_cdata)

        return _RSAPublicKey(self, rsa_cdata, evp_pkey)

    def _create_evp_pkey_gc(self):
        evp_pkey = self._lib.EVP_PKEY_new()
        self.openssl_assert(evp_pkey != self._ffi.NULL)
        evp_pkey = self._ffi.gc(evp_pkey, self._lib.EVP_PKEY_free)
        return evp_pkey

    def _rsa_cdata_to_evp_pkey(self, rsa_cdata):
        evp_pkey = self._create_evp_pkey_gc()
        res = self._lib.EVP_PKEY_set1_RSA(evp_pkey, rsa_cdata)
        self.openssl_assert(res == 1)
        return evp_pkey

    def _bytes_to_bio(self, data: bytes) -> _MemoryBIO:
        """
        Return a _MemoryBIO namedtuple of (BIO, char*).

        The char* is the storage for the BIO and it must stay alive until the
        BIO is finished with.
        """
        data_ptr = self._ffi.from_buffer(data)
        bio = self._lib.BIO_new_mem_buf(data_ptr, len(data))
        self.openssl_assert(bio != self._ffi.NULL)

        return _MemoryBIO(self._ffi.gc(bio, self._lib.BIO_free), data_ptr)

    def _create_mem_bio_gc(self):
        """
        Creates an empty memory BIO.
        """
        bio_method = self._lib.BIO_s_mem()
        self.openssl_assert(bio_method != self._ffi.NULL)
        bio = self._lib.BIO_new(bio_method)
        self.openssl_assert(bio != self._ffi.NULL)
        bio = self._ffi.gc(bio, self._lib.BIO_free)
        return bio

    def _read_mem_bio(self, bio) -> bytes:
        """
        Reads a memory BIO. This only works on memory BIOs.
        """
        buf = self._ffi.new("char **")
        buf_len = self._lib.BIO_get_mem_data(bio, buf)
        self.openssl_assert(buf_len > 0)
        self.openssl_assert(buf[0] != self._ffi.NULL)
        bio_data = self._ffi.buffer(buf[0], buf_len)[:]
        return bio_data

    def _evp_pkey_to_private_key(
        self, evp_pkey, unsafe_skip_rsa_key_validation: bool
    ) -> PrivateKeyTypes:
        """
        Return the appropriate type of PrivateKey given an evp_pkey cdata
        pointer.
        """

        key_type = self._lib.EVP_PKEY_id(evp_pkey)

        if key_type == self._lib.EVP_PKEY_RSA:
            rsa_cdata = self._lib.EVP_PKEY_get1_RSA(evp_pkey)
            self.openssl_assert(rsa_cdata != self._ffi.NULL)
            rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
            return _RSAPrivateKey(
                self,
                rsa_cdata,
                evp_pkey,
                unsafe_skip_rsa_key_validation=unsafe_skip_rsa_key_validation,
            )
        elif (
            key_type == self._lib.EVP_PKEY_RSA_PSS
            and not self._lib.CRYPTOGRAPHY_IS_LIBRESSL
            and not self._lib.CRYPTOGRAPHY_IS_BORINGSSL
            and not self._lib.CRYPTOGRAPHY_OPENSSL_LESS_THAN_111E
        ):
            # At the moment the way we handle RSA PSS keys is to strip the
            # PSS constraints from them and treat them as normal RSA keys
            # Unfortunately the RSA * itself tracks this data so we need to
            # extract, serialize, and reload it without the constraints.
            rsa_cdata = self._lib.EVP_PKEY_get1_RSA(evp_pkey)
            self.openssl_assert(rsa_cdata != self._ffi.NULL)
            rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
            bio = self._create_mem_bio_gc()
            res = self._lib.i2d_RSAPrivateKey_bio(bio, rsa_cdata)
            self.openssl_assert(res == 1)
            return self.load_der_private_key(
                self._read_mem_bio(bio),
                password=None,
                unsafe_skip_rsa_key_validation=unsafe_skip_rsa_key_validation,
            )
        elif key_type == self._lib.EVP_PKEY_DSA:
            return rust_openssl.dsa.private_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == self._lib.EVP_PKEY_EC:
            ec_cdata = self._lib.EVP_PKEY_get1_EC_KEY(evp_pkey)
            self.openssl_assert(ec_cdata != self._ffi.NULL)
            ec_cdata = self._ffi.gc(ec_cdata, self._lib.EC_KEY_free)
            return _EllipticCurvePrivateKey(self, ec_cdata, evp_pkey)
        elif key_type in self._dh_types:
            return rust_openssl.dh.private_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == getattr(self._lib, "EVP_PKEY_ED25519", None):
            # EVP_PKEY_ED25519 is not present in CRYPTOGRAPHY_IS_LIBRESSL
            return rust_openssl.ed25519.private_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == getattr(self._lib, "EVP_PKEY_X448", None):
            # EVP_PKEY_X448 is not present in CRYPTOGRAPHY_IS_LIBRESSL
            return rust_openssl.x448.private_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == self._lib.EVP_PKEY_X25519:
            return rust_openssl.x25519.private_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == getattr(self._lib, "EVP_PKEY_ED448", None):
            # EVP_PKEY_ED448 is not present in CRYPTOGRAPHY_IS_LIBRESSL
            return rust_openssl.ed448.private_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        else:
            raise UnsupportedAlgorithm("Unsupported key type.")

    def _evp_pkey_to_public_key(self, evp_pkey) -> PublicKeyTypes:
        """
        Return the appropriate type of PublicKey given an evp_pkey cdata
        pointer.
        """

        key_type = self._lib.EVP_PKEY_id(evp_pkey)

        if key_type == self._lib.EVP_PKEY_RSA:
            rsa_cdata = self._lib.EVP_PKEY_get1_RSA(evp_pkey)
            self.openssl_assert(rsa_cdata != self._ffi.NULL)
            rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
            return _RSAPublicKey(self, rsa_cdata, evp_pkey)
        elif (
            key_type == self._lib.EVP_PKEY_RSA_PSS
            and not self._lib.CRYPTOGRAPHY_IS_LIBRESSL
            and not self._lib.CRYPTOGRAPHY_IS_BORINGSSL
            and not self._lib.CRYPTOGRAPHY_OPENSSL_LESS_THAN_111E
        ):
            rsa_cdata = self._lib.EVP_PKEY_get1_RSA(evp_pkey)
            self.openssl_assert(rsa_cdata != self._ffi.NULL)
            rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
            bio = self._create_mem_bio_gc()
            res = self._lib.i2d_RSAPublicKey_bio(bio, rsa_cdata)
            self.openssl_assert(res == 1)
            return self.load_der_public_key(self._read_mem_bio(bio))
        elif key_type == self._lib.EVP_PKEY_DSA:
            return rust_openssl.dsa.public_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == self._lib.EVP_PKEY_EC:
            ec_cdata = self._lib.EVP_PKEY_get1_EC_KEY(evp_pkey)
            if ec_cdata == self._ffi.NULL:
                errors = self._consume_errors()
                raise ValueError("Unable to load EC key", errors)
            ec_cdata = self._ffi.gc(ec_cdata, self._lib.EC_KEY_free)
            return _EllipticCurvePublicKey(self, ec_cdata, evp_pkey)
        elif key_type in self._dh_types:
            return rust_openssl.dh.public_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == getattr(self._lib, "EVP_PKEY_ED25519", None):
            # EVP_PKEY_ED25519 is not present in CRYPTOGRAPHY_IS_LIBRESSL
            return rust_openssl.ed25519.public_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == getattr(self._lib, "EVP_PKEY_X448", None):
            # EVP_PKEY_X448 is not present in CRYPTOGRAPHY_IS_LIBRESSL
            return rust_openssl.x448.public_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == self._lib.EVP_PKEY_X25519:
            return rust_openssl.x25519.public_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        elif key_type == getattr(self._lib, "EVP_PKEY_ED448", None):
            # EVP_PKEY_ED448 is not present in CRYPTOGRAPHY_IS_LIBRESSL
            return rust_openssl.ed448.public_key_from_ptr(
                int(self._ffi.cast("uintptr_t", evp_pkey))
            )
        else:
            raise UnsupportedAlgorithm("Unsupported key type.")

    def _oaep_hash_supported(self, algorithm: hashes.HashAlgorithm) -> bool:
        if self._fips_enabled and isinstance(algorithm, hashes.SHA1):
            return False

        return isinstance(
            algorithm,
            (
                hashes.SHA1,
                hashes.SHA224,
                hashes.SHA256,
                hashes.SHA384,
                hashes.SHA512,
            ),
        )

    def rsa_padding_supported(self, padding: AsymmetricPadding) -> bool:
        if isinstance(padding, PKCS1v15):
            return True
        elif isinstance(padding, PSS) and isinstance(padding._mgf, MGF1):
            # SHA1 is permissible in MGF1 in FIPS even when SHA1 is blocked
            # as signature algorithm.
            if self._fips_enabled and isinstance(padding._mgf._algorithm, hashes.SHA1):
                return True
            else:
                return self.hash_supported(padding._mgf._algorithm)
        elif isinstance(padding, OAEP) and isinstance(padding._mgf, MGF1):
            return self._oaep_hash_supported(
                padding._mgf._algorithm
            ) and self._oaep_hash_supported(padding._algorithm)
        else:
            return False

    def rsa_encryption_supported(self, padding: AsymmetricPadding) -> bool:
        if self._fips_enabled and isinstance(padding, PKCS1v15):
            return False
        else:
            return self.rsa_padding_supported(padding)

    def generate_dsa_parameters(self, key_size: int) -> dsa.DSAParameters:
        if key_size not in (1024, 2048, 3072, 4096):
            raise ValueError("Key size must be 1024, 2048, 3072, or 4096 bits.")

        return rust_openssl.dsa.generate_parameters(key_size)

    def generate_dsa_private_key(
        self, parameters: dsa.DSAParameters
    ) -> dsa.DSAPrivateKey:
        return parameters.generate_private_key()

    def generate_dsa_private_key_and_parameters(
        self, key_size: int
    ) -> dsa.DSAPrivateKey:
        parameters = self.generate_dsa_parameters(key_size)
        return self.generate_dsa_private_key(parameters)

    def load_dsa_private_numbers(
        self, numbers: dsa.DSAPrivateNumbers
    ) -> dsa.DSAPrivateKey:
        dsa._check_dsa_private_numbers(numbers)
        return rust_openssl.dsa.from_private_numbers(numbers)

    def load_dsa_public_numbers(
        self, numbers: dsa.DSAPublicNumbers
    ) -> dsa.DSAPublicKey:
        dsa._check_dsa_parameters(numbers.parameter_numbers)
        return rust_openssl.dsa.from_public_numbers(numbers)

    def load_dsa_parameter_numbers(
        self, numbers: dsa.DSAParameterNumbers
    ) -> dsa.DSAParameters:
        dsa._check_dsa_parameters(numbers)
        return rust_openssl.dsa.from_parameter_numbers(numbers)

    def dsa_supported(self) -> bool:
        return not self._lib.CRYPTOGRAPHY_IS_BORINGSSL and not self._fips_enabled

    def dsa_hash_supported(self, algorithm: hashes.HashAlgorithm) -> bool:
        if not self.dsa_supported():
            return False
        return self.signature_hash_supported(algorithm)

    def cmac_algorithm_supported(self, algorithm) -> bool:
        return self.cipher_supported(algorithm, CBC(b"\x00" * algorithm.block_size))

    def create_cmac_ctx(self, algorithm: BlockCipherAlgorithm) -> _CMACContext:
        return _CMACContext(self, algorithm)

    def load_pem_private_key(
        self,
        data: bytes,
        password: typing.Optional[bytes],
        unsafe_skip_rsa_key_validation: bool,
    ) -> PrivateKeyTypes:
        return self._load_key(
            self._lib.PEM_read_bio_PrivateKey,
            data,
            password,
            unsafe_skip_rsa_key_validation,
        )

    def load_pem_public_key(self, data: bytes) -> PublicKeyTypes:
        mem_bio = self._bytes_to_bio(data)
        # In OpenSSL 3.0.x the PEM_read_bio_PUBKEY function will invoke
        # the default password callback if you pass an encrypted private
        # key. This is very, very, very bad as the default callback can
        # trigger an interactive console prompt, which will hang the
        # Python process. We therefore provide our own callback to
        # catch this and error out properly.
        userdata = self._ffi.new("CRYPTOGRAPHY_PASSWORD_DATA *")
        evp_pkey = self._lib.PEM_read_bio_PUBKEY(
            mem_bio.bio,
            self._ffi.NULL,
            self._ffi.addressof(
                self._lib._original_lib, "Cryptography_pem_password_cb"
            ),
            userdata,
        )
        if evp_pkey != self._ffi.NULL:
            evp_pkey = self._ffi.gc(evp_pkey, self._lib.EVP_PKEY_free)
            return self._evp_pkey_to_public_key(evp_pkey)
        else:
            # It's not a (RSA/DSA/ECDSA) subjectPublicKeyInfo, but we still
            # need to check to see if it is a pure PKCS1 RSA public key (not
            # embedded in a subjectPublicKeyInfo)
            self._consume_errors()
            res = self._lib.BIO_reset(mem_bio.bio)
            self.openssl_assert(res == 1)
            rsa_cdata = self._lib.PEM_read_bio_RSAPublicKey(
                mem_bio.bio,
                self._ffi.NULL,
                self._ffi.addressof(
                    self._lib._original_lib, "Cryptography_pem_password_cb"
                ),
                userdata,
            )
            if rsa_cdata != self._ffi.NULL:
                rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
                evp_pkey = self._rsa_cdata_to_evp_pkey(rsa_cdata)
                return _RSAPublicKey(self, rsa_cdata, evp_pkey)
            else:
                self._handle_key_loading_error()

    def load_pem_parameters(self, data: bytes) -> dh.DHParameters:
        return rust_openssl.dh.from_pem_parameters(data)

    def load_der_private_key(
        self,
        data: bytes,
        password: typing.Optional[bytes],
        unsafe_skip_rsa_key_validation: bool,
    ) -> PrivateKeyTypes:
        # OpenSSL has a function called d2i_AutoPrivateKey that in theory
        # handles this automatically, however it doesn't handle encrypted
        # private keys. Instead we try to load the key two different ways.
        # First we'll try to load it as a traditional key.
        bio_data = self._bytes_to_bio(data)
        key = self._evp_pkey_from_der_traditional_key(bio_data, password)
        if key:
            return self._evp_pkey_to_private_key(key, unsafe_skip_rsa_key_validation)
        else:
            # Finally we try to load it with the method that handles encrypted
            # PKCS8 properly.
            return self._load_key(
                self._lib.d2i_PKCS8PrivateKey_bio,
                data,
                password,
                unsafe_skip_rsa_key_validation,
            )

    def _evp_pkey_from_der_traditional_key(self, bio_data, password):
        key = self._lib.d2i_PrivateKey_bio(bio_data.bio, self._ffi.NULL)
        if key != self._ffi.NULL:
            key = self._ffi.gc(key, self._lib.EVP_PKEY_free)
            if password is not None:
                raise TypeError("Password was given but private key is not encrypted.")

            return key
        else:
            self._consume_errors()
            return None

    def load_der_public_key(self, data: bytes) -> PublicKeyTypes:
        mem_bio = self._bytes_to_bio(data)
        evp_pkey = self._lib.d2i_PUBKEY_bio(mem_bio.bio, self._ffi.NULL)
        if evp_pkey != self._ffi.NULL:
            evp_pkey = self._ffi.gc(evp_pkey, self._lib.EVP_PKEY_free)
            return self._evp_pkey_to_public_key(evp_pkey)
        else:
            # It's not a (RSA/DSA/ECDSA) subjectPublicKeyInfo, but we still
            # need to check to see if it is a pure PKCS1 RSA public key (not
            # embedded in a subjectPublicKeyInfo)
            self._consume_errors()
            res = self._lib.BIO_reset(mem_bio.bio)
            self.openssl_assert(res == 1)
            rsa_cdata = self._lib.d2i_RSAPublicKey_bio(mem_bio.bio, self._ffi.NULL)
            if rsa_cdata != self._ffi.NULL:
                rsa_cdata = self._ffi.gc(rsa_cdata, self._lib.RSA_free)
                evp_pkey = self._rsa_cdata_to_evp_pkey(rsa_cdata)
                return _RSAPublicKey(self, rsa_cdata, evp_pkey)
            else:
                self._handle_key_loading_error()

    def load_der_parameters(self, data: bytes) -> dh.DHParameters:
        return rust_openssl.dh.from_der_parameters(data)

    def _cert2ossl(self, cert: x509.Certificate) -> typing.Any:
        data = cert.public_bytes(serialization.Encoding.DER)
        mem_bio = self._bytes_to_bio(data)
        x509 = self._lib.d2i_X509_bio(mem_bio.bio, self._ffi.NULL)
        self.openssl_assert(x509 != self._ffi.NULL)
        x509 = self._ffi.gc(x509, self._lib.X509_free)
        return x509

    def _ossl2cert(self, x509_ptr: typing.Any) -> x509.Certificate:
        bio = self._create_mem_bio_gc()
        res = self._lib.i2d_X509_bio(bio, x509_ptr)
        self.openssl_assert(res == 1)
        return x509.load_der_x509_certificate(self._read_mem_bio(bio))

    def _key2ossl(self, key: PKCS12PrivateKeyTypes) -> typing.Any:
        data = key.private_bytes(
            serialization.Encoding.DER,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        mem_bio = self._bytes_to_bio(data)

        evp_pkey = self._lib.d2i_PrivateKey_bio(
            mem_bio.bio,
            self._ffi.NULL,
        )
        self.openssl_assert(evp_pkey != self._ffi.NULL)
        return self._ffi.gc(evp_pkey, self._lib.EVP_PKEY_free)

    def _load_key(
        self, openssl_read_func, data, password, unsafe_skip_rsa_key_validation
    ) -> PrivateKeyTypes:
        mem_bio = self._bytes_to_bio(data)

        userdata = self._ffi.new("CRYPTOGRAPHY_PASSWORD_DATA *")
        if password is not None:
            utils._check_byteslike("password", password)
            password_ptr = self._ffi.from_buffer(password)
            userdata.password = password_ptr
            userdata.length = len(password)

        evp_pkey = openssl_read_func(
            mem_bio.bio,
            self._ffi.NULL,
            self._ffi.addressof(
                self._lib._original_lib, "Cryptography_pem_password_cb"
            ),
            userdata,
        )

        if evp_pkey == self._ffi.NULL:
            if userdata.error != 0:
                self._consume_errors()
                if userdata.error == -1:
                    raise TypeError(
                        "Password was not given but private key is encrypted"
                    )
                else:
                    assert userdata.error == -2
                    raise ValueError(
                        "Passwords longer than {} bytes are not supported "
                        "by this backend.".format(userdata.maxsize - 1)
                    )
            else:
                self._handle_key_loading_error()

        evp_pkey = self._ffi.gc(evp_pkey, self._lib.EVP_PKEY_free)

        if password is not None and userdata.called == 0:
            raise TypeError("Password was given but private key is not encrypted.")

        assert (password is not None and userdata.called == 1) or password is None

        return self._evp_pkey_to_private_key(evp_pkey, unsafe_skip_rsa_key_validation)

    def _handle_key_loading_error(self) -> typing.NoReturn:
        errors = self._consume_errors()

        if not errors:
            raise ValueError(
                "Could not deserialize key data. The data may be in an "
                "incorrect format or it may be encrypted with an unsupported "
                "algorithm."
            )

        elif (
            errors[0]._lib_reason_match(
                self._lib.ERR_LIB_EVP, self._lib.EVP_R_BAD_DECRYPT
            )
            or errors[0]._lib_reason_match(
                self._lib.ERR_LIB_PKCS12,
                self._lib.PKCS12_R_PKCS12_CIPHERFINAL_ERROR,
            )
            or (
                self._lib.Cryptography_HAS_PROVIDERS
                and errors[0]._lib_reason_match(
                    self._lib.ERR_LIB_PROV,
                    self._lib.PROV_R_BAD_DECRYPT,
                )
            )
        ):
            raise ValueError("Bad decrypt. Incorrect password?")

        elif any(
            error._lib_reason_match(
                self._lib.ERR_LIB_EVP,
                self._lib.EVP_R_UNSUPPORTED_PRIVATE_KEY_ALGORITHM,
            )
            for error in errors
        ):
            raise ValueError("Unsupported public key algorithm.")

        else:
            raise ValueError(
                "Could not deserialize key data. The data may be in an "
                "incorrect format, it may be encrypted with an unsupported "
                "algorithm, or it may be an unsupported key type (e.g. EC "
                "curves with explicit parameters).",
                errors,
            )

    def elliptic_curve_supported(self, curve: ec.EllipticCurve) -> bool:
        try:
            curve_nid = self._elliptic_curve_to_nid(curve)
        except UnsupportedAlgorithm:
            curve_nid = self._lib.NID_undef

        group = self._lib.EC_GROUP_new_by_curve_name(curve_nid)

        if group == self._ffi.NULL:
            self._consume_errors()
            return False
        else:
            self.openssl_assert(curve_nid != self._lib.NID_undef)
            self._lib.EC_GROUP_free(group)
            return True

    def elliptic_curve_signature_algorithm_supported(
        self,
        signature_algorithm: ec.EllipticCurveSignatureAlgorithm,
        curve: ec.EllipticCurve,
    ) -> bool:
        # We only support ECDSA right now.
        if not isinstance(signature_algorithm, ec.ECDSA):
            return False

        return self.elliptic_curve_supported(curve)

    def generate_elliptic_curve_private_key(
        self, curve: ec.EllipticCurve
    ) -> ec.EllipticCurvePrivateKey:
        """
        Generate a new private key on the named curve.
        """

        if self.elliptic_curve_supported(curve):
            ec_cdata = self._ec_key_new_by_curve(curve)

            res = self._lib.EC_KEY_generate_key(ec_cdata)
            self.openssl_assert(res == 1)

            evp_pkey = self._ec_cdata_to_evp_pkey(ec_cdata)

            return _EllipticCurvePrivateKey(self, ec_cdata, evp_pkey)
        else:
            raise UnsupportedAlgorithm(
                f"Backend object does not support {curve.name}.",
                _Reasons.UNSUPPORTED_ELLIPTIC_CURVE,
            )

    def load_elliptic_curve_private_numbers(
        self, numbers: ec.EllipticCurvePrivateNumbers
    ) -> ec.EllipticCurvePrivateKey:
        public = numbers.public_numbers

        ec_cdata = self._ec_key_new_by_curve(public.curve)

        private_value = self._ffi.gc(
            self._int_to_bn(numbers.private_value), self._lib.BN_clear_free
        )
        res = self._lib.EC_KEY_set_private_key(ec_cdata, private_value)
        if res != 1:
            self._consume_errors()
            raise ValueError("Invalid EC key.")

        with self._tmp_bn_ctx() as bn_ctx:
            self._ec_key_set_public_key_affine_coordinates(
                ec_cdata, public.x, public.y, bn_ctx
            )
            # derive the expected public point and compare it to the one we
            # just set based on the values we were given. If they don't match
            # this isn't a valid key pair.
            group = self._lib.EC_KEY_get0_group(ec_cdata)
            self.openssl_assert(group != self._ffi.NULL)
            set_point = backend._lib.EC_KEY_get0_public_key(ec_cdata)
            self.openssl_assert(set_point != self._ffi.NULL)
            computed_point = self._lib.EC_POINT_new(group)
            self.openssl_assert(computed_point != self._ffi.NULL)
            computed_point = self._ffi.gc(computed_point, self._lib.EC_POINT_free)
            res = self._lib.EC_POINT_mul(
                group,
                computed_point,
                private_value,
                self._ffi.NULL,
                self._ffi.NULL,
                bn_ctx,
            )
            self.openssl_assert(res == 1)
            if self._lib.EC_POINT_cmp(group, set_point, computed_point, bn_ctx) != 0:
                raise ValueError("Invalid EC key.")

        evp_pkey = self._ec_cdata_to_evp_pkey(ec_cdata)

        return _EllipticCurvePrivateKey(self, ec_cdata, evp_pkey)

    def load_elliptic_curve_public_numbers(
        self, numbers: ec.EllipticCurvePublicNumbers
    ) -> ec.EllipticCurvePublicKey:
        ec_cdata = self._ec_key_new_by_curve(numbers.curve)
        with self._tmp_bn_ctx() as bn_ctx:
            self._ec_key_set_public_key_affine_coordinates(
                ec_cdata, numbers.x, numbers.y, bn_ctx
            )
        evp_pkey = self._ec_cdata_to_evp_pkey(ec_cdata)

        return _EllipticCurvePublicKey(self, ec_cdata, evp_pkey)

    def load_elliptic_curve_public_bytes(
        self, curve: ec.EllipticCurve, point_bytes: bytes
    ) -> ec.EllipticCurvePublicKey:
        ec_cdata = self._ec_key_new_by_curve(curve)
        group = self._lib.EC_KEY_get0_group(ec_cdata)
        self.openssl_assert(group != self._ffi.NULL)
        point = self._lib.EC_POINT_new(group)
        self.openssl_assert(point != self._ffi.NULL)
        point = self._ffi.gc(point, self._lib.EC_POINT_free)
        with self._tmp_bn_ctx() as bn_ctx:
            res = self._lib.EC_POINT_oct2point(
                group, point, point_bytes, len(point_bytes), bn_ctx
            )
            if res != 1:
                self._consume_errors()
                raise ValueError("Invalid public bytes for the given curve")

        res = self._lib.EC_KEY_set_public_key(ec_cdata, point)
        self.openssl_assert(res == 1)
        evp_pkey = self._ec_cdata_to_evp_pkey(ec_cdata)
        return _EllipticCurvePublicKey(self, ec_cdata, evp_pkey)

    def derive_elliptic_curve_private_key(
        self, private_value: int, curve: ec.EllipticCurve
    ) -> ec.EllipticCurvePrivateKey:
        ec_cdata = self._ec_key_new_by_curve(curve)

        group = self._lib.EC_KEY_get0_group(ec_cdata)
        self.openssl_assert(group != self._ffi.NULL)

        point = self._lib.EC_POINT_new(group)
        self.openssl_assert(point != self._ffi.NULL)
        point = self._ffi.gc(point, self._lib.EC_POINT_free)

        value = self._int_to_bn(private_value)
        value = self._ffi.gc(value, self._lib.BN_clear_free)

        with self._tmp_bn_ctx() as bn_ctx:
            res = self._lib.EC_POINT_mul(
                group, point, value, self._ffi.NULL, self._ffi.NULL, bn_ctx
            )
            self.openssl_assert(res == 1)

            bn_x = self._lib.BN_CTX_get(bn_ctx)
            bn_y = self._lib.BN_CTX_get(bn_ctx)

            res = self._lib.EC_POINT_get_affine_coordinates(
                group, point, bn_x, bn_y, bn_ctx
            )
            if res != 1:
                self._consume_errors()
                raise ValueError("Unable to derive key from private_value")

        res = self._lib.EC_KEY_set_public_key(ec_cdata, point)
        self.openssl_assert(res == 1)
        private = self._int_to_bn(private_value)
        private = self._ffi.gc(private, self._lib.BN_clear_free)
        res = self._lib.EC_KEY_set_private_key(ec_cdata, private)
        self.openssl_assert(res == 1)

        evp_pkey = self._ec_cdata_to_evp_pkey(ec_cdata)

        return _EllipticCurvePrivateKey(self, ec_cdata, evp_pkey)

    def _ec_key_new_by_curve(self, curve: ec.EllipticCurve):
        curve_nid = self._elliptic_curve_to_nid(curve)
        return self._ec_key_new_by_curve_nid(curve_nid)

    def _ec_key_new_by_curve_nid(self, curve_nid: int):
        ec_cdata = self._lib.EC_KEY_new_by_curve_name(curve_nid)
        self.openssl_assert(ec_cdata != self._ffi.NULL)
        return self._ffi.gc(ec_cdata, self._lib.EC_KEY_free)

    def elliptic_curve_exchange_algorithm_supported(
        self, algorithm: ec.ECDH, curve: ec.EllipticCurve
    ) -> bool:
        if self._fips_enabled and not isinstance(curve, self._fips_ecdh_curves):
            return False

        return self.elliptic_curve_supported(curve) and isinstance(algorithm, ec.ECDH)

    def _ec_cdata_to_evp_pkey(self, ec_cdata):
        evp_pkey = self._create_evp_pkey_gc()
        res = self._lib.EVP_PKEY_set1_EC_KEY(evp_pkey, ec_cdata)
        self.openssl_assert(res == 1)
        return evp_pkey

    def _elliptic_curve_to_nid(self, curve: ec.EllipticCurve) -> int:
        """
        Get the NID for a curve name.
        """

        curve_aliases = {"secp192r1": "prime192v1", "secp256r1": "prime256v1"}

        curve_name = curve_aliases.get(curve.name, curve.name)

        curve_nid = self._lib.OBJ_sn2nid(curve_name.encode())
        if curve_nid == self._lib.NID_undef:
            raise UnsupportedAlgorithm(
                f"{curve.name} is not a supported elliptic curve",
                _Reasons.UNSUPPORTED_ELLIPTIC_CURVE,
            )
        return curve_nid

    @contextmanager
    def _tmp_bn_ctx(self):
        bn_ctx = self._lib.BN_CTX_new()
        self.openssl_assert(bn_ctx != self._ffi.NULL)
        bn_ctx = self._ffi.gc(bn_ctx, self._lib.BN_CTX_free)
        self._lib.BN_CTX_start(bn_ctx)
        try:
            yield bn_ctx
        finally:
            self._lib.BN_CTX_end(bn_ctx)

    def _ec_key_set_public_key_affine_coordinates(
        self,
        ec_cdata,
        x: int,
        y: int,
        bn_ctx,
    ) -> None:
        """
        Sets the public key point in the EC_KEY context to the affine x and y
        values.
        """

        if x < 0 or y < 0:
            raise ValueError("Invalid EC key. Both x and y must be non-negative.")

        x = self._ffi.gc(self._int_to_bn(x), self._lib.BN_free)
        y = self._ffi.gc(self._int_to_bn(y), self._lib.BN_free)
        group = self._lib.EC_KEY_get0_group(ec_cdata)
        self.openssl_assert(group != self._ffi.NULL)
        point = self._lib.EC_POINT_new(group)
        self.openssl_assert(point != self._ffi.NULL)
        point = self._ffi.gc(point, self._lib.EC_POINT_free)
        res = self._lib.EC_POINT_set_affine_coordinates(group, point, x, y, bn_ctx)
        if res != 1:
            self._consume_errors()
            raise ValueError("Invalid EC key.")
        res = self._lib.EC_KEY_set_public_key(ec_cdata, point)
        self.openssl_assert(res == 1)

    def _private_key_bytes(
        self,
        encoding: serialization.Encoding,
        format: serialization.PrivateFormat,
        encryption_algorithm: serialization.KeySerializationEncryption,
        key,
        evp_pkey,
        cdata,
    ) -> bytes:
        # validate argument types
        if not isinstance(encoding, serialization.Encoding):
            raise TypeError("encoding must be an item from the Encoding enum")
        if not isinstance(format, serialization.PrivateFormat):
            raise TypeError("format must be an item from the PrivateFormat enum")
        if not isinstance(
            encryption_algorithm, serialization.KeySerializationEncryption
        ):
            raise TypeError(
                "Encryption algorithm must be a KeySerializationEncryption " "instance"
            )

        # validate password
        if isinstance(encryption_algorithm, serialization.NoEncryption):
            password = b""
        elif isinstance(encryption_algorithm, serialization.BestAvailableEncryption):
            password = encryption_algorithm.password
            if len(password) > 1023:
                raise ValueError(
                    "Passwords longer than 1023 bytes are not supported by "
                    "this backend"
                )
        elif (
            isinstance(encryption_algorithm, serialization._KeySerializationEncryption)
            and encryption_algorithm._format
            is format
            is serialization.PrivateFormat.OpenSSH
        ):
            password = encryption_algorithm.password
        else:
            raise ValueError("Unsupported encryption type")

        # PKCS8 + PEM/DER
        if format is serialization.PrivateFormat.PKCS8:
            if encoding is serialization.Encoding.PEM:
                write_bio = self._lib.PEM_write_bio_PKCS8PrivateKey
            elif encoding is serialization.Encoding.DER:
                write_bio = self._lib.i2d_PKCS8PrivateKey_bio
            else:
                raise ValueError("Unsupported encoding for PKCS8")
            return self._private_key_bytes_via_bio(write_bio, evp_pkey, password)

        # TraditionalOpenSSL + PEM/DER
        if format is serialization.PrivateFormat.TraditionalOpenSSL:
            if self._fips_enabled and not isinstance(
                encryption_algorithm, serialization.NoEncryption
            ):
                raise ValueError(
                    "Encrypted traditional OpenSSL format is not "
                    "supported in FIPS mode."
                )
            key_type = self._lib.EVP_PKEY_id(evp_pkey)

            if encoding is serialization.Encoding.PEM:
                if key_type == self._lib.EVP_PKEY_RSA:
                    write_bio = self._lib.PEM_write_bio_RSAPrivateKey
                else:
                    assert key_type == self._lib.EVP_PKEY_EC
                    write_bio = self._lib.PEM_write_bio_ECPrivateKey
                return self._private_key_bytes_via_bio(write_bio, cdata, password)

            if encoding is serialization.Encoding.DER:
                if password:
                    raise ValueError(
                        "Encryption is not supported for DER encoded "
                        "traditional OpenSSL keys"
                    )
                if key_type == self._lib.EVP_PKEY_RSA:
                    write_bio = self._lib.i2d_RSAPrivateKey_bio
                else:
                    assert key_type == self._lib.EVP_PKEY_EC
                    write_bio = self._lib.i2d_ECPrivateKey_bio
                return self._bio_func_output(write_bio, cdata)

            raise ValueError("Unsupported encoding for TraditionalOpenSSL")

        # OpenSSH + PEM
        if format is serialization.PrivateFormat.OpenSSH:
            if encoding is serialization.Encoding.PEM:
                return ssh._serialize_ssh_private_key(
                    key, password, encryption_algorithm
                )

            raise ValueError(
                "OpenSSH private key format can only be used" " with PEM encoding"
            )

        # Anything that key-specific code was supposed to handle earlier,
        # like Raw.
        raise ValueError("format is invalid with this key")

    def _private_key_bytes_via_bio(self, write_bio, evp_pkey, password) -> bytes:
        if not password:
            evp_cipher = self._ffi.NULL
        else:
            # This is a curated value that we will update over time.
            evp_cipher = self._lib.EVP_get_cipherbyname(b"aes-256-cbc")

        return self._bio_func_output(
            write_bio,
            evp_pkey,
            evp_cipher,
            password,
            len(password),
            self._ffi.NULL,
            self._ffi.NULL,
        )

    def _bio_func_output(self, write_bio, *args) -> bytes:
        bio = self._create_mem_bio_gc()
        res = write_bio(bio, *args)
        self.openssl_assert(res == 1)
        return self._read_mem_bio(bio)

    def _public_key_bytes(
        self,
        encoding: serialization.Encoding,
        format: serialization.PublicFormat,
        key,
        evp_pkey,
        cdata,
    ) -> bytes:
        if not isinstance(encoding, serialization.Encoding):
            raise TypeError("encoding must be an item from the Encoding enum")
        if not isinstance(format, serialization.PublicFormat):
            raise TypeError("format must be an item from the PublicFormat enum")

        # SubjectPublicKeyInfo + PEM/DER
        if format is serialization.PublicFormat.SubjectPublicKeyInfo:
            if encoding is serialization.Encoding.PEM:
                write_bio = self._lib.PEM_write_bio_PUBKEY
            elif encoding is serialization.Encoding.DER:
                write_bio = self._lib.i2d_PUBKEY_bio
            else:
                raise ValueError(
                    "SubjectPublicKeyInfo works only with PEM or DER encoding"
                )
            return self._bio_func_output(write_bio, evp_pkey)

        # PKCS1 + PEM/DER
        if format is serialization.PublicFormat.PKCS1:
            # Only RSA is supported here.
            key_type = self._lib.EVP_PKEY_id(evp_pkey)
            if key_type != self._lib.EVP_PKEY_RSA:
                raise ValueError("PKCS1 format is supported only for RSA keys")

            if encoding is serialization.Encoding.PEM:
                write_bio = self._lib.PEM_write_bio_RSAPublicKey
            elif encoding is serialization.Encoding.DER:
                write_bio = self._lib.i2d_RSAPublicKey_bio
            else:
                raise ValueError("PKCS1 works only with PEM or DER encoding")
            return self._bio_func_output(write_bio, cdata)

        # OpenSSH + OpenSSH
        if format is serialization.PublicFormat.OpenSSH:
            if encoding is serialization.Encoding.OpenSSH:
                return ssh.serialize_ssh_public_key(key)

            raise ValueError("OpenSSH format must be used with OpenSSH encoding")

        # Anything that key-specific code was supposed to handle earlier,
        # like Raw, CompressedPoint, UncompressedPoint
        raise ValueError("format is invalid with this key")

    def dh_supported(self) -> bool:
        return not self._lib.CRYPTOGRAPHY_IS_BORINGSSL

    def generate_dh_parameters(self, generator: int, key_size: int) -> dh.DHParameters:
        return rust_openssl.dh.generate_parameters(generator, key_size)

    def generate_dh_private_key(self, parameters: dh.DHParameters) -> dh.DHPrivateKey:
        return parameters.generate_private_key()

    def generate_dh_private_key_and_parameters(
        self, generator: int, key_size: int
    ) -> dh.DHPrivateKey:
        return self.generate_dh_private_key(
            self.generate_dh_parameters(generator, key_size)
        )

    def load_dh_private_numbers(self, numbers: dh.DHPrivateNumbers) -> dh.DHPrivateKey:
        return rust_openssl.dh.from_private_numbers(numbers)

    def load_dh_public_numbers(self, numbers: dh.DHPublicNumbers) -> dh.DHPublicKey:
        return rust_openssl.dh.from_public_numbers(numbers)

    def load_dh_parameter_numbers(
        self, numbers: dh.DHParameterNumbers
    ) -> dh.DHParameters:
        return rust_openssl.dh.from_parameter_numbers(numbers)

    def dh_parameters_supported(
        self, p: int, g: int, q: typing.Optional[int] = None
    ) -> bool:
        try:
            rust_openssl.dh.from_parameter_numbers(dh.DHParameterNumbers(p=p, g=g, q=q))
        except ValueError:
            return False
        else:
            return True

    def dh_x942_serialization_supported(self) -> bool:
        return self._lib.Cryptography_HAS_EVP_PKEY_DHX == 1

    def x25519_load_public_bytes(self, data: bytes) -> x25519.X25519PublicKey:
        return rust_openssl.x25519.from_public_bytes(data)

    def x25519_load_private_bytes(self, data: bytes) -> x25519.X25519PrivateKey:
        return rust_openssl.x25519.from_private_bytes(data)

    def x25519_generate_key(self) -> x25519.X25519PrivateKey:
        return rust_openssl.x25519.generate_key()

    def x25519_supported(self) -> bool:
        if self._fips_enabled:
            return False
        return not self._lib.CRYPTOGRAPHY_LIBRESSL_LESS_THAN_370

    def x448_load_public_bytes(self, data: bytes) -> x448.X448PublicKey:
        return rust_openssl.x448.from_public_bytes(data)

    def x448_load_private_bytes(self, data: bytes) -> x448.X448PrivateKey:
        return rust_openssl.x448.from_private_bytes(data)

    def x448_generate_key(self) -> x448.X448PrivateKey:
        return rust_openssl.x448.generate_key()

    def x448_supported(self) -> bool:
        if self._fips_enabled:
            return False
        return (
            not self._lib.CRYPTOGRAPHY_IS_LIBRESSL
            and not self._lib.CRYPTOGRAPHY_IS_BORINGSSL
        )

    def ed25519_supported(self) -> bool:
        if self._fips_enabled:
            return False
        return self._lib.CRYPTOGRAPHY_HAS_WORKING_ED25519

    def ed25519_load_public_bytes(self, data: bytes) -> ed25519.Ed25519PublicKey:
        return rust_openssl.ed25519.from_public_bytes(data)

    def ed25519_load_private_bytes(self, data: bytes) -> ed25519.Ed25519PrivateKey:
        return rust_openssl.ed25519.from_private_bytes(data)

    def ed25519_generate_key(self) -> ed25519.Ed25519PrivateKey:
        return rust_openssl.ed25519.generate_key()

    def ed448_supported(self) -> bool:
        if self._fips_enabled:
            return False
        return (
            not self._lib.CRYPTOGRAPHY_IS_LIBRESSL
            and not self._lib.CRYPTOGRAPHY_IS_BORINGSSL
        )

    def ed448_load_public_bytes(self, data: bytes) -> ed448.Ed448PublicKey:
        return rust_openssl.ed448.from_public_bytes(data)

    def ed448_load_private_bytes(self, data: bytes) -> ed448.Ed448PrivateKey:
        return rust_openssl.ed448.from_private_bytes(data)

    def ed448_generate_key(self) -> ed448.Ed448PrivateKey:
        return rust_openssl.ed448.generate_key()

    def aead_cipher_supported(self, cipher) -> bool:
        return aead._aead_cipher_supported(self, cipher)

    def _zero_data(self, data, length: int) -> None:
        # We clear things this way because at the moment we're not
        # sure of a better way that can guarantee it overwrites the
        # memory of a bytearray and doesn't just replace the underlying char *.
        for i in range(length):
            data[i] = 0

    @contextlib.contextmanager
    def _zeroed_null_terminated_buf(self, data):
        """
        This method takes bytes, which can be a bytestring or a mutable
        buffer like a bytearray, and yields a null-terminated version of that
        data. This is required because PKCS12_parse doesn't take a length with
        its password char * and ffi.from_buffer doesn't provide null
        termination. So, to support zeroing the data via bytearray we
        need to build this ridiculous construct that copies the memory, but
        zeroes it after use.
        """
        if data is None:
            yield self._ffi.NULL
        else:
            data_len = len(data)
            buf = self._ffi.new("char[]", data_len + 1)
            self._ffi.memmove(buf, data, data_len)
            try:
                yield buf
            finally:
                # Cast to a uint8_t * so we can assign by integer
                self._zero_data(self._ffi.cast("uint8_t *", buf), data_len)

    def load_key_and_certificates_from_pkcs12(
        self, data: bytes, password: typing.Optional[bytes]
    ) -> typing.Tuple[
        typing.Optional[PrivateKeyTypes],
        typing.Optional[x509.Certificate],
        typing.List[x509.Certificate],
    ]:
        pkcs12 = self.load_pkcs12(data, password)
        return (
            pkcs12.key,
            pkcs12.cert.certificate if pkcs12.cert else None,
            [cert.certificate for cert in pkcs12.additional_certs],
        )

    def load_pkcs12(
        self, data: bytes, password: typing.Optional[bytes]
    ) -> PKCS12KeyAndCertificates:
        if password is not None:
            utils._check_byteslike("password", password)

        bio = self._bytes_to_bio(data)
        p12 = self._lib.d2i_PKCS12_bio(bio.bio, self._ffi.NULL)
        if p12 == self._ffi.NULL:
            self._consume_errors()
            raise ValueError("Could not deserialize PKCS12 data")

        p12 = self._ffi.gc(p12, self._lib.PKCS12_free)
        evp_pkey_ptr = self._ffi.new("EVP_PKEY **")
        x509_ptr = self._ffi.new("X509 **")
        sk_x509_ptr = self._ffi.new("Cryptography_STACK_OF_X509 **")
        with self._zeroed_null_terminated_buf(password) as password_buf:
            res = self._lib.PKCS12_parse(
                p12, password_buf, evp_pkey_ptr, x509_ptr, sk_x509_ptr
            )
        if res == 0:
            self._consume_errors()
            raise ValueError("Invalid password or PKCS12 data")

        cert = None
        key = None
        additional_certificates = []

        if evp_pkey_ptr[0] != self._ffi.NULL:
            evp_pkey = self._ffi.gc(evp_pkey_ptr[0], self._lib.EVP_PKEY_free)
            # We don't support turning off RSA key validation when loading
            # PKCS12 keys
            key = self._evp_pkey_to_private_key(
                evp_pkey, unsafe_skip_rsa_key_validation=False
            )

        if x509_ptr[0] != self._ffi.NULL:
            x509 = self._ffi.gc(x509_ptr[0], self._lib.X509_free)
            cert_obj = self._ossl2cert(x509)
            name = None
            maybe_name = self._lib.X509_alias_get0(x509, self._ffi.NULL)
            if maybe_name != self._ffi.NULL:
                name = self._ffi.string(maybe_name)
            cert = PKCS12Certificate(cert_obj, name)

        if sk_x509_ptr[0] != self._ffi.NULL:
            sk_x509 = self._ffi.gc(sk_x509_ptr[0], self._lib.sk_X509_free)
            num = self._lib.sk_X509_num(sk_x509_ptr[0])

            # In OpenSSL < 3.0.0 PKCS12 parsing reverses the order of the
            # certificates.
            indices: typing.Iterable[int]
            if (
                self._lib.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER
                or self._lib.CRYPTOGRAPHY_IS_BORINGSSL
            ):
                indices = range(num)
            else:
                indices = reversed(range(num))

            for i in indices:
                x509 = self._lib.sk_X509_value(sk_x509, i)
                self.openssl_assert(x509 != self._ffi.NULL)
                x509 = self._ffi.gc(x509, self._lib.X509_free)
                addl_cert = self._ossl2cert(x509)
                addl_name = None
                maybe_name = self._lib.X509_alias_get0(x509, self._ffi.NULL)
                if maybe_name != self._ffi.NULL:
                    addl_name = self._ffi.string(maybe_name)
                additional_certificates.append(PKCS12Certificate(addl_cert, addl_name))

        return PKCS12KeyAndCertificates(key, cert, additional_certificates)

    def serialize_key_and_certificates_to_pkcs12(
        self,
        name: typing.Optional[bytes],
        key: typing.Optional[PKCS12PrivateKeyTypes],
        cert: typing.Optional[x509.Certificate],
        cas: typing.Optional[typing.List[_PKCS12CATypes]],
        encryption_algorithm: serialization.KeySerializationEncryption,
    ) -> bytes:
        password = None
        if name is not None:
            utils._check_bytes("name", name)

        if isinstance(encryption_algorithm, serialization.NoEncryption):
            nid_cert = -1
            nid_key = -1
            pkcs12_iter = 0
            mac_iter = 0
            mac_alg = self._ffi.NULL
        elif isinstance(encryption_algorithm, serialization.BestAvailableEncryption):
            # PKCS12 encryption is hopeless trash and can never be fixed.
            # OpenSSL 3 supports PBESv2, but Libre and Boring do not, so
            # we use PBESv1 with 3DES on the older paths.
            if self._lib.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER:
                nid_cert = self._lib.NID_aes_256_cbc
                nid_key = self._lib.NID_aes_256_cbc
            else:
                nid_cert = self._lib.NID_pbe_WithSHA1And3_Key_TripleDES_CBC
                nid_key = self._lib.NID_pbe_WithSHA1And3_Key_TripleDES_CBC
            # At least we can set this higher than OpenSSL's default
            pkcs12_iter = 20000
            # mac_iter chosen for compatibility reasons, see:
            # https://www.openssl.org/docs/man1.1.1/man3/PKCS12_create.html
            # Did we mention how lousy PKCS12 encryption is?
            mac_iter = 1
            # MAC algorithm can only be set on OpenSSL 3.0.0+
            mac_alg = self._ffi.NULL
            password = encryption_algorithm.password
        elif (
            isinstance(encryption_algorithm, serialization._KeySerializationEncryption)
            and encryption_algorithm._format is serialization.PrivateFormat.PKCS12
        ):
            # Default to OpenSSL's defaults. Behavior will vary based on the
            # version of OpenSSL cryptography is compiled against.
            nid_cert = 0
            nid_key = 0
            # Use the default iters we use in best available
            pkcs12_iter = 20000
            # See the Best Available comment for why this is 1
            mac_iter = 1
            password = encryption_algorithm.password
            keycertalg = encryption_algorithm._key_cert_algorithm
            if keycertalg is PBES.PBESv1SHA1And3KeyTripleDESCBC:
                nid_cert = self._lib.NID_pbe_WithSHA1And3_Key_TripleDES_CBC
                nid_key = self._lib.NID_pbe_WithSHA1And3_Key_TripleDES_CBC
            elif keycertalg is PBES.PBESv2SHA256AndAES256CBC:
                if not self._lib.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER:
                    raise UnsupportedAlgorithm(
                        "PBESv2 is not supported by this version of OpenSSL"
                    )
                nid_cert = self._lib.NID_aes_256_cbc
                nid_key = self._lib.NID_aes_256_cbc
            else:
                assert keycertalg is None
                # We use OpenSSL's defaults

            if encryption_algorithm._hmac_hash is not None:
                if not self._lib.Cryptography_HAS_PKCS12_SET_MAC:
                    raise UnsupportedAlgorithm(
                        "Setting MAC algorithm is not supported by this "
                        "version of OpenSSL."
                    )
                mac_alg = self._evp_md_non_null_from_algorithm(
                    encryption_algorithm._hmac_hash
                )
                self.openssl_assert(mac_alg != self._ffi.NULL)
            else:
                mac_alg = self._ffi.NULL

            if encryption_algorithm._kdf_rounds is not None:
                pkcs12_iter = encryption_algorithm._kdf_rounds

        else:
            raise ValueError("Unsupported key encryption type")

        if cas is None or len(cas) == 0:
            sk_x509 = self._ffi.NULL
        else:
            sk_x509 = self._lib.sk_X509_new_null()
            sk_x509 = self._ffi.gc(sk_x509, self._lib.sk_X509_free)

            # This list is to keep the x509 values alive until end of function
            ossl_cas = []
            for ca in cas:
                if isinstance(ca, PKCS12Certificate):
                    ca_alias = ca.friendly_name
                    ossl_ca = self._cert2ossl(ca.certificate)
                    if ca_alias is None:
                        res = self._lib.X509_alias_set1(ossl_ca, self._ffi.NULL, -1)
                    else:
                        res = self._lib.X509_alias_set1(
                            ossl_ca, ca_alias, len(ca_alias)
                        )
                    self.openssl_assert(res == 1)
                else:
                    ossl_ca = self._cert2ossl(ca)
                ossl_cas.append(ossl_ca)
                res = self._lib.sk_X509_push(sk_x509, ossl_ca)
                backend.openssl_assert(res >= 1)

        with self._zeroed_null_terminated_buf(password) as password_buf:
            with self._zeroed_null_terminated_buf(name) as name_buf:
                ossl_cert = self._cert2ossl(cert) if cert else self._ffi.NULL
                ossl_pkey = self._key2ossl(key) if key is not None else self._ffi.NULL

                p12 = self._lib.PKCS12_create(
                    password_buf,
                    name_buf,
                    ossl_pkey,
                    ossl_cert,
                    sk_x509,
                    nid_key,
                    nid_cert,
                    pkcs12_iter,
                    mac_iter,
                    0,
                )

            if self._lib.Cryptography_HAS_PKCS12_SET_MAC and mac_alg != self._ffi.NULL:
                self._lib.PKCS12_set_mac(
                    p12,
                    password_buf,
                    -1,
                    self._ffi.NULL,
                    0,
                    mac_iter,
                    mac_alg,
                )

        self.openssl_assert(p12 != self._ffi.NULL)
        p12 = self._ffi.gc(p12, self._lib.PKCS12_free)

        bio = self._create_mem_bio_gc()
        res = self._lib.i2d_PKCS12_bio(bio, p12)
        self.openssl_assert(res > 0)
        return self._read_mem_bio(bio)

    def poly1305_supported(self) -> bool:
        if self._fips_enabled:
            return False
        return self._lib.Cryptography_HAS_POLY1305 == 1

    def pkcs7_supported(self) -> bool:
        return not self._lib.CRYPTOGRAPHY_IS_BORINGSSL

    def load_pem_pkcs7_certificates(self, data: bytes) -> typing.List[x509.Certificate]:
        utils._check_bytes("data", data)
        bio = self._bytes_to_bio(data)
        p7 = self._lib.PEM_read_bio_PKCS7(
            bio.bio, self._ffi.NULL, self._ffi.NULL, self._ffi.NULL
        )
        if p7 == self._ffi.NULL:
            self._consume_errors()
            raise ValueError("Unable to parse PKCS7 data")

        p7 = self._ffi.gc(p7, self._lib.PKCS7_free)
        return self._load_pkcs7_certificates(p7)

    def load_der_pkcs7_certificates(self, data: bytes) -> typing.List[x509.Certificate]:
        utils._check_bytes("data", data)
        bio = self._bytes_to_bio(data)
        p7 = self._lib.d2i_PKCS7_bio(bio.bio, self._ffi.NULL)
        if p7 == self._ffi.NULL:
            self._consume_errors()
            raise ValueError("Unable to parse PKCS7 data")

        p7 = self._ffi.gc(p7, self._lib.PKCS7_free)
        return self._load_pkcs7_certificates(p7)

    def _load_pkcs7_certificates(self, p7) -> typing.List[x509.Certificate]:
        nid = self._lib.OBJ_obj2nid(p7.type)
        self.openssl_assert(nid != self._lib.NID_undef)
        if nid != self._lib.NID_pkcs7_signed:
            raise UnsupportedAlgorithm(
                "Only basic signed structures are currently supported. NID"
                " for this data was {}".format(nid),
                _Reasons.UNSUPPORTED_SERIALIZATION,
            )

        sk_x509 = p7.d.sign.cert
        num = self._lib.sk_X509_num(sk_x509)
        certs = []
        for i in range(num):
            x509 = self._lib.sk_X509_value(sk_x509, i)
            self.openssl_assert(x509 != self._ffi.NULL)
            cert = self._ossl2cert(x509)
            certs.append(cert)

        return certs


class GetCipherByName:
    def __init__(self, fmt: str):
        self._fmt = fmt

    def __call__(self, backend: Backend, cipher: CipherAlgorithm, mode: Mode):
        cipher_name = self._fmt.format(cipher=cipher, mode=mode).lower()
        evp_cipher = backend._lib.EVP_get_cipherbyname(cipher_name.encode("ascii"))

        # try EVP_CIPHER_fetch if present
        if (
            evp_cipher == backend._ffi.NULL
            and backend._lib.Cryptography_HAS_300_EVP_CIPHER
        ):
            evp_cipher = backend._lib.EVP_CIPHER_fetch(
                backend._ffi.NULL,
                cipher_name.encode("ascii"),
                backend._ffi.NULL,
            )

        backend._consume_errors()
        return evp_cipher


def _get_xts_cipher(backend: Backend, cipher: AES, mode):
    cipher_name = f"aes-{cipher.key_size // 2}-xts"
    return backend._lib.EVP_get_cipherbyname(cipher_name.encode("ascii"))


backend = Backend()

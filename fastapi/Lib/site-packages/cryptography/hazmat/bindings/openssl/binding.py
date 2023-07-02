# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import os
import sys
import threading
import types
import typing
import warnings

import cryptography
from cryptography.exceptions import InternalError
from cryptography.hazmat.bindings._rust import _openssl, openssl
from cryptography.hazmat.bindings.openssl._conditional import CONDITIONAL_NAMES


def _openssl_assert(
    lib,
    ok: bool,
    errors: typing.Optional[typing.List[openssl.OpenSSLError]] = None,
) -> None:
    if not ok:
        if errors is None:
            errors = openssl.capture_error_stack()

        raise InternalError(
            "Unknown OpenSSL error. This error is commonly encountered when "
            "another library is not cleaning up the OpenSSL error stack. If "
            "you are using cryptography with another library that uses "
            "OpenSSL try disabling it before reporting a bug. Otherwise "
            "please file an issue at https://github.com/pyca/cryptography/"
            "issues with information on how to reproduce "
            "this. ({!r})".format(errors),
            errors,
        )


def _legacy_provider_error(loaded: bool) -> None:
    if not loaded:
        raise RuntimeError(
            "OpenSSL 3.0's legacy provider failed to load. This is a fatal "
            "error by default, but cryptography supports running without "
            "legacy algorithms by setting the environment variable "
            "CRYPTOGRAPHY_OPENSSL_NO_LEGACY. If you did not expect this error,"
            " you have likely made a mistake with your OpenSSL configuration."
        )


def build_conditional_library(
    lib: typing.Any,
    conditional_names: typing.Dict[str, typing.Callable[[], typing.List[str]]],
) -> typing.Any:
    conditional_lib = types.ModuleType("lib")
    conditional_lib._original_lib = lib  # type: ignore[attr-defined]
    excluded_names = set()
    for condition, names_cb in conditional_names.items():
        if not getattr(lib, condition):
            excluded_names.update(names_cb())

    for attr in dir(lib):
        if attr not in excluded_names:
            setattr(conditional_lib, attr, getattr(lib, attr))

    return conditional_lib


class Binding:
    """
    OpenSSL API wrapper.
    """

    lib: typing.ClassVar = None
    ffi = _openssl.ffi
    _lib_loaded = False
    _init_lock = threading.Lock()
    _legacy_provider: typing.Any = ffi.NULL
    _legacy_provider_loaded = False
    _default_provider: typing.Any = ffi.NULL

    def __init__(self) -> None:
        self._ensure_ffi_initialized()

    def _enable_fips(self) -> None:
        # This function enables FIPS mode for OpenSSL 3.0.0 on installs that
        # have the FIPS provider installed properly.
        _openssl_assert(self.lib, self.lib.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER)
        self._base_provider = self.lib.OSSL_PROVIDER_load(self.ffi.NULL, b"base")
        _openssl_assert(self.lib, self._base_provider != self.ffi.NULL)
        self.lib._fips_provider = self.lib.OSSL_PROVIDER_load(self.ffi.NULL, b"fips")
        _openssl_assert(self.lib, self.lib._fips_provider != self.ffi.NULL)

        res = self.lib.EVP_default_properties_enable_fips(self.ffi.NULL, 1)
        _openssl_assert(self.lib, res == 1)

    @classmethod
    def _ensure_ffi_initialized(cls) -> None:
        with cls._init_lock:
            if not cls._lib_loaded:
                cls.lib = build_conditional_library(_openssl.lib, CONDITIONAL_NAMES)
                cls._lib_loaded = True
                # As of OpenSSL 3.0.0 we must register a legacy cipher provider
                # to get RC2 (needed for junk asymmetric private key
                # serialization), RC4, Blowfish, IDEA, SEED, etc. These things
                # are ugly legacy, but we aren't going to get rid of them
                # any time soon.
                if cls.lib.CRYPTOGRAPHY_OPENSSL_300_OR_GREATER:
                    if not os.environ.get("CRYPTOGRAPHY_OPENSSL_NO_LEGACY"):
                        cls._legacy_provider = cls.lib.OSSL_PROVIDER_load(
                            cls.ffi.NULL, b"legacy"
                        )
                        cls._legacy_provider_loaded = (
                            cls._legacy_provider != cls.ffi.NULL
                        )
                        _legacy_provider_error(cls._legacy_provider_loaded)

                    cls._default_provider = cls.lib.OSSL_PROVIDER_load(
                        cls.ffi.NULL, b"default"
                    )
                    _openssl_assert(cls.lib, cls._default_provider != cls.ffi.NULL)

    @classmethod
    def init_static_locks(cls) -> None:
        cls._ensure_ffi_initialized()


def _verify_package_version(version: str) -> None:
    # Occasionally we run into situations where the version of the Python
    # package does not match the version of the shared object that is loaded.
    # This may occur in environments where multiple versions of cryptography
    # are installed and available in the python path. To avoid errors cropping
    # up later this code checks that the currently imported package and the
    # shared object that were loaded have the same version and raise an
    # ImportError if they do not
    so_package_version = _openssl.ffi.string(_openssl.lib.CRYPTOGRAPHY_PACKAGE_VERSION)
    if version.encode("ascii") != so_package_version:
        raise ImportError(
            "The version of cryptography does not match the loaded "
            "shared object. This can happen if you have multiple copies of "
            "cryptography installed in your Python path. Please try creating "
            "a new virtual environment to resolve this issue. "
            "Loaded python version: {}, shared object version: {}".format(
                version, so_package_version
            )
        )

    _openssl_assert(
        _openssl.lib,
        _openssl.lib.OpenSSL_version_num() == openssl.openssl_version(),
    )


_verify_package_version(cryptography.__version__)

Binding.init_static_locks()

if sys.platform == "win32" and os.environ.get("PROCESSOR_ARCHITEW6432") is not None:
    warnings.warn(
        "You are using cryptography on a 32-bit Python on a 64-bit Windows "
        "Operating System. Cryptography will be significantly faster if you "
        "switch to using a 64-bit Python.",
        UserWarning,
        stacklevel=2,
    )

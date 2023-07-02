# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import annotations

import typing


def cryptography_has_set_cert_cb() -> typing.List[str]:
    return [
        "SSL_CTX_set_cert_cb",
        "SSL_set_cert_cb",
    ]


def cryptography_has_ssl_st() -> typing.List[str]:
    return [
        "SSL_ST_BEFORE",
        "SSL_ST_OK",
        "SSL_ST_INIT",
        "SSL_ST_RENEGOTIATE",
    ]


def cryptography_has_tls_st() -> typing.List[str]:
    return [
        "TLS_ST_BEFORE",
        "TLS_ST_OK",
    ]


def cryptography_has_evp_pkey_dhx() -> typing.List[str]:
    return [
        "EVP_PKEY_DHX",
    ]


def cryptography_has_mem_functions() -> typing.List[str]:
    return [
        "Cryptography_CRYPTO_set_mem_functions",
    ]


def cryptography_has_x509_store_ctx_get_issuer() -> typing.List[str]:
    return [
        "X509_STORE_set_get_issuer",
    ]


def cryptography_has_ed448() -> typing.List[str]:
    return [
        "EVP_PKEY_ED448",
        "NID_ED448",
    ]


def cryptography_has_ed25519() -> typing.List[str]:
    return [
        "NID_ED25519",
        "EVP_PKEY_ED25519",
    ]


def cryptography_has_poly1305() -> typing.List[str]:
    return [
        "NID_poly1305",
        "EVP_PKEY_POLY1305",
    ]


def cryptography_has_evp_digestfinal_xof() -> typing.List[str]:
    return [
        "EVP_DigestFinalXOF",
    ]


def cryptography_has_fips() -> typing.List[str]:
    return [
        "FIPS_mode_set",
        "FIPS_mode",
    ]


def cryptography_has_ssl_sigalgs() -> typing.List[str]:
    return [
        "SSL_CTX_set1_sigalgs_list",
    ]


def cryptography_has_psk() -> typing.List[str]:
    return [
        "SSL_CTX_use_psk_identity_hint",
        "SSL_CTX_set_psk_server_callback",
        "SSL_CTX_set_psk_client_callback",
    ]


def cryptography_has_psk_tlsv13() -> typing.List[str]:
    return [
        "SSL_CTX_set_psk_find_session_callback",
        "SSL_CTX_set_psk_use_session_callback",
        "Cryptography_SSL_SESSION_new",
        "SSL_CIPHER_find",
        "SSL_SESSION_set1_master_key",
        "SSL_SESSION_set_cipher",
        "SSL_SESSION_set_protocol_version",
    ]


def cryptography_has_custom_ext() -> typing.List[str]:
    return [
        "SSL_CTX_add_client_custom_ext",
        "SSL_CTX_add_server_custom_ext",
        "SSL_extension_supported",
    ]


def cryptography_has_tlsv13_functions() -> typing.List[str]:
    return [
        "SSL_VERIFY_POST_HANDSHAKE",
        "SSL_CTX_set_ciphersuites",
        "SSL_verify_client_post_handshake",
        "SSL_CTX_set_post_handshake_auth",
        "SSL_set_post_handshake_auth",
        "SSL_SESSION_get_max_early_data",
        "SSL_write_early_data",
        "SSL_read_early_data",
        "SSL_CTX_set_max_early_data",
    ]


def cryptography_has_raw_key() -> typing.List[str]:
    return [
        "EVP_PKEY_new_raw_private_key",
        "EVP_PKEY_new_raw_public_key",
        "EVP_PKEY_get_raw_private_key",
        "EVP_PKEY_get_raw_public_key",
    ]


def cryptography_has_engine() -> typing.List[str]:
    return [
        "ENGINE_by_id",
        "ENGINE_init",
        "ENGINE_finish",
        "ENGINE_get_default_RAND",
        "ENGINE_set_default_RAND",
        "ENGINE_unregister_RAND",
        "ENGINE_ctrl_cmd",
        "ENGINE_free",
        "ENGINE_get_name",
        "ENGINE_ctrl_cmd_string",
        "ENGINE_load_builtin_engines",
        "ENGINE_load_private_key",
        "ENGINE_load_public_key",
        "SSL_CTX_set_client_cert_engine",
    ]


def cryptography_has_verified_chain() -> typing.List[str]:
    return [
        "SSL_get0_verified_chain",
    ]


def cryptography_has_srtp() -> typing.List[str]:
    return [
        "SSL_CTX_set_tlsext_use_srtp",
        "SSL_set_tlsext_use_srtp",
        "SSL_get_selected_srtp_profile",
    ]


def cryptography_has_providers() -> typing.List[str]:
    return [
        "OSSL_PROVIDER_load",
        "OSSL_PROVIDER_unload",
        "ERR_LIB_PROV",
        "PROV_R_WRONG_FINAL_BLOCK_LENGTH",
        "PROV_R_BAD_DECRYPT",
    ]


def cryptography_has_op_no_renegotiation() -> typing.List[str]:
    return [
        "SSL_OP_NO_RENEGOTIATION",
    ]


def cryptography_has_dtls_get_data_mtu() -> typing.List[str]:
    return [
        "DTLS_get_data_mtu",
    ]


def cryptography_has_300_fips() -> typing.List[str]:
    return [
        "EVP_default_properties_is_fips_enabled",
        "EVP_default_properties_enable_fips",
    ]


def cryptography_has_ssl_cookie() -> typing.List[str]:
    return [
        "SSL_OP_COOKIE_EXCHANGE",
        "DTLSv1_listen",
        "SSL_CTX_set_cookie_generate_cb",
        "SSL_CTX_set_cookie_verify_cb",
    ]


def cryptography_has_pkcs7_funcs() -> typing.List[str]:
    return [
        "SMIME_write_PKCS7",
        "PEM_write_bio_PKCS7_stream",
        "PKCS7_sign_add_signer",
        "PKCS7_final",
        "PKCS7_verify",
        "SMIME_read_PKCS7",
        "PKCS7_get0_signers",
    ]


def cryptography_has_bn_flags() -> typing.List[str]:
    return [
        "BN_FLG_CONSTTIME",
        "BN_set_flags",
        "BN_prime_checks_for_size",
    ]


def cryptography_has_evp_pkey_dh() -> typing.List[str]:
    return [
        "EVP_PKEY_set1_DH",
    ]


def cryptography_has_300_evp_cipher() -> typing.List[str]:
    return ["EVP_CIPHER_fetch", "EVP_CIPHER_free"]


def cryptography_has_unexpected_eof_while_reading() -> typing.List[str]:
    return ["SSL_R_UNEXPECTED_EOF_WHILE_READING"]


def cryptography_has_pkcs12_set_mac() -> typing.List[str]:
    return ["PKCS12_set_mac"]


def cryptography_has_ssl_op_ignore_unexpected_eof() -> typing.List[str]:
    return [
        "SSL_OP_IGNORE_UNEXPECTED_EOF",
    ]


def cryptography_has_get_extms_support() -> typing.List[str]:
    return ["SSL_get_extms_support"]


def cryptography_has_evp_pkey_set_peer_ex() -> typing.List[str]:
    return ["EVP_PKEY_derive_set_peer_ex"]


def cryptography_has_evp_aead() -> typing.List[str]:
    return [
        "EVP_aead_chacha20_poly1305",
        "EVP_AEAD_CTX_free",
        "EVP_AEAD_CTX_seal",
        "EVP_AEAD_CTX_open",
        "EVP_AEAD_max_overhead",
        "Cryptography_EVP_AEAD_CTX_new",
    ]


# This is a mapping of
# {condition: function-returning-names-dependent-on-that-condition} so we can
# loop over them and delete unsupported names at runtime. It will be removed
# when cffi supports #if in cdef. We use functions instead of just a dict of
# lists so we can use coverage to measure which are used.
CONDITIONAL_NAMES = {
    "Cryptography_HAS_SET_CERT_CB": cryptography_has_set_cert_cb,
    "Cryptography_HAS_SSL_ST": cryptography_has_ssl_st,
    "Cryptography_HAS_TLS_ST": cryptography_has_tls_st,
    "Cryptography_HAS_EVP_PKEY_DHX": cryptography_has_evp_pkey_dhx,
    "Cryptography_HAS_MEM_FUNCTIONS": cryptography_has_mem_functions,
    "Cryptography_HAS_X509_STORE_CTX_GET_ISSUER": (
        cryptography_has_x509_store_ctx_get_issuer
    ),
    "Cryptography_HAS_ED448": cryptography_has_ed448,
    "Cryptography_HAS_ED25519": cryptography_has_ed25519,
    "Cryptography_HAS_POLY1305": cryptography_has_poly1305,
    "Cryptography_HAS_FIPS": cryptography_has_fips,
    "Cryptography_HAS_SIGALGS": cryptography_has_ssl_sigalgs,
    "Cryptography_HAS_PSK": cryptography_has_psk,
    "Cryptography_HAS_PSK_TLSv1_3": cryptography_has_psk_tlsv13,
    "Cryptography_HAS_CUSTOM_EXT": cryptography_has_custom_ext,
    "Cryptography_HAS_TLSv1_3_FUNCTIONS": cryptography_has_tlsv13_functions,
    "Cryptography_HAS_RAW_KEY": cryptography_has_raw_key,
    "Cryptography_HAS_EVP_DIGESTFINAL_XOF": (cryptography_has_evp_digestfinal_xof),
    "Cryptography_HAS_ENGINE": cryptography_has_engine,
    "Cryptography_HAS_VERIFIED_CHAIN": cryptography_has_verified_chain,
    "Cryptography_HAS_SRTP": cryptography_has_srtp,
    "Cryptography_HAS_PROVIDERS": cryptography_has_providers,
    "Cryptography_HAS_OP_NO_RENEGOTIATION": (cryptography_has_op_no_renegotiation),
    "Cryptography_HAS_DTLS_GET_DATA_MTU": cryptography_has_dtls_get_data_mtu,
    "Cryptography_HAS_300_FIPS": cryptography_has_300_fips,
    "Cryptography_HAS_SSL_COOKIE": cryptography_has_ssl_cookie,
    "Cryptography_HAS_PKCS7_FUNCS": cryptography_has_pkcs7_funcs,
    "Cryptography_HAS_BN_FLAGS": cryptography_has_bn_flags,
    "Cryptography_HAS_EVP_PKEY_DH": cryptography_has_evp_pkey_dh,
    "Cryptography_HAS_300_EVP_CIPHER": cryptography_has_300_evp_cipher,
    "Cryptography_HAS_UNEXPECTED_EOF_WHILE_READING": (
        cryptography_has_unexpected_eof_while_reading
    ),
    "Cryptography_HAS_PKCS12_SET_MAC": cryptography_has_pkcs12_set_mac,
    "Cryptography_HAS_SSL_OP_IGNORE_UNEXPECTED_EOF": (
        cryptography_has_ssl_op_ignore_unexpected_eof
    ),
    "Cryptography_HAS_GET_EXTMS_SUPPORT": cryptography_has_get_extms_support,
    "Cryptography_HAS_EVP_PKEY_SET_PEER_EX": (cryptography_has_evp_pkey_set_peer_ex),
    "Cryptography_HAS_EVP_AEAD": (cryptography_has_evp_aead),
}

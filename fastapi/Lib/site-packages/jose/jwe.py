import binascii
import json
import zlib
from collections.abc import Mapping
from struct import pack

from . import jwk
from .backends import get_random_bytes
from .constants import ALGORITHMS, ZIPS
from .exceptions import JWEError, JWEParseError
from .utils import base64url_decode, base64url_encode, ensure_binary


def encrypt(
    plaintext,
    key,
    encryption=ALGORITHMS.A256GCM,
    algorithm=ALGORITHMS.DIR,
    zip=None,
    cty=None,
    kid=None,
):
    """Encrypts plaintext and returns a JWE cmpact serialization string.

    Args:
        plaintext (bytes): A bytes object to encrypt
        key (str or dict): The key(s) to use for encrypting the content. Can be
            individual JWK or JWK set.
        encryption (str, optional): The content encryption algorithm used to
            perform authenticated encryption on the plaintext to produce the
            ciphertext and the Authentication Tag.  Defaults to A256GCM.
        algorithm (str, optional): The cryptographic algorithm used
            to encrypt or determine the value of the CEK.  Defaults to dir.
        zip (str, optional): The compression algorithm) applied to the
            plaintext before encryption. Defaults to None.
        cty (str, optional): The media type for the secured content.
            See http://www.iana.org/assignments/media-types/media-types.xhtml
        kid (str, optional): Key ID for the provided key

    Returns:
        bytes: The string representation of the header, encrypted key,
            initialization vector, ciphertext, and authentication tag.

    Raises:
        JWEError: If there is an error signing the token.

    Examples:
        >>> from jose import jwe
        >>> jwe.encrypt('Hello, World!', 'asecret128bitkey', algorithm='dir', encryption='A128GCM')
        'eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4R0NNIn0..McILMB3dYsNJSuhcDzQshA.OfX9H_mcUpHDeRM4IA.CcnTWqaqxNsjT4eCaUABSg'

    """
    plaintext = ensure_binary(plaintext)  # Make sure it's bytes
    if algorithm not in ALGORITHMS.SUPPORTED:
        raise JWEError("Algorithm %s not supported." % algorithm)
    if encryption not in ALGORITHMS.SUPPORTED:
        raise JWEError("Algorithm %s not supported." % encryption)
    key = jwk.construct(key, algorithm)
    encoded_header = _encoded_header(algorithm, encryption, zip, cty, kid)

    plaintext = _compress(zip, plaintext)
    enc_cek, iv, cipher_text, auth_tag = _encrypt_and_auth(
        key, algorithm, encryption, zip, plaintext, encoded_header
    )

    jwe_string = _jwe_compact_serialize(
        encoded_header, enc_cek, iv, cipher_text, auth_tag
    )
    return jwe_string


def decrypt(jwe_str, key):
    """Decrypts a JWE compact serialized string and returns the plaintext.

    Args:
        jwe_str (str): A JWE to be decrypt.
        key (str or dict): A key to attempt to decrypt the payload with. Can be
            individual JWK or JWK set.

    Returns:
        bytes: The plaintext bytes, assuming the authentication tag is valid.

    Raises:
        JWEError: If there is an exception verifying the token.

    Examples:
        >>> from jose import jwe
        >>> jwe.decrypt(jwe_string, 'asecret128bitkey')
        'Hello, World!'
    """
    (
        header,
        encoded_header,
        encrypted_key,
        iv,
        cipher_text,
        auth_tag,
    ) = _jwe_compact_deserialize(jwe_str)

    # Verify that the implementation understands and can process all
    # fields that it is required to support, whether required by this
    # specification, by the algorithms being used, or by the "crit"
    # Header Parameter value, and that the values of those parameters
    # are also understood and supported.

    try:
        # Determine the Key Management Mode employed by the algorithm
        # specified by the "alg" (algorithm) Header Parameter.
        alg = header["alg"]
        enc = header["enc"]
        if alg not in ALGORITHMS.SUPPORTED:
            raise JWEError("Algorithm %s not supported." % alg)
        if enc not in ALGORITHMS.SUPPORTED:
            raise JWEError("Algorithm %s not supported." % enc)

    except KeyError:
        raise JWEParseError("alg and enc headers are required!")

    # Verify that the JWE uses a key known to the recipient.
    key = jwk.construct(key, alg)

    # When Direct Key Agreement or Key Agreement with Key Wrapping are
    # employed, use the key agreement algorithm to compute the value
    # of the agreed upon key.  When Direct Key Agreement is employed,
    # let the CEK be the agreed upon key.  When Key Agreement with Key
    # Wrapping is employed, the agreed upon key will be used to
    # decrypt the JWE Encrypted Key.
    #
    # When Key Wrapping, Key Encryption, or Key Agreement with Key
    # Wrapping are employed, decrypt the JWE Encrypted Key to produce
    # the CEK.  The CEK MUST have a length equal to that required for
    # the content encryption algorithm.  Note that when there are
    # multiple recipients, each recipient will only be able to decrypt
    # JWE Encrypted Key values that were encrypted to a key in that
    # recipient's possession.  It is therefore normal to only be able
    # to decrypt one of the per-recipient JWE Encrypted Key values to
    # obtain the CEK value.  Also, see Section 11.5 for security
    # considerations on mitigating timing attacks.
    if alg == ALGORITHMS.DIR:
        # When Direct Key Agreement or Direct Encryption are employed,
        # verify that the JWE Encrypted Key value is an empty octet
        # sequence.

        # Record whether the CEK could be successfully determined for this
        # recipient or not.
        cek_valid = encrypted_key == b""

        # When Direct Encryption is employed, let the CEK be the shared
        # symmetric key.
        cek_bytes = _get_key_bytes_from_key(key)
    else:
        try:
            cek_bytes = key.unwrap_key(encrypted_key)

            # Record whether the CEK could be successfully determined for this
            # recipient or not.
            cek_valid = True
        except NotImplementedError:
            raise JWEError(f"alg {alg} is not implemented")
        except Exception:
            # Record whether the CEK could be successfully determined for this
            # recipient or not.
            cek_valid = False

            # To mitigate the attacks described in RFC 3218 [RFC3218], the
            # recipient MUST NOT distinguish between format, padding, and length
            # errors of encrypted keys.  It is strongly recommended, in the event
            # of receiving an improperly formatted key, that the recipient
            # substitute a randomly generated CEK and proceed to the next step, to
            # mitigate timing attacks.
            cek_bytes = _get_random_cek_bytes_for_enc(enc)

    # Compute the Encoded Protected Header value BASE64URL(UTF8(JWE
    # Protected Header)).  If the JWE Protected Header is not present
    # (which can only happen when using the JWE JSON Serialization and
    # no "protected" member is present), let this value be the empty
    # string.
    protected_header = encoded_header

    # Let the Additional Authenticated Data encryption parameter be
    # ASCII(Encoded Protected Header).  However, if a JWE AAD value is
    # present (which can only be the case when using the JWE JSON
    # Serialization), instead let the Additional Authenticated Data
    # encryption parameter be ASCII(Encoded Protected Header || '.' ||
    # BASE64URL(JWE AAD)).
    aad = protected_header

    # Decrypt the JWE Ciphertext using the CEK, the JWE Initialization
    # Vector, the Additional Authenticated Data value, and the JWE
    # Authentication Tag (which is the Authentication Tag input to the
    # calculation) using the specified content encryption algorithm,
    # returning the decrypted plaintext and validating the JWE
    # Authentication Tag in the manner specified for the algorithm,
    # rejecting the input without emitting any decrypted output if the
    # JWE Authentication Tag is incorrect.
    try:
        plain_text = _decrypt_and_auth(cek_bytes, enc, cipher_text, iv, aad, auth_tag)
    except NotImplementedError:
        raise JWEError(f"enc {enc} is not implemented")
    except Exception as e:
        raise JWEError(e)

    # If a "zip" parameter was included, uncompress the decrypted
    # plaintext using the specified compression algorithm.
    if plain_text is not None:
        plain_text = _decompress(header.get("zip"), plain_text)

    return plain_text if cek_valid else None


def get_unverified_header(jwe_str):
    """Returns the decoded headers without verification of any kind.

    Args:
        jwe_str (str): A compact serialized JWE to decode the headers from.

    Returns:
        dict: The dict representation of the JWE headers.

    Raises:
        JWEError: If there is an exception decoding the JWE.
    """
    header = _jwe_compact_deserialize(jwe_str)[0]
    return header


def _decrypt_and_auth(cek_bytes, enc, cipher_text, iv, aad, auth_tag):
    """
    Decrypt and verify the data

    Args:
        cek_bytes (bytes): cek to derive encryption and possible auth key to
            verify the auth tag
        cipher_text (bytes): Encrypted data
        iv (bytes): Initialization vector (iv) used to encrypt data
        aad (bytes): Additional Authenticated Data used to verify the data
        auth_tag (bytes): Authentication ntag to verify the data

    Returns:
        (bytes): Decrypted data
    """
    # Decrypt the JWE Ciphertext using the CEK, the JWE Initialization
    # Vector, the Additional Authenticated Data value, and the JWE
    # Authentication Tag (which is the Authentication Tag input to the
    # calculation) using the specified content encryption algorithm,
    # returning the decrypted plaintext
    # and validating the JWE
    # Authentication Tag in the manner specified for the algorithm,
    if enc in ALGORITHMS.HMAC_AUTH_TAG:
        (
            encryption_key,
            mac_key,
            key_len,
        ) = _get_encryption_key_mac_key_and_key_length_from_cek(cek_bytes, enc)
        auth_tag_check = _auth_tag(cipher_text, iv, aad, mac_key, key_len)
    elif enc in ALGORITHMS.GCM:
        encryption_key = jwk.construct(cek_bytes, enc)
        auth_tag_check = auth_tag  # GCM check auth on decrypt
    else:
        raise NotImplementedError(f"enc {enc} is not implemented!")

    plaintext = encryption_key.decrypt(cipher_text, iv, aad, auth_tag)
    if auth_tag != auth_tag_check:
        raise JWEError("Invalid JWE Auth Tag")

    return plaintext


def _get_encryption_key_mac_key_and_key_length_from_cek(cek_bytes, enc):
    derived_key_len = len(cek_bytes) // 2
    mac_key_bytes = cek_bytes[0:derived_key_len]
    mac_key = _get_hmac_key(enc, mac_key_bytes)
    encryption_key_bytes = cek_bytes[-derived_key_len:]
    encryption_alg, _ = enc.split("-")
    encryption_key = jwk.construct(encryption_key_bytes, encryption_alg)
    return encryption_key, mac_key, derived_key_len


def _jwe_compact_deserialize(jwe_bytes):
    """
    Deserialize and verify the header and segments are appropriate.

    Args:
        jwe_bytes (bytes): The compact serialized JWE
    Returns:
        (dict, bytes, bytes, bytes, bytes, bytes)
    """

    # Base64url decode the encoded representations of the JWE
    # Protected Header, the JWE Encrypted Key, the JWE Initialization
    # Vector, the JWE Ciphertext, the JWE Authentication Tag, and the
    # JWE AAD, following the restriction that no line breaks,
    # whitespace, or other additional characters have been used.
    jwe_bytes = ensure_binary(jwe_bytes)
    try:
        (
            header_segment,
            encrypted_key_segment,
            iv_segment,
            cipher_text_segment,
            auth_tag_segment,
        ) = jwe_bytes.split(b".", 4)
        header_data = base64url_decode(header_segment)
    except ValueError:
        raise JWEParseError("Not enough segments")
    except (TypeError, binascii.Error):
        raise JWEParseError("Invalid header")

    # Verify that the octet sequence resulting from decoding the
    # encoded JWE Protected Header is a UTF-8-encoded representation
    # of a completely valid JSON object conforming to RFC 7159
    # [RFC7159]; let the JWE Protected Header be this JSON object.
    #
    # If using the JWE Compact Serialization, let the JOSE Header be
    # the JWE Protected Header.  Otherwise, when using the JWE JSON
    # Serialization, let the JOSE Header be the union of the members
    # of the JWE Protected Header, the JWE Shared Unprotected Header
    # and the corresponding JWE Per-Recipient Unprotected Header, all
    # of which must be completely valid JSON objects.  During this
    # step, verify that the resulting JOSE Header does not contain
    # duplicate Header Parameter names.  When using the JWE JSON
    # Serialization, this restriction includes that the same Header
    # Parameter name also MUST NOT occur in distinct JSON object
    # values that together comprise the JOSE Header.

    try:
        header = json.loads(header_data)
    except ValueError as e:
        raise JWEParseError(f"Invalid header string: {e}")

    if not isinstance(header, Mapping):
        raise JWEParseError("Invalid header string: must be a json object")

    try:
        encrypted_key = base64url_decode(encrypted_key_segment)
    except (TypeError, binascii.Error):
        raise JWEParseError("Invalid encrypted key")

    try:
        iv = base64url_decode(iv_segment)
    except (TypeError, binascii.Error):
        raise JWEParseError("Invalid IV")

    try:
        ciphertext = base64url_decode(cipher_text_segment)
    except (TypeError, binascii.Error):
        raise JWEParseError("Invalid cyphertext")

    try:
        auth_tag = base64url_decode(auth_tag_segment)
    except (TypeError, binascii.Error):
        raise JWEParseError("Invalid auth tag")

    return header, header_segment, encrypted_key, iv, ciphertext, auth_tag


def _encoded_header(alg, enc, zip, cty, kid):
    """
    Generate an appropriate JOSE header based on the values provided
    Args:
        alg (str): Key wrap/negotiation algorithm
        enc (str): Encryption algorithm
        zip (str): Compression method
        cty (str): Content type of the encrypted data
        kid (str): ID for the key used for the operation

    Returns:
        bytes: JSON object of header based on input
    """
    header = {"alg": alg, "enc": enc}
    if zip:
        header["zip"] = zip
    if cty:
        header["cty"] = cty
    if kid:
        header["kid"] = kid
    json_header = json.dumps(
        header,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return base64url_encode(json_header)


def _big_endian(int_val):
    return pack("!Q", int_val)


def _encrypt_and_auth(key, alg, enc, zip, plaintext, aad):
    """
    Generate a content encryption key (cek) and initialization
    vector (iv) based on enc and alg, compress the plaintext based on zip,
    encrypt the compressed plaintext using the cek and iv based on enc

    Args:
        key (Key): The key provided for encryption
        alg (str): The algorithm use for key wrap/negotiation
        enc (str): The encryption algorithm with which to encrypt the plaintext
        zip (str): The compression algorithm with which to compress the plaintext
        plaintext (bytes): The data to encrypt
        aad (str): Additional authentication data utilized for generating an
                    auth tag

    Returns:
          (bytes, bytes, bytes, bytes): A tuple of the following data
                                 (key wrapped cek, iv, cipher text, auth tag)
    """
    try:
        cek_bytes, kw_cek = _get_cek(enc, alg, key)
    except NotImplementedError:
        raise JWEError(f"alg {alg} is not implemented")

    if enc in ALGORITHMS.HMAC_AUTH_TAG:
        (
            encryption_key,
            mac_key,
            key_len,
        ) = _get_encryption_key_mac_key_and_key_length_from_cek(cek_bytes, enc)
        iv, ciphertext, tag = encryption_key.encrypt(plaintext, aad)
        auth_tag = _auth_tag(ciphertext, iv, aad, mac_key, key_len)
    elif enc in ALGORITHMS.GCM:
        encryption_key = jwk.construct(cek_bytes, enc)
        iv, ciphertext, auth_tag = encryption_key.encrypt(plaintext, aad)
    else:
        raise NotImplementedError(f"enc {enc} is not implemented!")

    return kw_cek, iv, ciphertext, auth_tag


def _get_hmac_key(enc, mac_key_bytes):
    """
    Get an HMACKey for the provided encryption algorithm and key bytes

    Args:
        enc (str): Encryption algorithm
        mac_key_bytes (bytes): vytes for the HMAC key

    Returns:
         (HMACKey): The key to perform HMAC actions
    """
    _, hash_alg = enc.split("-")
    mac_key = jwk.construct(mac_key_bytes, hash_alg)
    return mac_key


def _compress(zip, plaintext):
    """
    Compress the plaintext based on the algorithm supplied

    Args:
        zip (str): Compression Algorithm
        plaintext (bytes): plaintext to compress

    Returns:
        (bytes): Compressed plaintext
    """
    if zip not in ZIPS.SUPPORTED:
        raise NotImplementedError("ZIP {} is not supported!")
    if zip is None:
        compressed = plaintext
    elif zip == ZIPS.DEF:
        compressed = zlib.compress(plaintext)
    else:
        raise NotImplementedError("ZIP {} is not implemented!")
    return compressed


def _decompress(zip, compressed):
    """
    Decompress the plaintext based on the algorithm supplied

    Args:
        zip (str): Compression Algorithm
        plaintext (bytes): plaintext to decompress

    Returns:
        (bytes): Compressed plaintext
    """
    if zip not in ZIPS.SUPPORTED:
        raise NotImplementedError("ZIP {} is not supported!")
    if zip is None:
        decompressed = compressed
    elif zip == ZIPS.DEF:
        decompressed = zlib.decompress(compressed)
    else:
        raise NotImplementedError("ZIP {} is not implemented!")
    return decompressed


def _get_cek(enc, alg, key):
    """
    Get the content encryption key

    Args:
        enc (str): Encryption algorithm
        alg (str): kwy wrap/negotiation algorithm
        key (Key): Key provided to encryption method

    Return:
        (bytes, bytes): Tuple of (cek bytes and wrapped cek)
    """
    if alg == ALGORITHMS.DIR:
        cek, wrapped_cek = _get_direct_key_wrap_cek(key)
    else:
        cek, wrapped_cek = _get_key_wrap_cek(enc, key)

    return cek, wrapped_cek


def _get_direct_key_wrap_cek(key):
    """
    Get the cek and wrapped cek from the encryption key direct

    Args:
        key (Key): Key provided to encryption method

    Return:
        (Key, bytes): Tuple of (cek Key object and wrapped cek)
    """
    # Get the JWK data to determine how to derive the cek
    jwk_data = key.to_dict()
    if jwk_data["kty"] == "oct":
        # Get the last half of an octal key as the cek
        cek_bytes = _get_key_bytes_from_key(key)
        wrapped_cek = b""
    else:
        raise NotImplementedError("JWK type {} not supported!".format(jwk_data["kty"]))
    return cek_bytes, wrapped_cek


def _get_key_bytes_from_key(key):
    """
    Get the raw key bytes from a Key object

    Args:
        key (Key): Key from which to extract the raw key bytes
    Returns:
        (bytes) key data
    """
    jwk_data = key.to_dict()
    encoded_key = jwk_data["k"]
    cek_bytes = base64url_decode(encoded_key)
    return cek_bytes


def _get_key_wrap_cek(enc, key):
    """_get_rsa_key_wrap_cek
    Get the content encryption key for RSA key wrap

    Args:
        enc (str): Encryption algorithm
        key (Key): Key provided to encryption method

    Returns:
        (Key, bytes): Tuple of (cek Key object and wrapped cek)
    """
    cek_bytes = _get_random_cek_bytes_for_enc(enc)
    wrapped_cek = key.wrap_key(cek_bytes)
    return cek_bytes, wrapped_cek


def _get_random_cek_bytes_for_enc(enc):
    """
    Get the random cek bytes based on the encryptionn algorithm

    Args:
        enc (str): Encryption algorithm

    Returns:
        (bytes) random bytes for cek key
    """
    if enc == ALGORITHMS.A128GCM:
        num_bits = 128
    elif enc == ALGORITHMS.A192GCM:
        num_bits = 192
    elif enc in (ALGORITHMS.A128CBC_HS256, ALGORITHMS.A256GCM):
        num_bits = 256
    elif enc == ALGORITHMS.A192CBC_HS384:
        num_bits = 384
    elif enc == ALGORITHMS.A256CBC_HS512:
        num_bits = 512
    else:
        raise NotImplementedError(f"{enc} not supported")
    cek_bytes = get_random_bytes(num_bits // 8)
    return cek_bytes


def _auth_tag(ciphertext, iv, aad, mac_key, tag_length):
    """
    Get ann auth tag from the provided data

    Args:
        ciphertext (bytes): Encrypted value
        iv (bytes): Initialization vector
        aad (bytes): Additional Authenticated Data
        mac_key (bytes): Key to use in generating the MAC
        tag_length (int): How log the tag should be

    Returns:
        (bytes) Auth tag
    """
    al = _big_endian(len(aad) * 8)
    auth_tag_input = aad + iv + ciphertext + al
    signature = mac_key.sign(auth_tag_input)
    auth_tag = signature[0:tag_length]
    return auth_tag


def _jwe_compact_serialize(encoded_header, encrypted_cek, iv, cipher_text, auth_tag):
    """
    Generate a compact serialized JWE

    Args:
        encoded_header (bytes): Base64 URL Encoded JWE header JSON
        encrypted_cek (bytes): Encrypted content encryption key (cek)
        iv (bytes): Initialization vector (IV)
        cipher_text (bytes): Cipher text
        auth_tag (bytes): JWE Auth Tag

    Returns:
        (str): JWE compact serialized string
    """
    cipher_text = ensure_binary(cipher_text)
    encoded_encrypted_cek = base64url_encode(encrypted_cek)
    encoded_iv = base64url_encode(iv)
    encoded_cipher_text = base64url_encode(cipher_text)
    encoded_auth_tag = base64url_encode(auth_tag)
    return (
        encoded_header
        + b"."
        + encoded_encrypted_cek
        + b"."
        + encoded_iv
        + b"."
        + encoded_cipher_text
        + b"."
        + encoded_auth_tag
    )

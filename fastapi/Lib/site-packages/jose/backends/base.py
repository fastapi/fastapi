from ..utils import base64url_encode, ensure_binary


class Key:
    """
    A simple interface for implementing JWK keys.
    """

    def __init__(self, key, algorithm):
        pass

    def sign(self, msg):
        raise NotImplementedError()

    def verify(self, msg, sig):
        raise NotImplementedError()

    def public_key(self):
        raise NotImplementedError()

    def to_pem(self):
        raise NotImplementedError()

    def to_dict(self):
        raise NotImplementedError()

    def encrypt(self, plain_text, aad=None):
        """
        Encrypt the plain text and generate an auth tag if appropriate

        Args:
            plain_text (bytes): Data to encrypt
            aad (bytes, optional): Authenticated Additional Data if key's algorithm supports auth mode

        Returns:
            (bytes, bytes, bytes): IV, cipher text, and auth tag
        """
        raise NotImplementedError()

    def decrypt(self, cipher_text, iv=None, aad=None, tag=None):
        """
        Decrypt the cipher text and validate the auth tag if present
        Args:
            cipher_text (bytes): Cipher text to decrypt
            iv (bytes): IV if block mode
            aad (bytes): Additional Authenticated Data to verify if auth mode
            tag (bytes): Authentication tag if auth mode

        Returns:
            bytes: Decrypted value
        """
        raise NotImplementedError()

    def wrap_key(self, key_data):
        """
        Wrap the the plain text key data

        Args:
            key_data (bytes): Key data to wrap

        Returns:
            bytes: Wrapped key
        """
        raise NotImplementedError()

    def unwrap_key(self, wrapped_key):
        """
        Unwrap the the wrapped key data

        Args:
            wrapped_key (bytes): Wrapped key data to unwrap

        Returns:
            bytes: Unwrapped key
        """
        raise NotImplementedError()


class DIRKey(Key):
    def __init__(self, key_data, algorithm):
        self._key = ensure_binary(key_data)
        self._alg = algorithm

    def to_dict(self):
        return {
            "alg": self._alg,
            "kty": "oct",
            "k": base64url_encode(self._key),
        }

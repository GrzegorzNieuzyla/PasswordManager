from password_manager.encryption.key_derivator import KeyDerivator
from password_manager.models.encryption_metadata import EncryptionMetadata


def test_derive():
    metadata = EncryptionMetadata()
    metadata.hmac = 'SHA512'
    metadata.salt = b'2' * 16
    metadata.key_len = 64
    metadata.iterations = 10
    key = KeyDerivator("password", metadata).derive()
    assert len(key) == 64

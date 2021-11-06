from secrets import token_bytes

from password_manager.encryption.key_derivator import KeyDerivator
from password_manager.models.encryption_metadata import EncryptionMetadata
from typing import Tuple


class KeyGenerator:
    def __init__(self, passphrase: str):
        self.passphrase: str = passphrase

    def generate(self) -> Tuple[bytes, EncryptionMetadata]:
        metadata: EncryptionMetadata = self._create_metadata()
        key: bytes = KeyDerivator(self.passphrase, metadata).derive()
        return key, metadata

    @staticmethod
    def _create_metadata() -> EncryptionMetadata:
        salt: bytes = token_bytes(16)
        return EncryptionMetadata(salt=salt, iterations=10 ** 6, hmac='SHA512', key_len=32)

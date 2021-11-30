from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2

from password_manager.models.encryption_metadata import EncryptionMetadata


class KeyDerivator:
    def __init__(self, passphrase: str, metadata: EncryptionMetadata):
        self.passphrase: str = passphrase
        self.metadata: EncryptionMetadata = metadata

    def derive(self) -> bytes:
        """
        Derive key from password and encryption options
        """
        if self.metadata.hmac == 'SHA512':
            module = SHA512
        else:
            raise AttributeError(f'HMAC {self.metadata.hmac} is not supported')

        return PBKDF2(self.passphrase, self.metadata.salt, self.metadata.key_len,
                      count=self.metadata.iterations, hmac_hash_module=module)

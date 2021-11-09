from secrets import token_bytes
from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from password_manager.repositories.record import RecordRepository


class EncryptedRecordWriter:
    def __init__(self, repository: RecordRepository, key: bytes):
        self.repository: RecordRepository = repository
        self.key: bytes = key

    def add(self, data: bytes) -> int:
        ciphertext, iv = self._encrypt(data)
        return self.repository.add(json_data=ciphertext, iv=iv)

    def update(self, id_: int, data: bytes) -> None:
        ciphertext, iv = self._encrypt(data)
        self.repository.update(id_, iv, ciphertext)

    def delete(self, id_: int) -> None:
        self.repository.delete(id_)

    def _encrypt(self, data: bytes) -> Tuple[bytes, bytes]:
        iv: bytes = token_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        ciphertext: bytes = cipher.encrypt(pad(data, block_size=AES.block_size))
        return ciphertext, iv

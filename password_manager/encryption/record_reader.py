from typing import Dict, List

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from password_manager.models.record import Record
from password_manager.repositories.record import RecordRepository


class EncryptedRecordReader:
    def __init__(self, repository: RecordRepository, key: bytes):
        self.repository: RecordRepository = repository
        self.key: bytes = key

    def get_all(self) -> Dict[int, bytes]:
        """
        Decrypt all records and return them
        """
        records: List[Record] = self.repository.get_all()
        return {record.id: self._decrypt(record.json_record_data, record.aes_iv) for record in records}

    def _decrypt(self, data: bytes, iv: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        plaintext: bytes = unpad(cipher.decrypt(data), block_size=AES.block_size)
        return plaintext

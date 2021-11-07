from typing import Optional

from password_manager.database_manager import DatabaseManager
from password_manager.encryption.record_reader import EncryptedRecordReader
from password_manager.encryption.record_writer import EncryptedRecordWriter
from password_manager.repositories.encryption_metadata import EncryptionMetadataRepository


class ApplicationContext:
    def __init__(self):
        self.database_manager: Optional[DatabaseManager] = None
        self.metadata_repository: Optional[EncryptionMetadataRepository] = None
        self.data_writer: Optional[EncryptedRecordWriter] = None
        self.data_reader: Optional[EncryptedRecordReader] = None


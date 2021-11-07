from typing import Optional

from password_manager.controllers.create_database import CreateDatabaseController
from password_manager.controllers.login import LoginController
from password_manager.database_manager import DatabaseManager
from password_manager.encryption.record_reader import EncryptedRecordReader
from password_manager.encryption.record_writer import EncryptedRecordWriter
from password_manager.logger import Logger
from password_manager.repositories.encryption_metadata import EncryptionMetadataRepository
from password_manager.repositories.record import RecordRepository


class ApplicationContext:
    def __init__(self):
        self.database_manager: Optional[DatabaseManager] = None
        self.metadata_repository: Optional[EncryptionMetadataRepository] = None
        self.data_writer: Optional[EncryptedRecordWriter] = None
        self.data_reader: Optional[EncryptedRecordReader] = None
        self.create_database_controller: CreateDatabaseController = CreateDatabaseController(self)
        self.login_controller: LoginController = LoginController(self)

    def initialize_data_access(self, key: bytes):
        if self.database_manager is None:
            raise ValueError("Database manager is not initialized")
        self.data_writer = EncryptedRecordWriter(RecordRepository(self.database_manager), key)
        self.data_reader = EncryptedRecordReader(RecordRepository(self.database_manager), key)

    def initialize_database(self, db_path: str):
        self.database_manager = DatabaseManager(db_path)
        self.metadata_repository = EncryptionMetadataRepository(self.database_manager)
        Logger.info(f"Switched to database file {db_path}")

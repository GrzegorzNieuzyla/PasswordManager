from typing import Optional

from password_manager.database_manager import DatabaseManager
from password_manager.encryption.record_reader import EncryptedRecordReader
from password_manager.encryption.record_writer import EncryptedRecordWriter
from password_manager.integration.controller import IntegrationController
from password_manager.repositories.encryption_metadata import EncryptionMetadataRepository
from password_manager.repositories.record import RecordRepository
from password_manager.utils.logger import Logger
from password_manager.utils.options import get_generation_options
from password_manager.utils.password_generator import GenerationOptions


class ApplicationContext:
    """
    Class holding references to all required objects that need to be retrieved at runtime
    """

    def __init__(self) -> None:
        # avoid circular imports
        from password_manager.controllers.create_database import CreateDatabaseController
        from password_manager.controllers.login import LoginController
        from password_manager.controllers.main_window import MainWindowController

        self.database_manager: Optional[DatabaseManager] = None
        self.metadata_repository: Optional[EncryptionMetadataRepository] = None
        self.data_writer: Optional[EncryptedRecordWriter] = None
        self.data_reader: Optional[EncryptedRecordReader] = None
        self.integration_controller: Optional[IntegrationController] = None
        self.create_database_controller: CreateDatabaseController = CreateDatabaseController(self)
        self.login_controller: LoginController = LoginController(self)
        self.main_window_controller: MainWindowController = MainWindowController(self)
        self.password_generation_options: GenerationOptions = get_generation_options()
        self.run_server = True

    def initialize_data_access(self, key: bytes) -> None:
        """
        Initialize objects for data encryption and decryption
        """
        if self.database_manager is None:
            raise ValueError("Database manager is not initialized")
        self.data_writer = EncryptedRecordWriter(RecordRepository(self.database_manager), key)
        self.data_reader = EncryptedRecordReader(RecordRepository(self.database_manager), key)

    def initialize_database(self, db_path: str) -> None:
        """
        Initialize database from filename
        """
        self.database_manager = DatabaseManager(db_path)
        self.metadata_repository = EncryptionMetadataRepository(self.database_manager)
        Logger.info(f"Switched to database file {db_path}")

    def get_data_writer(self) -> EncryptedRecordWriter:
        if self.data_writer is None:
            raise ValueError("Data writer is not initialized")
        return self.data_writer

    def get_data_reader(self) -> EncryptedRecordReader:
        if self.data_reader is None:
            raise ValueError("Data reader is not initialized")
        return self.data_reader

    def get_metadata_repository(self) -> EncryptionMetadataRepository:
        if self.metadata_repository is None:
            raise ValueError("Metadata repository is not initialized")
        return self.metadata_repository

    def get_database_manager(self) -> DatabaseManager:
        if self.database_manager is None:
            raise ValueError("Database manager is not initialized")
        return self.database_manager

    def get_integration_controller(self) -> 'IntegrationController':
        if self.integration_controller is None:
            raise ValueError("Integration controller is not initialized")
        return self.integration_controller

    def initialize_integration_server(self, key_file: str, cert_file: str, port: int) -> None:
        self.integration_controller = IntegrationController(key_file, cert_file, port)

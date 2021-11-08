from password_manager.database_manager import DatabaseManager
from password_manager.models.encryption_metadata import EncryptionMetadata


class EncryptionMetadataRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add_or_update(self, salt: bytes, iterations: int, hmac: str, key_len: int) -> None:
        with self.db_manager.create_session() as session:
            metadata: EncryptionMetadata = session.query(EncryptionMetadata).first()
            if metadata is None:
                metadata = EncryptionMetadata(salt=salt, iterations=iterations, hmac=hmac, key_len=key_len)
                session.add(metadata)
            else:
                metadata.salt = salt
                metadata.iterations = iterations
                metadata.hmac = hmac
                metadata.key_len = key_len
            session.commit()

    def get(self) -> EncryptionMetadata:
        with self.db_manager.create_session() as session:
            return session.query(EncryptionMetadata).first()

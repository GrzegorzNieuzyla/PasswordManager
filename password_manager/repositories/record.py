from typing import List

from password_manager.database_manager import DatabaseManager
from password_manager.models.record import Record


class RecordRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add(self, iv: bytes, json_data: bytes) -> int:
        """
        Add new encrypted record to database
        """
        with self.db_manager.create_session() as session:
            record = Record(aes_iv=iv, json_record_data=json_data)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def update(self, id_: int, iv: bytes, json_data: bytes) -> None:
        """
        Update given encrypted record
        """
        with self.db_manager.create_session() as session:
            record = session.query(Record).get(id_)
            record.aes_iv = iv
            record.json_record_data = json_data
            session.commit()

    def delete(self, id_: int) -> None:
        """
        Delete given record
        """
        with self.db_manager.create_session() as session:
            record = session.query(Record).get(id_)
            session.delete(record)
            session.commit()

    def get_all(self) -> List[Record]:
        """
        Retrieve all encrypted records
        """
        with self.db_manager.create_session() as session:
            return session.query(Record).all()

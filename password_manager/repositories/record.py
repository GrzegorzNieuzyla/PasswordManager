from password_manager.database_manager import DatabaseManager
from password_manager.models.record import Record
from typing import List


class RecordRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add(self, record: Record):
        with self.db_manager.create_session() as session:
            session.add(record)
            session.commit()

    def update(self, id_: int, iv: bytes, json_data: bytes):
        with self.db_manager.create_session() as session:
            record = session.query(Record).get(id_)
            record.aes_iv = iv
            record.json_record_data = json_data
            session.commit()

    def get_all(self) -> List[Record]:
        with self.db_manager.create_session() as session:
            return session.query(Record).all()

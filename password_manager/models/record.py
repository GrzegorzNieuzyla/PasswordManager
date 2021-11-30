from sqlalchemy import Column, Integer, BLOB

from password_manager.database_manager import ModelBase


class Record(ModelBase):
    """
    Database object containing encrypted JSON record
    """
    __tablename__ = 'RECORDS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    aes_iv = Column(BLOB, nullable=False, unique=True)
    json_record_data = Column(BLOB, nullable=False)

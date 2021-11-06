from sqlalchemy import Column, Integer, BLOB, String
from password_manager.models import ModelBase


class EncryptionMetadata(ModelBase):
    __tablename__ = 'ENCRYPTION_METADATA'
    salt = Column(BLOB, nullable=False, primary_key=True)
    iterations = Column(Integer, nullable=False)
    hmac = Column(String, nullable=False)
    key_len = Column(Integer, nullable=False)

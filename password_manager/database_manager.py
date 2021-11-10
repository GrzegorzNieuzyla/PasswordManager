from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from password_manager.models import ModelBase


class DatabaseManager:
    def __init__(self, db_path: str):
        self.path: str = db_path
        self.engine = create_engine(URL.create('sqlite', database=db_path), echo=False)
        ModelBase.metadata.create_all(bind=self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def create_session(self) -> Session:
        return self.session_factory()

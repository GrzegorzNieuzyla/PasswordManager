import json
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class RecordData:
    title: str
    website: str
    loginUrl: str
    login: str
    password: str
    description: str
    modificationDate: int

    def get_modification_date(self) -> datetime:
        return datetime.fromtimestamp(self.modificationDate)

    def serialize(self) -> bytes:
        return json.dumps(asdict(self)).encode()

    @staticmethod
    def deserialize(data: bytes) -> 'RecordData':
        return RecordData(**json.loads(data.decode()))

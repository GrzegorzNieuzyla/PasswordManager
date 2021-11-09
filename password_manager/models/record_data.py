import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class RecordData:
    id_: int
    title: str
    website: str
    loginUrl: str
    login: str
    password: str
    description: str
    modificationDate: int

    def get_modification_date(self) -> datetime:
        return datetime.fromtimestamp(self.modificationDate)

    def get_days_from_modification(self) -> int:
        date = self.get_modification_date()
        today = datetime.today()
        return (today - date).days

    def serialize(self) -> bytes:
        raw_record = dataclasses.asdict(self)
        del raw_record['id_']
        return json.dumps(raw_record).encode()

    @staticmethod
    def deserialize(data: bytes, id_: int) -> 'RecordData':
        return RecordData(**json.loads(data.decode()), id_=id_)

    @staticmethod
    def deserialize_all(records: Dict[int, bytes]) -> Dict[int, 'RecordData']:
        return {key: RecordData.deserialize(data, key) for key, data in records.items()}

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
        """
        Convert timestamp to DataTime object
        """
        return datetime.fromtimestamp(self.modificationDate)

    def get_days_from_modification(self) -> int:
        date = self.get_modification_date()
        today = datetime.today()
        return (today - date).days

    def serialize(self) -> bytes:
        """
        Serialize record to bytes, remove code-only `id_` field
        """
        raw_record = dataclasses.asdict(self)
        del raw_record['id_']
        return json.dumps(raw_record).encode()

    @staticmethod
    def deserialize(data: bytes, id_: int) -> 'RecordData':
        """
        Create record from bytes, add code-only 'id_' field
        """
        return RecordData(**json.loads(data.decode()), id_=id_)

    @staticmethod
    def deserialize_all(records: Dict[int, bytes]) -> Dict[int, 'RecordData']:
        """
        Get list of records from serialized JSON
        """
        return {key: RecordData.deserialize(data, key) for key, data in records.items()}

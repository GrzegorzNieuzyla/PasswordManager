import dataclasses
import json
from typing import Dict

from password_manager.models.record_data import RecordData


class RecordSerializer:
    @staticmethod
    def serialize(record: RecordData) -> bytes:
        return json.dumps(dataclasses.asdict(record)).encode()

    @staticmethod
    def deserialize(data: bytes):
        return RecordData(**json.loads(data.decode()))

    @staticmethod
    def deserialize_all(records: Dict[int, bytes]) -> Dict[int, RecordData]:
        return {key: RecordSerializer.deserialize(data) for key, data in records.items()}

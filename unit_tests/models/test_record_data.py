import dataclasses
import json
from datetime import datetime

from password_manager.models.record_data import RecordData


def test_get_days_from_modification():
    record = RecordData(0, '', '', '', '', '', '', 222222222)
    assert record.get_days_from_modification() == (datetime.today() - datetime.fromtimestamp(222222222)).days


def test_serialize():
    record = RecordData(0, 'a', 'b', 'c', 'd', 'e', 'f', 222222222)
    expected = {
        'title': 'a',
        'website': 'b',
        'loginUrl': 'c',
        'login': 'd',
        'password': 'e',
        'description': 'f',
        'modificationDate': 222222222
    }
    assert json.dumps(expected).encode() == record.serialize()


def test_deserialize():
    expected = {
        'title': 'a',
        'website': 'b',
        'loginUrl': 'c',
        'login': 'd',
        'password': 'e',
        'description': 'f',
        'modificationDate': 222222222
    }
    assert dataclasses.asdict(RecordData.deserialize(json.dumps(expected).encode(), 2)) == {**expected, 'id_': 2}

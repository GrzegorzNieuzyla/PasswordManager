from pytest_mock import MockerFixture

from password_manager.encryption.record_reader import EncryptedRecordReader
from password_manager.encryption.record_writer import EncryptedRecordWriter
from password_manager.models.record import Record


def test_e2e_encryption(mocker: MockerFixture):
    import os
    x = os.getcwd()
    repository = mocker.MagicMock()
    enc_data = {}

    def add_mock(iv, json_data, result=enc_data):
        result['iv'] = iv
        result['data'] = json_data
        return 2

    repository.add = add_mock
    plaintext = "An unencrypted message"
    key = b'1234' * 8
    writer = EncryptedRecordWriter(repository, key)
    assert writer.add(plaintext.encode()) == 2

    def get_all_mock():
        record = Record()
        record.aes_iv = enc_data['iv']
        record.json_record_data = enc_data['data']
        record.id = 2
        return [record]

    repository.get_all = get_all_mock

    reader = EncryptedRecordReader(repository, key)
    decrypted = reader.get_all()[2]
    assert decrypted.decode() == plaintext

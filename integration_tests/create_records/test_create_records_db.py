from integration_tests.fixture import IntegrationServerFixture
from password_manager.models.record_data import RecordData


def test_create_records_compare_with_database():
    with IntegrationServerFixture() as fixture:
        fixture.run_integration_server(22223, 'test.pmdb', 'password')
        login = 'xxxx'
        response = fixture.make_request(
            f"https://localhost:22223/v1/api/createpassword?url=www.google.com&login={login}")

        assert response.status_code == 200
        json = response.json()
        assert 'password' in json
        password = json['password']
        raw_records = fixture.context.data_reader.get_all()
        records = RecordData.deserialize_all(raw_records)
        assert len(records) == 1
        record = list(records.values())[0]
        assert record.password == password
        assert record.login == login

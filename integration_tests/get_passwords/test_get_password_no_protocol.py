import json
from urllib.parse import quote_plus

from integration_tests.utils import IntegrationServerFixture
from password_manager.models.record_data import RecordData


def test_get_password_for_website_without_protocol_in_url():
    with IntegrationServerFixture() as fixture:
        fixture.run_integration_server(22245, 'test.db', 'password')
        record = RecordData(1, "", "", "website.com", "login1", "password1", "", 0)
        record2 = RecordData(2, "", "website.com", "", "login2", "password2", "", 0)
        fixture.context.data_writer.add(record.serialize())
        fixture.context.data_writer.add(record2.serialize())
        fixture.context.main_window_controller.try_load_data()

        response = fixture.make_request(
            f"https://localhost:22245/v1/api/password?url={quote_plus('https://' + record.loginUrl)}")
        assert response.status_code == 200

        json_data = json.loads(response.text)
        assert len(json_data) == 2
        data = json_data[0]
        assert 'login' in data
        assert 'password' in data
        assert data['password'] == record.password
        assert data['login'] == record.login

        data = json_data[1]
        assert 'login' in data
        assert 'password' in data
        assert data['password'] == record2.password
        assert data['login'] == record2.login

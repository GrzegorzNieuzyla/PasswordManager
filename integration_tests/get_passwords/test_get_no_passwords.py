import json

from integration_tests.fixture import IntegrationServerFixture
from password_manager.models.record_data import RecordData


def test_get_no_password():
    with IntegrationServerFixture() as fixture:
        fixture.run_integration_server(22243, 'test.pmdb', 'password')
        record = RecordData(1, "", "", "https://website.com", "login1", "password1", "", 0)
        fixture.context.data_writer.add(record.serialize())
        fixture.context.main_window_controller.try_load_data()

        response = fixture.make_request(f"https://localhost:22243/v1/api/password?url=https://notexisting.com")
        assert response.status_code == 200

        data = json.loads(response.text)
        assert len(data) == 0

from integration_tests.utils import IntegrationServerFixture
from password_manager.models.record_data import RecordData


def test_get_sites():
    with IntegrationServerFixture() as fixture:
        fixture.run_integration_server(22233, 'test.db', 'password')
        record1 = RecordData(1, "", "", "https://website1.com", "", "", "", 0)
        record2 = RecordData(2, "", "", "https://website2.com", "", "", "", 0)
        fixture.context.data_writer.add(record1.serialize())
        fixture.context.data_writer.add(record2.serialize())
        fixture.context.main_window_controller.try_load_data()

        response = fixture.make_request("https://localhost:22233/v1/api/sites")

        assert response.status_code == 200
        json = response.json()
        assert len(json) == 2
        assert json[0] == record1.loginUrl
        assert json[1] == record2.loginUrl

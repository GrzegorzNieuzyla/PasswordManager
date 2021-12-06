from string import ascii_lowercase

from integration_tests.fixture import IntegrationServerFixture
from password_manager.utils.password_generator import GenerationOptions


def test_create_records_password_options():
    with IntegrationServerFixture() as fixture:
        fixture.run_integration_server(22264, 'test.pmdb', 'password')
        fixture.context.password_generation_options = GenerationOptions(False, False, False, True, "", 70)
        login = 'zxcv'
        response = fixture.make_request(
            f"https://localhost:22264/v1/api/createpassword?url=www.google.com&login={login}")

        assert response.status_code == 200
        json = response.json()
        assert 'password' in json
        password = json['password']

        retrieve_response = fixture.make_request("https://localhost:22264/v1/api/password?url=www.google.com")
        assert retrieve_response.status_code == 200

        json = response.json()
        assert 'login' in json
        assert 'password' in json
        assert json['login'] == login
        assert json['password'] == password

        assert len(password) == 70
        assert all(c in ascii_lowercase for c in password)

from integration_tests.fixture import IntegrationServerFixture


def test_create_records_compare_with_request():
    with IntegrationServerFixture() as fixture:
        fixture.run_integration_server(22224, 'test.db', 'password')
        login = 'zxcv'
        response = fixture.make_request(
            f"https://localhost:22224/v1/api/createpassword?url=www.google.com&login={login}")

        assert response.status_code == 200
        json = response.json()
        assert 'password' in json
        password = json['password']

        retrieve_response = fixture.make_request("https://localhost:22224/v1/api/password?url=www.google.com")
        assert retrieve_response.status_code == 200

        json = response.json()
        assert 'login' in json
        assert 'password' in json
        assert json['login'] == login
        assert json['password'] == password

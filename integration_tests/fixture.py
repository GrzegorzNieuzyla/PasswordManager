import os

import requests
from PyQt6.QtWidgets import QApplication
from requests.adapters import HTTPAdapter
from requests.models import Response
from urllib3 import Retry

from password_manager.application_context import ApplicationContext
from password_manager.encryption.key_generator import KeyGenerator
from password_manager.integration.controller import IntegrationController


class IntegrationServerFixture:
    def run_integration_server(self, port_number: int, db_location: str, password: str):
        self.app = QApplication([])
        self.context = ApplicationContext()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.context.integration_controller = IntegrationController(f'{dir_path}/res/test_key.pem',
                                                                    f'{dir_path}/res/test_cert.pem',
                                                                    port_number)
        self.context.integration_controller.server_thread.daemon = True
        self.context.initialize_database(db_location)
        key, metadata = KeyGenerator(password).generate()
        self.context.get_metadata_repository().add_or_update(metadata.salt, metadata.iterations,
                                                             metadata.hmac, metadata.key_len)
        self.context.initialize_data_access(key)
        assert self.context.main_window_controller.try_load_data()

    @staticmethod
    def make_request(url: str) -> Response:
        s = requests.Session()
        retries = Retry(total=10,
                        backoff_factor=0.2)

        s.mount('https://', HTTPAdapter(max_retries=retries))

        return s.get(url, verify=False)

    def __enter__(self):
        return self

    def __exit__(self, _, __, ___):
        self.cleanup()

    def cleanup(self):
        os.remove(self.context.database_manager.path)
        self.app.quit()
        del self.app

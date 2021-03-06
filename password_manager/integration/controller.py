import os
from threading import Thread
from typing import List, Callable, Optional, Tuple, Dict, Union, Any

from password_manager.certificate import generate_certificate
from password_manager.integration.server import Server


class IntegrationController:
    """
    Controller managing the flask server needed for browser extension
    """

    def __init__(self, key_file: str, cert_file: str, port: int) -> None:
        if not os.path.exists(key_file) or not os.path.exists(cert_file):
            generate_certificate(cert_file, key_file)
        self.get_sites_handler: Optional[Callable[[], List[str]]] = None
        self.get_password_handler: Optional[Callable[[str], List[Tuple[str, str]]]] = None
        self.create_password_handler: Optional[Callable[[str, str], str]] = None
        self.server = Server(key_file=key_file, cert_file=cert_file)
        self.port = port
        self.server_thread = Thread(target=lambda s=self: s.server.run_server(s.handle_get_sites,
                                                                              s.handle_get_password,
                                                                              s.handle_create_password,
                                                                              s.port))

    def start_server(self) -> None:
        self.server_thread.start()

    def set_get_sites_handler(self, handler: Callable[[], List[str]]) -> None:
        self.get_sites_handler = handler

    def set_get_password_handler(self, handler: Callable[[str], List[Tuple[str, str]]]) -> None:
        self.get_password_handler = handler

    def set_create_password_handler(self, handler: Callable[[str, str], str]) -> None:
        self.create_password_handler = handler

    def handle_get_sites(self) -> Union[Dict[str, str], List[str]]:
        if not self.get_sites_handler:
            raise Exception("No handler defined")
        return self.get_sites_handler()

    def handle_get_password(self, url: str) -> List[Dict[str, str]]:
        if not self.get_password_handler:
            raise Exception("No handler defined")
        user_data = self.get_password_handler(url)
        return list(map(lambda x: {'login': x[0], 'password': x[1]}, user_data))

    def handle_create_password(self, url: str, login: str) -> Dict[str, str]:
        if not self.create_password_handler:
            raise Exception("No handler defined")
        password = self.create_password_handler(url, login)
        return {'password': password, 'login': login}

    def get_routing(self) -> Dict[str, Any]:
        return {
            "v1/api/sites": self.handle_get_sites,
            "v1/api/password": self.handle_get_password,
            "v1/api/createpassword": self.handle_create_password,
        }

# TODO: Refresh periodically every n minutes or on click
# TODO: Refresh GUI on data change
# TODO: v1/api/sites -> [sites]
# TODO: v1/api/password?url=url -> login, password
# TODO: v1/api/createpassword?url=url&login=login -> password
import ssl
from http.server import HTTPServer
from threading import Thread
from typing import List, Callable, Optional, Tuple, Dict, Union

from password_manager.integration.server import Server


class IntegrationController:
    def __init__(self, key_file: str, cert_file: str) -> None:
        self.get_sites_handler: Optional[Callable[[], List[str]]] = None
        self.get_password_handler: Optional[Callable[[str], List[Tuple[str, str]]]] = None
        self.create_password_handler: Optional[Callable[[str, str], str]] = None
        self.server = HTTPServer(('localhost', 8000), Server)
        self.server.socket = ssl.wrap_socket(self.server.socket,
                                             keyfile=key_file,
                                             certfile=cert_file, server_side=True)
        Server.instance.register("v1/api/sites", self.handle_get_sites)
        Server.instance.register("v1/api/password", self.handle_get_password)
        Server.instance.register("v1/api/createpassword", self.handle_create_password)
        self.server_thread = Thread(target=lambda controller=self: controller.server.serve_forever())
        self.server_thread.start()

    def set_get_sites_handler(self, handler: Callable[[], List[str]]) -> None:
        self.get_sites_handler = handler

    def set_get_password_handler(self, handler: Callable[[str], List[Tuple[str, str]]]) -> None:
        self.get_password_handler = handler

    def set_create_password_handler(self, handler: Callable[[str, str], str]) -> None:
        self.create_password_handler = handler

    def handle_get_sites(self, _: Dict[str, str]) -> Union[Dict[str, str], List[str]]:
        if not self.get_sites_handler:
            raise Exception("No handler defined")
        return self.get_sites_handler()

    def handle_get_password(self, parameters: Dict[str, str]) -> Union[Dict[str, str], List[Dict[str, str]]]:
        if not self.get_password_handler:
            raise Exception("No handler defined")
        if 'url' not in parameters:
            raise Exception("No `url' parameter defined")
        user_data = self.get_password_handler(parameters['url'])
        return list(map(lambda x: {'login': x[0], 'password': x[1]}, user_data))

    def handle_create_password(self, parameters: Dict[str, str]) -> Union[Dict[str, str], Dict[str, str]]:
        if not self.create_password_handler:
            raise Exception("No handler defined")
        if 'url' not in parameters:
            raise Exception("No `url' parameter defined")
        if 'login' not in parameters:
            raise Exception("No `login' parameter defined")
        password = self.create_password_handler(parameters['url'], parameters['login'])
        return {'password': password}

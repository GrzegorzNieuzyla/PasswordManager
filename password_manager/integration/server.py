import json
from http.server import BaseHTTPRequestHandler
from typing import Tuple, Callable, Dict, Union, List, Any
from urllib.parse import parse_qs


class Server(BaseHTTPRequestHandler):
    instance: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Server, self).__init__(*args, **kwargs)
        self.handlers: Dict[str, Callable[[Dict[str, str]], Union[Dict, List]]] = {}
        self.instance = self

    def _set_headers(self, status_code: int) -> None:
        self.send_response(status_code)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self) -> None:
        path, parameters = self._parse_parameters()
        if path in self.handlers:
            try:
                response = self.handlers[path](parameters)
                self._set_headers(200)
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(f'{{ "error": "No defined handler for \"{path}\"" }}'.encode())

    def _parse_parameters(self) -> Tuple[str, dict]:
        if '?' not in self.path:
            return self.path, {}
        split = self.path.split('?')
        return split[0], parse_qs(split[1])

    def register(self, path: str, handler: Callable[[Dict[str, str]], Union[Dict[str, str], List[str]]]) -> None:
        self.handlers[path] = handler

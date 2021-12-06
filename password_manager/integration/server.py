from typing import Callable, Union, List, Dict, Any

from flask import Flask, Response
from flask import jsonify
from flask import request


class Server:
    def __init__(self, cert_file: str, key_file: str) -> None:
        self.cert_file = cert_file
        self.key_file = key_file

    def run_server(self, get_sites_handler: Callable[[], Union[List[str], Dict[str, str]]],
                   get_password_handler: Callable[[str], Union[List[str], Dict[str, str]]],
                   create_password_handler: Callable[[str, str], Union[List[str], Dict[str, str]]],
                   port: int) -> None:
        app = Flask(__name__)

        @app.route("/v1/api/sites")
        def sites() -> Response:
            return jsonify(get_sites_handler())

        @app.route("/v1/api/password")
        def password() -> Any:
            url = request.args.get('url', default=None)
            if not url:
                return {'error': '"url" parameter not provided'}, 400
            return jsonify(get_password_handler(url))

        @app.route("/v1/api/createpassword")
        def create_password() -> Any:
            login = request.args.get('login', default=None)
            url = request.args.get('url', default=None)
            if not url:
                return {'error': '"url" parameter not provided'}, 400
            if not login:
                return {'error': '"login" parameter not provided'}, 400
            return jsonify(create_password_handler(url, login))

        @app.route("/")
        def index() -> Any:
            return """
            <div>
            <h3>Extension installed successfully</h3>
            <p>Right click -> Password manager to access creating and retrieving user data</p>
            </div>
            """

        context = (self.cert_file, self.key_file)
        app.run(debug=False, ssl_context=context, port=port)

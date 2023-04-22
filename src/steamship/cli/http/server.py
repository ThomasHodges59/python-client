from socketserver import TCPServer
from typing import Optional

from steamship.cli.http.handler import make_handler
from steamship.invocable import Invocable


class SteamshipHTTPServer:
    """A simple HTTP Server that wraps an invocable (package or plugin).

    To use, call:

       server = SteamshipHTTPServer(invocable)
       server.start()

    To shut down, call:

       server.stop()

    """

    invocable: Invocable
    port: int
    server: TCPServer
    default_api_key: Optional[str] = (None,)
    invocable_handle: str = (None,)
    invocable_version_handle: str = (None,)
    invocable_instance_handle: str = (None,)

    def __init__(
        self,
        invocable: Invocable,
        port: int = 8080,
        default_api_key: Optional[str] = None,
        invocable_handle: str = None,
        invocable_version_handle: str = None,
        invocable_instance_handle: str = None,
    ):
        self.invocable = invocable
        self.port = port
        self.default_api_key = default_api_key
        self.invocable_handle = invocable_handle
        self.invocable_version_handle = invocable_version_handle
        self.invocable_instance_handle = invocable_instance_handle

    def start(self):
        """Start the server."""
        self.server = TCPServer(
            ("", self.port),
            make_handler(
                self.invocable,
                self.port,
                default_api_key=self.default_api_key,
                invocable_handle=self.invocable_handle,
                invocable_version_handle=self.invocable_version_handle,
                invocable_instance_handle=self.invocable_instance_handle,
            ),
        )
        self.server.serve_forever()

    def stop(self):
        """Stop the server."""
        self.server.shutdown()

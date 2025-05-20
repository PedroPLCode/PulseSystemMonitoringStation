from unittest.mock import MagicMock
from app.utils.exception_handler import exception_handler
from app.utils import get_ip_address


def make_request(headers=None, remote_addr=None):
    req = MagicMock()
    req.headers = headers or {}
    req.remote_addr = remote_addr
    return req


def test_get_ip_address_with_x_forwarded_for():
    headers = {"X-Forwarded-For": "1.2.3.4, 5.6.7.8"}
    req = make_request(headers=headers, remote_addr="9.9.9.9")
    ip = get_ip_address(req)
    assert ip == "1.2.3.4"


def test_get_ip_address_without_x_forwarded_for():
    req = make_request(headers={}, remote_addr="9.9.9.9")
    ip = get_ip_address(req)
    assert ip == "9.9.9.9"


def test_get_ip_address_exception(monkeypatch):
    class BadRequest:
        @property
        def headers(self):
            raise Exception("Some error")

        @property
        def remote_addr(self):
            return "9.9.9.9"

    req = BadRequest()
    ip = get_ip_address(req)
    assert ip == "unknown"

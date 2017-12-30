from unittest import TestCase
from bitcoinrpc.data_types import AuthProxyConfig, ServiceUrl, parse_service_url


class TestDataTypes(TestCase):
    def setUp(self):
        self.username = "user"
        self.password = "secret"
        self.hostname = "localhost"
        self.port = 8332
        self.scheme = "http"
        self.url_example = f"{self.scheme}://{self.username}:{self.password}@{self.hostname}:{self.port}"
        self.service_url_example = ServiceUrl(username=self.username.encode(), password=self.password.encode(),
                                              scheme=self.scheme, path="", hostname=self.hostname, port=self.port)
        self.config_example = {"service_url": self.service_url_example,
                               "timeout": 30,
                               "user_agent": """AuthServiceProxy/0.1"""}

    def test_parse_url(self):
        self.assertRaises(AssertionError, parse_service_url, raw="httx://obviously@malformed@localhost:abc")
        res = parse_service_url(raw="http://user:secret@localhost:8332")
        expected = {"scheme": "http", "username": "user".encode(), "password": "secret".encode(),
                    "hostname": "localhost", "port": 8332, "path": ""}

        self.assertDictEqual(res._asdict(), expected)

    def test_config_creation(self):
        c = AuthProxyConfig(service_url=parse_service_url(self.url_example))
        self.assertSetEqual(set(c._asdict().keys()), set(self.config_example.keys()))
        self.assertSetEqual(set(c._asdict().values()), set(self.config_example.values()))
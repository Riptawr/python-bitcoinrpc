from unittest import TestCase
from bitcoinrpc.data_types import AuthProxyConfig
from bitcoinrpc.authproxy import AuthServiceProxy


class TestAuthProxy(TestCase):
    def setUp(self):
        self.url_example = "http://user:secret@localhost:8332"
        self.config_example = {"service_url": self.url_example,
                               "timeout": 30,
                               "connection": None,
                               "user_agent": """AuthServiceProxy/0.1""",
                               "service_name": None}

    def test_config_creation(self):
        c = AuthProxyConfig(service_url=self.url_example)
        self.assertSetEqual(set(c._asdict().keys()), set(self.config_example.keys()))
        self.assertSetEqual(set(c._asdict().values()), set(self.config_example.values()))

    def test_feature_equivalence_config(self):
        c = AuthProxyConfig(service_url="http://user:secret@localhost:8332")
        service = AuthServiceProxy(**c._asdict())
        res = service.getinfo()
        keys = ['deprecation-warning', 'version', 'protocolversion', 'walletversion', 'balance', 'blocks', 'timeoffset', 'connections', 'proxy', 'difficulty', 'testnet', 'keypoololdest', 'keypoolsize', 'unlocked_until', 'paytxfee', 'relayfee', 'errors']
        self.assertSetEqual(set(keys), set(res.keys()))

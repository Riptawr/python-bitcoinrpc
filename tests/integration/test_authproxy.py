from unittest import TestCase
from bitcoinrpc.data_types import AuthProxyConfig, parse_service_url
from bitcoinrpc.authproxy import AuthServiceProxy


class TestAuthProxy(TestCase):
    def test_feature_equivalence_config(self):
        c = AuthProxyConfig(service_url=parse_service_url("http://user:secret@localhost:8332"))
        service = AuthServiceProxy(c)
        res = service.getinfo()  # TODO: replace with something that will not be deprecated
        keys = ['deprecation-warning', 'version', 'protocolversion', 'walletversion', 'balance', 'blocks', 'timeoffset',
                'connections', 'proxy', 'difficulty', 'testnet', 'keypoololdest', 'keypoolsize', 'unlocked_until',
                'paytxfee', 'relayfee', 'errors']

        self.assertSetEqual(set(keys), set(res.keys()))
        res2 = service.getinfo()
        self.assertSetEqual(set(keys), set(res2.keys()), msg="Multiple calls do not re-use connection")

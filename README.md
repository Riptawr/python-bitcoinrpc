# python3-bitcoinrpc

This is a port & refactored version python-bitcoinrpc for **Python 3.6 or higher**

Apart from the initial configuration, the API did not change and most examples for bitcoinrpc should still work.

## Setup

1. install requirements ```pip -r requirements.txt```
2. ```python3.6 setup.py install```

## Testing
1. build the provided docker container, 
which will run a **insecure** bitcoin-core (bitcoind) node.
 See [container_build_instructions](./deployment/bitcoind/README.md)
2. from the root dir run coverage ```coverage run --source=. -m unittest discover -s tests```
3. check the abysmal coverage percentage ```coverage report```





## Examples

create a config programatically
```python
from bitcoinrpc.data_types import parse_service_url, AuthProxyConfig, JSONRPCException

url = "http://user:password@hostip:8332"
config = AuthProxyConfig(parse_service_url(url))
client = AuthServiceProxy(config)
```

```python
from bitcoinrpc.authproxy import AuthServiceProxy,

best_block_hash = client.getbestblockhash()
print(client.getblock(best_block_hash))

# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
commands = [ [ "getblockhash", height] for height in range(100) ]
block_hashes = client.batch_(commands)
blocks = client.batch_([ [ "getblock", h ] for h in block_hashes ])
block_times = [ block["time"] for block in blocks ]
print(block_times)
```

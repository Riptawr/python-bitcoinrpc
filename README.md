# python3-bitcoinrpc

This is a port & refactored version python-bitcoinrpc for Python 3.6+

Since the use-case changed to run inside a container, setup.py support is dropped.
Apart from the initial configuration, the API did not change and most examples for bitcoinrpc should still work.

## Setup

1. install requirements ```pip -r requirements.txt```

## Testing
1. have a bitcoind listening, make sure -rpcallowip is pointing to your local network and the daemon listens on the local ip
 ```bitcoind -server -rpcuser=user -rpcpassword=secret -rpcbind=192.168.0.100 -rpcallowip=192.168.0.0/24```
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

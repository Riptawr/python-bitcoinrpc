## Container is provided for purposes of running integration tests

Settings are inherently insecure, please do not use it in production

### How to build  
1. from this dir, run ```docker build -t testbitcoind .```
2. start with ```docker run --rm --net=host testbitcoind```
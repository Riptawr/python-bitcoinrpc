FROM ubuntu:16.04

MAINTAINER Alexander Korolev <blog.droidcraft.org>

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt -y install python-software-properties
RUN DEBIAN_FRONTEND=noninteractive apt -y install software-properties-common
RUN DEBIAN_FRONTEND=noninteractive apt -y install git
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN add-apt-repository ppa:bitcoin/bitcoin
RUN apt update && DEBIAN_FRONTEND=noninteractive apt -y install python3.6 python3.6-dev python3-pip bitcoind
RUN apt-get clean

# Use python 3.6 by default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

WORKDIR /opt/
VOLUME /datadir
#https://github.com/moby/moby/issues/1996 -> add --build-arg CACHEBUST=$(date +%s) to docker build command
# will run below commands without using the cache
ARG CACHEBUST=1
RUN git clone -b port_to_py3 https://github.com/Riptawr/python-bitcoinrpc.git /opt/
RUN pip3 install -r /opt/requirements.txt

CMD ["bitcoind", "-server", "-rpcuser=user", "-rpcpassword=secret"]
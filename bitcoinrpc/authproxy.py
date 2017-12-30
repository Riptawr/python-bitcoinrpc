
"""
  Copyright 2017 Alexander Korolev
  AuthServiceProxy has the following improvements:
  - ported from Python 2.x to Python 3.6
  - extracted argument parsing / config parsing from AuthServiceProxy logic into separate function
  - replaced constants in scope with class fields passed, as kwargs with defaults, to init
  - type hints added to discern effects from functions
  - Pythonic `if` checks
  - PEP 8
  - tests

  Previous Copyright, from jgarzik/bitcoin-rpc:

  Copyright 2011 Jeff Garzik

  AuthServiceProxy has the following improvements over python-jsonrpc's
  ServiceProxy class:

  - HTTP connections persist for the life of the AuthServiceProxy object
    (if server supports HTTP/1.1)
  - sends protocol 'version', per JSON-RPC 1.1
  - sends proper, incrementing 'id'
  - sends Basic HTTP authentication headers
  - parses all JSON numbers that look like floats as Decimal
  - uses standard Python json lib

  Previous copyright, from python-jsonrpc/jsonrpc/proxy.py:

  Copyright (c) 2007 Jan-Klaas Kollhof

  This file is part of jsonrpc.

  jsonrpc is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation; either version 2.1 of the License, or
  (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this software; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import base64
import decimal
import json
import logging
from typing import Optional, Union
from http import client
from .data_types import AuthProxyConfig, ServiceUrl
from http.client import HTTPConnection, HTTPSConnection


class JSONRPCException(Exception):
    def __init__(self, rpc_error):
        parent_args = []
        try:
            parent_args.append(rpc_error['message'])
        except:
            pass
        Exception.__init__(self, *parent_args)
        self.error = rpc_error
        self.code = rpc_error['code'] if 'code' in rpc_error else None
        self.message = rpc_error['message'] if 'message' in rpc_error else None

    def __str__(self):
        return '%d: %s' % (self.code, self.message)

    def __repr__(self):
        return '<%s \'%s\'>' % (self.__class__.__name__, self)


def encode_decimal(o: decimal.Decimal) -> float:
    if isinstance(o, decimal.Decimal):
        return float(round(o, 8))
    raise TypeError(repr(o) + " is not JSON serializable")


class AuthServiceProxy(object):
    __id_count = 0

    def __init__(self, config: AuthProxyConfig,
                 service_name=None,
                 connection: Union[Optional[HTTPSConnection], Optional[HTTPConnection]]=None):

        self.__log = logging.getLogger("BitcoinRPC")
        self.__service_url: ServiceUrl = config.service_url
        self.__service_name: Optional[str] = service_name
        self.__user_agent = config.user_agent
        self.__port: int = config.service_url.port or 80
        self.__config = config

        authpair = self.__service_url.username + b':' + self.__service_url.password
        self.__auth_header = b'Basic ' + base64.b64encode(authpair)
        self.__timeout = config.timeout

        if connection:
            # Callables re-use the connection of the original proxy
            self.__conn = connection
        elif self.__service_url.scheme == 'https':
            self.__conn = client.HTTPSConnection(self.__service_url.hostname, self.__port,
                                                 timeout=self.__timeout)
        else:
            self.__conn = client.HTTPConnection(self.__service_url.hostname, self.__port,
                                                timeout=self.__timeout)
        self.__service_name = service_name

    def __getattr__(self, name):
        """ Used to make the calls via `.` on the service object """
        if name.startswith('__') and name.endswith('__'):
            # Check to prevent users from calling private fields
            raise AttributeError
        if self.__service_name is not None:
            name = "%s.%s" % (self.__service_name, name)
        return AuthServiceProxy(config=self.__config, service_name=name, connection=self.__conn)

    def __call__(self, *args):
        AuthServiceProxy.__id_count += 1

        self.__log.debug("-%s-> %s %s" % (AuthServiceProxy.__id_count, self.__service_name,
                                 json.dumps(args, default=encode_decimal)))
        postdata = json.dumps({'version': '1.1',
                               'method': self.__service_name,
                               'params': args,
                               'id': AuthServiceProxy.__id_count}, default=encode_decimal)
        self.__conn.request('POST', self.__service_url.path, postdata,
                            {'Host': self.__service_url.hostname,
                             'User-Agent': self.__user_agent,
                             'Authorization': self.__auth_header,
                             'Content-type': 'application/json'})
        self.__conn.sock.settimeout(self.__timeout)

        response = self._get_response()
        if response.get('error') is not None:
            raise JSONRPCException(response['error'])
        elif 'result' not in response:
            raise JSONRPCException({
                'code': -343, 'message': 'missing JSON-RPC result'})

        return response['result']

    def batch_(self, rpc_calls):
        """Batch RPC call.
           Pass array of arrays: [ [ "method", params... ], ... ]
           Returns array of results.
        """
        batch_data = []
        for rpc_call in rpc_calls:
            AuthServiceProxy.__id_count += 1
            m = rpc_call.pop(0)
            batch_data.append({"jsonrpc":"2.0", "method":m, "params":rpc_call, "id":AuthServiceProxy.__id_count})

        postdata = json.dumps(batch_data, default=encode_decimal)
        self.__log.debug("--> "+postdata)
        self.__conn.request('POST', self.__url.path, postdata,
                            {'Host': self.__url.hostname,
                             'User-Agent': USER_AGENT,
                             'Authorization': self.__auth_header,
                             'Content-type': 'application/json'})
        results = []
        responses = self._get_response()
        for response in responses:
            if response['error'] is not None:
                raise JSONRPCException(response['error'])
            elif 'result' not in response:
                raise JSONRPCException({
                    'code': -343, 'message': 'missing JSON-RPC result'})
            else:
                results.append(response['result'])
        return results

    def _get_response(self):
        http_response = self.__conn.getresponse()
        if http_response is None:
            raise JSONRPCException({
                'code': -342, 'message': 'missing HTTP response from server'})

        content_type = http_response.getheader('Content-Type')
        if content_type != 'application/json':
            raise JSONRPCException({
                'code': -342, 'message': 'non-JSON HTTP response with \'%i %s\' from server' % (http_response.status, http_response.reason)})

        responsedata = http_response.read().decode('utf8')
        response = json.loads(responsedata, parse_float=decimal.Decimal)
        if "error" in response and response["error"] is None:
            self.__log.debug("<-%s- %s" % (response["id"], json.dumps(response["result"], default=encode_decimal)))
        else:
            self.__log.debug("<-- "+responsedata)
        return response



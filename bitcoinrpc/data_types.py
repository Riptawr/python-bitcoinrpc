from typing import NamedTuple, Optional, Union
from http.client import HTTPConnection, HTTPSConnection


class AuthProxyConfig(NamedTuple):
    service_url: str
    user_agent: str = """AuthServiceProxy/0.1"""
    service_name: Optional[str] = None
    timeout: int = 30
    connection: Union[Optional[HTTPSConnection], Optional[HTTPConnection]] = None

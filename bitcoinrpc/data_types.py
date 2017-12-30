from typing import NamedTuple, Optional, Union
from urllib import parse


class ServiceUrl(NamedTuple):
    scheme: str
    username: str
    password: str
    port: int
    hostname: str
    path: str


class AuthProxyConfig(NamedTuple):
    service_url: ServiceUrl
    user_agent: str = """AuthServiceProxy/0.1"""
    timeout: int = 30


def parse_service_url(raw: str) -> Union[Exception, ServiceUrl]:
    try:
        parsed = parse.urlparse(raw)
        (user, pw, scheme, path, hostname) = (parsed.username, parsed.password,
                                              parsed.scheme, parsed.path, parsed.hostname)
        if user:
            user = user.encode("utf-8")
        else:
            raise AssertionError(f"Malformed string {raw}")

        if pw:
            pw = pw.encode("utf-8")
        else:
            raise AssertionError(f"Malformed string {raw}")

        return ServiceUrl(hostname=hostname, username=user, password=pw, scheme=scheme, path=path, port=8332)

    except AttributeError:
        # Proxy is not handling them, so we do neither
        # Todo: handle after behaviour-equivalence tests are done
        pass

    except AssertionError:
        raise

    except Exception as ex:
        print(f"Failed to parse raw string to ServiceUrl: {raw}")
        raise ex
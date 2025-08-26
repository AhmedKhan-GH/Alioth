import requests
import logging

from sockshandler import is_ip
from typing_inspection.typing_objects import is_any

from .decorators import *
import socket

log = logging.getLogger(__name__)

@try_catch(exit_on_error=False, default_return=False, catch_exceptions=requests.exceptions.RequestException)
def check_url_connection(url, headers = None, timeout = 5):
    """Check connection to a given URL."""
    response = requests.get(url, headers = headers, timeout=timeout)
    is_available = response.status_code == 200
    log.debug(f"Connection to {url}: {'OK' if is_available else 'FAILED'}")
    return is_available

@try_catch(exit_on_error=False, default_return=False, catch_exceptions=socket.error)
def check_port_connection(host, port, timeout = 5):
    """Check connection to a given port."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()

    is_available = result == 0
    log.debug(f"Connection to {host}:{port}: {'OK' if is_available else 'FAILED'}")
    return is_available

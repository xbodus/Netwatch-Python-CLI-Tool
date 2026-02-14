"""
Parse strace output for analyzing
"""

import re
from .models import SocketInfo, ConnectionInfo, DataTransfer



def parse_socket(line: str) -> SocketInfo:
    """
    Parse socket info

    Example: socket(PF_INET, SOCK_STREAM, IPPROTO_TCP) = 3
    """
    pattern = r'socket\((.+), (.+), (.+)\) = (\d+)'
    match = re.match(pattern, line)

    if match:
        family, sock_type, protocol, fd = match.groups()
        return SocketInfo(family=family, sock_type=sock_type, protocol=protocol, fd=int(fd))
    raise ValueError("Unable to parse socket info")


def parse_connection(line: str) -> ConnectionInfo:
    """
    Parse connection info

    Example: connect(3, {sa_family=AF_INET, sin_port=htons(5555), sin_addr=inet_addr("192.168.10.1")}, 16) = 0
    """
    pattern = r'connect\((\d+), \{.+=(.+), .+=.+\((\d+)\), .+=.+\("(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})"\)\}, \d+\) = \d+'
    match = re.match(pattern, line)

    if match:
        fd, family, port, ip = match.groups()
        return ConnectionInfo(fd=int(fd), family=family, port=int(port), ip=ip)
    raise ValueError("Unable to parse connection info")


def parse_data(line: str) -> DataTransfer:
    """
    Parse Data Transfer (Write/Read Operations)

    Examples:  
        - write(3, "Hello World!\n", 13) = 13
        - read(3, "Boo!\n", 2048) = 5
    """
    pattern = r'([a-z]+)\((\d+), "(.+\n)", (\d+)\) = (\d+)'
    match = re.match(pattern, line)

    if match:
        operation, fd, data, bytes_requested, bytes_transferred = match.groups()
        return DataTransfer(
            operation=operation, 
            fd=int(fd), 
            data=data, 
            bytes_requested=int(bytes_requested), 
            bytes_transferred=int(bytes_transferred)
        )
    raise ValueError("Unable to parse data transfer")

"""
Define project data structures in data classes

Example:

    @dataclass
    class ConnectionInfo:
        fd: int
        ip: str
        port: int
        bytes_sent: int = 0
        bytes_received: int = 0
        
        # You CAN add methods!
        def total_bytes(self) -> int:
            return self.bytes_sent + self.bytes_received
        
        def is_high_volume(self, threshold: int = 10000) -> bool:
            return self.total_bytes() > threshold

Use case example:    
    conn = ConnectionInfo(fd=3, ip="192.168.10.1", port=5555)
    print(conn.ip)

Dataclasses for syscall data (SocketInfo, ConnectionInfo, DataTransfer)
"""
from dataclasses import dataclass


@dataclass
class SocketInfo:
    """
    Socket info
    Each entry decribes a variable required for making a connection

    Structure: socket(PF_INET, SOCK_STREAM, IPPROTP_TCP) = 3
    """
    family: str  # PF_INET (Protocol Family) or AF_INET (Address Family)
    sock_type: str  # SOCK_STREAM (TCP) or SOCK_DGRAM (UDP)
    protocol: str  # IPPROTO_TCP or IPPROTO_IP
    fd: int  # Assigned variable of socket (i.e. socket assigned to 3). fd = file descriptor


@dataclass
class ConnectionInfo:
    """
    Connection info
    Each entry describes a variable required for connecting to a socket

    Structure: connect(3, {sa_family=AF_INET, sin_port=htons(5555), sin_addr=inet_addr("192.168.10.1")}, 16) = 0
    """
    fd: int
    family: str
    port: int
    ip: str


@dataclass
class DataTransfer:
    """
    Data Transfer (Write, Read operations)
    Each entry describes a data transfer variable

    Structure examples:  
        - write(3, "Hello World!\n", 13) = 13
        - read(3, "Boo!\n", 2048) = 5
    """
    operation: str  # read or write
    fd: int
    data: str
    bytes_requested: int
    bytes_transferred: int
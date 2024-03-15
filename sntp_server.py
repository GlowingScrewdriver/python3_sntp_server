"""
This module defines classes to handle the communication operations of
the SNTP server, like sending and receiving messages.
"""

from sntp import SNTPMsg
from socket import (
    socket,
    AF_INET, SOCK_DGRAM,
)

class SNTPSocket (socket):
    def __init__ (self):
        socket.__init__ (self, AF_INET, SOCK_DGRAM) # UDP/IP socket
        self.bind (("", 123))              # Standard port number for SNTP


    def recvSNTP (self):
        """
        Return a single SNTP request from the socket
        """
        return SNTPMsg (* self.recvfrom (1024))


    def sendSNTP (self, msg):
        """
        Send an SNTP response back to the source of the corresponding request
        msg: an SNTPMsg object
        """
        self.sendto (msg, msg.addr)

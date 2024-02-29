#!/bin/python3
import time
import socket
from math import floor, ceil

class MsgField:
    """
    A single field in the message
    """
    def __init__ (self, name, offset, length, value = 0):
        """
        name: field name
        length: field length in bits
        """
        self.value = value
        self.offset = offset
        self.length = length

# This is an exhaustive list of all fields in an SNTP message
Fields = {
    "LI": MsgField ("LI", 0, 2),         # Leap indicator
    "VN": MsgField ("VN", 2, 3),          # Version
    "Mode": MsgField ("Mode", 5, 3),                  # 3 is client, 4 is server, 5 is broadcast
    "Stratum": MsgField ("Stratum", 8, 8),              # Position in the hierarchy
    "Poll": MsgField ("Poll", 16, 8),                  # At most, so many seconds between successive messages from server
    "Precision": MsgField ("Precision", 24, 8),             # System clock precision
    "RootDelay": MsgField ("RootDelay", 32, 32),             # Round-trip time from this server to the primary source (i.e. Stratum 0)
    "RootDispersion": MsgField ("RootDispersion", 64, 32),        # Not sure
    "ReferenceIdentifier": MsgField ("ReferenceIdentifier", 96, 32),   # For lower strata (such as ours), this is the IP address
    "ReferenceTimestamp": MsgField ("ReferenceTimestamp", 128, 64),  # When the clock was last synchronized
    "OriginateTimestamp": MsgField ("OriginateTimestamp", 192, 64), # When the request was sent from client
    "RecieveTimestamp": MsgField ("RecieveTimestamp", 256, 64),   # When the server recieved the request, or when the client recieved the reply
    "TransmitTimestamp": MsgField ("TransmitTimestamp", 320, 64),  # When the request was sent from client, or when the reply was sent from server
}
MsgSize = 0
for f in Fields: MsgSize += Fields [f].length
MsgSize = ceil (MsgSize / 8) # Size of the message, in bytes

class SNTPMsg (bytearray):
    """
    A class representing a single SNTP message.
    The request and the response are both instances of this class.
    Along with the fields of the message itself, objects of this class
    also hold information about where the message came from.

    This class inherits from bytearray to simplify certain tasks like the following:
    * To get/set any field `Field Name` in the message, use SNTPMsg["Field Name"]
    * To use the entire message as a bytearray, simply refer to
      it as if it were a bytearray (e.g. `write (SNTPMsg)`)

    These features may not be implemented:
    * Authentication (Key Identifier field)
    * Message digest
    * Broadcast modes
    """

    def __init__ (self, data = b'', addr = None):
        """
        data: bytes-like data
        addr: tuple containing information about where the data came from

        Note: `data` and `addr` can be from, e.g., the return value of socket.socket.recv ()
        """

        bytearray.__init__ (self, data or MsgSize)
        self.addr = addr


    def __str__ (self):
        """
        Prettier output than bytearray
        """
        BOXWIDTH = 78
        out = "╭" + "─"*(BOXWIDTH) + "╮\n"

        for f in Fields:
            out += '│'
            out += (f'{f}: {self[f]}' + " "*BOXWIDTH) [:BOXWIDTH]
            out += '│\n'

        out += "╰" + "─"*(BOXWIDTH) + "╯\n"
        return out


    def locateitem (self, key):
        """
        Helper for __setitem__ and __getitem__
        """
        # Bit boundaries of the field
        _start = Fields [key].offset
        _end = _start + Fields [key].length
        # Byte boundaries, may contain bits from fields before and after
        start = floor (_start/8)
        end = ceil (_end/8)

        shamt = (8 - (_end%8)) & 7

        # Masks to extract and preserve bits outside the bit boundaries
        mask_start = 0xff << 8 - _start%8
        mask_end = 0xff << shamt; mask_end = mask_end >> 8

        # start, end: start and end bytes of the field
        # mask_start, mask_end: masks to separate bits that belong to fields after and before
        # shamt: amount by which to shift the value before putting in a bytearray
        return start, end, mask_start & 255, mask_end & 255, shamt

        ######
        # Consider the following scenario, where each character is one bit,
        # and the desired field is all the n's (so the x's are irrelevant, but need to
        # be preserved):
        # start: 0                 end: 3
        # |                          |
        # xxxnnnnn nnnnnnnn nnnnnnxx xxxxxxxx shamt: 2
        #  |                      |
        # mask_start:          mask_end:
        # 1110000              00000011
        # Geddit?
        ######

    def __getitem__ (self, key):
        try:
            return bytearray.__getitem__ (self, key)
        except TypeError:
            # `key` should be a string containing a field name
            start, end, mask_start, mask_end, shamt = self.locateitem (key)

            field = self [start:end]
            field [0] &= ~mask_start
            val = int.from_bytes (field) >> shamt
            return val

    def __setitem__ (self, key, val):
        """
        The index can be either a byte offset (int) or a field name (str)
        In case of a field name, the underlying bytearray is populated with the data
        based on offsets retrieved from Fields
        """
        try:
            bytearray.__setitem__ (self, key, val)
        except TypeError:
            # `key` should be a string containing a field name
            start, end, mask_start, mask_end, shamt = self.locateitem (key)

            # Construct a bytearray from the value, and shift it to dodge the field after it
            fieldval = val << shamt
            field = bytearray (fieldval.to_bytes (length = end - start))
            # Preserve bits of fields after and before
            field [0] |= self [start] & mask_start
            field [-1] |= self [end - 1] & mask_end
            # Writeback
            self [start:end] = field


'''                          SNTP Message Format:
                     ===================================
                           1                   2                   3
       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9  0  1
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |LI | VN  |Mode |    Stratum    |     Poll      |   Precision    |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                          Root  Delay                           |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                       Root  Dispersion                         |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                     Reference Identifier                       |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                                                                |
      |                    Reference Timestamp (64)                    |
      |                                                                |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                                                                |
      |                    Originate Timestamp (64)                    |
      |                                                                |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                                                                |
      |                     Receive Timestamp (64)                     |
      |                                                                |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                                                                |
      |                     Transmit Timestamp (64)                    |
      |                                                                |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                 Key Identifier (optional) (32)                 |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
      |                                                                |
      |                                                                |
      |                 Message Digest (optional) (128)                |
      |                                                                |
      |                                                                |
      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''

#!/bin/python3
import sntp
import sntp_server


### Demo on how to use class sntp_server.SNTPSocket ###
if __name__ == "__main__":
    sock = sntp_server.SNTPSocket ()
    while True:
        msg = sock.recvSNTP ()
        print (msg)
        msg ["Mode"] = 4
        msg ["Stratum"] = 15
        msg ["LI"] = 0
        msg ["RecieveTimestamp"] = msg ["TransmitTimestamp"]
        msg ["OriginateTimestamp"] = msg ["TransmitTimestamp"]
        sock.sendSNTP (msg)

exit ()


### Demo on how to use class sntp.SNTPMsg ###
if __name__ == "__main__":
    # Constructing a message object
    msg = sntp.SNTPMsg ()
    # Assigning individual properties
    msg ["Mode"] = 3
    msg ["VN"] = 4
    msg ["Stratum"] = 15

    # Using the output
    print (repr (msg)) # A byte-by-byte hex representation, for debugging
    print (msg)

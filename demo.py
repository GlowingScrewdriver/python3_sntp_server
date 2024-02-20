#!/bin/python3
import sntp

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

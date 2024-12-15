## About the project
An SNTP server, implemented in Python3 as per [RFC 4330](https://www.rfc-editor.org/rfc/rfc4330).

## Pending tasks:
* Implement the server and mechanism to receive/send requests/responses (socket programming)
* Fields to be populated, at a _bare_ minimum:
  - [x] `ReferenceTimestamp`
  - [x] `OriginateTimestamp`
  - [x] `ReceiveTimestamp`
  - [x] `TransmitTimestamp`
* Fields that would be nice to implement:
  - [ ] `RootDelay`
  - [ ] `Poll`
  - [ ] `Precision`
  - [ ] `ReferenceIdentifier`

Note: Each of these is a key name in an `SNTPMsg` object.

## Notes on programming
The following section documents how to use this project's modules. Examples illustrating these details can be found in [demo.py](demo.py).
### Using class `SNTPMsg` (from [sntp.py](sntp.py))
This class is used to represent an SNTP message. Both clients' requests and the server's responses will be of this type.

The class is designed with two kinds of usage in mind:
* As a **key-value mapping**, much like a `dict`. The key is a field name as
  defined in the RFC document, and the value is an integer
  ```python3
  msg = sntp.SNTPMsg ()
  msg ["VN"] = 4 # Set VN (Version Number) to 4
  ```
* As a **bytearray**. This comes in use when the message is sent or recieved through the socket interface
  ```python3
  socket.send (msg)
  ```

### Using class `SNTPSocket` (from [sntp_server.py](sntp_server.py))
This class is a wrapper around Python's socket type (socket.socket) to simplify socket operations:
* The class defines two convenience functions, `SNTPSocket.recvSNTP` and `SNTPSocket.sendSNTP`.
  These are for receiving and sending a single SNTP message, respectively; both use `SNTPMsg` objects to represent their data.
* The class constructor also takes care of choosing the standard UDP port for SNTP (port 123) and binding to it to listen for requests.


### References:
* [Message format](https://www.rfc-editor.org/rfc/rfc4330#page-8)
* [Socket programming in Python](https://docs.python.org/3/howto/sockets.html)

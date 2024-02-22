## About the project
An SNTP server, implemented in Python3 as per [RFC 4330](https://www.rfc-editor.org/rfc/rfc4330).

## Pending tasks:
* Implement the server and mechanism to receive/send requests/responses (socket programming)
* Fields to be populated, at a _bare_ minimum:
  - `ReferenceTimestamp`
  - `OriginateTimestamp`
  - `ReceiveTimestamp`
  - `TransmitTimestamp`
* Fields that would be nice to implement:
  - `RootDelay`
  - `Poll`
  - `Precision`
  - `ReferenceIdentifier`

Note: Each of these is a key name in an `SNTPMsg` object.

## Notes on programming
### Using class `SNTPMsg`
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
See also: [demo.py](demo.py), [sntp.py](sntp.py)

### References:
* [Message format](https://www.rfc-editor.org/rfc/rfc4330#page-8)
* [Socket programming in Python](https://docs.python.org/3/howto/sockets.html)

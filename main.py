import socket
import time
from sntp import SNTPMsg # Assuming you have an SNTP module with an SNTPMsg class
import conversions
import client

def handle_request(request_msg, recv_time):
    # Process the client's request message
    # For simplicity, let's just return the current time in NTP format as a response.
    response_msg = SNTPMsg()
    response_msg["Mode"] = 4  # Server response
    response_msg["Stratum"] = 15  # Example stratum, adjust as needed
    response_msg["LI"] = 0
    response_msg["VN"] = 4
    response_msg["RecieveTimestamp"] = conversions.posix_to_ntp(recv_time) # time.time()
    response_msg["OriginateTimestamp"] = request_msg["TransmitTimestamp"]
    response_msg["TransmitTimestamp"] = conversions.posix_to_ntp(time.time())
    response_msg["ReferenceTimestamp"] = client.sync_time

    return response_msg

def start_sntp_server(server_address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((server_address, port))
        print(f"Server is listening on {server_address}:{port}")

        while True:
            client_request, client_address = server_socket.recvfrom(1024)
            recv_time = time.time ()

            # Parse the received data into an SNTP message object
            request_msg = SNTPMsg(client_request)

            print ("Got request from", client_address)
            print (request_msg)

            # Process the request and generate a response
            # For best results, send the result immediately
            # after calling handle_request
            response_msg = handle_request(request_msg, recv_time)
            # Send the response to the client
            server_socket.sendto(response_msg, client_address)
            print ("Sent response to", client_address)
            print (response_msg)

if __name__ == "__main__":
    # Set your server address and port
    server_address = '' # Bind to all interfaces
    server_port = 123  # Standard UDP port

    client.set_sntp_time ()
    # Start the SNTP server
    start_sntp_server(server_address, server_port)

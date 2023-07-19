# In this example, you'll need to replace 'example.com' with the hostname or IP address of your server. Make sure to 
# provide the correct paths to the client certificate (CLIENT_CERT_FILE), private key (CLIENT_KEY_FILE), and CA certificate (CA_CERT_FILE) files.
# The ssl.create_default_context() function is used to create an SSL context that performs server certificate verification using the provided CA 
# certificate file. The load_cert_chain() method is used to load the client certificate and private key into the SSL context. The wrap_socket() method 
# wraps the socket with SSL/TLS and performs the handshake with the server.
# Once the connection is established, you can send and receive data using the sendall() and recv() methods of the SSL socket.
# Remember to install the necessary dependencies and ensure you have the required certificates and private key files before running the code.


import socket
import ssl

# Set the server hostname and port
SERVER_HOST = 'example.com'
SERVER_PORT = 443

# Set the paths to the client certificate and private key files
CLIENT_CERT_FILE = 'client.crt'
CLIENT_KEY_FILE = 'client.key'

# Set the path to the CA certificate file (to verify the server's certificate)
CA_CERT_FILE = 'ca.crt'

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket with SSL/TLS
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT_FILE)
ssl_context.load_cert_chain(certfile=CLIENT_CERT_FILE, keyfile=CLIENT_KEY_FILE)
ssl_sock = ssl_context.wrap_socket(sock, server_hostname=SERVER_HOST)

try:
    # Connect to the server
    ssl_sock.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to", SERVER_HOST)

    # Send data
    ssl_sock.sendall(b"Hello, server!")

    # Receive data
    data = ssl_sock.recv(1024)
    print("Received:", data.decode())

finally:
    # Close the connection
    ssl_sock.close()

import socket
import ssl

# Set the server hostname and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 443

# Set the paths to the server certificate and private key files
SERVER_CERT_FILE = 'server.crt'
SERVER_KEY_FILE = 'server.key'

# Set the path to the CA certificate file (to verify the client's certificate)
CA_CERT_FILE = 'ca.crt'

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
sock.bind((SERVER_HOST, SERVER_PORT))
print("Server listening on", SERVER_HOST, "port", SERVER_PORT)

# Listen for incoming connections
sock.listen(1)

# Wrap the socket with SSL/TLS
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=SERVER_CERT_FILE, keyfile=SERVER_KEY_FILE)
ssl_context.load_verify_locations(cafile=CA_CERT_FILE)

while True:
    # Accept a client connection
    client_sock, client_addr = sock.accept()
    print("Accepted connection from", client_addr)

    # Wrap the client socket with SSL/TLS
    ssl_sock = ssl_context.wrap_socket(client_sock, server_side=True)

    try:
        # Perform mutual authentication
        client_cert = ssl_sock.getpeercert()
        if not client_cert:
            raise ssl.SSLError("Client certificate not provided.")

        # Print client certificate information
        print("Client certificate subject:", dict(client_cert)['subject'])
        print("Client certificate issuer:", dict(client_cert)['issuer'])

        # Receive data from the client
        data = ssl_sock.recv(1024)
        print("Received from client:", data.decode())

        # Send a response back to the client
        ssl_sock.sendall(b"Hello, client!")

    finally:
        # Close the client connection
        ssl_sock.close()

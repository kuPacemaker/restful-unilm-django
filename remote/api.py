import socket

def call(protocol):
    HOST, PORT, QUERY, TIMEOUT = parse_protocol(protocol)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(QUERY)

    recv = client_socket.recv(4096).decode('utf-8')
    client_socket.close()
    
    response = recv.split('\n')
    return response

def parse_protocol(protocol):
    HOST, PORT = protocol.node
    QUERY = protocol.gen_query().encode()
    TIMEOUT = protocol.timeout
    return HOST, PORT, QUERY, TIMEOUT
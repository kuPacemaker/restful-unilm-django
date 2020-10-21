import socket

def call(protocol):
    HOST, PORT = protocol.__node__
    QUERY = protocol.gen_query().encode()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(15.0)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(QUERY)

    recv = client_socket.recv(4096).decode('utf-8')
    client_socket.close()
    
    response = recv.split('\n')
    return response

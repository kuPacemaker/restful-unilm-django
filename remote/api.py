from remote.interface import nodes

def call(query, service):
    HOST, PORT = nodes[service]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(15.0)
    client_socket.connect((HOST, PORT))

    client_socket.sendall(query.encode())
    recv = client_socket.recv(4096).decode('utf-8')
    client_socket.close()
    
    response = recv.split('\n')
    return response

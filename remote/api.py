import socket

def call(protocol):
    HOST, PORT, QUERY, TIMEOUT = protocol.parse()
    csock = setup_socket_connection(HOST, PORT, timeout)
    response = []
    for each_query in QUERY:
        csock.sendall(each_query)
        res = csock.recv(4096).decode('utf-8')
        response.append(res.split('\n'))
    csock.close()
    protocol.notify_response(response)
    return response

def setup_socket_connection(host, port, timeout):
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.settimeout(timeout)
    csock.connect((host, port))
    return csock
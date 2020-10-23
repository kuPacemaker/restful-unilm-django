import socket

def call(protocol):
    HOST, PORT, QUERY, TIMEOUT = protocol.parse()
    csock = setup_socket_connection(HOST, PORT, TIMEOUT)

    for each_query in QUERY:
        csock.sendall(each_query.encode())
        res = csock.recv(4096).decode('utf-8')
        res = res.split('\n')
        protocol.notify_response(res)
        
    csock.close()
    

def setup_socket_connection(host, port, timeout):
    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.settimeout(timeout)
    csock.connect((host, port))
    return csock
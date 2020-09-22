import socket

HOST = '117.16.136.170'
PORT = 2593

def call_qg_interface(qa, iters):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10.0)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(qa.encode())
    
    question = []
    for i in range(iters):
        q = client_socket.recv(4096).decode('ascii')
        question.append(q)
        
    client_socket.close()

    return question
import socket

HOST = '117.16.136.170'
PORT = 2593

def call_qg_interface(qa):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10.0)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(qa.encode())
    
    recv = client_socket.recv(4096).decode('ascii')
    client_socket.close()
    
    questions = recv.split('\n')
    return questions
import socket

HOST = '117.16.136.170'
PORT = 3421

def call_qa_interface(qa):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(15.0)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(qa.encode())
    
    recv = client_socket.recv(4096).decode('utf-8')
    client_socket.close()
    
    questions = recv.split('\n')
    return questions

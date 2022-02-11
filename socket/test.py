"""
Write some tests here
"""
from concurrent.futures import process
import socket
import multiprocessing as mp


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def createServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)





def main():
    processServer = mp.Process(target=createServer)
    processClient = mp.Process()


if __name__ == "__main__":
    main()


        




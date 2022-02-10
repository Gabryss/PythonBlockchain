import socket
import os

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("127.0.0.2", 8888))
    serversocket.listen(0)

    # Child Process
    if os.fork() == 0:
        accept_conn("child", serversocket)

    accept_conn("parent", serversocket)

def accept_conn(message, s):
    while True:
        c, addr = s.accept()
        print(addr)
        print('Got connection from in {0}').format(message) 
        c.send('Thank you for your connecting to %s\n' % message)
        c.close()

if __name__ == "__main__":
    main()
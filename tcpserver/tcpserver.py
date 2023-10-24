import socket
import time
import threading
import atexit

global sock

def do_work(conn_socket):
    buff = conn_socket.recv(1024)
    print(buff)
    time.sleep(5)
    conn_socket.send(b'HTTP/1.1 200 OK\r\n\r\nHello, World!\r\n')
    conn_socket.close()

def close_socket():
    sock.close()

def main():
    global sock
    atexit.register(close_socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET is the address family for IPv4, SOCK_STREAM is the socket type for the TCP protocol
    sock.bind(('localhost', 1800)) # values passed to bind depend on the address family. For IPv4 it accepts a hostname and port
    sock.listen()
    all_threads = []
    while True:
        conn_socket, addr = sock.accept()
        print(addr)
        th = threading.Thread(target=do_work, args=[conn_socket])
        all_threads.append(th)
        th.start()

if __name__ == '__main__':
    main()
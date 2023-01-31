# This is a sample Python script.
import socket
from multiprocessing import Process, Queue
from readchar import readkey, key
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

username = ''


def byte_string_decode(byte_string):
    return byte_string.decode('utf-8')


def wait_for_messages(q, sock):
    msg = sock.recv(1024)
    q.put(byte_string_decode(msg))


def try_connect(sock):
    try:
        sock.connect(('localhost', 55000))
    except TimeoutError:
        while True:
            print('Connection failed, press Enter and try again\n')
            k = readkey()
            if k == key.ENTER:
                break
        try_connect(sock)


def spawn_process(sock):
    q = Queue()
    p = Process(target=wait_for_messages, args=(q, sock,))
    p.start()
    return q


def set_username(sock):
    username = input('Hello, Guest! Please provide your Username so that we can identify you.\n')
    sock.send(bytes(f'[{username}]', encoding='UTF-8'))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try_connect(sock)
    set_username(sock)
    q = spawn_process(sock)
    while True:
        msg_to_send = input()
        msg_received = q.get()
        print(msg_received)
        sock.send(bytes(f'[{username}] {msg_to_send}', encoding='UTF-8'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# This is a sample Python script.
import socket
import time
import threading
import queue
from readchar import readkey, key
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

username = ''


def byte_string_decode(byte_string):
    return byte_string.decode('utf-8')


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


def read_kb_input(q):
    while True:
        input_str = input()
        q.put(input_str)


def set_username(sock):
    username = input('Hello, Guest! Please provide your Username so that we can identify you.\n')
    sock.send(bytes(f'[{username}]', encoding='UTF-8'))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try_connect(sock)
    set_username(sock)
    q = queue.Queue()
    p = threading.Thread(target=read_kb_input, args=(q,), daemon=True)
    p.start()
    while True:
        if q.qsize() > 0:
            msg_typed = q.get()
            print(msg_typed)
            sock.send(bytes(f'[{username}] {msg_typed}', encoding='UTF-8'))
        #  new_chat_msg = byte_string_decode(sock.recv(1024))
        #  print(new_chat_msg)
        time.sleep(0.01)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

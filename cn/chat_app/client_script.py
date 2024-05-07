'''
USAGE: move to this folder where server_script.py and client_script.py is present

Both the server and client script can then be run
   from the Command prompt (in Windows) or from bash
   Terminal (Linux users) by simply typing

   "python server_script.py"

    1st client python client_script.py  ".
    2nd client python client_script.py  ".
    3rd client python client_script.py  ".
    .   ...    ...
    .   ...    ...
    .   ...    ...

'''

import socket
import threading

def send():
    while True:
        msg = input('\nMe > ')
        cli_sock.send(msg.encode())  # Encode the message before sending

def receive():
    while True:
        sen_name = cli_sock.recv(1024).decode()  # Decode received data
        data = cli_sock.recv(1024).decode()  # Decode received data

        print('\n' + sen_name + ' > ' + data)

if __name__ == "__main__":
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023
    cli_sock.connect((HOST, PORT))
    print('Connected to remote host...')
    uname = input('Enter your name to enter the chat > ')
    cli_sock.send(uname.encode())  # Encode the username before sending

    thread_send = threading.Thread(target=send)
    thread_send.start()

    thread_receive = threading.Thread(target=receive)
    thread_receive.start()

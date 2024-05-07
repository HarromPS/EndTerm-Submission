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

def accept_client():
    while True:
        # accept
        cli_sock, cli_add = ser_sock.accept()
        uname = cli_sock.recv(1024).decode()  # Decode received data
        CONNECTION_LIST.append((uname, cli_sock))
        print('%s is now connected' % uname)
        thread_client = threading.Thread(target=broadcast_usr, args=[uname, cli_sock])
        thread_client.start()

def broadcast_usr(uname, cli_sock):
    while True:
        try:
            data = cli_sock.recv(1024).decode()  # Decode received data
            if data:
                print("{0} spoke".format(uname))
                b_usr(uname, data)
        except Exception as e:
            print("Error:", e)
            break

def b_usr(sen_name, msg):
    for client in CONNECTION_LIST:
        if client[0] != sen_name:
            client[1].send((sen_name + ": " + msg).encode())  # Add delimiter and encode message before sending

if __name__ == "__main__":
    CONNECTION_LIST = []

    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 5023
    ser_sock.bind((HOST, PORT))

    # listen
    ser_sock.listen(1)
    print('Chat server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target=accept_client)
    thread_ac.start()

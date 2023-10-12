import socket,os,time
from argparse import ArgumentParser
from jsonutils import jsonfile
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("127.0.0.1", 2020)
timeout = 500


def data_handler(response : bytes):
    data = jsonfile.loads(response.decode().replace('\'','\"'))
    print(data)

def send(data : bytes,flags : int = None):
    try:
        client.connect(address)
        client.send(data,flags if flags is not None else ...)
        client.close()
    except ConnectionRefusedError as e:
        print(e)

def receive():
    client.bind(address)
    client.listen(1)
    started_at = time.time()
    data = None

    while data is None and (time.time() - started_at) < timeout: 
        #stop the connection when data is ! None or the time passed is greater than timeout.
        server_socket, addr = client.accept()
        if addr[0] == '127.0.0.1':
            data = server_socket.recv(1024)
            data_handler(data)

        server_socket.close()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('action',choices=['send','sendreceive','receive'],type=str,help='')
    parser.add_argument('command',choices=['say'],type=str,help='')
    parser.add_argument('arguments',type=str,help='')

    args = parser.parse_args()

    if args.action =='send':
        print(args.args)
        command = f'{args.command}{args.args}'
        print(command)
        send(command.encode())
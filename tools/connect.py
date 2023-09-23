import socket, os


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("127.0.0.1", 2020)


def send(data : bytes,flags : int = None):
    client.connect(address)
    client.send(data,flags if flags is not None else ...)
    client.close()

def receive():
    pass



if __name__ == '__main__':
    pass
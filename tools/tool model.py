import socket,sys
import argparse

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#address = ("127.0.0.1", 4040)

def send_command(args : argparse.Namespace):
    try:
        command = {}
        sender.connect((args.address,args.port))
        sender.send(str(command).encode())
        sender.close()
    except AssertionError as e:
        print(e)
        return 1
    else:
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interazione')
    parser.add_argument('--address','-addr',default="127.0.0.1", type=str, help='IP address (0.0.0.0) default: (127.0.0.1).')
    parser.add_argument('--port','-p',default=4040, type=int, help='Port (0000) default: (4040).')
    sys.exit(send_command(parser.parse_args()))
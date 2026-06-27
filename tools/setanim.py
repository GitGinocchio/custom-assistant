import socket,sys
import argparse

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#address = ("127.0.0.1", 4040)

def send_request(args : argparse.Namespace):
    try:
        assert str(args.animation).endswith('.anim') or str(args.animation).endswith('.tanim')
        command = {"type" : "setanim","anim" : args.animation}
        client.connect((args.address,args.port))
        client.send(str(command).encode())
        client.close()
    except Exception as e:
        print(e)
        return 1
    else:
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interazione con setanim.')
    parser.add_argument('--address','-addr',default="127.0.0.1", type=str, help='IP address (0.0.0.0) default: (127.0.0.1).')
    parser.add_argument('--port','-p',default=4040, type=int, help='Port (0000) default: (4040).')
    parser.add_argument('animation', type=str, help='Animation file to be used with extension .anim or .tanim.')
    sys.exit(send_request(parser.parse_args()))
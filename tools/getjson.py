import socket,sys
import argparse

send_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_request(args : argparse.Namespace):
    try:
        command = {
            "type": "getjson",
            "filename" : args.filename,
            "keys" : args.keys
        }
        send_client.connect((args.address,args.port))
        send_client.send(str(command).encode())
        send_client.close()
    except Exception as e:
        print(e)
        return 1
    else:
        try:
            receive_client.bind((args.address, 2020))
            receive_client.listen(1)
            response_socket, addr = receive_client.accept()
            if addr[0] == '127.0.0.1':
                data = response_socket.recv(1024)
                print(data.decode('utf-8'))
            response_socket.close()

        except Exception as e:
            print(e)
            return 1
        else:
            return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interazione con jsonfile.')
    parser.add_argument('--address','-addr',default="127.0.0.1", type=str, help='IP address (0.0.0.0) default: (127.0.0.1).')
    parser.add_argument('--port','-p',default=4040, type=int, help='Port (0000) default: (4040).')
    parser.add_argument('filename', type=str, help='File json da aprire per ottenerne i dati.')
    parser.add_argument('-keys','-k', nargs='*', type=str, default=[], help='Inserisci le chiavi dei valori che vuoi ottenere')
    sys.exit(send_request(parser.parse_args()))
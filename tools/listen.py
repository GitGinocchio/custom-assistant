import socket,sys
import argparse

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#address = ("127.0.0.1", 4040)

def send_request(args : argparse.Namespace):
    try:
        command = {
            "type":"listen",
            "triggers" : args.triggers,
            "min_confidence": args.min_confidence,
            "threshold_factor" : args.threshold_factor,
            "timeout" : args.timeout,
            "silence_duration" : args.silence_duration
        }
        client.connect((args.address,args.port))
        client.send(str(command).encode())
        client.close()
    except Exception as e:
        print(e)
        return 1
    else:
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interazione con Listen.')
    parser.add_argument('--address','-addr',default="127.0.0.1", type=str, help='IP address (0.0.0.0) default: (127.0.0.1).')
    parser.add_argument('--port','-p',default=4040, type=int, help='Port (0000) default: (4040).')
    parser.add_argument('-triggers','-t',nargs='*',type=str, default=[], help='Una lista di stringhe che devono essere presenti nella frase riconosciuta per dare un output valido (se non presente ogni output e\' valido). Default: []')
    parser.add_argument('-min_confidence','-minc', type=float, default=0.0,help='Il minimo valore di confidence che puo\' essere accettato per ottenere un risultato valido (se non e\' presente ogni output e\' valido). Default: None')
    parser.add_argument('-threshold_factor','-tf', type=float, default=0.1,help='Il fattore di threshold utilizzato nel calcolo della massima ampiezza dell\'audio. Default: 0.1')
    parser.add_argument('-min_time','-mint', type=float, default=0.0,help='Il minimo tempo della registrazione in secondi. Default: 0.0')
    parser.add_argument('-timeout','-to', type=float, default=0.0,help='Il tempo massimo in secondi della durata della registrazione. Default: None')
    parser.add_argument('-silence_duration','-sd', type=float, default=2.0,help='il tempo massimo in secondi in cui e\' presente silenzio. Default: 2.0')
    sys.exit(send_request(parser.parse_args()))
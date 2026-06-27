from PyQt5.QtCore import pyqtSignal, QThread
import socket



class SocketConnection(QThread):
    def __init__(self,*,ip : str = '127.0.0.1', receiveport : int = 4040, sendport : int = 2020, parent=None):
        super().__init__(parent)
        self.receiveport, self.sendport, self.ip = receiveport, sendport, ip
        self.receiversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiversocket.bind((self.ip, self.receiveport))
        self.sendersocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = False

    def run(self):
        self.active = True
        self.receiversocket.listen(1)
        
        while self.active:
            receivedsocket, addr = self.receiversocket.accept()
            if addr[0] == self.ip:
                data = receivedsocket.recv(1024)
                self.handle_data(data)
            receivedsocket.close()

    def stop(self): self.active = False

    def send(self, data : bytes):
        self.sendersocket.connect((self.ip, self.sendport))
        self.sendersocket.send(data)
        self.sendersocket.close()

    def handle_data(self, response : bytes):
        try:
            response = dict(self.parent().jsonthread.jsonfile.loads(response.decode().replace('\'', '\"')))
            if response['type'] == 'say':
                self.parent().saythread.say(response['sentence'],response['volume'])
            elif response['type'] == 'listen':
                input = self.parent().listenthread._listenfunction(triggers=response['triggers'],min_confidence=response['min_confidence'],threshold_factor=response["threshold_factor"],timeout=response["timeout"],silence_duration=response["silence_duration"])
                print(input)
                self.send(str(input).encode('utf8'))
            elif response['type'] == 'getjson':
                value = self.parent().jsonthread.getvalue(response["filename"],response["keys"])
                print(value)
                self.send(str(value).encode('utf8'))
        except Exception as e: print(e)
from PyQt5.QtCore import pyqtSignal, QThread
from listen import Listener
from ai import Ai
from say import TTS
from NLPTS import NLPTS
from jsonutils import jsonfile
import os,time,subprocess,socket

#Vorrei spostare qui tutte le animazioni perche' rallentano il programma..

#from QAnimations import Animation,ThresholdAnimation
#loadinganim = Animation(self,'loading.anim',color=(0,255,0))
#waveanim = Animation(self,'wave.anim',color=(0,255,0))
#thresholdanim = ThresholdAnimation(self,'threshold.anim',color=(0,255,0),fn=self.listenthread.L.get_microphone_threshold,values=[0.007,0.01,0.03,0.05,0.07,0.1,0.3,0.5])



#threads
class ListengThread(QThread):
    listenthreadsignal = pyqtSignal(tuple)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.L = Listener(lang='it-IT')

    def listen(self):
        prompt = None
        while prompt is None:
            print('listening...')
            prompt, info = self.L.listen(triggers=['google','ehi google'],min_confidence=0.9,threshold_factor=0.7,silence_duration=1.5,timeout=5,min_time=0)
            if prompt is not None:
                return (prompt, info)

    def run(self):
        self.parent().thresholdanim.start() #start threshold animation of system tray icon.
        prompt = None
        while prompt is None:
            print('listening...')
            prompt, info = self.L.listen(triggers=['google','ehi google'],min_confidence=0.9,threshold_factor=0.7,silence_duration=1.5,timeout=5,min_time=0)
            if prompt is not None:
                self.listenthreadsignal.emit((prompt,info))
                prompt = None
                self.parent().thresholdanim.stop()
                self.parent().loadinganim.start()

#utilizzare la classe SayThread per implementare TTS (meglio un thread separato da SocketConnection)
#questo e' utile anche perche' posso fare delle animazioni specifiche per questo processo...
class SayThread(QThread):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.tts = TTS(lang='it',tld='com')
    
    def run(self):pass



class ProcessingThread(QThread):
    #processingthreadsignal = pyqtSignal(tuple)
    def __init__(self,parent=None,device : str = 'cpu',model : str = 'latest'):
        super().__init__(parent)
        models = [model for model in os.listdir('../models')]
        models.sort(key=lambda x: str(os.path.basename(x)).split('.')[:2],reverse=True)
        self.ai = Ai(datafp=os.path.join('../models',models[0] if model == 'latest' else model),device=device)
        self.nlpts = NLPTS(os.path.join('../models',models[0] if model == 'latest' else model),['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|'])

    def run(self): pass

    def process(self, data):
        timer = time.time()
        try:
            tag,prob = self.ai.process(data[0])
            content = jsonfile(r'..\commands\{}\config.json'.format(tag))
            assert content['enabled'], "command disabled."
            info = self.nlpts.find(self.nlpts.parse_and_tokenize(data[0]),tag=tag)
            cmd = [r'..\commands\{}\{}'.format(tag,content['autorun']),data[0],info if info is not None else '',*list(content['args'])]
        except AssertionError: pass
        except Exception as e: print(e)
        else:
            try:
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True,shell=content['shell'])
                print('----------------------------------------------------------------')
                print("(autorun start execute) time: ",time.time() - timer)
                print(cmd)
                process.wait()
            except subprocess.CalledProcessError as e:
                print("Process error: ",e)
            except subprocess.TimeoutExpired as e:
                print("Timeout expired: ",e)
            except Exception as e:
                print("Anomalous error occurred {}".format(e))
            finally:
                #print("pid:",process.pid,"returncode:",process.returncode,"stderr:",process.stderr.read())
                try:
                    with open("..\commands\{}\logs.log".format(tag),'a',encoding='utf-8') as logfile:
                        log = "\n[{}] [pid: {}] [returncode: {}] : {}".format(time.strftime('%Y-%m-%d %H:%M:%S'),process.pid,process.returncode,str(process.stderr.read()).replace('\n',' '))
                        logfile.write(log)
                except Exception as e:
                    print(e)

                print("(total execute) time: ",time.time() - timer)
                print('----------------------------------------------------------------')
                self.parent().thresholdanim.start()



class SocketConnection(QThread):
    def __init__(self,parent=None,rport : int = 4040,sport : int = 2020):
        super().__init__(parent)
        self.rport, self.sport = rport, sport

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", self.rport))
        self.server_socket.listen(1)
        
        while True:
            client_socket, addr = self.server_socket.accept()
            if addr[0] == '127.0.0.1':
                data = client_socket.recv(1024)
                self.handle_data(data)
            client_socket.close()
    
    def send(self, data : bytes):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", self.sport))
        client_socket.send(data)
        client_socket.close()

    def handle_data(self, response : bytes):
        try:
            response = dict(jsonfile.loads(response.decode().replace('\'', '\"')))
            if response['type'] == 'say':
                print(response)
                #self.parent().tts.say(response['sentence'],response['volume'])

        except Exception as e: print(e)
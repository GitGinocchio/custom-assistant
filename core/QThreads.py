from PyQt5.QtCore import pyqtSignal, QThread
from ai import Ai
from NLPTS import NLPTS
from jsonutils import jsonfile
import os,time,subprocess,socket

#>>> say
import gtts
import soundfile as sf
import sounddevice as sd
from scipy import signal
import time,os,io,numpy as np
#<<< say
#>>> listen
import speech_recognition
#<<< listen



#threads
"""
class ListeningThread(QThread):
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
"""

class ListeningThread(QThread):
    listenthreadsignal = pyqtSignal(tuple)
    def __init__(self,parent=None,device : int | str = None,lang : str = 'en-US',triggers : list[str] = [],min_confidence : float = None,nretry : int = -1,threshold_factor : float = 0.1, min_time : float = 0.0,timeout : float = None, silence_duration : float = 2.0, wait : bool = True):
        super().__init__(parent)
        self.device = sd.query_devices(device if device is not None else sd.default.device[0],'input')
        self.recognizer = speech_recognition.Recognizer()
        self.lang = lang
        self.triggers = triggers
        self.min_confidence = min_confidence
        self.nretry = nretry
        self.threshold_factor = threshold_factor
        self.min_time = min_time
        self.timeout = timeout
        self.silence_duration = silence_duration
        self._wait = wait
        self.streams = []

    def run(self):
        self.parent().thresholdanim.start() #start threshold animation of system tray icon.
        prompt = None
        while prompt is None:
            print('listening...')
            prompt, info = self._listenfunction(triggers=self.triggers,min_confidence=self.min_confidence,nretry=self.nretry,threshold_factor=self.threshold_factor,min_time=self.min_time,timeout=self.timeout,silence_duration=self.silence_duration,wait=self._wait)
            if prompt is not None:
                self.listenthreadsignal.emit((prompt,info))
                prompt = None
                self.parent().thresholdanim.stop()

    def get_microphone_threshold(self,duration=0.1,*,device : int = None):
        audio = sd.rec(int(duration * int(self.device['default_samplerate'])),samplerate=int(self.device['default_samplerate']),channels=int(self.device['max_input_channels']),device=device if device is not None else self.device['index'])
        sd.wait()
        return audio.max()

    def _listenfunction(self,*,triggers : list[str] = [],min_confidence : float = None,nretry : int = -1,threshold_factor : float = 0.1, min_time : float = 0.0,timeout : float = None, silence_duration : float = 2.0, wait : bool = True,with_animations : bool = True):
        start = time.time()
        
        Input = None
        confidence = None
        recording = []
        max_amplitude = 0.0
        silence_timer = None
        finished = False

        def callback(indata, frames, sd_time, status):
            nonlocal finished,max_amplitude,silence_timer
            recording.append(indata.copy())

            current_max = np.max(np.abs(indata))
            max_amplitude = max(current_max, max_amplitude)

            #print(current_max, max_amplitude)

            if current_max <= max_amplitude * threshold_factor and (time.time() - start) >= min_time: 
                if silence_timer is None:
                    silence_timer = time.time()
            else:
                silence_timer = None
            
            if silence_timer is not None and (time.time() - silence_timer) >= silence_duration: #stoppa l'ascolto se il tempo di silenzio ha superato il limite
                finished = True
                raise sd.CallbackStop()
            
            if timeout is not None and (time.time() - start) >= timeout: #stoppa l'ascolto se viene superato il tempo limite
                finished = True
                raise sd.CallbackStop()

        def finished_callback():
            nonlocal finished
            if finished: self.streams.remove(stream)

        stream = sd.InputStream(samplerate=int(self.device['default_samplerate']),device=self.device['index'],channels=int(self.device['max_input_channels']),callback=callback,finished_callback=finished_callback)

        try: stream.start()
        except sd.PortAudioError as e: stream = None
        else: self.streams.append(stream)

        if wait:
            try:
                while stream.active: pass
                filelike = io.BytesIO() #sf.SoundFile()
                sf.write(filelike,np.concatenate(recording),int(stream.samplerate),format='WAVEX') #filelike.write(np.concatenate(recording).tobytes())
                filelike.seek(0)

                audiodata = speech_recognition.AudioData(filelike.read(), int(stream.samplerate), stream.samplesize)
                data = self.recognizer.recognize_google(audiodata,language=self.lang,show_all=True) #with_confidence=True

                if len(data) != 0:
                    Input = (data['alternative'][0]['transcript']).lower()
                    confidence = (data['alternative'][0]['confidence'])

                    if triggers and not any(trigger.lower() in Input.lower() for trigger in triggers): Input = None
                    
                    if min_confidence is not None and min_confidence > confidence: Input = None
            except speech_recognition.RequestError as e:
                print("Api Error: {}".format(e))
                print("Details: {}: {}, {}: {}, {}: {}".format("Input", Input,"confidence", confidence,"0:10b",audiodata.get_raw_data()[0:10]))
        
        return (Input, {'stream' : stream,'confidence' : confidence, 'duration_recording': float(time.time() - start),'samplerate' : int(self.device['default_samplerate']),'channels' : int(self.device['max_input_channels'])})

    def stop(self, stream : sd.InputStream = None):
        """
        stream: OutputStream, optional
            if stream is None will stopped the first stream of the list of streams\n
            else will be stopped the stream specified...
        """
        try:
            assert len(self.streams) != 0, "There are no streams to stop"
            if stream is not None:
                stream_index = self.streams.index(stream)
                self.streams[stream_index].stop()
            else:
                self.streams[0].stop()
        except Exception as e: pass

    def remove(self, stream : sd.InputStream = None):
        """
        stream: OutputStream, optional
            if stream is None will removed the first stream of the list of streams\n
            else will be removed the stream specified...
        """
        try:
            assert len(self.streams) != 0, "There are no streams to stop"
            if stream is not None:
                self.streams.remove(stream)
            else:
                self.streams.pop(0)
        except Exception as e: pass



#utilizzare la classe SayThread per implementare TTS (meglio un thread separato da SocketConnection)
#questo e' utile anche perche' posso fare delle animazioni specifiche per questo processo...
class SayThread(QThread):
    saythreadsignal = pyqtSignal(dict)
    def __init__(self,parent=None, device : str | int | None = None, lang : str = 'en',tld : str = 'com',slow : bool = False):
        super().__init__(parent)
        self.device = sd.query_devices(device if device is not None else sd.default.device[1],'output')
        self.lang = lang
        self.tld = tld
        self.slow = slow
        self.streams = []
    
    def run(self): pass

    def say(self,sentence : str,volume : float = 1.0, wait : bool = True):
        assert volume >= 0.01 and volume <= 5.0, "Invalid volume level, level must be between 0.01 and 5.0"
        
        tts = gtts.gTTS(text=sentence, lang=self.lang, tld=self.tld, slow=self.slow,lang_check=True)
        fileobj = io.BytesIO()
        tts.write_to_fp(fileobj)
        fileobj.seek(0)

        audiodata, sr_audiodata = sf.read(fileobj, dtype='float32')
        audiodata = np.expand_dims(audiodata, axis=1) if audiodata.ndim == 1 else audiodata
        samplerate = self.device['default_samplerate'] if sr_audiodata > self.device['default_samplerate'] else sr_audiodata
        audiodata = signal.resample(audiodata, int(len(audiodata) * self.device['default_samplerate'] / sr_audiodata)) if sr_audiodata > self.device['default_samplerate'] else audiodata
        audiodata *= volume
        duration = len(audiodata) / samplerate

        frame = 0
        finished = False

        def callback(outdata, frames, time, status):
            nonlocal frame,finished

            self.saythreadsignal.emit({"threshold": np.max(np.abs(outdata)),"frames": frames,"frame" : frame,"time" : time,"status" : status})
            chunksize = min(len(audiodata) - frame, frames)
            outdata[:chunksize] = audiodata[frame:frame + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                finished = True
                raise sd.CallbackStop()
            frame += chunksize

        def finished_callback():
            nonlocal finished
            if finished: pass
            else: pass

        stream = sd.OutputStream(float(samplerate),device=self.device['index'],channels=self.device['max_output_channels'],callback=callback,finished_callback=finished_callback)

        try:
            stream.start()
        except sd.PortAudioError as e:
            print(e)
            stream = None
        else:
            self.streams.append(stream)

        if wait: time.sleep(duration)
        return (duration), {'stream': stream,'samplerate' : samplerate,'channels' : self.device['max_output_channels']}



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
                self.parent().saythread.say(response['sentence'],response['volume'])
            elif response['type'] == 'listen':
                pass
                #self.parent().listenthread.listen()

        except Exception as e: print(e)
from PyQt5.QtCore import pyqtSignal, QThread
import nltk,torch,torch.nn as nn,numpy as np,os,time,subprocess,socket,io,soundfile as sf,sounddevice as sd,speech_recognition,gtts,json
from datetime import datetime
from nltk.stem.porter import PorterStemmer
from torch.utils.data import Dataset, DataLoader
from scipy import signal



class ListenThread(QThread):
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
        prompt = None
        while prompt is None:
            print('listening...')
            prompt, info = self._listenfunction(triggers=self.triggers,min_confidence=self.min_confidence,nretry=self.nretry,threshold_factor=self.threshold_factor,min_time=self.min_time,timeout=self.timeout,silence_duration=self.silence_duration,wait=self._wait)
            if prompt is not None:
                self.listenthreadsignal.emit((prompt,info))
                prompt = None

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

class JsonThread(QThread):
    jsonthreadsignal = pyqtSignal(dict)
    def __init__(self,parent=None):
        super().__init__(parent)

    class jsonfile:
        def __init__(self,fp : str = None,*,indent : int = 3,encoding : str = 'utf-8',autosave : bool = True):
            assert fp.endswith('.json'),'fp must be a json file and end with ".json"'
            self.fp = fp
            self.indent = indent
            self.encoding = encoding
            self.autosave = autosave
            if os.path.exists(self.fp):
                with open(self.fp, 'r', encoding=encoding) as jsf: self.content = json.load(jsf)
            else: 
                self.content = {}
                if self.autosave: self.save()

        def __str__(self):
            return str(self.content)

        def __len__(self):
            return len(self.content)

        def __contains__(self, __k):
            return __k in self.content

        def __getitem__(self, __k):
            if __k in self.content: return self.content[__k]
            else: raise KeyError(f"Key '{__k}' not found in JSON data.")

        def __setitem__(self, __k, __v):
            self.content[__k] = __v
            if self.autosave:self.save()

        def __delitem__(self, __k):
            if __k in self.content:
                del self.content[__k]
                if self.autosave:self.save()
            else:
                raise KeyError(f"Key '{__k}' not found in '{self.fp}'.")

        def __iter__(self):
            return iter(self.content)

        def __next__(self):
            raise StopIteration

        def keys(self):
            return self.content.keys()

        def clear(self):
            self.content = {}
            if self.autosave: self.save()

        def loads(data : str | bytes):
            return dict(json.loads(data))

        def dumps(data : dict):
            return json.dumps(data)

        def save(self,content : dict = None):
            with open(self.fp, 'w',encoding=self.encoding) as jsf: json.dump(content if content is not None else self.content,jsf,indent=self.indent,ensure_ascii=True)

    def getvalue(self, fp : str, args : list[str]):
        content = self.jsonfile(fp)
        try:
            last_c = content
            for arg in args:
                last_c = last_c[arg]
        except ValueError | KeyError:
            return None
        else:
            return last_c

class AiThread(QThread):
    aithreadsignal = pyqtSignal(dict)
    def __init__(self,parent=None,device : str = 'cpu',model : int | str = 0,language : str = 'Italian',ignore_words : list[str] = []):
        super().__init__(parent)
        models = [model for model in os.listdir('../models')]
        models.sort(key=lambda x: str(os.path.basename(x)).split('.')[:2],reverse=True)
        if device == 'cuda' and not torch.cuda.is_available(): raise ValueError('Error: selected device is type CUDA but is not available.')
        self.data = torch.load(os.path.join('../models',models[model] if type(model) is int else model),encoding='utf-8')
        self.ignore_words = ignore_words
        self.language = language
        self.device = torch.device('cuda' if device == 'cuda' and torch.cuda.is_available() else 'cpu')
        self.stemmer = PorterStemmer()
        self.model = self.NeuralNet(self.data["input_size"], self.data["hidden_size"], self.data["output_size"]).to(self.device)
        self.model.load_state_dict(self.data["model_state"])
        self.model.eval()

    class NeuralNet(nn.Module):
        def __init__(self, input_size, hidden_size, num_classes):
            super(AiThread.NeuralNet, self).__init__()
            self.flatten = nn.Flatten()
            self.l1 = nn.Linear(input_size, hidden_size) 
            self.l2 = nn.Linear(hidden_size, hidden_size)
            self.l3 = nn.Linear(hidden_size, num_classes)
            self.relu = nn.ReLU(True)
        
        def forward(self, x):
            out = self.l1(x)
            out = self.relu(out)
            out = self.l2(out)
            out = self.relu(out)
            out = self.l3(out)
            
            return out

    def prediction(self,sentence : str,*, min_prob : float = None,preserve_line : bool = True):
        #for word in self.data['intents']["Callers"]: Sentence = Sentence.replace(word,'').strip()
        
        for word in self.ignore_words: sentence = sentence.replace(word,'')
        sentence = nltk.word_tokenize(sentence.lower(),language=self.language,preserve_line=preserve_line)
        stemmed = [self.stemmer.stem(word) for word in sentence]
        X = np.zeros(len(self.data['all_words']), dtype=np.float32)
        for idx, w in enumerate(self.data['all_words']):
            if w in stemmed: X[idx] = 1
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.data['tags'][predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > min_prob if min_prob is not None else float(self.data['benchmark']['min_prob']):
            for intent in self.data['intents']:
                if tag == intent["tag"]:
                    tokenized = []
                    [[tokenized.append(word) for word in nltk.word_tokenize(str(pattern).lower(),language=self.language,preserve_line=True) if word not in tokenized] for pattern in intent['patterns']]#lemmatizer.lemmatize(word)
                    stemmed = [self.stemmer.stem(word,to_lowercase=True) for word in tokenized]

                    for index in range(-1, -len(sentence)-1, -1):
                        if any(w == sentence[index] for w in tokenized) and any(sentence[index].find(w) for w in stemmed): # or any(sentence[index].find(w) for w in stemmed)
                            if index + 1 in range(-1,-len(sentence)-1,-1): 
                                return str(intent['tag']), float(prob.item()),' '.join(sentence[index + 1::])
                            else: 
                                return str(intent['tag']), float(prob.item()), None

        return None, float(prob.item()), None

class TrainAiThread(QThread):
    trainaithreadsignal = pyqtSignal(dict)
    def __init__(self,parent, commandspath : str,*,epochs : int, lr : float, hidden_size : int, device : str):
        super().__init__(parent)
        self.intents,self.tags,self.words,self.xy,self.x,self.y = [],[],[],[],[],[]
        for dir in os.listdir(commandspath):
            if os.path.isdir(os.path.join(commandspath,dir)):
                content = self.parent().jsonthread.jsonfile(os.path.join(commandspath,dir,'config.json'))
                self.intents.append({'tag' : dir,'patterns' : content['patterns']})
                self.tags.append(dir)
                for pattern in content['patterns']:
                    words = nltk.word_tokenize(pattern,language=self.parent().aithread.language,preserve_line=True)
                    self.words.extend(words)
                    self.xy.append((words, dir))
        self.words = sorted(set([self.parent().aithread.stemmer.stem(w) for w in self.words if w not in self.parent().aithread.ignore_words]))
        self.tags = sorted(set(self.tags))
        for (pattern_sentence, tag) in self.xy:
            bag = np.zeros(len(self.words), dtype=np.float32)
            for idx, w in enumerate(self.words):
                if w in [self.parent().aithread.stemmer.stem(word) for word in pattern_sentence]: bag[idx] = 1
            self.x.append(bag)
            self.y.append(self.tags.index(tag))
        #----------------------------------------------------------------
        self.epochs = epochs
        self.learning_rate = lr
        self.batch_size = int(len(np.array(self.x)[0]) ** 0.5)
        self.input_size = len(np.array(self.x)[0])
        self.hidden_size = hidden_size
        self.output_size = len(self.tags)
        #----------------------------------------------------------------
        self.device = torch.device('cuda' if device.lower() == 'cuda' and torch.cuda.is_available() else 'cpu')
        self.model = self.parent().aithread.NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.traindataset = DataLoader(dataset=self.ChatDataset(np.array(self.x),np.array(self.y)),batch_size=self.batch_size,shuffle=True,num_workers=0)
        self.testdataset = DataLoader(dataset=self.ChatDataset(np.array(self.x),np.array(self.y)),batch_size=self.batch_size,shuffle=True,num_workers=0)
        self.loss_params = {}
        self.loss = nn.CrossEntropyLoss(*self.loss_params)
        self.optim_params = {"lr" : self.learning_rate,"betas" : (0.9, 0.999),"eps" : 0.00000001,"weight_decay" : 0.01,"amsgrad" : True}
        self.optim = torch.optim.AdamW(params=self.model.parameters(),**self.optim_params)

    def run(self):
        total_labels = 0
        correct_labels = 0
        train_loss = 0
        test_loss = 0
        sumprobs = 0
        accuracy = 0

        for epoch in range(1,self.epochs + 1):
            for batch, (inputs, labels) in enumerate(self.traindataset):
                self.model.train()
                inputs = inputs.to(self.device)
                labels = labels.to(dtype=torch.long).to(self.device)

                outputs = self.model(inputs)
                loss = self.loss(outputs, labels)

                self.optim.zero_grad()
                loss.backward()
                self.optim.step()

                l, current = loss.item(), (batch + 1) * len(inputs)
                train_loss += loss.item()
                train_loss /= len(self.traindataset)

            with torch.no_grad():
                self.model.eval()
                for inputs, labels in self.testdataset:
                    inputs = inputs.to(self.device)
                    labels = labels.to(dtype=torch.long).to(self.device)

                    outputs = self.model(inputs)

                    loss = self.loss(outputs, labels)

                    test_loss += loss.item()

                    _, predicted = torch.max(outputs.data, dim=1)
                    total_labels += labels.size(0)
                    correct_labels += (predicted == labels).sum().item()
            
            sentence = nltk.word_tokenize('',language=self.parent().aithread.language,preserve_line=True)
            X = np.zeros(len(self.words), dtype=np.float32)
            for idx, w in enumerate(self.words):
                if w in [self.parent().aithread.stemmer.stem(word) for word in sentence]: X[idx] = 1
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(self.device)
            output = self.model(X)
            _, predicted = torch.max(output, dim=1)
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            sumprobs += prob.item()

            test_loss /= len(self.testdataset)
            accuracy = correct_labels / total_labels * 100
            
            data = {'epoch' : epoch,'train_loss' : train_loss,'test_loss' : test_loss,'min_prob' : sumprobs / epoch,'accuracy' : accuracy,'total_labels' : total_labels,'correct_labels' : correct_labels}
            self.trainaithreadsignal.emit(data)

        data = {'epoch' : self.epochs,'train_loss' : train_loss,'test_loss' : test_loss,'min_prob' : sumprobs / self.epochs,'accuracy' : accuracy,'total_labels' : total_labels,'correct_labels' : correct_labels}
        self.trainaithreadsignal.emit(data)

    class ChatDataset(Dataset):
        def __init__(self,X_train,Y_train):
            self.n_samples = len(X_train)
            self.x_data = X_train
            self.y_data = Y_train

        # support indexing such that dataset[i] can be used to get i-th sample
        def __getitem__(self, index):
            return self.x_data[index], self.y_data[index]

        # we can call len(dataset) to return the size
        def __len__(self):
            return self.n_samples

    def save(self, filename : str):
        data = {
        "intents" : self.intents,
        "model_state": self.model.state_dict(),
        "input_size": self.input_size,
        "hidden_size": self.hidden_size,
        "output_size": self.output_size,
        "all_words": self.all_words,
        "tags": self.tags,
        "benchmark": {
            "num_epochs" : self.epochs,
            "learning_rate" : self.learning_rate,
            "final_train_loss" : self.train_loss, 
            "final_test_loss" : self.test_loss,
            "accuracy" : f"{self.accuracy}%",
            "min_prob" : float(sum(self.probs_list)/len(self.probs_list)),
            "total_labels" : self.total_labels,
            "correct_labels" : self.correct_labels
            },
        "metadata" : {
            "datetime" : datetime.now().strftime('%d/%m%Y - %H:%M:%S')
        },
        "spec" : {
            "criterion" : str(type(self.loss)),
            "optimizer" : str(type(self.optim)),
            "criterion_params" : self.loss_params,
            "optimizer_params" : self.optim_params,
            "cuda_available" : torch.cuda.is_available(),
            "device_spec" : {"index" : self.device.index, "type" : self.device.type,"name" : ""}
        }

        }
        try:
            torch.save(data, "../models/{}.{}.{}.pth".format(datetime.now().day,datetime.now().month,datetime.now().year) if filename is None else filename)
        except Exception as e: print(e)

class StartProcessThread(QThread):
    processingthreadsignal = pyqtSignal(dict)
    def __init__(self,parent=None):
        super().__init__(parent)

    def process(self, data : tuple):
        timer = time.time()
        self.parent().animator.set_animation(r'D:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\ui\animations\loading.anim')
        try:
            tag,prob,info = self.parent().aithread.prediction(data[0])
            assert tag is not None, "tag is None"
            content = self.parent().jsonthread.jsonfile(r'..\commands\{}\config.json'.format(tag))
            assert content['enabled'], "command disabled."
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
            except subprocess.CalledProcessError as e: print("Process error: ",e)
            except subprocess.TimeoutExpired as e: print("Timeout expired: ",e)
            except Exception as e: print("Anomalous error occurred {}".format(e))
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
        finally:
            self.parent().animator.set_animation(r'D:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\ui\animations\threshold.tanim')

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
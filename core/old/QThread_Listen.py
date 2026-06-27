from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np,time,io,soundfile as sf,sounddevice as sd,speech_recognition

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
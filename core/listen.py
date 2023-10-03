import speech_recognition
import soundfile as sf
import sounddevice as sd
import time,os,io,numpy as np



class Listener:
    def __init__(self,device : int | str = None,lang : str = 'en-US'):
        self.device = sd.query_devices(device if device is not None else sd.default.device[0],'input')
        self.recognizer = speech_recognition.Recognizer()
        self.lang = lang
        self.streams = []

    def get_microphone_threshold(self,duration=0.1,*,device : int = None):
        audio = sd.rec(int(duration * int(self.device['default_samplerate'])),samplerate=int(self.device['default_samplerate']),channels=int(self.device['max_input_channels']),device=device if device is not None else self.device['index'])
        sd.wait()
        return audio.max()

    def listen(self,triggers : list[str] = [],min_confidence : float = None,nretry : int = -1,threshold_factor : float = 0.1, min_time : float = 0.0,timeout : float = None, silence_duration : float = 2.0, wait : bool = True):
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
    
        return Input, {'stream' : stream,'confidence' : confidence, 'duration_recording': float(time.time() - start),'samplerate' : int(self.device['default_samplerate']),'channels' : int(self.device['max_input_channels'])}

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

    def continue_listening(self, stream : sd.InputStream = None):
        """
        stream: OutputStream, optional
            if stream is None will played the first stream of the list of streams\n
            else will be played the stream specified...
        """
        try:
            assert len(self.streams) != 0, "There are no streams to play"

            if stream is not None:
                stream_index = self.streams.index(stream)
                self.streams[stream_index].start()
            else:
                self.streams[0].start()
        except Exception as e: 
            print(e)
            pass



if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    import argparse
    parser = argparse.ArgumentParser(description='Interazione con TTS.')
    parser.add_argument('-device','-d', type=str, default=None,help='Dispositivo di ingresso audio da utilizzare. (int [device index] | str [device name]) Default: il tuo dispositivo standard di ingresso')
    parser.add_argument('-lang','-l', type=str, default='en-US',help='Lingua che viene utilizzata per riconoscere le parole. Default: \'en-US\'')
    parser.add_argument('-triggers','-t',nargs='*',type=str, default=[], help='Una lista di stringhe che devono essere presenti nella frase riconosciuta per dare un output valido (se non presente ogni output e\' valido). Default: []')
    parser.add_argument('-min_confidence','-minc', type=float, default=None,help='Il minimo valore di confidence che puo\' essere accettato per ottenere un risultato valido (se non e\' presente ogni output e\' valido). Default: None')
    parser.add_argument('-threshold_factor','-tf', type=float, default=0.1,help='Il fattore di threshold utilizzato nel calcolo della massima ampiezza dell\'audio. Default: 0.1')
    parser.add_argument('-min_time','-mint', type=float, default=0.0,help='Il minimo tempo della registrazione in secondi. Default: 0.0')
    parser.add_argument('-timeout','-to', type=float, default=None,help='Il tempo massimo in secondi della durata della registrazione. Default: None')
    parser.add_argument('-silence_duration','-sd', type=float, default=2.0,help='il tempo massimo in secondi in cui e\' presente silenzio. Default: 2.0')

    args = parser.parse_args()

    l = Listener(args.device if args.device is None else int(args.device) if args.device.isnumeric() else args.device,args.lang)
    data = l.listen(args.triggers,args.min_confidence,-1,args.threshold_factor,args.min_time,args.timeout,args.silence_duration,True)
    print(data)

#python -u "d:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\listen.py" -l "it-IT" -t "Ginevra" -sd 0.5 -tf 0.05 -to 10
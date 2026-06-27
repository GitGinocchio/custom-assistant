from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np,time,io,soundfile as sf,sounddevice as sd,gtts
from scipy import signal



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
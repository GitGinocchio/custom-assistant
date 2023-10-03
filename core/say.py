import gtts
import soundfile as sf
import sounddevice as sd
from scipy import signal
import time,os,io,numpy as np

class TTS:
    def __init__(self,device : int | str | None, lang : str, tld : str, slow : bool):
        self.device = sd.query_devices(device if device is not None else sd.default.device[1],'output')
        self.lang = lang
        self.tld = tld
        self.slow = slow
        self.streams = []

    def say(self,sentence : str,volume : float = 1.0,wait : bool = True):
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

        current_frame = 0
        finished = False

        def callback(outdata, frames, time, status):
            nonlocal current_frame,finished
            if status: print('status: ',status)
            chunksize = min(len(audiodata) - current_frame, frames)
            outdata[:chunksize] = audiodata[current_frame:current_frame + chunksize]
            if chunksize < frames:
                outdata[chunksize:] = 0
                finished = True
                raise sd.CallbackStop()
            current_frame += chunksize

        def finished_callback():
            nonlocal finished
            if finished:
                pass
                #finished
            else:
                #stopped
                pass

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

def get_tlds(): 
    return ['com', 'ad', 'ae', 'com.af', 'com.ag', 'com.ai', 'al', 'am', 'co.ao', 'com.ar', 'as', 'at', 'com.au', 'az', 'ba', 'com.bd', 'be', 'bf', 'bg', 'com.bh', 'bi', 'bj', 'com.bn', 'com.bo', 'com.br', 'bs', 'bt', 'co.bw', 'by', 'com.bz', 'ca', 'cd', 'cf', 'cg', 'ch', 'ci', 'co.ck', 'cl', 'cm', 'cn', 'com.co', 'co.cr', 'com.cu', 'cv', 'com.cy', 'cz', 'de', 'dj', 'dk', 'dm', 'com.do', 'dz', 'com.ec', 'ee', 'com.eg', 'es', 'com.et', 'fi', 'com.fj', 'fm', 'fr', 'ga', 'ge', 'gg', 'com.gh', 'com.gi', 'gl', 'gm', 'gr', 'com.gt','gy', 'com.hk', 'hn', 'hr', 'ht', 'hu', 'co.id', 'ie', 'co.il', 'im', 'co.in', 'iq', 'is', 'it', 'je', 'com.jm', 'jo', 'co.jp', 'co.ke', 'com.kh', 'ki', 'kg', 'co.kr', 'com.kw', 'kz', 'la', 'com.lb', 'li', 'lk', 'co.ls', 'lt', 'lu', 'lv', 'com.ly', 'co.ma', 'md', 'me', 'mg', 'mk', 'ml', 'com.mm', 'mn', 'ms', 'com.mt', 'mu', 'mv', 'mw', 'com.mx', 'com.my', 'co.mz', 'com.na', 'com.ng', 'com.ni', 'ne', 'nl', 'no', 'com.np', 'nr', 'nu', 'co.nz', 'com.om', 'com.pa', 'com.pe', 'com.pg', 'com.ph', 'com.pk', 'pl', 'pn', 'com.pr', 'ps', 'pt', 'com.py', 'com.qa', 'ro', 'ru', 'rw', 'com.sa', 'com.sb', 'sc', 'se', 'com.sg', 'sh', 'si', 'sk', 'com.sl', 'sn', 'so', 'sm', 'sr', 'st', 'com.sv', 'td', 'tg', 'co.th', 'com.tj', 'tl', 'tm', 'tn', 'to', 'com.tr', 'tt', 'com.tw', 'co.tz', 'com.ua', 'co.ug', 'co.uk', 'com.uy', 'co.uz', 'com.vc', 'co.ve', 'vg', 'co.vi', 'com.vn', 'vu', 'ws', 'rs', 'co.za', 'co.zm', 'co.zw', 'cat']

def get_langs():
    return list(gtts.lang.tts_langs().keys())



if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    import argparse
    parser = argparse.ArgumentParser(description='Interazione con TTS.')

    parser.add_argument('sentence', type=str, help='Frase che viene inviata all\'API di google per ottenere un file audio.')
    parser.add_argument('-devices', action='store_true', default=False,help='Se mostrare a schermo tutti i dispositivi disponibili. (VIENE ESEGUITO SOLO QUESTO COMANDO.) Default: False')
    parser.add_argument('-device','-d', type=str, default=None,help='Dispositivo di uscita audio da utilizzare. (int [device index] | str [device name]) Default: your default output device')
    parser.add_argument('-lang','-l', type=(str), default='en',choices=get_langs(),help='Lingua da utilizzare per la pronuncia da parte dell\'API google. Default: \'en\' ')
    parser.add_argument('-tld', type=(str), default='com',choices=get_tlds(),help='Dominio di alto livello da utilizzare per l\'accento. Default: \'com\' ')
    parser.add_argument('-slow','-s', action='store_true', default=False,help='Se impostare la riproduzione della frase con una velocita\' piu\' lenta. Default: False')
    parser.add_argument('-volume','-v', type=float, default=1.0, help='Seleziona il volume per la riproduzione. Default: 1.0')

    args = parser.parse_args()

    if args.devices:
        devices_list = sd.query_devices()

        for device in devices_list:
            if device['max_output_channels'] > 0: print(f"{device['index']} - Name: {device['name']} Samplerate: {device['default_samplerate']} ")
    else:
        tts = TTS(args.device if args.device is None else int(args.device) if args.device.isnumeric() else args.device,args.lang,args.tld,args.slow)
        tts.say(args.sentence,args.volume,True)
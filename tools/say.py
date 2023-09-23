import soundfile as sf
import sounddevice as sd
import time,socket,io,numpy as np,gtts

#def get_tlds(): 
    #return ['com', 'ad', 'ae', 'com.af', 'com.ag', 'com.ai', 'al', 'am', 'co.ao', 'com.ar', 'as', 'at', 'com.au', 'az', 'ba', 'com.bd', 'be', 'bf', 'bg', 'com.bh', 'bi', 'bj', 'com.bn', 'com.bo', 'com.br', 'bs', 'bt', 'co.bw', 'by', 'com.bz', 'ca', 'cd', 'cf', 'cg', 'ch', 'ci', 'co.ck', 'cl', 'cm', 'cn', 'com.co', 'co.cr', 'com.cu', 'cv', 'com.cy', 'cz', 'de', 'dj', 'dk', 'dm', 'com.do', 'dz', 'com.ec', 'ee', 'com.eg', 'es', 'com.et', 'fi', 'com.fj', 'fm', 'fr', 'ga', 'ge', 'gg', 'com.gh', 'com.gi', 'gl', 'gm', 'gr', 'com.gt','gy', 'com.hk', 'hn', 'hr', 'ht', 'hu', 'co.id', 'ie', 'co.il', 'im', 'co.in', 'iq', 'is', 'it', 'je', 'com.jm', 'jo', 'co.jp', 'co.ke', 'com.kh', 'ki', 'kg', 'co.kr', 'com.kw', 'kz', 'la', 'com.lb', 'li', 'lk', 'co.ls', 'lt', 'lu', 'lv', 'com.ly', 'co.ma', 'md', 'me', 'mg', 'mk', 'ml', 'com.mm', 'mn', 'ms', 'com.mt', 'mu', 'mv', 'mw', 'com.mx', 'com.my', 'co.mz', 'com.na', 'com.ng', 'com.ni', 'ne', 'nl', 'no', 'com.np', 'nr', 'nu', 'co.nz', 'com.om', 'com.pa', 'com.pe', 'com.pg', 'com.ph', 'com.pk', 'pl', 'pn', 'com.pr', 'ps', 'pt', 'com.py', 'com.qa', 'ro', 'ru', 'rw', 'com.sa', 'com.sb', 'sc', 'se', 'com.sg', 'sh', 'si', 'sk', 'com.sl', 'sn', 'so', 'sm', 'sr', 'st', 'com.sv', 'td', 'tg', 'co.th', 'com.tj', 'tl', 'tm', 'tn', 'to', 'com.tr', 'tt', 'com.tw', 'co.tz', 'com.ua', 'co.ug', 'co.uk', 'com.uy', 'co.uz', 'com.vc', 'co.ve', 'vg', 'co.vi', 'com.vn', 'vu', 'ws', 'rs', 'co.za', 'co.zm', 'co.zw', 'cat']

#def get_langs():
    #return list(gtts.lang.tts_langs().keys())

def say(sentence : str,*, device : int | str = None, volume : float = 1.0, wait : bool = True, lang : str = 'it', tld : str = 'com', slow : bool = False,connect : bool = False):
    device = sd.query_devices(device if device is not None else sd.default.device[1],'output')
    tts = gtts.gTTS(text=sentence, lang=lang, tld=tld, slow=slow,lang_check=True)
    filelike = io.BytesIO()
    tts.write_to_fp(filelike)
    filelike.seek(0)

    #-----------------------------------------------------------------------------------------------------
    #audiodata, sr_audiodata = sf.read(filelike, dtype='float32',always_2d=True)
    #audiodata *= volume
    #duration = len(audiodata) / sr_audiodata #device['default_samplerate'] #samplerate
                    


        #audiodata = np.expand_dims(audiodata, axis=1) if audiodata.ndim == 1 else audiodata
        #samplerate = device['default_samplerate'] if sr_audiodata > device['default_samplerate'] else sr_audiodata
        #audiodata = signal.resample(audiodata, int(len(audiodata) * device['default_samplerate'] / sr_audiodata)) if sr_audiodata > device['default_samplerate'] else audiodata
        #print(f"device: {device}")
        #print(f'sr-audiodata: {sr_audiodata},sr-device: {device["default_samplerate"]},final sr: {samplerate}, duration: {duration}')
    #-----------------------------------------------------------------------------------------------------
    audiodata, sr_audiodata = sf.read(filelike, dtype='float64')
    audiodata *= volume
    audiodata = np.expand_dims(audiodata, axis=1) if audiodata.ndim == 1 else audiodata
    duration = len(audiodata) / sr_audiodata
    #-----------------------------------------------------------------------------------------------------
    
    frame = 0
    finished = False

    def callback(outdata, frames, time, status):
        nonlocal frame,finished
        #if status: print('status: ',status)

        if connect:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("127.0.0.1", 4040))
                client.send(str({"type" : "threshold", "value" : np.max(np.abs(outdata))}).encode('utf-8'))
                client.close()
            except ConnectionRefusedError as e:
                print(e)

        chunksize = min(len(audiodata) - frame, frames)
        outdata[:chunksize] = audiodata[frame:frame + chunksize]
        if chunksize < frames:
            outdata[chunksize:] = 0
            finished = True
            raise sd.CallbackStop()
        frame += chunksize

    def finished_callback():
        nonlocal finished
        if finished: 
            stream.stop()
            stream.close()
        else: pass
                                        #samplerate
    try: stream = sd.OutputStream(float(sr_audiodata),device=device['index'],channels=device['max_output_channels'],callback=callback,finished_callback=finished_callback)
    except sd.PortAudioError as e: print(e)
    else:
        try: 
            stream.start()
        except sd.PortAudioError as e: 
            print(e)
        else:
            if wait: time.sleep(duration)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Interazione con TTS.')

    parser.add_argument('sentence', type=str, help='Frase che viene inviata all\'API di google per ottenere un file audio.')
    parser.add_argument('--device','-d', type=str, default=None,help='Dispositivo di uscita audio da utilizzare. (int [device index] | str [device name]) Default: your default output device')
    parser.add_argument('--lang','-l', type=(str), default='it',help='Lingua da utilizzare per la pronuncia da parte dell\'API google. Default: \'en\' ')
    parser.add_argument('--tld', type=(str), default='com',help='Dominio di alto livello da utilizzare per l\'accento. Default: \'com\' ')
    parser.add_argument('--slow','-s', action='store_true', default=False,help='Se impostare la riproduzione della frase con una velocita\' piu\' lenta. Default: False')
    parser.add_argument('--connect','-c', action='store_true', default=False,help='Se impostare una comunicazione con il programma principale. Default: False')
    parser.add_argument('--volume','-v', type=float, default=1.0, help='Seleziona il volume per la riproduzione. Default: 1.0')

    args = parser.parse_args()
    say(args.sentence,device=args.device,volume=args.volume,wait=True,lang=args.lang,tld=args.tld,slow=args.slow,connect=args.connect)
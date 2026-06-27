
from ast import Pass
import time
from datetime import datetime
from time import sleep
import wikipedia
from os import kill
import os
import pyttsx3
import subprocess
from speech_recognition import Recognizer, Microphone
import pandas as pd 
import numpy as np
from pandas import read_excel


start1 = time.time()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[-1].id)
r = Recognizer()
print("The time used to execute this is given below")
end = time.time()
time_passed = (end - start1)
print(time_passed)

###FILE DATI###
dr = pd.read_excel(r'Settings.xlsx')
dt = pd.DataFrame(dr)

ds = pd.read_excel(r'CachedApp.xlsx')
df = pd.DataFrame(ds)


def inizio_value():
    inizio_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE INIZIALE" ]))
    inizio_value = str.strip(inizio_value.replace("Name: VALUE, dtype: bool",""))
    inizio_value = inizio_value[5::]

    if inizio_value == "True" :
        def inizio():
            inizio =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE INIZIALE" ]))
            inizio = str.strip(inizio.replace("Name: OBJECT, dtype: object",""))
            inizio = inizio[5::]
            print (inizio)
            print("")
            engine.say (inizio)
            engine.runAndWait()
            inizio()
    else:
        pass
inizio_value()

def ascolto_value():
    ascolto_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
    ascolto_value = str.strip(ascolto_value.replace("Name: VALUE, dtype: bool",""))
    ascolto_value = ascolto_value[5::]

    if ascolto_value == "True" :
        def ascolto():
            ascolto =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
            ascolto = str.strip(ascolto.replace("Name: OBJECT, dtype: object",""))
            ascolto = ascolto[5::]
            print (ascolto)
            #engine.say (ascolto)
            #engine.runAndWait()
        ascolto()
    else:
        pass

def richiesta_value():
    richiesta_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
    richiesta_value = str.strip(richiesta_value.replace("Name: VALUE, dtype: bool",""))
    richiesta_value = richiesta_value[5::]

    if richiesta_value == "True" :
        def richiesta():
            richiesta =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
            richiesta = str.strip(richiesta.replace("Name: OBJECT, dtype: object",""))
            richiesta = richiesta[5::]
            print (richiesta)
            print("")
            engine.say (richiesta)
            engine.runAndWait()
        richiesta()
    else:
        pass

def ripetere_value():
    ripetere_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE RIPETERE" ]))
    ripetere_value = str.strip(ripetere_value.replace("Name: VALUE, dtype: bool",""))
    ripetere_value = ripetere_value[5::]

    if ripetere_value == "True" :
        def ripetere():
            ripetere =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RIPETERE" ]))
            ripetere = str.strip(ripetere.replace("Name: OBJECT, dtype: object",""))
            ripetere = ripetere[5::]
            print (ripetere)
            engine.say(ripetere)
            engine.runAndWait()
        ripetere()
    else:
        pass


def risposte():
    try:
        with Microphone(device_index=None, sample_rate=48000, chunk_size=512) as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1.0
            richiesta_value()
            ascolto_value()
            audio = r.listen(source, timeout=3)
            testo = r.recognize_google(audio, language="it-IT").lower()
            print(testo)
            print("")      
    except:
        start()


 ###RISPOSTE###

    if any(parola in testo for parola in [ "apri"]):
        ds = pd.read_excel(r'CachedApp.xlsx')
        df = pd.DataFrame(ds)
        testo = str.strip(testo.replace("apri",""))

        disco =(str(df["DISCO"] [df["APP"] == testo]))
        disco = str.strip(disco.replace("Name: DISCO, dtype: object",""))
        disco = disco[5::]
        #print(disco)


        dir1 = (str(df["DIR1"] [df["APP"] == testo]))
        dir1 = str.strip(dir1.replace("Name: DIR1, dtype: object",""))
        dir1 = dir1[5::]
        #print(dir1)

        dir2 = (str(df["DIR2"] [df["APP"] == testo]))
        dir2 = str.strip(dir2.replace("Name: DIR2, dtype: object",""))
        dir2 = dir2[5::]
        #print(dir2)

        dir3 = (str(df["DIR3"] [df["APP"] == testo]))
        dir3 = str.strip(dir3.replace("Name: DIR3, dtype: object",""))
        dir3 = dir3[5::]
        #print(dir3)

        dir4 = (str(df["DIR4"] [df["APP"] == testo]))
        dir4 = str.strip(dir4.replace("Name: DIR4, dtype: object",""))
        dir4 = dir4[5::]
        #print(dir4)

        dir5 = (str(df["DIR5"] [df["APP"] == testo]))
        dir5 = str.strip(dir5.replace("Name: DIR5, dtype: object",""))
        dir5 = dir5[5::]
        #print(dir5)

        direxe = (str(df["EXE"] [df["APP"] == testo]))
        direxe = str.strip(direxe.replace("Name: EXE, dtype: object",""))
        direxe = direxe[5::]




        exe = str(disco + dir1 + dir2 + dir3 + dir4 + dir5 + direxe)

        if "NaN" in exe:
            exe = str.strip(exe.replace("NaN",""))

        print(exe)

        try:
            print("sto aprendo " + testo)
            engine.say("sto aprendo " + testo)
            engine.runAndWait()
            subprocess.run([exe])
            start()
        except:
            print("errore durante l'apertura di " + testo + ", prova a controllare il percorso dell'applicazione")
            engine.say("errore durante l'apertura di " + testo + ", prova a controllare il percorso dell'applicazione")
            sleep(1)
            ripetere_value()
            risposte()
     
    elif any(parola in testo for parola in ["chiudi"]):


        ds = pd.read_excel(r'CachedApp.xlsx')
        df = pd.DataFrame(ds)

        if "chiudi" in testo:
            testo = str.strip(testo.replace("chiudi",""))

        disco =(str(df["DISCO"] [df["APP"] == testo]))
        disco = str.strip(disco.replace("Name: DISCO, dtype: object",""))
        disco = disco[5::]

        dir1 = (str(df["DIR1"] [df["APP"] == testo]))
        dir1 = str.strip(dir1.replace("Name: DIR1, dtype: object",""))
        dir1 = dir1[5::]

        dir2 = (str(df["DIR2"] [df["APP"] == testo]))
        dir2 = str.strip(dir2.replace("Name: DIR2, dtype: object",""))
        dir2 = dir2[5::]

        dir3 = (str(df["DIR3"] [df["APP"] == testo]))
        dir3 = str.strip(dir3.replace("Name: DIR3, dtype: object",""))
        dir3 = dir3[5::]

        dir4 = (str(df["DIR4"] [df["APP"] == testo]))
        dir4 = str.strip(dir4.replace("Name: DIR4, dtype: object",""))
        dir4 = dir4[5::]

        dir5 = (str(df["DIR5"] [df["APP"] == testo]))
        dir5 = str.strip(dir5.replace("Name: DIR5, dtype: object",""))
        dir5 = dir5[5::]

        direxe = (str(df["EXE"] [df["APP"] == testo]))
        direxe = str.strip(direxe.replace("Name: EXE, dtype: object",""))
        direxe = direxe[5::]




        exe = str(disco + dir1 + dir2 + dir3 + dir4 + dir5 + direxe)

        if "NaN" in exe:
            exe = str.strip(exe.replace("NaN",""))

        print(exe)

        try:
            os.kill([exe])
            print("sto chiudendo " + testo)
            engine.say("sto chiudendo " + testo)
            engine.runAndWait()
            start()
        except:
            print("errore durante la chiusura di " + testo + ", prova a controllare il percorso dell'applicazione")
            engine.say("errore durante la chiusura di " + testo + ", prova a controllare il percorso dell'applicazione")
            sleep(1)
            ripetere_value()
            risposte()

    elif any(parola in testo for parola in ["ore", "ora", "orario"]):
        risposta = f"sono le ore {datetime.now().strftime('%H e %M')}"
        print (risposta)
        engine.say(risposta)
        engine.runAndWait()
        start()
    
    elif any(parola in testo for parola in ["leggi ad alta voce"]):
        print("scrivi qui la frase:")
        engine.say("scrivi qui la frase:")
        engine.runAndWait()
        risposta = input()
        engine.say(risposta)
        engine.runAndWait()
        start()

    elif any(parola in testo for parola in ["sai parlare in corsivo"]):
        print("ma certo, amiœ, ho studiato e ora sono tra i migliori alunnæ,seguo tutte le lezioni di cörsivœ, non vedo l'ora arrivi la prossima verificæ")
        engine.say("ma certo. amiœ. ho studiato e ora sono tra i migliori alunnæ. seguo tutte le lezioni di cörsivœ. non vedo l'ora arrivi la prossima verificæ")
        engine.runAndWait()
        sleep(3)
        start()

    elif any(parola in testo for parola in [ "cerca", "qual", "significa", "significato"]):
        testo = str.strip(testo.replace("cerca", ""))
        testo = str.strip(testo.replace("cos'", ""))
        testo = str.strip(testo.replace("qual", ""))
        testo = str.strip(testo.replace("significato", ""))
        testo = str.strip(testo.replace("significa", ""))
        testo = str.strip(testo.replace("è", ""))
        testo = str.strip(testo.replace("l'", ""))
        testo = str.strip(testo.replace("che", ""))


        wikipedia.set_lang("IT")
        print(testo)
        risposta = wikipedia.summary( testo , sentences=3)


        print( "Secondo Wikipedia:" + '\n' + risposta)
        engine.say("Secondo Wikipedia: " + "," + risposta)
        engine.runAndWait()
        start()

    elif any(parola in testo for parola in [ "spegniti", "stop"]):
        print("siri si sta spegnendo...")
        engine.say ("siri si sta spegnendo")
        engine.runAndWait()
        kill

    elif any(parola in testo for parola in ["spegni"]):
        if any(parola in testo for parola in ["pc", "computer"]):
            os.system('shutdown /s /t 0')
        else:
            ripetere_value()
            risposte()

    else:
        ripetere_value()
        risposte()


def start():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    r = Recognizer()

    try:
        with Microphone(device_index= None, sample_rate=48000, chunk_size=512) as source:
            r.adjust_for_ambient_noise(source)
            ascolto_value()
            audio = r.listen(source, timeout= 0 )
            testo = r.recognize_google(audio, language="it-IT").lower()

            if "ehi siri" in testo:
                print(testo)
                print("")
                risposte()
    except:
        start()



start()



#for voice in voices:
    #print (voice)
#HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_IT-IT_ELSA_11.0





from datetime import datetime
import time
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




engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
r = Recognizer()

###FILE DATI###
dr = pd.read_excel(r'C:\Users\Giulio Tognetto\Desktop\Python\Siri\Settings.xlsx')
dt = pd.DataFrame(dr)

#ds = pd.read_excel(r'C:\Users\Giulio Tognetto\Desktop\Python\Siri\CachedApp.xlsx')
#df = pd.DataFrame(ds)

start1 = time.time()
try:
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
    else:
        pass
    
    
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
    else:
        pass
    
    
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
    else:
        pass
except:
    print("controlla le impostazioni...")
    engine.say("controlla le impostazioni...")
    engine.runAndWait()
    kill

def start():
    try:
        with Microphone(device_index=None, sample_rate=48000, chunk_size=512) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.phrase_time_limit=5
            r.pause_threshold = 1.0
            if richiesta_value == "True" :
                richiesta()
            if ascolto_value == "True":
                ascolto()
            audio = r.listen(source, timeout=3)
            testo = r.recognize_google(audio, language="it-IT").lower()

        if "ehi siri" in testo:
            testo = str.strip(testo.replace("ehi siri",""))
            print(testo)
            print("")


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
                except:
                    print("errore durante l'apertura di " + testo + ", prova a controllare il percorso dell'applicazione")
                    engine.say("errore durante l'apertura di " + testo + ", prova a controllare il percorso dell'applicazione")
                    engine.runAndWait()
                    sleep(1)
                    if ripetere_value == "True" :
                        ripetere()
                finally:
                    start()

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
                        print("sto chiudendo " + testo)
                        engine.say("sto chiudendo " + testo)
                        engine.runAndWait()
                        os.system("TASKKILL /F /IM " + exe)
                    except:
                        print("errore durante la chiusura di " + testo + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo")
                        engine.say("errore durante la chiusura di " + testo + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo")
                        sleep(1)
                        if ripetere_value == "True" :
                            ripetere()      
                    finally:
                        start()

            elif any(parola in testo for parola in ["ore", "ora", "orario"]):
                try:
                    risposta = f"sono le ore {datetime.now().strftime('%H e %M')}"
                    print (risposta)
                    engine.say(risposta)
                    engine.runAndWait()
                finally:
                    start()

            elif any(parola in testo for parola in ["leggi quello che scrivo"]):
                try:
                    print("scrivi qui la frase:")
                    engine.say("scrivi qui la frase:")
                    engine.runAndWait()
                    risposta = input()
                    engine.say(risposta)
                    engine.runAndWait()
                finally:
                    start()

            elif any(parola in testo for parola in ["sai parlare in corsivo"]):
                try:
                    print("ma certo, amiœ, ho studiato e ora sono tra i migliori alunnæ,seguo tutte le lezioni di cörsivœ, non vedo l'ora arrivi la prossima verificæ")
                    engine.say("ma certo. amiœ. ho studiato e ora sono tra i migliori alunnæ. seguo tutte le lezioni di cörsivœ. non vedo l'ora arrivi la prossima verificæ")
                    engine.runAndWait()
                    sleep(3)
                finally:
                    start()

            elif any(parola in testo for parola in ["cerca", "qual", "significa", "significato"]):
                try:
                    testo = str.strip(testo.replace("cerca", ""))
                    testo = str.strip(testo.replace("cos'", ""))
                    testo = str.strip(testo.replace("qual", ""))
                    testo = str.strip(testo.replace("significato", ""))
                    testo = str.strip(testo.replace("significa", ""))
                    testo = str.strip(testo.replace("è", ""))
                    testo = str.strip(testo.replace("l'", ""))
                    testo = str.strip(testo.replace("che", ""))
                    testo = str.strip(testo.replace("il", ""))
                    testo = str.strip(testo.replace("di", ""))
                    print(testo)





                    wikipedia.set_lang("it")
                    risposta = wikipedia.summary( testo, sentences=3)
                    print( "Secondo Wikipedia:" + '\n' + risposta)
                    engine.say("Secondo Wikipedia: " + "," + risposta)
                    engine.runAndWait()
                finally:
                    start()

            elif any(parola in testo for parola in ["spegniti", "stop"]):
                try:
                    print("siri si sta spegnendo...")
                    engine.say ("siri si sta spegnendo")
                    engine.runAndWait()
                    kill
                except:
                    start()

            elif any(parola in testo for parola in ["spegni"]):
                try:
                    if any(parola in testo for parola in ["pc", "computer"]):
                        os.system('shutdown /s /t 0')
                except:
                    if ripetere_value == "True" :
                        ripetere()
                finally:
                    start()


            else:
                if testo == (str.strip("")):
                    pass
                else:
                    if ripetere_value == "True" :
                        ripetere()
                start()


        else:
            start()

    except:
        start()




print("The time used to execute this is given below")
end = time.time()
time_passed = (end - start1)
print(time_passed)


start()



#for voice in voices:
    #print (voice)
#HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_IT-IT_ELSA_11.0


from datetime import datetime
import random
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pyautogui as p
import time
from time import sleep
from googlesearch import search
import wikipedia
from os import kill
import os
import pyttsx3
import subprocess
import speech_recognition
from speech_recognition import Recognizer, Microphone
import pandas as pd 
import numpy as np
from pandas import read_excel


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
r = Recognizer()



###FILE DATI###
#r'C:\Users\Giulio Tognetto\Desktop\Python\Siri\CachedApp.xlsx'




try:
    dr = pd.read_excel(r'SavedSettings.xlsx')
    dr = pd.read_excel('SavedSettings.xlsx')
    print("non ho usato l'except")
except FileNotFoundError:
    dr = pd.read_excel(r'C:\Users\Giulio Tognetto\Desktop\Python\Siri\SavedSettings.xlsx')
    print("ho usato l'except")
finally:
    dt = pd.DataFrame(dr)



try:
    inizio_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE INIZIALE" ]))
    inizio_value = str.strip(inizio_value.replace("Name: VALUE, dtype: bool",""))
    inizio_value = inizio_value[5::]
    def inizio():
        inizio =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE INIZIALE" ]))
        inizio = str.strip(inizio.replace("Name: OBJECT, dtype: object",""))
        inizio = inizio[5::]
        print (inizio)
        print("")
        engine.say (inizio)
        engine.runAndWait()
    if inizio_value == "True" :
        inizio()
except:
    print("controlla le impostazioni...")
    engine.say("controlla le impostazioni...")
    engine.runAndWait()


try:
    ascolto_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
    ascolto_value = str.strip(ascolto_value.replace("Name: VALUE, dtype: bool",""))
    ascolto_value = ascolto_value[5::]
    def ascolto():
        ascolto =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
        ascolto = str.strip(ascolto.replace("Name: OBJECT, dtype: object",""))
        ascolto = ascolto[5::]
        print (ascolto)
except:
    print("controlla le impostazioni...")
    engine.say("controlla le impostazioni...")
    engine.runAndWait()


try:
    richiesta_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
    richiesta_value = str.strip(richiesta_value.replace("Name: VALUE, dtype: bool",""))
    richiesta_value = richiesta_value[5::]
    def richiesta():
        richiesta =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
        richiesta = str.strip(richiesta.replace("Name: OBJECT, dtype: object",""))
        richiesta = richiesta[5::]
        print (richiesta)
        print("")
        engine.say (richiesta)
        engine.runAndWait()
except:
    print("controlla le impostazioni...")
    engine.say("controlla le impostazioni...")
    engine.runAndWait()


try:
    ripetere_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE RIPETERE" ]))
    ripetere_value = str.strip(ripetere_value.replace("Name: VALUE, dtype: bool",""))
    ripetere_value = ripetere_value[5::]
    def ripetere():
        ripetere =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RIPETERE" ]))
        ripetere = str.strip(ripetere.replace("Name: OBJECT, dtype: object",""))
        ripetere = ripetere[5::]
        print (ripetere)
        engine.say(ripetere)
        engine.runAndWait()     
except:
    print("controlla le impostazioni...")
    engine.say("controlla le impostazioni...")
    engine.runAndWait()


try:
    tempo_impiegato_value =(str(dt["VALUE"] [dt["SETTING"] == "TEMPO IMPIEGATO" ]))
    tempo_impiegato_value = str.strip(tempo_impiegato_value.replace("Name: VALUE, dtype: bool",""))
    tempo_impiegato_value = tempo_impiegato_value[5::]
    def tempo_impiegato():
        tempoimp =(str(dt["OBJECT"] [dt["SETTING"] == "TEMPO IMPIEGATO" ]))
        tempoimp = str.strip(tempoimp.replace("Name: OBJECT, dtype: object",""))
        tempoimp = tempoimp[5::]
        print(tempoimp)
except:
    print("controlla le impostazioni...")
    engine.say("controlla le impostazioni...")
    engine.runAndWait()





def start():
    try:
        if tempo_impiegato_value == "True":
            start1 = time.time()
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



        ###RISPOSTE###

        if "ehi siri" in testo:
            testo = str.strip(testo.replace("ehi siri",""))
            print(testo)
            print("")



            if any(parola in testo for parola in ["apri"]):                                                                                                     #APRI
                ds = pd.read_excel(r'C:\Users\Giulio Tognetto\Desktop\Python\Siri\CachedApp.xlsx')
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
                    #print(exe)

                if "https" in exe:

                    try:
                        chrome_driver = ChromeDriverManager().install()
                        driver = Chrome(service=Service(chrome_driver))
                        driver.maximize_window()
                        link = exe
                        driver.get(link)
                        input()
    

                    except:
                        print("errore durante l'apertura di " + testo + ", prova a controllare il percorso dell'applicazione")
                        engine.say("errore durante l'apertura di " + testo + ", prova a controllare il percorso dell'applicazione")
                        engine.runAndWait()
                        sleep(1)
                        if ripetere_value == "True" :
                            ripetere()
                else:
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

            elif any(parola in testo for parola in ["chiudi"]):                                                                                                 #CHIUDI
                ds = pd.read_excel(r'C:\Users\Giulio Tognetto\Desktop\Python\Siri\CachedApp.xlsx')
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

            elif any(parola in testo for parola in ["ore", "ora", "orario"]):                                                                                   #ORARIO
                try:
                    risposta = f"sono le ore {datetime.now().strftime('%H e %M')}"
                    print (risposta)
                    engine.say(risposta)
                    engine.runAndWait()
                except:
                    print("non sono stata in grado di risalire all'ora attuale,riprova piu tardi...")

            elif any(parola in testo for parola in ["play", "pausa", "skip", "avanti", "indietro", "volume of", "volume off", "volume on"]):                    #MUSICA
                if any(parola in testo for parola in ["play","pausa"]):

                    if testo == "play" or "pausa":
                        p.hotkey('playpause')

                    #else:
                        #testo = str.strip(testo.replace("play",""))
                        #nome_playlist = testo
                        #subprocess.run('spotify.exe')
                        #sleep(10)
                        #p.hotkey('ctrl', 'l')
                        #p.write(nome_playlist)
                        #p.leftClick


                elif any(parola in testo for parola in ["skip","avanti"]):
                    p.hotkey('nexttrack')
            
                elif any(parola in testo for parola in ["indietro"]):
                    p.press('prevtrack',2)

                elif any(parola in testo for parola in ["volume off", "volume of", "volume on"]):
                    p.hotkey('volumemute')
            
            elif any(parola in testo for parola in ["quanto fa"]):                                                                                              #CALCOLATRICE
                testo = str.strip(testo.replace("quanto fa",""))
                if "piu" in testo:
                    testo = str.strip(testo.replace("piu","+"))

                if "meno" in testo:
                    testo = str.strip(testo.replace("meno","-"))
            
                if "per" in testo:
                    testo = str.strip(testo.replace("per","*"))

                if "diviso" in testo:
                    testo = str.strip(testo.replace("diviso","/"))
                
                if "elevato" in testo:
                    testo = str.strip(testo.replace("elevato",","))

                if "a" in testo:
                    testo = str.strip(testo.replace("a",""))

                try:

                    ###PRIMO NUMERO###

                    testo = testo + "_"
                    testo = str.strip(testo.replace("","'"))
                    testo = str.strip(testo.replace("' '","_"))
                    #print(testo)

                    pos=1
                    numero = testo

                    while True:
                        (numero[0:pos]) 
                        pos = pos + 1

                        if any(parola in (numero[0:pos]) for parola in ["_"]): 
                            break 


                    numero = numero[0:pos]

                    numero = str.strip(numero.replace("'",""))
                    numero = str.strip(numero.replace("_",""))


                    ###RISPOSTA1###
                    risposta = int(numero)


                    ###SECONDO NUMERO###

                    pos2 = pos +2
                    pos3 = pos2 +1
                    numero2 = testo

                    while True:
                        (numero2[pos2:pos3]) 
                        pos3 = pos3 + 1

                        if any(parola in (numero2[pos2:pos3]) for parola in ["'_'"]): 
                            break 

                    numero2 = numero2[pos2:pos3]

                    numero2 = str.strip(numero2.replace("'",""))
                    numero2 = str.strip(numero2.replace("_",""))


                    ###RISPOSTA2###
                    risposta2 = int(numero2)
                except ValueError:
                    print("ValueError")

                
                try:
                    if any(segno in testo for segno in ["+"]):
                        testo = str.strip(testo.replace("_","' '"))
                        testo = str.strip(testo.replace("'",""))
                        testo = str.strip(testo.replace("+","piu"))
                    

                        rispostasomma = risposta + risposta2 
                        rispostadef = (testo + ", e' uguale a " + str(rispostasomma))

                        print(rispostadef)
                        engine.say(rispostadef)
                        engine.runAndWait()
                    
                    if any(segno in testo for segno in ["-"]):
                        testo = str.strip(testo.replace("_","' '"))
                        testo = str.strip(testo.replace("'",""))
                        testo = str.strip(testo.replace("-","meno"))


                        rispostasottrazione = risposta - risposta2 
                        rispostadef = (testo + ", e' uguale a " + str(rispostasottrazione))

                        print(rispostadef)
                        engine.say(rispostadef)
                        engine.runAndWait()

                    if any(segno in testo for segno in ["*"]):
                        testo = str.strip(testo.replace("_","' '"))
                        testo = str.strip(testo.replace("'",""))
                        testo = str.strip(testo.replace("*","per"))


                        rispostaper = risposta * risposta2 
                        rispostadef = (testo + ", e' uguale a " + str(rispostaper))

                        print(rispostadef)
                        engine.say(rispostadef)
                        engine.runAndWait()

                    if any(segno in testo for segno in [","]):
                        testo = str.strip(testo.replace("_","' '"))
                        testo = str.strip(testo.replace("'",""))
                        testo = str.strip(testo.replace(",","elevato"))


                        rispostaper = risposta ** risposta2 
                        rispostadef = (testo + ", e' uguale a " + str(rispostaper))

                        print(rispostadef)
                        engine.say(rispostadef)
                        engine.runAndWait()

                    if any(segno in testo for segno in ["/"]):
                        testo = str.strip(testo.replace("_","' '"))
                        testo = str.strip(testo.replace("'",""))
                        testo = str.strip(testo.replace("/","diviso"))


                        rispostadiviso = risposta / risposta2 
                        rispostadef = (testo + ", e' uguale a " + str(rispostadiviso))

                        print(rispostadef)
                        engine.say(rispostadef)
                        engine.runAndWait()

                except UnboundLocalError:
                    print("UnboundLocalError: local variable 'risposta2' referenced before assignment")
                except ValueError:
                    print("ValueError")

            elif any(parola in testo for parola in ["ripeti"]):                                                                                                 #TTS
                try:
                    testo = str.strip(testo.replace("ripeti",""))
                    print(testo)
                    engine.say(testo)
                    engine.runAndWait()
                except:
                    pass

            elif any(parola in testo for parola in ["sai parlare in corsivo"]):                                                                                 #CORSIVO
                try:
                    print("ma certo, amiœ, ho studiato e ora sono tra i migliori alunnæ,seguo tutte le lezioni di cörsivœ, non vedo l'ora arrivi la prossima verificæ")
                    engine.say("ma certo. amiœ. ho studiato e ora sono tra i migliori alunnæ. seguo tutte le lezioni di cörsivœ. non vedo l'ora arrivi la prossima verificæ")
                    engine.runAndWait()
                    sleep(3)
                except:
                    pass

            elif any(parola in testo for parola in ["cerca", "cosa sono", "significa", "significato"]):                                                         #WIKIPEDIA \ GOOGLE
                try:
                    testo = str.strip(testo.replace("cerca", ""))
                    testo = str.strip(testo.replace("cos'", ""))
                    testo = str.strip(testo.replace("sono", ""))
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
                except:
                    print("errore durante la ricerca della risposta")
                    engine.say("errore durante la ricerca della risposta")
                    engine.runAndWait()
                    if ripetere_value == "True" :
                        ripetere()

            elif any(parola in testo for parola in ["spegniti"]):                                                                                               #SPEGNI SIRI
                try:
                    print("siri si sta spegnendo...")
                    engine.say ("siri si sta spegnendo")
                    engine.runAndWait()
                    kill
                except:
                    if ripetere_value == "True" :
                        ripetere()

            elif any(parola in testo for parola in ["spegni"]):                                                                                                 #SPEGNI UN DISPOSITIVO
                
                try:
                    if any(parola in testo for parola in ["pc", "computer"]):
                        os.system('shutdown /s /t 0')
                except:
                    if ripetere_value == "True" :
                        ripetere()

            elif any(parola in testo for parola in ["ciuccia melo", "ciucciamelo","ciuccio melo"]):
                numero = random.random()
                print(numero)
                if numero <= 0.5:
                    print("va bene con molto piacere giulio, ma ti ricordo che deniel e' molto piu' bravo di un' intelligenza artificiale")
                    engine.say("va bene con molto piacere giulio, ma ti ricordo che deniel e' molto piu' bravo di un' intelligenza artificiale")
                    engine.runAndWait()
                else:
                    print("mi dispiace ma non posso ciucciartelo ora")
                    engine.say("mi dispiace ma non posso ciucciartelo ora")
                    engine.runAndWait()




            else:
                if ripetere_value == "True" :
                    ripetere()
                start()


        ###RISPOSTE SECONDARIE###

        if "siri" in testo:
            if any(parola in testo for parola in ["ciao", "buongiorno","buonasera","ehila'","ehi"]):
                cifra = random.randint(1, 3) 
                if cifra == 1: risposta = "Ciao"
                if cifra == 2: risposta = "Ehila'"
                if cifra == 3: risposta = "Ehi"
                





                print(risposta)
                engine.say(risposta)
                engine.runAndWait()



            #if any(parola in testo for parola in ["come stai"]):








    except speech_recognition.WaitTimeoutError:
        print("")
        #print("speech_recognition.WaitTimeoutError: listening timed out while waiting for phrase to start")
        start()
    except speech_recognition.UnknownValueError:
        print("")
        #print("if not isinstance(actual_result, dict) or len(actual_result.get(""alternative"", [])) == 0: raise UnknownValueError() \\\ speech_recognition.UnknownValueError")
        start()
    finally:
        if tempo_impiegato_value == "True":
            print("")
            tempo_impiegato()
            end = time.time()
            time_passed = (end - start1)
            print(time_passed)
        #start()





start()






















#start = time.time()
        
#print("The time used to execute this is given below")
#end = time.time()
#time_passed = (end - start1)
#print(time_passed)





#for voice in voices:
    #print (voice)
#HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_IT-IT_ELSA_11.0


from datetime import datetime
import random
from unicodedata import name
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pyautogui as p
import time
from time import sleep
from googlesearch import search
import googlesearch
import wikipedia
from os import kill
import os
import pyttsx3
import subprocess
import speech_recognition
from speech_recognition import Recognizer, Microphone
import pandas as pd 
import numpy as np
import bs4
import requests
import webbrowser

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
r = Recognizer()





class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

class Cashed:
    request_name = 0
    request_text = 1
    request_dialog = 0
    name = "NaN"
    text = "NaN"
    dialog = "NaN"
    saved_text = "NaN"
    start = 0

try:
    try:
        dr = pd.read_excel(r'Desktop\siri\Settings.xlsx')
        ds = pd.read_excel(r'Desktop\siri\CachedApp.xlsx')
        print( bcolors.WARNING + "Non mi e' servita la directory intera" + bcolors.RESET)
    except FileNotFoundError:
        dr = pd.read_excel(r"C:\Users\Giulio Tognetto\Desktop\siri\Settings.xlsx")
        ds = pd.read_excel(r'C:\Users\Giulio Tognetto\Desktop\siri\CachedApp.xlsx')
        print( bcolors.FAIL +"Mi e' servita la directory intera" + bcolors.RESET)
    finally:
        dt = pd.DataFrame(dr)
        df = pd.DataFrame(ds)


    inizio_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE INIZIALE" ]))
    inizio_value = str.strip(inizio_value.replace("Name: VALUE, dtype: bool",""))
    inizio_value = inizio_value[5::]
    def inizio():
        inizio =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE INIZIALE" ]))
        inizio = str.strip(inizio.replace("Name: OBJECT, dtype: object",""))
        inizio = inizio[5::]
        print(inizio)
        print("")
        engine.say ( bcolors.WARNING + inizio + bcolors.RESET)
        engine.runAndWait()
    if inizio_value == "True" :
        inizio()

    ascolto_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
    ascolto_value = str.strip(ascolto_value.replace("Name: VALUE, dtype: bool",""))
    ascolto_value = ascolto_value[5::]
    def ascolto():
        ascolto =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
        ascolto = str.strip(ascolto.replace("Name: OBJECT, dtype: object",""))
        ascolto = ascolto[5::]
        print (bcolors.OK + ascolto + bcolors.RESET) 

    richiesta_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
    richiesta_value = str.strip(richiesta_value.replace("Name: VALUE, dtype: bool",""))
    richiesta_value = richiesta_value[5::]
    def richiesta():
        richiesta =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
        richiesta = str.strip(richiesta.replace("Name: OBJECT, dtype: object",""))
        richiesta = richiesta[5::]
        print (bcolors.OK + richiesta + bcolors.RESET)
        print("")
        engine.say (richiesta)
        engine.runAndWait()

    ripetere_value =(str(dt["VALUE"] [dt["SETTING"] == "FRASE RIPETERE" ]))
    ripetere_value = str.strip(ripetere_value.replace("Name: VALUE, dtype: bool",""))
    ripetere_value = ripetere_value[5::]
    def ripetere():
        ripetere =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RIPETERE" ]))
        ripetere = str.strip(ripetere.replace("Name: OBJECT, dtype: object",""))
        ripetere = ripetere[5::]
        print (bcolors.OK + ripetere + bcolors.RESET)
        engine.say(ripetere)
        engine.runAndWait()   

    tempo_impiegato_value =(str(dt["VALUE"] [dt["SETTING"] == "TEMPO IMPIEGATO" ]))
    tempo_impiegato_value = str.strip(tempo_impiegato_value.replace("Name: VALUE, dtype: bool",""))
    tempo_impiegato_value = tempo_impiegato_value[5::]
    def tempo_impiegato():
        tempoimp =(str(dt["OBJECT"] [dt["SETTING"] == "TEMPO IMPIEGATO" ]))
        tempoimp = str.strip(tempoimp.replace("Name: OBJECT, dtype: object",""))
        tempoimp = tempoimp[5::]
        print(bcolors.WARNING + tempoimp + bcolors.RESET)
except:
    print("controlla le impostazioni...")
    engine.say("controlla le impostazioni...")
    engine.runAndWait()
















def Listening():
    try:
        if tempo_impiegato_value == "True":
            Cashed.start = time.time()
        with Microphone(device_index=None, sample_rate=48000, chunk_size=512) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.phrase_time_limit=3
            r.pause_threshold = 0.5
            if richiesta_value == "True" :
                richiesta()
            if ascolto_value == "True":
                ascolto()
            audio = r.listen(source, timeout=3)


            if Cashed.request_text == 1:
                Cashed.text = r.recognize_google(audio, language="it-IT").lower()
                Cashed.saved_text = Cashed.text
                Cashed.request_text = 0
                Attempt()
            if Cashed.request_name == 1:
                Cashed.name = r.recognize_google(audio, language="it-IT").lower()
                Cashed.text = Cashed.saved_text
                Cashed.request_name = 0
                Attempt()
            if Cashed.request_dialog == 1:
                Cashed.dialog = r.recognize_google(audio, language="it-IT").lower()
                Cashed.text = Cashed.saved_text
                Cashed.request_dialog = 0
                Attempt()



            if Cashed.text == "siri":
                Listening()


    except speech_recognition.WaitTimeoutError:
        #print("speech_recognition.WaitTimeoutError: listening timed out while waiting for phrase to start")
        Cashed.request_text = 1
        Cashed.request_name = 0
        Listening()
    except speech_recognition.UnknownValueError:
        #print("if not isinstance(actual_result, dict) or len(actual_result.get(""alternative"", [])) == 0: raise UnknownValueError() \\\ speech_recognition.UnknownValueError")
        Cashed.request_text = 1
        Cashed.request_name = 0
        Listening()



def Attempt():


    try:

        if "siri" in Cashed.text:
            Cashed.text = str.strip(Cashed.text.replace("siri",""))
            print("testo=" + Cashed.text)
            print("testo salvato=" + Cashed.saved_text)
            print("nome salvato=" + Cashed.name)
            print("richiesta dialogo=" + str(Cashed.request_dialog))



            ###RISPOSTE###






            if any(parola in Cashed.text for parola in ["ciao","ehi","buongiorno","buonasera","buon pomeriggio"]):                                                  #SALUTI
                ora_attuale = int(datetime.now().strftime('%H'))


                def conversation():
                    try:
                        cifra = random.randint(1,2)
                        if cifra == 1:                      #come stai
                            cifra = random.randint(1,3)
                            if cifra == 1:  risposta = "Come stai? "
                            if cifra == 2:  risposta = "Come stai oggi? "
                            if cifra == 3:  risposta = "Come va? "
                        if cifra == 2:                      #come va relativo alla giornata
                            if ora_attuale >= 1  and ora_attuale < 12:
                                cifra = random.randint(1,3)
                                if cifra == 1:  risposta = "Come ti sei svegliato oggi? "
                                if cifra == 2:  risposta = "Come sta andando la mattinata? "
                                if cifra == 3:  risposta = "Come va questa mattinata? "
                            if ora_attuale >= 12 and ora_attuale < 18:
                                cifra = random.randint(1,3)
                                if cifra == 1:  risposta = "Come sta andando il pomeriggio? "
                                if cifra == 2:  risposta = "Cosa fai questo pomeriggio? "
                                if cifra == 3:  risposta = "Come impegnerai questo pomeriggio? "
                            if ora_attuale >= 18 and ora_attuale < 1:
                                cifra = random.randint(1,3)
                                if cifra == 1:  risposta = "Come va la serata? "
                                if cifra == 2:  risposta = "Come sta andando la tua serata? "
                                if cifra == 3:  risposta = "Cosa fari questa sera? "
                        #if cifra == 3:
                    
                        print(risposta)
                        engine.say(risposta)
                        engine.runAndWait()

                        Cashed.request_dialog = 1
                        Listening()
                    except:
                        print(bcolors.FAIL + "errore nella conversazione" + bcolors.RESET)                 
                    finally:
                        if Cashed.request_dialog == 0:
                            Cashed.text = "NaN"
                            Cashed.request_text = 1
                            Listening()

                if Cashed.request_dialog == 1:
                    Cashed.request_dialog = 0
                    conversation()

                def saluti():
                    cifra = random.randint(1,3)

                    if cifra == 1:  risposta = "Ciao "
                    if cifra == 2:  risposta = "Ehi "
                    if cifra == 3:
                        if ora_attuale >= 1  and ora_attuale < 12:
                            risposta = "Buongiorno "
                        if ora_attuale >= 12 and ora_attuale < 18:
                            risposta = "Buon pomeriggio "
                        if ora_attuale >= 18 and ora_attuale > 1:
                            risposta = "Buonasera "




                    if Cashed.name == "NaN":
                        Cashed.request_name = 1
                        risposta = str.strip(risposta) + ", chi sei?"
                        print(bcolors.OK + risposta + bcolors.RESET)
                        engine.say(risposta)
                        engine.runAndWait()
                        Listening()
                    else:
                        Cashed.name = str.strip(Cashed.name.replace("mi chiamo",""))
                        Cashed.name = str.strip(Cashed.name.replace("il mio nome è",""))
                        Cashed.name = str.strip(Cashed.name.replace("puoi chiamarmi",""))
                        Cashed.name = str.strip(Cashed.name.replace("sono",""))
                        risposta = risposta + Cashed.name
                        print(bcolors.OK + risposta + bcolors.RESET)
                        engine.say(risposta)
                        engine.runAndWait()


                    cifra = random.randint(1,10)
                    if cifra <=5:
                        conversation()

                saluti()

                Cashed.text = str.strip(Cashed.text.replace("ciao",""))
                Cashed.text = str.strip(Cashed.text.replace("ehi",""))
                Cashed.text = str.strip(Cashed.text.replace("buongiorno",""))
                Cashed.text = str.strip(Cashed.text.replace("buonasera",""))
                Cashed.text = str.strip(Cashed.text.replace("buon pomeriggio",""))




            if any(parola in Cashed.text for parola in ["ore", "ora"]):                                                                                             #ORARIO
                try:
                    risposta = f"sono le ore {datetime.now().strftime('%H e %M')}"
                    print (bcolors.OK + risposta + bcolors.RESET)
                    engine.say(risposta)
                    engine.runAndWait()
                except:
                    print(bcolors.WARNING + "non sono stata in grado di risalire all'ora attuale,riprova piu tardi..." + bcolors.RESET)
                Cashed.text = str.strip(Cashed.text.replace("che",""))
                Cashed.text = str.strip(Cashed.text.replace("ora",""))
                Cashed.text = str.strip(Cashed.text.replace("ore",""))
                Cashed.text = str.strip(Cashed.text.replace("sono",""))
                Cashed.text = str.strip(Cashed.text.replace("è",""))
                

            if any(parola in Cashed.text for parola in["temperatura","clima"]):                                                                                     #TEMPERATURA
                try:

                    Cashed.text = str.strip(Cashed.text.replace(" a ","-a-"))
                    Cashed.text = str.strip(Cashed.text.replace("che",""))
                    Cashed.text = str.strip(Cashed.text.replace("temperatura",""))
                    Cashed.text = str.strip(Cashed.text.replace("è"," "))
                    Cashed.text = str.strip(Cashed.text.replace("c'"," "))
                
                    link = "https://www.msn.com/it-it/meteo/previsioni/"



                    if "-a-" in Cashed.text:
                        Cashed.text = str.strip(Cashed.text.replace("-a-",""))
                        Cashed.text = str.strip(Cashed.text.replace(" ","-"))
                        informazioni_location = Cashed.text






                        link_location = link + informazioni_location
                        #print(link_location)

                    else:

                        response = requests.get(link)
                        response.raise_for_status()
                        soup = bs4.BeautifulSoup(response.text,'html.parser')



                        soup = bs4.BeautifulSoup(response.text,'html.parser')
                        div_location = soup.find('div', id='WeatherOverviewLocationName')
                        a_informazioni = div_location.find('a')
                        informazioni_location = str(a_informazioni.get_text('location_name_main_container-E1_1'))
                        #print(informazioni_location)


                        link_location = link + informazioni_location

                    response_posizione = requests.get(link_location)
                    response_posizione.raise_for_status()
                    soup_posizione = bs4.BeautifulSoup(response_posizione.text,'html.parser')



                    div_overall = soup_posizione.find('div', class_='overallContainer-E1_1')
                    p_informazioni = div_overall.find('p')
                    informazioni_principali = str(p_informazioni.get_text('summaryDescCompact-E1_1'))
                

                    div_container = div_overall.find('div', class_='summaryContainerCompact-E1_1')
                    div_actual_temperature = div_container.find('div', id='OverviewCurrentTemperature')
                    a_informazioni_temp = div_actual_temperature.find('a')
                    informazioni_temperatura_attuale = str(a_informazioni_temp.get_text('summaryTemperatureUnit-E1_1'))
                    informazioni_temperatura_attuale = informazioni_temperatura_attuale.replace("summaryTemperatureUnit-E1_1","")


                    div_detail = soup_posizione.find('div', class_='detailItemLineCompact-E1_1')
                
                
                
                    div_vento = div_detail.find('div', id= 'CurrentDetailLineWindValue')
                    informazioni_vento = str(div_vento.get_text('CurrentDetailLineWindValue'))
                
                
                    div_umidita = div_detail.find('div', id= 'CurrentDetailLineHumidityValue')
                    informazioni_umidita = str(div_umidita.get_text('CurrentDetailLineHumidityValue'))
                
                
                    div_visibilita = div_detail.find('div', id= 'CurrentDetailLineVisibilityValue')
                    informazioni_visibilita = str(div_visibilita.get_text('CurrentDetailLineVisibilityValue'))
                
                    print("Vento: " + informazioni_vento)
                    print("umidita': " + informazioni_umidita)
                    print("visibilita': " + informazioni_visibilita)

                    informazioni_principali = ("a " + informazioni_location + (" La temperatura corrente È di " + (str(informazioni_temperatura_attuale.replace("C",""))) + (", ") + informazioni_principali))
                
                    print(bcolors.OK + informazioni_principali + bcolors.RESET)
                    engine.say(informazioni_principali)
                    engine.runAndWait()
                except:
                    print(bcolors.WARNING + "non sono stata in grado di arrivare alla rtemperatura corrente a" + informazioni_location + bcolors.RESET)        
                

            if any(parola in Cashed.text for parola in ["play", "pausa", "skip","schippa", "avanti", "indietro", "volume of", "volume off", "volume on"]):          #MUSICA

                
                if any(parola in Cashed.text for parola in ["play","pausa"]):
                    if Cashed.text == "play" or "pausa":
                        p.hotkey('playpause')

                    #else:
                        #testo = str.strip(testo.replace("play",""))
                        #nome_playlist = testo
                        #subprocess.run('spotify.exe')
                        #sleep(10)
                        #p.hotkey('ctrl', 'l')
                        #p.write(nome_playlist)
                        #p.leftClick


                if any(parola in Cashed.text for parola in ["skip","avanti","schippa"]):
                    p.hotkey('nexttrack')
            
                if any(parola in Cashed.text for parola in ["indietro"]):
                    p.press('prevtrack',2)

                if any(parola in Cashed.text for parola in ["volume off", "volume of", "volume on"]):
                    p.hotkey('volumemute')
            
                Cashed.text = str.strip(Cashed.text.replace("play",""))
                Cashed.text = str.strip(Cashed.text.replace("pausa",""))
                Cashed.text = str.strip(Cashed.text.replace("skip",""))
                Cashed.text = str.strip(Cashed.text.replace("avanti",""))
                Cashed.text = str.strip(Cashed.text.replace("indietro",""))
                Cashed.text = str.strip(Cashed.text.replace("volume off",""))
                Cashed.text = str.strip(Cashed.text.replace("volume of",""))
                Cashed.text = str.strip(Cashed.text.replace("volume on",""))    
                

            if any(parola in Cashed.text for parola in ["sai parlare in corsivo"]):                                                                                 #CORSIVO
                try:
                    print( bcolors.OK + "ma certo, amiooœ, ho studiato e ora sono tra i migliori alunneæ,seguo tutte le lezioni di cörsivooœ, non vedo l'ora arrivi la prossima verificaaæ" + bcolors.RESET)
                    engine.say("ma certo, amiooœ, ho studiato e ora sono tra i migliori alunneæ,seguo tutte le lezioni di cörsivooœ, non vedo l'ora arrivi la prossima verificaaæ")
                    engine.runAndWait()
                    sleep(3)
                except:
                    pass
                Cashed.text = str.strip(Cashed.text.replace("sai parlare in corsivo",""))  


            if any(parola in Cashed.text for parola in ["spegni"]):                                                                                                 #SPEGNI UN DISPOSITIVO
                Cashed.text = str.strip(Cashed.text.replace("spegni",""))
                try:
                    if any(parola in Cashed.text for parola in ["pc", "computer"]):
                        os.system('shutdown /s /t 0')


                
                except:
                    if ripetere_value == "True" :
                        ripetere()


            if any(parola in Cashed.text for parola in ["cerca", "cosa sono", "significa", "significato"]):                                                         #WIKIPEDIA \ GOOGLE
                try:
                    Cashed.text = str.strip(Cashed.text.replace("cerca", ""))
                    Cashed.text = str.strip(Cashed.text.replace("cos'", ""))
                    Cashed.text = str.strip(Cashed.text.replace("cosa", ""))
                    Cashed.text = str.strip(Cashed.text.replace("sono", ""))
                    Cashed.text = str.strip(Cashed.text.replace("qual", ""))
                    Cashed.text = str.strip(Cashed.text.replace("significato", ""))
                    Cashed.text = str.strip(Cashed.text.replace("significa", ""))
                    Cashed.text = str.strip(Cashed.text.replace("è", ""))
                    Cashed.text = str.strip(Cashed.text.replace("l'", ""))
                    Cashed.text = str.strip(Cashed.text.replace("che", ""))
                    Cashed.text = str.strip(Cashed.text.replace("il", ""))
                    Cashed.text = str.strip(Cashed.text.replace("di", ""))
                    
                    print(bcolors.OK +"cerco il significato di " + Cashed.text + bcolors.RESET)
                    engine.say("cerco il significato di " + Cashed.text)
                    engine.runAndWait()





                    wikipedia.set_lang("it")
                    risposta = wikipedia.summary( Cashed.text, sentences=3)
                    print( bcolors.OK +"Secondo Wikipedia:" + '\n' + risposta + bcolors.RESET)
                    engine.say("Secondo Wikipedia: " + "," + risposta)
                    engine.runAndWait()
                except:
                    print( bcolors.WARNING +"errore durante la ricerca della risposta" + bcolors.RESET)
                    engine.say("errore durante la ricerca della risposta")
                    engine.runAndWait()
                    if ripetere_value == "True" :
                        ripetere()


            elif any(parola in Cashed.text for parola in ["apri"]):                                                                                                 #APRI

                Cashed.text = str.strip(Cashed.text.replace("apri",""))

            


                disco =(str(df["DISCO"] [df["APP"] == Cashed.text]))
                disco = str.strip(disco.replace("Name: DISCO, dtype: object",""))
                disco = disco[5::]
                #print(disco)


                dir1 = (str(df["DIR1"] [df["APP"] == Cashed.text]))
                dir1 = str.strip(dir1.replace("Name: DIR1, dtype: object",""))
                dir1 = dir1[5::]
                #print(dir1)

                dir2 = (str(df["DIR2"] [df["APP"] == Cashed.text]))
                dir2 = str.strip(dir2.replace("Name: DIR2, dtype: object",""))
                dir2 = dir2[5::]
                #print(dir2)

                dir3 = (str(df["DIR3"] [df["APP"] == Cashed.text]))
                dir3 = str.strip(dir3.replace("Name: DIR3, dtype: object",""))
                dir3 = dir3[5::]
                #print(dir3)

                dir4 = (str(df["DIR4"] [df["APP"] == Cashed.text]))
                dir4 = str.strip(dir4.replace("Name: DIR4, dtype: object",""))
                dir4 = dir4[5::]
                #print(dir4)

                dir5 = (str(df["DIR5"] [df["APP"] == Cashed.text]))
                dir5 = str.strip(dir5.replace("Name: DIR5, dtype: object",""))
                dir5 = dir5[5::]
                #print(dir5)

                direxe = (str(df["EXE"] [df["APP"] == Cashed.text]))
                direxe = str.strip(direxe.replace("Name: EXE, dtype: object",""))
                direxe = direxe[5::]




                exe = str(disco + dir1 + dir2 + dir3 + dir4 + dir5 + direxe)

                if "NaN" in exe:
                    exe = str.strip(exe.replace("NaN",""))
                    #print(exe)

                if "http" in exe:
                    try:
                        chrome_driver = ChromeDriverManager().install()
                        driver = Chrome(service=Service(chrome_driver))
                        driver.maximize_window()
                        link = exe
                        driver.get(link)
                        input()
    

                    except:
                        print(bcolors.WARNING + "errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione" + bcolors.RESET)
                        engine.say("errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione")
                        engine.runAndWait()
                        sleep(1)
                        if ripetere_value == "True" :
                            ripetere()
                elif "exe" in exe:
                    try:
                        print(bcolors.OK +"sto aprendo " + Cashed.text + bcolors.RESET)
                        engine.say("sto aprendo " + Cashed.text)
                        engine.runAndWait()
                        subprocess.run([exe])
                    except:
                        print(bcolors.WARNING + "errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione" + bcolors.RESET)
                        engine.say("errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione")
                        engine.runAndWait()
                        sleep(1)
                        if ripetere_value == "True" :
                            ripetere()


            elif any(parola in Cashed.text for parola in ["chiudi"]):                                                                                               #CHIUDI

                if "chiudi" in Cashed.text:
                    Cashed.text = str.strip(Cashed.text.replace("chiudi",""))

                    disco =(str(df["DISCO"] [df["APP"] == Cashed.text]))
                    disco = str.strip(disco.replace("Name: DISCO, dtype: object",""))
                    disco = disco[5::]

                    dir1 = (str(df["DIR1"] [df["APP"] == Cashed.text]))
                    dir1 = str.strip(dir1.replace("Name: DIR1, dtype: object",""))
                    dir1 = dir1[5::]

                    dir2 = (str(df["DIR2"] [df["APP"] == Cashed.text]))
                    dir2 = str.strip(dir2.replace("Name: DIR2, dtype: object",""))
                    dir2 = dir2[5::]

                    dir3 = (str(df["DIR3"] [df["APP"] == Cashed.text]))
                    dir3 = str.strip(dir3.replace("Name: DIR3, dtype: object",""))
                    dir3 = dir3[5::]

                    dir4 = (str(df["DIR4"] [df["APP"] == Cashed.text]))
                    dir4 = str.strip(dir4.replace("Name: DIR4, dtype: object",""))
                    dir4 = dir4[5::]

                    dir5 = (str(df["DIR5"] [df["APP"] == Cashed.text]))
                    dir5 = str.strip(dir5.replace("Name: DIR5, dtype: object",""))
                    dir5 = dir5[5::]

                    direxe = (str(df["EXE"] [df["APP"] == Cashed.text]))
                    direxe = str.strip(direxe.replace("Name: EXE, dtype: object",""))
                    direxe = direxe[5::]




                    exe = str(disco + dir1 + dir2 + dir3 + dir4 + dir5 + direxe)

                    if "NaN" in exe:
                        exe = str.strip(exe.replace("NaN",""))

                    #print(exe)

                    try:
                        print(bcolors.OK + "sto chiudendo " + Cashed.text + bcolors.RESET)
                        engine.say("sto chiudendo " + Cashed.text)
                        engine.runAndWait()
                        os.system("TASKKILL /F /IM " + exe)
                    except:
                        print(bcolors.WARNING +"errore durante la chiusura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo" + bcolors.RESET)
                        engine.say("errore durante la chiusura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo")
                        sleep(1)
                        if ripetere_value == "True" :
                            ripetere()


            elif any(parola in Cashed.text for parola in ["quanto fa"]):                                                                                            #CALCOLATRICE
                Cashed.text = str.strip(Cashed.text.replace("quanto fa",""))
                if "piu" in Cashed.text:
                    Cashed.text = str.strip(Cashed.text.replace("piu","+"))

                if "meno" in Cashed.text:
                    Cashed.text = str.strip(Cashed.text.replace("meno","-"))
            
                if "per" in Cashed.text:
                    Cashed.text = str.strip(Cashed.text.replace("per","*"))

                if "diviso" in Cashed.text:
                    Cashed.text = str.strip(Cashed.text.replace("diviso","/"))
                
                if "elevato" in Cashed.text:
                    Cashed.text = str.strip(Cashed.text.replace("elevato",","))

                if "a" in Cashed.text:
                    Cashed.text = str.strip(Cashed.text.replace("a",""))

                try:

                    ###PRIMO NUMERO###

                    Cashed.text = Cashed.text + "_"
                    Cashed.text = str.strip(Cashed.text.replace("","'"))
                    Cashed.text = str.strip(Cashed.text.replace("' '","_"))
                    

                    pos=1
                    numero = Cashed.text

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
                    numero2 = Cashed.text

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
                    print(bcolors.WARNING + "ValueError" + bcolors.RESET)

                
                try:
                    if any(segno in Cashed.text for segno in ["+"]):
                        Cashed.text = str.strip(Cashed.text.replace("_","' '"))
                        Cashed.text = str.strip(Cashed.text.replace("'",""))
                        Cashed.text = str.strip(Cashed.text.replace("+","piu"))
                    

                        rispostasomma = risposta + risposta2 
                        rispostadef = (Cashed.text + ", e' uguale a " + str(rispostasomma))


                    
                    if any(segno in Cashed.text for segno in ["-"]):
                        Cashed.text = str.strip(Cashed.text.replace("_","' '"))
                        Cashed.text = str.strip(Cashed.text.replace("'",""))
                        Cashed.text = str.strip(Cashed.text.replace("-","meno"))


                        rispostasottrazione = risposta - risposta2 
                        rispostadef = (Cashed.text + ", e' uguale a " + str(rispostasottrazione))


                    if any(segno in Cashed.text for segno in ["*"]):
                        Cashed.text = str.strip(Cashed.text.replace("_","' '"))
                        Cashed.text = str.strip(Cashed.text.replace("'",""))
                        Cashed.text = str.strip(Cashed.text.replace("*","per"))


                        rispostaper = risposta * risposta2 
                        rispostadef = (Cashed.text + ", e' uguale a " + str(rispostaper))


                    if any(segno in Cashed.text for segno in [","]):
                        Cashed.text = str.strip(Cashed.text.replace("_","' '"))
                        Cashed.text = str.strip(Cashed.text.replace("'",""))
                        Cashed.text = str.strip(Cashed.text.replace(",","elevato"))


                        rispostaper = risposta ** risposta2 
                        rispostadef = (Cashed.text + ", e' uguale a " + str(rispostaper))



                    if any(segno in Cashed.text for segno in ["/"]):
                        Cashed.text = str.strip(Cashed.text.replace("_","' '"))
                        Cashed.text = str.strip(Cashed.text.replace("'",""))
                        Cashed.text = str.strip(Cashed.text.replace("/","diviso"))


                        rispostadiviso = risposta / risposta2 
                        rispostadef = (Cashed.text + ", e' uguale a " + str(rispostadiviso))

                    print(bcolors.OK + rispostadef + bcolors.RESET)
                    engine.say(rispostadef)
                    engine.runAndWait()

                except UnboundLocalError:
                    print(bcolors.WARNING + "UnboundLocalError: local variable 'risposta2' referenced before assignment" + bcolors.RESET)
                except ValueError:
                    print(bcolors.WARNING + "ValueError" + bcolors.RESET)


            elif any(parola in Cashed.text for parola in ["ripeti"]):                                                                                               #TTS
                try:
                    Cashed.text = str.strip(Cashed.text.replace("ripeti",""))
                    print(bcolors.OK + Cashed.text + bcolors.RESET)
                    engine.say(Cashed.text)
                    engine.runAndWait()
                except:
                    print("non sono stata in grado di ripetere la frase")


            elif any(parola in Cashed.text for parola in ["spegniti","stop"]):                                                                                      #SPEGNI SIRI
                try:
                    print("siri si sta spegnendo...")
                    engine.say ("siri si sta spegnendo")
                    engine.runAndWait()
                    kill
                except:
                    if ripetere_value == "True" :
                        ripetere()


            #elif 






    except:
        Cashed.request_text = 1
        Cashed.request_name = 0
        Listening()
    finally:
        Cashed.request_text = 1
        Cashed.text = "NaN"
        
        if Cashed.saved_text == "siri":
            pass
        elif "siri" in Cashed.text:
            if tempo_impiegato_value == "True":
                tempo_impiegato()
                end = time.time()
                time_passed = (end - Cashed.start)
                print(bcolors.WARNING + str(time_passed) + bcolors.RESET)
        Listening()


Listening()



from datetime import datetime
from pathlib import Path
import random
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pyautogui as p
import time
from time import sleep
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
#p.write('Hello world!', interval=0.25)

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

class Cashed:
    loop = 1
    start = 0

    request_name = 0
    request_text = 1
    request_dialog = 0
    request_saluto = 1
    request_risposta = 0

    name = "NaN"
    text = "NaN"
    risposta = "NaN"
    dialog = "NaN"
    saved_text = "NaN"

class Alphabet:

    a = ["ciao","ehi","buongiorno","buonasera","buon pomeriggio"]
    b = ["ore", "ora"]
    c = ["temperatura","clima","tempo"]
    d = ["riproduci","play", "pausa", "skip","schippa", "avanti", "indietro", "volume" ]
    e = ["screenshot"]
    f = ["sai parlare in corsivo"]
    g = ["spegni"]
    h = ["cerca", "significa"]
    i = ["apri", "esegui"]
    j = ["chiudi"]
    k = ["quanto fa"]
    l = ["ripeti"]
    m = ["spegniti","stop","exit"]



    null = '_'
    Alphabet = a + b + c + d + e + f + g + h + i + j + k + l + m

class patH:
    disco = "NaN"
    dir1 = "NaN"
    dir2 = "NaN"
    dir3 = "NaN"
    dir4 = "NaN"
    dir5 = "NaN"
    EXE = "NaN"

    All = [disco,dir1,dir2,dir3,dir4,dir5,EXE]
    Path = "NaN"
    Exe = "NaN"
    Path_exe = "NaN"



try:
    ###Checking file location###
    try:
        path = Path(__file__).absolute().parent
        dr = pd.read_excel(path / 'Files/Settings.xlsx')
        ds = pd.read_excel(path / 'Files/CashedApp.xlsx')
    except FileNotFoundError as e:
        print(e)
        Cashed.loop = 0
        kill
    finally:
        dt = pd.DataFrame(dr)
        df = pd.DataFrame(ds)

    ###Saved Bool###

    class value:
        inizio = "NaN"
        ascolto = "NaN"
        richiesta = "NaN"
        ripetere = "NaN"
        tempo_impiegato = "NaN"


        var = [inizio,ascolto,richiesta,ripetere,tempo_impiegato]
    
    n = 0
    for setting in ["FRASE INIZIALE","FRASE ASCOLTO","FRASE RICHIESTA","FRASE RIPETERE","TEMPO IMPIEGATO"]:
        val = (str(dt["VALUE"] [dt["SETTING"] == setting ]))
        val = str.strip(val.replace("Name: VALUE, dtype: bool",""))
        val = val[5::]

        value.var[n] = val
    
        n = n + 1
        
    value.inizio = value.var[0]
    value.ascolto = value.var[1]
    value.richiesta = value.var[2]
    value.ripetere = value.var[3]
    value.tempo_impiegato = value.var[4]


    ###Function###
    def inizio():
        inizio =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE INIZIALE" ]))
        inizio = str.strip(inizio.replace("Name: OBJECT, dtype: object",""))
        inizio = inizio[5::]
        print(inizio)
        #print("")
        engine.say ( bcolors.WARNING + inizio + bcolors.RESET)
        engine.runAndWait()
    if value.inizio == "True" :
        inizio()

    def ascolto():
        ascolto =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
        ascolto = str.strip(ascolto.replace("Name: OBJECT, dtype: object",""))
        ascolto = ascolto[5::]
        print (bcolors.OK + ascolto + bcolors.RESET) 

    def richiesta():
        richiesta =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
        richiesta = str.strip(richiesta.replace("Name: OBJECT, dtype: object",""))
        richiesta = richiesta[5::]
        print (bcolors.OK + richiesta + bcolors.RESET)
        #print("")
        engine.say (richiesta)
        engine.runAndWait()

    def ripetere():
        ripetere =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RIPETERE" ]))
        ripetere = str.strip(ripetere.replace("Name: OBJECT, dtype: object",""))
        ripetere = ripetere[5::]
        print (bcolors.OK + ripetere + bcolors.RESET)
        engine.say(ripetere)
        engine.runAndWait()   

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
        if value.tempo_impiegato == "True":
            Cashed.start = time.time()
        with Microphone(device_index=None, sample_rate=48000, chunk_size=512) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.phrase_time_limit=3
            r.pause_threshold = 0.5
            if value.richiesta == "True":
                richiesta()
            if value.ascolto == "True":
                ascolto()
            audio = r.listen(source, timeout=3)
            TTS = r.recognize_google(audio, language="it-IT").lower()
            #TTS = "siri "

            if Cashed.request_name == 1:
                Cashed.name = TTS
                Cashed.text = Cashed.saved_text
                Cashed.request_name = 0
                Attempt()
            if Cashed.request_text == 1:
                Cashed.text = TTS
                Cashed.saved_text = Cashed.text
                Attempt()
            if Cashed.request_dialog == 1:
                Cashed.dialog = TTS
                Cashed.text = Cashed.saved_text
                Attempt()
               


    except speech_recognition.WaitTimeoutError as e:
        #print(e)
        Cashed.request_text = 1
        Cashed.request_name = 0
        Cashed.request_dialog = 0
        Listening()
    except speech_recognition.UnknownValueError as e:
        #print(e)
        Cashed.request_text = 1
        Cashed.request_name = 0
        Cashed.request_dialog = 0
        Listening()



def Attempt():

    try:

        if Cashed.request_dialog == 1:

            if any(parola in Cashed.text for parola in ["ciao","ehi","buongiorno","buonasera","buon pomeriggio"]):                                                  #DIALOGO
                ora_attuale = int(datetime.now().strftime('%H'))

                for parola in ["ciao","ehi","buongiorno","buonasera","buon pomeriggio"]:
                    Cashed.text = Cashed.text.replace(parola,"")


                def conversation():

                    try:
                        cifra = random.randint(1,2)
                        if cifra == 1:                      #come stai
                            cifra = random.randint(1,3)
                            if cifra == 1:  Cashed.risposta = "Come stai? "
                            if cifra == 2:  Cashed.risposta = "Come stai oggi? "
                            if cifra == 3:  Cashed.risposta = "Come va? "
                        if cifra == 2:                      #come va relativo alla giornata
                            if ora_attuale >= 1  and ora_attuale < 12:
                                cifra = random.randint(1,3)
                                if cifra == 1:  Cashed.risposta = "Come ti sei svegliato oggi? "
                                if cifra == 2:  Cashed.risposta = "Come sta andando la mattinata? "
                                if cifra == 3:  Cashed.risposta = "Come va questa mattinata? "
                            if ora_attuale >= 12 and ora_attuale < 18:
                                cifra = random.randint(1,3)
                                if cifra == 1:  Cashed.risposta = "Come sta andando il pomeriggio? "
                                if cifra == 2:  Cashed.risposta = "Cosa fai questo pomeriggio? "
                                if cifra == 3:  Cashed.risposta = "Come impegnerai questo pomeriggio? "
                            if ora_attuale >= 18 and ora_attuale < 1:
                                cifra = random.randint(1,3)
                                if cifra == 1:  Cashed.risposta = "Come va la serata? "
                                if cifra == 2:  Cashed.risposta = "Come sta andando la tua serata? "
                                if cifra == 3:  Cashed.risposta = "Cosa fari questa sera? "
                        #if cifra == 3:
                    
                        print(bcolors.OK + Cashed.risposta + bcolors.RESET)
                        engine.say(Cashed.risposta)
                        engine.runAndWait()

                        Cashed.request_dialog = 1
                        Cashed.request_saluto = 0
                        Listening()
                        print(Cashed.dialog)
                    except:
                        print(bcolors.FAIL + "errore nella conversazione" + bcolors.RESET)
                    finally:
                        Cashed.request_dialog = 0
                        Cashed.request_text = 1
                        Listening()


                def saluti():
                    cifra = random.randint(1,3)

                    if cifra == 1:  Cashed.risposta = "Ciao "
                    if cifra == 2:  Cashed.risposta = "Ehi "
                    if cifra == 3:
                        if ora_attuale >= 1  and ora_attuale < 12:
                            Cashed.risposta = "Buongiorno "
                        if ora_attuale >= 12 and ora_attuale < 18:
                            Cashed.risposta = "Buon pomeriggio "
                        if ora_attuale >= 18 and ora_attuale > 1:
                            Cashed.risposta = "Buonasera "


                    if Cashed.name == "NaN":
                        Cashed.risposta = str.strip(Cashed.risposta) + ", chi sei?"
                        print(bcolors.OK + Cashed.risposta + bcolors.RESET)
                        engine.say(Cashed.risposta)
                        engine.runAndWait()
                        Cashed.request_name = 1
                        Cashed.request_dialog = 1
                        Cashed.request_text = 0
                        Listening()
                    else:
                        Cashed.request_dialog = 0
                        Cashed.name = str.strip(Cashed.name.replace("mi chiamo",""))
                        Cashed.name = str.strip(Cashed.name.replace("il mio nome è",""))
                        Cashed.name = str.strip(Cashed.name.replace("puoi chiamarmi",""))
                        Cashed.name = str.strip(Cashed.name.replace("sono",""))
                        
                        
                        
                        Cashed.risposta = Cashed.risposta + Cashed.name
                        print(bcolors.OK + Cashed.risposta + bcolors.RESET)
                        engine.say(Cashed.risposta)
                        engine.runAndWait()

                    cifra = random.randint(1,10)
                    if cifra <=3:
                        Cashed.request_saluto = 0
                        conversation()
                    else:
                        Cashed.request_text = 1
                        Cashed.request_dialog = 0
                        Cashed.request_name = 0
                        Attempt()

                if Cashed.request_saluto == 1:
                    saluti()


        if Cashed.request_text == 1:


            if any(parola in Cashed.text for parola in ["siri"]):
                for parola in ["siri"]:
                    Cashed.text = str.strip(Cashed.text.replace(parola,""))
                print(Cashed.text.capitalize())     

                ###RISPOSTE###

                if any(parola in Cashed.text for parola in Alphabet.a):         #SALUTI
                    Cashed.request_dialog = 1
                    Cashed.request_text = 0
                    Cashed.text = Cashed.saved_text
                    Attempt()


                if any(parola in Cashed.text for parola in Alphabet.b):         #ORARIO
                    try:
                        Cashed.risposta = f"sono le ore {datetime.now().strftime('%H e %M')}"
                        print (bcolors.OK + Cashed.risposta + bcolors.RESET)
                        engine.say(Cashed.risposta)
                        engine.runAndWait()
                    except:
                        print(bcolors.WARNING + "non sono stata in grado di risalire all'ora attuale,riprova piu tardi..." + bcolors.RESET)

                    for parola in ["che","ora","ore","sono","è"]:
                        Cashed.text = Cashed.text.replace(parola,"")


                if any(parola in Cashed.text for parola in Alphabet.c):         #TEMPERATURA
                    try:
                        for parola in ["che","temperatura","è","c'"]:
                            Cashed.text = Cashed.text.replace(parola,"")
                        Cashed.text = str.strip(Cashed.text.replace(" a ","-a-"))
                
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
                

                if any(parola in Cashed.text for parola in Alphabet.d):         #MUSICA

                    if any(parola in Cashed.text for parola in ["riproduci"]):
                        print("FUNZIONE NON ANCORA DISPONIBILE")
                        engine.say("FUNZIONE NON ANCORA DISPONIBILE")
                        engine.runAndWait()
                        kill






                        Cashed.saved_text = Cashed.text
                        Cashed.text = str.strip(Cashed.text.replace("riproduci","["))
                        for parola in ["riproduci", "su","con"]:
                            Cashed.text = Cashed.text.replace(parola," ] ")
                        #print(Cashed.text)
                        
                        class b:
                            brano = "NaN"
                            app = "NaN"

                        def Controllo_quadro():
                            pos = 1
                            while True:
                                (Cashed.text[0:pos]) 
                                pos = pos + 1

                                if any(parola in (Cashed.text[0:pos]) for parola in ["["]):
                                    break
                            pos1 = pos 
                            pos = pos - 1
                            while True:
                                (Cashed.text[pos:pos1]) 
                                pos1 = pos1 + 1


                                if any(parola in (Cashed.text[pos:pos1]) for parola in ["]"]):
                                    break
                            pos2 = pos1 
                            pos1 = pos1 - 2


                            b.brano = str.strip(Cashed.text[pos:pos1])
                            b.app = str.strip(Cashed.text[pos2::])
                        Controllo_quadro()



                        Cashed.text = b.app

                        app = str(df["APP"] [df["APP"] == Cashed.text])
                        app = str.strip(app.replace("Name: APP, dtype: object",""))
                        app = app[5::]



                        app = "s([], )"
                        if app != "s([], )":






































                            sleep(1)
                            p.hotkey('ctrl', 'l')
                            p.write(b.brano)
                            sleep(1)
                            p.leftClick
                            sleep(1)
                            p.moveTo(800, 370)
                            sleep(2)
                            p.leftClick




                            #while True:
                                #X, Y = p.position()
                                #print(X, Y)

                        else:
                            print("FUNZIONE NON ANCORA DISPONIBILE")
                        
                        for parola in ["]","[",b.brano, b.app]:
                            Cashed.text = Cashed.text.replace(parola,"")

                    if any(parola in Cashed.text for parola in [" play"," pausa"]):
                        if Cashed.text == "play" or "pausa":
                            p.hotkey('playpause')
                            for parola in [" play"," pausa"]:
                                Cashed.text = Cashed.text.replace(parola,"")

                    if any(parola in Cashed.text for parola in [" skip"," avanti"," schippa"]):
                        p.hotkey('nexttrack')
                        for parola in [" skip"," avanti"," schippa"]:
                            Cashed.text = Cashed.text.replace(parola,"")
            
                    if any(parola in Cashed.text for parola in [" indietro"]):
                        p.press('prevtrack',2)
                        for parola in [" indietro"]:
                            Cashed.text = Cashed.text.replace(parola,"")

                    if any(parola in Cashed.text for parola in [" volume "]):
                        Cashed.text = Cashed.text.replace("volume","")
                        if any(parola in Cashed.text for parola in ["muto"]):
                            p.hotkey('volumemute')
                            Cashed.text = Cashed.text.replace("muto","")
                        if any(parola in Cashed.text for parola in ["zero"]):
                            p.press('volumedown',50)
                            Cashed.text = Cashed.text.replace("zero","")
                        if any(parola in Cashed.text for parola in [" 10"," 20"," 30"," 40"," 50"," 60"," 70"," 80"," 90"," 100"]):
                            Cashed.text = (Cashed.text.replace(" a ", ""))
                            volume = str.strip(Cashed.text)
                            volume = volume[0:3]
    
                            volume = (int(volume) / 2)
                            volume = (str(volume).replace(".0",""))


                            p.press('volumedown',100)
                            p.press('volumeup',int(volume))


                            for parola in ["10","20","30","40","50","60","70","80","90","100"]:
                                Cashed.text = Cashed.text.replace(parola,"")
                        else:
                            print("valore non accettato")
                                    
                    for parola in ["play","pausa","skip","avanti","schippa","indietro","volume"]:
                        Cashed.text = Cashed.text.replace(parola,"")

                
                if any(parola in Cashed.text for parola in Alphabet.e):         #SCREENSHOT
                    p.screenshot(path / 'ScreenShot.png')
                    print(bcolors.OK + "Ho fatto uno ScreenShot" + bcolors.RESET)
                    engine.say("Ho fatto uno ScreenShot")
                    engine.runAndWait()

                    for parola in ["screenshot"]:
                        Cashed.text = Cashed.text.replace(parola,"")


                if any(parola in Cashed.text for parola in Alphabet.f):         #CORSIVO
                    try:
                        print( bcolors.OK + "ma certo, amiooœ, ho studiato e ora sono tra i migliori alunneæ,seguo tutte le lezioni di cörsivooœ, non vedo l'ora arrivi la prossima verificaaæ" + bcolors.RESET)
                        engine.say("ma certo, amiooœ, ho studiato e ora sono tra i migliori alunneæ,seguo tutte le lezioni di cörsivooœ, non vedo l'ora arrivi la prossima verificaaæ")
                        engine.runAndWait()
                        sleep(3)
                    except:
                        pass


                    for parola in ["sai parlare in corsivo"]:
                        Cashed.text = str.strip(Cashed.text.replace(parola,""))


                if any(parola in Cashed.text for parola in Alphabet.g):         #SPEGNI UN DISPOSITIVO

                    try:
                        if any(parola in Cashed.text for parola in ["pc", "computer"]):
                            os.system('shutdown /s /t 0')


                    except:
                        if value.ripetere == "True" :
                            ripetere()


                    for parola in ["spegni"]:
                        Cashed.text = Cashed.text.replace(parola,"")


                if any(parola in Cashed.text for parola in Alphabet.h):         #WIKIPEDIA \ GOOGLE
                    
                    try:
                        for parola in ["cerca","cosa","significato","significa","il","di"]:
                            Cashed.text = str.strip(Cashed.text.replace(parola,""))                      
                        print(bcolors.OK +"cerco il significato di " + Cashed.text + bcolors.RESET)
                        engine.say("cerco il significato di " + Cashed.text)
                        engine.runAndWait()
                        
                        
                        try:
                            wikipedia.set_lang("it")
                            Cashed.risposta = wikipedia.summary(Cashed.text, sentences=3)


                            for parola in [',','.',';',':']:
                                Cashed.risposta = str.strip(Cashed.risposta.replace(parola,'\n'))
                            for parola in ['==']:
                                Cashed.risposta = str.strip(Cashed.risposta.replace(parola, '||'))



                            print( bcolors.OK +"Secondo Wikipedia:"+ bcolors.RESET + '\n' + Cashed.risposta)
                            engine.say("Secondo Wikipedia: " + "," + Cashed.risposta)
                            engine.runAndWait()
                        except:
                            link = googlesearch.lucky(Cashed.saved_text)
                            link = googlesearch.filter_result(link=link)
                            webbrowser.open_new_tab(link)

                            print(bcolors.OK +"ho trovato questo risultato" + bcolors.RESET)
                            engine.say("ho trovato questo risultato")
                            engine.runAndWait()

                        #search(query=link,tld=domain[1],lang='it',tbs=3,safe='on')
                    except:
                        pass


                elif any(parola in Cashed.text for parola in Alphabet.i):       #APRI
                    for parola in ["apri","esegui"]:
                        Cashed.text = str.strip(Cashed.text.replace(parola,""))
                    
                    def Find_App():
      
                        n = 0
                        for colums in ["DISCO","DIR1","DIR2","DIR3","DIR4","DIR5","EXE"]:
                            a = (str(df[colums] [df["APP"] == Cashed.text]))

                            for i in ["Name:","dtype: object", "DISCO","DIR1","DIR2","DIR3","DIR4","DIR5","EXE",","]:
                                a = str.strip(a.replace(i,""))
                            a = a[5::]


                            patH.All[n] = a

                            n = n + 1

                        patH.disco = patH.All[0]
                        patH.dir1 = patH.All[1]
                        patH.dir2 = patH.All[2]
                        patH.dir3 = patH.All[3]
                        patH.dir4 = patH.All[4]
                        patH.dir5 = patH.All[5]
                        patH.EXE = patH.All[6]



                        patH.Path_exe = str.strip(patH.disco + patH.dir1 + patH.dir2 + patH.dir3 + patH.dir4 + patH.dir5 + patH.EXE)
                        


                        if "NaN" in patH.Path_exe:
                            patH.Path_exe = str.strip(patH.Path_exe.replace("NaN",""))        
                    Find_App()

                    def Find_Exe():
                        n = 0

                        while True:
                            patH.Path_exe[n::]
                            
                            if "\\" in patH.Path_exe[n::]:
                                n = n + 1                         
                            if not "\\" in patH.Path_exe[n::]:
                                patH.Exe = patH.Path_exe[n::]
                                break
                    Find_Exe()


                    if "http" in patH.Path_exe:
                        try:
                            print(bcolors.OK + "sto aprendo " + Cashed.text + bcolors.RESET)
                            engine.say("sto aprendo " + Cashed.text)
                            engine.runAndWait()


                            link = str.strip(patH.Path_exe.replace(' ',''))
                            webbrowser.open_new_tab(link)
                        except:
                            print(bcolors.WARNING + "errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione" + bcolors.RESET)
                            engine.say("errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione")
                            engine.runAndWait()
                            sleep(1)
                            if value.ripetere == "True" :
                                ripetere()
                    elif "exe" in patH.Path_exe:
                        try:
                            print(bcolors.OK +"sto aprendo " + Cashed.text + bcolors.RESET)
                            engine.say("sto aprendo " + Cashed.text)
                            engine.runAndWait()
                            subprocess.Popen([patH.Path_exe])
                        except:
                            print(bcolors.WARNING + "errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione" + bcolors.RESET)
                            engine.say("errore durante l'apertura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione")
                            engine.runAndWait()
                            sleep(1)
                            if value.ripetere == "True" :
                                ripetere()
                    elif patH.Path_exe == "s([]   )s([]   )s([]   )s([]   )s([]   )s([]   )s([]   )":
                        try:
                            print(bcolors.WARNING + "non ho trovato nessuna applicazione chiamata " + Cashed.text + ", la cercherò per te sul tuo browser" + bcolors.RESET)
                            engine.say("non ho trovato nessuna applicazione chiamata: " + Cashed.text + ", la cercherò per te sul tuo browser")
                            engine.runAndWait()
                            link = googlesearch.lucky(Cashed.text)
                            webbrowser.open_new_tab(link)
                        except:
                            pass
                      
                
                elif any(parola in Cashed.text for parola in Alphabet.j):       #CHIUDI
                    for parola in ["chiudi"]:
                        Cashed.text = str.strip(Cashed.text.replace(parola,""))

                    ###FIND_APP_AND_EXE###
                    def Find_App():
      
                        n = 0
                        for colums in ["DISCO","DIR1","DIR2","DIR3","DIR4","DIR5","EXE"]:
                            a = (str(df[colums] [df["APP"] == Cashed.text]))

                            for i in ["Name:","dtype: object", "DISCO","DIR1","DIR2","DIR3","DIR4","DIR5","EXE",","]:
                                a = str.strip(a.replace(i,""))
                            a = a[5::]


                            patH.All[n] = a

                            n = n + 1

                        patH.disco = patH.All[0]
                        patH.dir1 = patH.All[1]
                        patH.dir2 = patH.All[2]
                        patH.dir3 = patH.All[3]
                        patH.dir4 = patH.All[4]
                        patH.dir5 = patH.All[5]
                        patH.EXE = patH.All[6]



                        patH.Path_exe = str.strip(patH.disco + patH.dir1 + patH.dir2 + patH.dir3 + patH.dir4 + patH.dir5 + patH.EXE)
                        


                        if "NaN" in patH.Path_exe:
                            patH.Path_exe = str.strip(patH.Path_exe.replace("NaN",""))        
                    

                        ###FIND_EXE###
                        def Find_Exe():
                            i = 0

                            while True:
                                patH.Path_exe[i::]
                            
                                if "\\" in patH.Path_exe[i::]:
                                    i = i + 1                         
                                if not "\\" in patH.Path_exe[i::]:
                                    patH.Exe = patH.Path_exe[i::]
                                    break
                        Find_Exe()                    
                    Find_App()


                    try:
                        print(bcolors.OK + "sto chiudendo " + Cashed.text + bcolors.RESET)
                        engine.say("sto chiudendo " + Cashed.text)
                        engine.runAndWait()
                        os.system("TASKKILL /F /IM " + patH.Exe)
                    except:
                        print(bcolors.WARNING +"errore durante la chiusura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo" + bcolors.RESET)
                        engine.say("errore durante la chiusura di " + Cashed.text + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo")
                        sleep(1)
                        if value.ripetere == "True" :
                            ripetere()


                elif any(parola in Cashed.text for parola in Alphabet.k):       #CALCOLATRICE
                    for parola in ["quanto fa"]:
                        Cashed.text = str.strip(Cashed.text.replace(parola,""))

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


                elif any(parola in Cashed.text for parola in Alphabet.l):       #TTS
                    try:
                        for parola in ["ripeti"]:
                            Cashed.text = str.strip(Cashed.text.replace(parola,""))

                        print(bcolors.OK + Cashed.text + bcolors.RESET)
                        engine.say(Cashed.text)
                        engine.runAndWait()
                    except:
                        print("non sono stata in grado di ripetere la frase")


                elif any(parola in Cashed.text for parola in Alphabet.m):       #SPEGNI SIRI
                    print("siri si sta spegnendo...")
                    engine.say ("siri si sta spegnendo")
                    engine.runAndWait()
                    Cashed.loop = 0
                    kill


                else:
                    t = str.strip(Cashed.text.replace(" ", "_"))
                    print(t)


                    for y in Alphabet.Alphabet:

                        if y in t:
                            x = False
                            break
                        if t == Alphabet.null:
                            x = False
                            break
                        else:
                            x = True
                    
                    
                    
                    
                    if x == True:
                        if value.ripetere == "True":
                            ripetere()


    except:
        Cashed.request_name = 0
        Cashed.request_dialog = 0
        Cashed.request_text = 1
        print(bcolors.FAIL + "errore" + bcolors.RESET)
        Listening()
    finally:
        Cashed.request_saluto = 1
        Cashed.text = "NaN"

        if Cashed.risposta != "NaN":
            Cashed.risposta = "NaN"
        if Cashed.saved_text == "siri":
            pass
        elif "siri" in Cashed.text:
            if value.tempo_impiegato == "True":
                tempo_impiegato()
                end = time.time()
                time_passed = (end - Cashed.start)
                print(bcolors.WARNING + str(time_passed) + bcolors.RESET)
        if Cashed.loop == 1:
            Listening()




if Cashed.loop == 1:
    Listening()



from datetime import datetime
import python_weather as pw
import asyncio
import keyboard as kb
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
import json
import bs4
import requests
import webbrowser
import sys
from Cecker import value
from Cecker import Function
from Cecker import df
from Cecker import path
from Cecker import bcolors
#p.write('Hello world!', interval=0.25)


class temp:
    n = 1
    nOperandType = 1
    loop = None
    PreCashedDato = None

class Orario:
    HHeMM = None
    Ptype = None



class Cashed:
    loop = 1
    start = 0

    request_name = 0
    request_text = 1
    request_dialog = 0
    request_saluto = 1
    request_risposta = 0

    TTS = "NaN"
    name = "NaN"
    text = "NaN"
    dato = "NaN"
    risposta = "NaN"
    dialog = "NaN"
    saved_text = "NaN"
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
class Alphabet:

    Caller = ["siri_","ok_google_","alexa_"]

    a = ["ciao","ehi","buongiorno","buonasera","buon pomeriggio"]
    b = ["_ore_", "_ora_","_promemoria_","_sveglia_"]
    c = ["_temperatura_c'è_a_","_clima_c'è_a_","_tempo_c'è_a_","_tempo_fa_a_","_temperatura_c'è_in_","_clima_c'è_in_","_tempo_c'è_in_","_tempo_fa_in_"] #_c'è_a_ #fa #a #in
    d = ["_riproduci_","_play", "_pausa", "_skip","_schippa", "_avanti", "_indietro", "_volume_" ]
    e = ["_screenshot"]
    f = ["sai_parlare_in_corsivo"]
    g = ['_spegni_','_riavvia_','_avvia_','_sospendi_','_iberna_']
    h = ["_cos'è_","_chi_è_","_cerca_il_significato_di_","cerca_"]
    i = ["_apri_", "_esegui_","_avvia_"]
    j = ["_chiudi_"]
    k = ["_quanto_fa_","_calcola_"]
    l = ["_ripeti_"]
    m = ["_spegniti","_stop","_exit"]



    null = '_'
    Alphabet = a + b + c + d + e + f + g + h + i + j + k + l + m
    accept_info = i + h + j + k + l + g + c + b
    accept_info.append(d[7])
    accept_info.append(d[0])
class Parser:

    Phrase = None
    Start = None
    Finish = None
    Separator = None

    def Parsing(Phrase: "any",Start: "any",Finish: "any",Separator:"any"):
        Parser.Phrase = Phrase
        Parser.Start = Start
        Parser.Finish = Finish
        Parser.Separator = Separator


        try:
            if Phrase.islower() == True:
                pass
            else:
                Phrase.lower()
        
            Phrase = Start + Phrase + Finish
            Phrase = Phrase.replace(' ',Separator)

            Cashed.TTS = Phrase
        except Exception as e:
            print(e)
    def UnParsing():
        if Parser.Phrase == None:
            raise UnboundLocalError("UnboundLocalError: Parser.Phrase is Unbound, try <Parser.Parsing(Phrase: any,Start: any,Finish: any,Separator:any)>")
        if Parser.Start == None:
            raise UnboundLocalError("UnboundLocalError: Parser.Start is Unbound, try <Parser.Parsing(Phrase: any,Start: any,Finish: any,Separator:any)>")
        if Parser.Finish == None:
            raise UnboundLocalError("UnboundLocalError: Parser.Finish is Unbound, try <Parser.Parsing(Phrase: any,Start: any,Finish: any,Separator:any)>")
        if Parser.Separator == None:
            raise UnboundLocalError("UnboundLocalError: Parser.Separator is Unbound, try <Parser.Parsing(Phrase: any,Start: any,Finish: any,Separator:any)>")
        else:
            try:
                if Parser.Phrase.islower() == True:
                    pass
                else:
                    Parser.Phrase.lower()
                    Parser.Phrase.capitalize()
        
                for i in [Parser.Start,Parser.Finish]:
                    Parser.Phrase = Parser.Phrase.replace(i,'')
                for i in [Parser.Separator]:
                    Parser.Phrase = Parser.Phrase.replace(i,' ')
        
                Cashed.TTS = Parser.Phrase
            except Exception as e:
                print(e)
    def ForceUnParsing(Phrase: "any",Start: "any",Finish: "any",Separator:"any",Disable_Capitalize: "bool"):
            Parser.Phrase = Phrase
            Parser.Start = Start
            Parser.Finish = Finish
            Parser.Separator = Separator
            try:

                for i in [Parser.Start,Parser.Finish]:
                    Parser.Phrase = Parser.Phrase.replace(i,'')
                for i in [Parser.Separator]:
                    Parser.Phrase = Parser.Phrase.replace(i,' ')

                Parser.Phrase = str.strip(Parser.Phrase)

                if Parser.Phrase.islower() == False:
                    Parser.Phrase = Parser.Phrase.lower()
                else:
                    pass

                if Disable_Capitalize == False:
                    Parser.Phrase = Parser.Phrase.capitalize()
                else:
                    pass

                Cashed.dato = Parser.Phrase

            except Exception as e:
                print(e)

    class Function():

        Function = None
        parola = None
        inizio_funzione = 0
        i = 0
        e = 1       

        def InfoFinder(Phrase:"str", ToPass: "value", Unparsing: "bool", Block_to_Function: "bool"):
            Parser.Function.e = Parser.Function.inizio_funzione + 1
            Dato = Phrase[Parser.Function.inizio_funzione:Parser.Function.e]


            if ToPass == -1:
                loop = True
                while loop == True:
                    
                    if Parser.Finish in Phrase[Parser.Function.inizio_funzione:Parser.Function.e]:
                        Dato = Phrase[Parser.Function.inizio_funzione:Parser.Function.e]
                        Cashed.dato = Dato
                        break                 
                    else:
                        if Block_to_Function == 1:
                            for parola in Alphabet.Alphabet:
                                if Phrase[Parser.Function.inizio_funzione:Parser.Function.e].find(parola) != -1:
                                    Parser.Function.e = Parser.Function.e - len(parola)
                                    Dato = Phrase[Parser.Function.inizio_funzione:Parser.Function.e]
                                    Cashed.dato = Dato
                                    loop = False
                                    break
                        Parser.Function.e = Parser.Function.e + 1

            elif ToPass != -1:
                Passed = 0
                while Passed < ToPass:
                    if Parser.Finish in Phrase[Parser.Function.inizio_funzione:Parser.Function.e]:
                        Dato = Phrase[Parser.Function.inizio_funzione:Parser.Function.e]
                        Cashed.dato = Dato
                        break
                    elif Parser.Separator in Phrase[Parser.Function.inizio_funzione:Parser.Function.e]:
                        Dato = Phrase[Parser.Function.inizio_funzione:Parser.Function.e]
                        Cashed.dato = Dato
                        Parser.Function.inizio_funzione = Parser.Function.e
                        Parser.Function.e = Parser.Function.e + 1
                        Passed = Passed + 1
                    else:
                        if Parser.Finish in Phrase[Parser.Function.inizio_funzione:Parser.Function.e]:
                            Dato = Phrase[Parser.Function.inizio_funzione:Parser.Function.e]
                            Cashed.dato = Dato
                            break
                        else:
                            Parser.Function.e = Parser.Function.e + 1
            
            if Unparsing == True:
                Parser.ForceUnParsing(Cashed.dato,'<','>','_',True)
               
        def FuncFinder(Phrase: "any", Find_Data: "bool", ToPass: "any"):
            def WordFinder():
                Parser.Function.e = Parser.Function.i + 1
                try:
                    while True:
                        if Parser.Function.parola in Phrase[Parser.Function.i:Parser.Function.e]:
                            Parser.Function.inizio_funzione = Parser.Function.e
                            Parser.Function.Function = Parser.Function.parola
                            Parser.Function.e = Parser.Function.e +1
                            
                            if Find_Data == True:
                                Parser.Function.InfoFinder(Phrase=Phrase,ToPass=ToPass)
                            break
                        else:
                            Parser.Function.e = Parser.Function.e+1
                        if Parser.Finish in Phrase[Parser.Function.i:Parser.Function.e]:
                            Parser.Function.e = 1
                            break
                except Exception as e:
                    print(e)
                finally:
                    pass

            for parola in Alphabet.accept_info:
                if Phrase.find(parola) != -1:
                    Parser.Function.parola = parola
                    Parser.Function.i = Phrase.find(Parser.Function.parola)
                    WordFinder()


engine = pyttsx3.init()
sys.setrecursionlimit(10000)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
r = Recognizer()
if value.inizio == "True" :
    Function.inizio()

#for voices in voices:
    #print(voices.name)

for index, name in enumerate(Microphone.list_microphone_names()):
    DeviceId = ('{0} | \"{1}\"'.format(index, name))


    if any(parola in str(DeviceId) for parola in ['Speakers','speakers','Altoparlanti','altoparlanti']):
        pass
        #print(bcolors.RED + DeviceId + bcolors.RESET)
    
    else:
        pass
        #print(bcolors.GREEN + DeviceId + bcolors.RESET)
    #print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))




if value.richiesta == "True":
    Function.richiesta()
if value.ascolto == "True":
    Function.ascolto()

def Listening():
    try:
        with Microphone(device_index=4, sample_rate=48000, chunk_size=1024) as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            r.pause_threshold = 0.5
                
            if value.tempo_impiegato == "True":
                Cashed.start = time.time()
            audio = r.listen(source,timeout=None,phrase_time_limit=5)

            Cashed.TTS = r.recognize_google(audio,language="it-IT").lower()
            #Cashed.TTS = 'siri che temperatura c\'è a Padova'
            #Cashed.TTS = 'siri imposta un promemoria per le 2:30'
            
            
            Parser.Parsing(Cashed.TTS,'<','>','_')
            if any(parola in Cashed.TTS for parola in Alphabet.Caller):
                print('\n' + bcolors.ACQUA + '-----[Task Accepted]-----' + bcolors.RESET + '\n')
                print(Cashed.TTS)

                with open(str(path) + "\Results\microphone-results "+ str(datetime.now().strftime('%H-%M-%S')) +".wav", "wb") as f:
                    wav_data = audio.get_wav_data()
                    f.write(wav_data)
                    #print(str(path) + "\microphone-results "+ str(datetime.now().strftime('%H-%M-%S')) +".wav")
                    #print(wav_file)






                try:
                    Exception_Called = False
                    if Cashed.request_name == 1:
                        Cashed.name = Cashed.TTS
                        Cashed.text = Cashed.saved_text
                        Cashed.request_name = 0
                    if Cashed.request_text == 1:
                        Cashed.text = Cashed.TTS
                        Cashed.saved_text = Cashed.text
                    if Cashed.request_dialog == 1:
                        Cashed.dialog = Cashed.TTS
                        Cashed.text = Cashed.saved_text
                except Exception as e:
                    Exception_Called = True
                    print(bcolors.RED + str(e) + bcolors.RESET)
                finally:
                    if Exception_Called == True:
                        kill
                    else:
                        Attempt()
            else:
                Listening()


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
    except KeyboardInterrupt as e:
        Cashed.request_text = 1
        Cashed.request_name = 0
        Cashed.request_dialog = 0
        #print(e)


def Attempt():
    try:

        if Cashed.request_text == 1:

            if any(parola in Cashed.text for parola in Alphabet.Caller):
                if any(parola in Cashed.text for parola in Alphabet.Alphabet):
                    pass
                else:
                    if value.ripetere == "True":
                        Function.ripetere()


                ###RISPOSTE###



                #RIAGGIUNGERE# riaggiungere dalla versione precedente
                if any(parola in Cashed.text for parola in Alphabet.a):         #SALUTI
                    Cashed.request_dialog = 1
                    Cashed.request_text = 0
                    Cashed.text = Cashed.saved_text
                    Attempt()

                #COMPLETATO# aggiungere piu' funzioni relative al tempo
                if any(parola in Cashed.text for parola in Alphabet.b):         #ORARIO



                    if any(parola in Cashed.text for parola in Alphabet.b[2:3]): #PROMEMORIA
                        #print(Alphabet.b[2:3])
                        try:
                            Parser.Function.FuncFinder(Cashed.text,False,None)

                            def HoursFinder():
                                Parser.Function.InfoFinder(Cashed.text,temp.n,True,True)
                                try:
                                    if Cashed.dato.isnumeric():
                                        if ':' in Cashed.dato:
                                            pass
                                        else:
                                            Orario.HHeMM = Cashed.dato + ':00'
                                            if len(Orario.HHeMM) == 4:
                                                Orario.HHeMM = '0' + Orario.HHeMM
                                            print("HHeMM = " + str(Orario.HHeMM))           
                                    elif ':' in Cashed.dato:
                                        Orario.HHeMM = Cashed.dato
                                        if len(Orario.HHeMM) == 4:
                                            Orario.HHeMM = '0' + Orario.HHeMM
                                        print("HHeMM = " + str(Orario.HHeMM))
                                    else:
                                        if Cashed.dato != temp.PreCashedDato:
                                            temp.PreCashedDato = Cashed.dato
                                            #print("valore non accettato " + Cashed.dato)
                                            temp.n = 1
                                            HoursFinder()
                                        else:
                                            pass
                                    
                                    Orario.Ptype = 'promemoria'
                                
                                
                                
                                except Exception as e:
                                    print(bcolors.RED + str(e) + bcolors.RESET)
                            HoursFinder()


                            cmd = 'python Orologio.py'
                            subprocess.run(cmd,start_new_session=True,restore_signals=True,shell=True)

                        
                        except Exception as e:
                            print(bcolors.RED + str(e) + bcolors.RESET)
                        finally:
                            for parola in Alphabet.b[2:3]:
                                Cashed.text = str.strip(Cashed.text.replace(parola,''))

                    if any(parola in Cashed.text for parola in Alphabet.b[3:4]): #SVEGLIA
                        #print(Alphabet.b[3:4])
                        try:
                            pass  
                        
                        
                        
                        except Exception as e:
                            print(bcolors.RED + str(e) + bcolors.RESET)
                        finally:
                            for parola in Alphabet.b[3:4]:
                                Cashed.text = str.strip(Cashed.text.replace(parola,''))

                    if any(parola in Cashed.text for parola in Alphabet.b[0:2]): #ORA ATTUALE
                        try:
                            Cashed.risposta = f"sono le ore {datetime.now().strftime('%H e %M')}"
                            print(bcolors.GREEN + Cashed.risposta + bcolors.RESET)
                            engine.say(Cashed.risposta)
                            engine.runAndWait()
                        except Exception as e:
                            print(bcolors.RED + e + bcolors.RESET)   
                        finally:
                            for parola in Alphabet.b[0:2]:
                                Cashed.text = Cashed.text.replace(parola,"")

                #SISTEMARE# aggiungere piu' richieste, ordinare...
                if any(parola in Cashed.text for parola in Alphabet.c):         #TEMPERATURA
                    Parser.Function.FuncFinder(Cashed.text,False,None)
                    try:
                        temp.n = -1
                        temp.loop = True
                        bypass = False
                        format = 'C'
                        #.strftime('%H e %M')

                        async def GetWeather():
                            try:
                                        #"Ora" : None,
                                        #"temperatura" : None,
                                        #"prob_sole" : None,
                                        #"prob_pioggia" : None,
                                        #"prob_nuvoloso" : None,
                                        #"descrizione" : None,
                                def WeatherInfo():
                                    array = [
                                        {"Ora0" : None},{"temperatura0" : None},{"prob_sole0" : None},{"prob_pioggia0" : None},{"prob_nuvoloso0" : None},{"descrizione0" : None},
                                        {"Ora1" : None},{"temperatura1" : None},{"prob_sole1" : None},{"prob_pioggia1" : None},{"prob_nuvoloso1" : None},{"descrizione1" : None},
                                        {"Ora2" : None},{"temperatura2" : None},{"prob_sole2" : None},{"prob_pioggia2" : None},{"prob_nuvoloso2" : None},{"descrizione2" : None},
                                        {"Ora3" : None},{"temperatura3" : None},{"prob_sole3" : None},{"prob_pioggia3" : None},{"prob_nuvoloso3" : None},{"descrizione3" : None},
                                        {"Ora4" : None},{"temperatura4" : None},{"prob_sole4" : None},{"prob_pioggia4" : None},{"prob_nuvoloso4" : None},{"descrizione4" : None},
                                        {"Ora5" : None},{"temperatura5" : None},{"prob_sole5" : None},{"prob_pioggia5" : None},{"prob_nuvoloso5" : None},{"descrizione5" : None},
                                        {"Ora6" : None},{"temperatura6" : None},{"prob_sole6" : None},{"prob_pioggia6" : None},{"prob_nuvoloso6" : None},{"descrizione6" : None},
                                        {"Ora7" : None},{"temperatura7" : None},{"prob_sole7" : None},{"prob_pioggia7" : None},{"prob_nuvoloso7" : None},{"descrizione7" : None},
                                        
                                        
                                        
                                        
                                        ]

                                    #first = array[7:13]
                                    #print(first)

                                    try:
                                        print(weather.nearest_area.region,weather.nearest_area.country,weather.nearest_area.name, weather.location)



                                        for forecast in weather.forecasts:
                                            print(bcolors.ACQUA + '\n' + str(forecast.date) + ' | ' + str(forecast.temperature) + '°'+ str(forecast.format) + '\n' + bcolors.RESET)
                                    
                                            for hourly in forecast.hourly:
                                                #array = ('ore: ' + (str(hourly.time)).replace('00','')  + ' | temperatura: ' + str(hourly.temperature) + '°'+ str(forecast.format)  + ' | probabilita di sole: ' + str(hourly.chance_of_sunshine) + '%' + ' | probabilita di pioggia: ' + str(hourly.chance_of_rain) + '%' + ' | probabilita di nuvoloso: ' + str(hourly.chance_of_overcast) + '%' + ' | descrizione giornata: ' + bcolors.ACQUA +  str(hourly.description) + bcolors.RESET)
                                                array = [{'ora' : str(hourly.time).replace('00',':00'),},{'temperatura' : str(hourly.temperature) + '°'+ str(forecast.format),},{'probabilita\' di sole' :str(hourly.chance_of_sunshine) + '%',},{'probabilita\' di pioggia' :str(hourly.chance_of_rain) + '%',},{'probabilita\' di nuvoloso' :str(hourly.chance_of_overcast) + '%',},{'descrizione' :str(hourly.description),},]
                                                print(array)






                                    except Exception as e:
                                        print(bcolors.RED + str(e) + bcolors.RESET)         




                                async with pw.Client(format=pw.IMPERIAL) as client:
                                    weather = await client.get(Cashed.dato,format=format) #city
                                    if weather.location == None:
                                        temp.loop = False
                                        engine.say('Expected \"ONE of this info(\'region\',\'country\',\'name = \'town\'\'\", got ' + str(Cashed.dato))
                                        engine.runAndWait()
                                        raise pw.InvalidArg(expected='ONE of this info(\'region\',\'country\',\'name = \'town\'\'',got=Cashed.dato + ')')
                                    else:
                                        temp.loop = False
                                        WeatherInfo()
                            
                            
  
                            except Exception as e:
                                print(bcolors.RED + str(e) + bcolors.RESET)
                        
                        while temp.loop == True:
                            try:
                                def CityFinder():
                                    Parser.Function.InfoFinder(Cashed.text,temp.n,True,True)
                                    Cashed.dato = str.strip(Cashed.dato).capitalize()

















                                CityFinder()
                                asyncio.run(GetWeather())
                            except Exception as e:
                                print(bcolors.RED + str(e) + bcolors.RESET)





                    except Exception as e:
                        print(bcolors.RED + str(e) + bcolors.RESET)
                    finally:
                        for parola in Alphabet.c:
                            Cashed.text = str.strip(Cashed.text.replace(parola,''))

                #COMPLETATO# cercare un metodo per riprodurre con spotify, anche solo online, cercare una soluzione piu' efficente per il volume
                if any(parola in Cashed.text for parola in Alphabet.d):         #MUSICA

                    if any(parola in Cashed.text for parola in ["_riproduci"]):

                        Parser.Function.FuncFinder(Cashed.text,False,None)
                        Parser.Function.InfoFinder(Cashed.text,-1,True,True)

                        link = googlesearch.lucky(Cashed.dato)
                        link = googlesearch.filter_result(link=link)
                        webbrowser.open_new_tab(link)

                        print(bcolors.GREEN +"riproduco " + Cashed.dato + bcolors.RESET)
                        engine.say("riproduco " + Cashed.dato)
                        engine.runAndWait()

                        for parola in ["_riproduci"]:
                            Cashed.text = Cashed.text.replace(parola,"")

                    if any(parola in Cashed.text for parola in ["_play","_pausa"]):
                        p.hotkey('playpause')
                        for parola in ["_play","_pausa"]:
                            Cashed.text = Cashed.text.replace(parola,"")

                    if any(parola in Cashed.text for parola in ["_skip","_avanti","_schippa"]):
                        p.hotkey('nexttrack')
                        for parola in ["_skip","_avanti","_schippa"]:
                            Cashed.text = Cashed.text.replace(parola,"")
            
                    if any(parola in Cashed.text for parola in ["_indietro"]):
                        p.press('prevtrack',2)
                        for parola in ["_indietro"]:
                            Cashed.text = Cashed.text.replace(parola,"")

                    if any(parola in Cashed.text for parola in ["_volume"]):
                        if any(parola in Cashed.text for parola in ["_muto"]):
                            p.hotkey('volumemute')
                            Cashed.text = Cashed.text.replace("_muto","")
                        if any(parola in Cashed.text for parola in ["_zero"]):
                            p.press('volumedown',50)
                            Cashed.text = Cashed.text.replace("_zero","")
                        if any(parola in Cashed.text for parola in ["_10","_20","_30","_40","_50","_60","_70","_80","_90","_100"]):
                            try:
                                Parser.Function.FuncFinder(Cashed.text,False,None)
                 
                                def VolumeIntFInder():
                                    Parser.Function.InfoFinder(str.strip(Cashed.text.replace("%",'')),temp.n,True,True)


                                    try:
                                        if Cashed.dato.isnumeric() == True:
                                            if any(parola in Cashed.text for parola in ["_10","_20","_30","_40","_50","_60","_70","_80","_90","_100"]):
                                                temp.n = 1
                                                
                                                Cashed.dato = float(Cashed.dato)
                                                float_volume = Cashed.dato / 2

                                                p.press('volumedown',50)
                                                p.press('volumeup',int(float_volume))


                                                print(bcolors.GREEN + "Volume al " + str(int(Cashed.dato)) + "%" + bcolors.RESET)
                                                engine.say("Volume al " + str(int(Cashed.dato)) + "%")
                                                engine.runAndWait() 
                                                
                                                for parola in [('_' + str(int(Cashed.dato)))]:
                                                    Cashed.text = Cashed.text.replace(parola,"")
                                            else:
                                                print("VALUE ERROR: (min value: 10 ,max value: 100, other values: \"muto\": X,\"zero\": 0)")
                                                raise ValueError
                                        else:
                                            temp.n = 1
                                            VolumeIntFInder()
                                    except Exception as e:
                                        temp.n = 1
                                        print(e) 
                                VolumeIntFInder()
                            except Exception as e:
                                print(e)
                        else:
                            print(bcolors.RED + "VALUE ERROR: (min value: 10 ,max value: 100, other values: \"muto\": X,\"zero\": 0)" + bcolors.RESET)
                        Cashed.text = Cashed.text.replace("_volume","")

                #COMPLETATO# aggiungere altre funzioni di pyautogui
                if any(parola in Cashed.text for parola in Alphabet.e):         #SCREENSHOT
                    try:
                        p.screenshot(str(path) + '\ScreenShots' + '\ScreenShots' + str(datetime.now().strftime(' %H-%M-%S')) + '.png' )
                        print(bcolors.GREEN + "Ho fatto uno ScreenShot" + '\n' + "Nome del file: " + 'ScreenShots' + str(datetime.now().strftime(' %H-%M-%S')) + '.png'  + bcolors.RESET)
                        engine.say("Ho fatto uno ScreenShot")
                        engine.runAndWait()

                    except Exception as e:
                        print(bcolors.RED + e + bcolors.RESET)
                    finally:
                        for parola in Alphabet.e:
                            Cashed.text = Cashed.text.replace(parola,"")

                #COMPLETARE#
                if any(parola in Cashed.text for parola in Alphabet.g):         #SPEGNI UN DISPOSITIVO
                    try:
                        Parser.Function.FuncFinder(Cashed.text,False,None)



                        if any(parola in Cashed.text for parola in '_spegni_'):
                            
                            if any(parola in Cashed.dato for parola in ["pc", "computer","windows"]):
                                def DeviceFinder():
                                    Parser.Function.InfoFinder(Cashed.text,temp.n,True,True)

                                    try:
                                        if any(parola in Cashed.dato for parola in ["pc", "computer"]):
                                            os.system('shutdown /s /t 0')

                                        else:
                                            temp.n = temp.n + 1
                                            DeviceFinder()
                                    except Exception as e:
                                        print(bcolors.RED + e + bcolors.RESET)
                                    finally:
                                        temp.n = 1
                                DeviceFinder()
                    
                        if any(parola in Cashed.text for parola in '_riavvia_'):
                            pass

                        if any(parola in Cashed.text for parola in '_avvia_'):
                            pass

                        if any(parola in Cashed.text for parola in '_sospendi_'):
                            pass

                        if any(parola in Cashed.text for parola in '_iberna_'):
                            pass
                    except Exception as e:
                        print(bcolors.RED + e + bcolors.RESET)
                    finally:
                        for parola in Alphabet.g:
                            Cashed.text = Cashed.text.replace(parola,"")

                #SISTEMARE# ogni tanto ci sono dei bug, migliorare la ricerca, maybe un altro pacchetto
                if any(parola in Cashed.text for parola in Alphabet.h):         #WIKIPEDIA \ GOOGLE

                    def Wikipedia(Lang: "str",Phrase: "str",Sentences: "float",Parsing: "bool"):
                        wikipedia.set_lang(Lang)
                        Cashed.risposta = wikipedia.summary(Phrase,sentences=Sentences)
                        #sentences=5
                        #'it'
                        #Cashed.dato

                        if Parsing == True:
                            for parola in [',','.',';',':','(',')']:
                                Cashed.risposta = str.strip(Cashed.risposta.replace(parola,parola +'\n'))
                            for parola in ['==','=']:
                                Cashed.risposta = str.strip(Cashed.risposta.replace(parola, '||'))        
                    def GoogleSearch(Phrase: 'any'):
                        link = googlesearch.lucky(Phrase)
                        link = googlesearch.filter_result(link=link)
                        webbrowser.open_new_tab(link)   
                    def FailedSearchSaved():
                        try:
                            GoogleSearch(Cashed.dato)

                            print(bcolors.GREEN +"ho trovato questo risultato" + bcolors.RESET)
                            engine.say("ho trovato questo risultato")
                            engine.runAndWait()
                        except Exception as e:
                            print(bcolors.RED + str(e) + bcolors.RESET)
                        finally:
                            for parola in Alphabet.h:
                                Cashed.text = str.strip(Cashed.text.replace(parola,''))

                    #search(query=link,tld=domain[1],lang='it',tbs=3,safe='on')
  
                    try:
                        Parser.Function.FuncFinder(Cashed.text,False,None)
                        Parser.Function.InfoFinder(Cashed.text,-1,True,True)
                        n = 0
                        for parola in ["_cos'è_","_chi_è_","_cerca_il_significato_di_"]:
                            if parola in Cashed.text:
                                n = n + 1
                            else:
                                pass
                        if n > 1:
                            print(bcolors.RED + "REQUEST ERROR: expected one request, but three were given: ( significato di, chi è, cos'è)")
                            sleep(10)
                            Listening()

                        print(bcolors.GREEN +"cerco " + Cashed.dato + bcolors.RESET)
                        engine.say("cerco " + Cashed.dato)
                        engine.runAndWait()

                        if any(parola in Cashed.text for parola in ["_significato_di"]):
                            try:
                                Wikipedia('it',Cashed.dato,5,True)


                                print(bcolors.GREEN +"Secondo Wikipedia:"+ bcolors.RESET + '\n' + Cashed.risposta)
                                engine.say("Secondo Wikipedia: " + "," + Cashed.risposta)
                                engine.runAndWait()
                            except Exception as e:
                                print(bcolors.RED + str(e) + bcolors.RESET)
                                FailedSearchSaved()

                        elif any(parola in Cashed.text for parola in ["_chi_è"]):             
                            try:
                                Wikipedia('it',Cashed.dato,5,True)

                                print(bcolors.GREEN +"Secondo Wikipedia:"+ bcolors.RESET + '\n' + Cashed.risposta)
                                engine.say("Secondo Wikipedia: " + "," + Cashed.risposta)
                                engine.runAndWait()

                            except Exception as e:
                                print(bcolors.RED + str(e) + bcolors.RESET)
                                FailedSearchSaved()

                        elif any(parola in Cashed.text for parola in ["_cos'è"]):
                            try:
                                Wikipedia('it',Cashed.dato,5,True)

                                print(bcolors.GREEN +"Secondo Wikipedia:"+ bcolors.RESET + '\n' + Cashed.risposta)
                                engine.say("Secondo Wikipedia: " + "," + Cashed.risposta)
                                engine.runAndWait()
                            except Exception as e:
                                print(bcolors.RED + str(e) + bcolors.RESET)
                                FailedSearchSaved()

                        else:
                            FailedSearchSaved()
                    except Exception as e:
                        print(bcolors.RED + str(e) + bcolors.RESET)
                    finally:
                        for parola in Alphabet.h:
                            Cashed.text = str.strip(Cashed.text.replace(parola,''))

                #COMPLETATO#
                if any(parola in Cashed.text for parola in Alphabet.i):         #APRI

                    Parser.Function.FuncFinder(Cashed.text,False,None)
                    Parser.Function.InfoFinder(Cashed.text,1,True,True)

                    def Find_App(Phrase: "any"):
                        n = 0
                        for colums in ["DISCO","DIR1","DIR2","DIR3","DIR4","DIR5","EXE"]:
                            a = (str(df[colums] [df["APP"] == Phrase]))

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
                    Find_App(Cashed.dato)

                    def Find_Exe(Path: "any"):
                        n = 0

                        while True:
                            Path[n::]
                            
                            if "\\" in Path[n::]:
                                n = n + 1                         
                            if not "\\" in Path[n::]:
                                patH.Exe = Path[n::]
                                break
                    Find_Exe(patH.Path_exe)


                    if "http" in patH.Path_exe:
                        try:
                            print(bcolors.GREEN + "sto aprendo " + Cashed.dato + bcolors.RESET)
                            engine.say("sto aprendo " + Cashed.dato)
                            engine.runAndWait()


                            link = str.strip(patH.Path_exe.replace(' ',''))
                            webbrowser.open_new_tab(link)
                        except:
                            print(bcolors.YELLOW + "errore durante l'apertura di " + Cashed.dato + ", prova a controllare il percorso dell'applicazione" + bcolors.RESET)
                            engine.say("errore durante l'apertura di " + Cashed.dato + ", prova a controllare il percorso dell'applicazione")
                            engine.runAndWait()
                            sleep(1)
                            if value.ripetere == "True" :
                                Function.ripetere()
                    elif "exe" in patH.Path_exe:
                        try:
                            print(bcolors.GREEN +"sto aprendo " + Cashed.dato + bcolors.RESET)
                            engine.say("sto aprendo " + Cashed.dato)
                            engine.runAndWait()
                            subprocess.Popen([patH.Path_exe])
                        except:
                            print(bcolors.YELLOW + "errore durante l'apertura di " + Cashed.dato + ", prova a controllare il percorso dell'applicazione" + bcolors.RESET)
                            engine.say("errore durante l'apertura di " + Cashed.dato + ", prova a controllare il percorso dell'applicazione")
                            engine.runAndWait()
                            sleep(1)
                            if value.ripetere == "True" :
                                Function.ripetere()
                    elif patH.Path_exe == "s([]   )s([]   )s([]   )s([]   )s([]   )s([]   )s([]   )":
                        try:
                            print(bcolors.YELLOW + "non ho trovato nessuna applicazione chiamata " + Cashed.dato + ", la cercherò per te sul tuo browser" + bcolors.RESET)
                            engine.say("non ho trovato nessuna applicazione chiamata: " + Cashed.dato + ", la cercherò per te sul tuo browser")
                            engine.runAndWait()
                            link = googlesearch.lucky(Cashed.dato)
                            webbrowser.open_new_tab(link)
                        except Exception as e:
                            print(bcolors.RED + e + bcolors.RESET)
                    for parola in Alphabet.i:
                        Cashed.text = Cashed.text.replace(parola,"")
                
                #SISTEMARE# aggiungere 'try' con piu soluzioni in caso di errore
                if any(parola in Cashed.text for parola in Alphabet.j):         #CHIUDI
                    Parser.Function.FuncFinder(Cashed.text,False,None)
                    Parser.Function.InfoFinder(Cashed.text,1,True,True)

                    ###FIND_APP_AND_EXE###
                    def Find_App(Phrase: "any"):
      
                        n = 0
                        for colums in ["DISCO","DIR1","DIR2","DIR3","DIR4","DIR5","EXE"]:
                            a = (str(df[colums] [df["APP"] == Phrase]))

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
                        def Find_Exe(Path: "any"):
                            i = 0

                            while True:
                                Path[i::]
                            
                                if "\\" in Path[i::]:
                                    i = i + 1                         
                                if not "\\" in Path[i::]:
                                    patH.Exe = Path[i::]
                                    break
                        Find_Exe(patH.Path_exe)                    
                    Find_App(Cashed.dato)

                    try:
                        print(bcolors.GREEN + "sto chiudendo " + Cashed.dato + bcolors.RESET)
                        engine.say("sto chiudendo " + Cashed.dato)
                        engine.runAndWait()
                        os.system("TASKKILL /F /IM " + patH.Exe)
                        for parola in Alphabet.j:
                            Cashed.text = Cashed.text.replace(parola,"")

                    except Exception as e:
                        print(bcolors.RED + e + bcolors.RESET)
                        print(bcolors.YELLOW +"errore durante la chiusura di " + Cashed.dato + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo" + bcolors.RESET)
                        engine.say("errore durante la chiusura di " + Cashed.dato + ", prova a controllare il percorso dell'applicazione o controlla se il nome dell'applicazione e' scritto tutto in minuscolo")

                #COMPLETATO# aggiungere operazioni complesse
                if any(parola in Cashed.text for parola in Alphabet.k):         #CALCOLATRICE
                    Parser.Function.FuncFinder(Cashed.text,False,None)
                    Parser.Function.InfoFinder(Cashed.text,-1,True,True)

                    def CalcParseAndUnparse(Task: 'int'):
                        if Task == 1:
                            if "_piu_" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("_piu_","_+_"))
                            if "_meno_" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("_meno_","_-_"))          
                            if "_per_" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("_per_","_*_"))
                            if "_diviso_" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("_diviso_","_/_"))               
                            if "_elevato_" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("_elevato_","_**_"))
                            if "_a_" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("_a_","_"))  
                        if Task == 2:

                            if "+" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("+","piu"))
                            if "-" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("-","meno"))          
                            if "*" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("*","per"))
                            if "/" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("/","diviso"))               
                            if "**" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("**","elevato"))
                            if "_a_" in Cashed.text:
                                Cashed.text = str.strip(Cashed.text.replace("","_a")) 
                    CalcParseAndUnparse(1)
                    ########################
                    class Calculator:
                        FirstNumber = None
                        OperandType = None
                        SecondNumber = None
                        Request = str(FirstNumber) + ' ' + str(OperandType) + ' ' + str(SecondNumber)

                    ########################
                    def FirstNumberFinder():
                        Parser.Function.InfoFinder(Cashed.text,temp.n,True,True)
                        try:
                            if Cashed.dato.isnumeric():
                                Calculator.FirstNumber = float(Cashed.dato)
                                #print("FirstNumber " + str(Calculator.FirstNumber))
                            else:
                                #print("valore non accettato " + Cashed.dato)
                                temp.n = 1
                                FirstNumberFinder()
                        except Exception as e:
                            print(bcolors.RED + str(e) + bcolors.RESET)

                    def OperandTypeFinder():
                        Parser.Function.InfoFinder(Cashed.text,temp.n,True,True)
                        try:
                            if any(parola in Cashed.dato for parola in ['+','-','*','/','**']):
                                Calculator.OperandType = Cashed.dato
                                temp.nOperandType = temp.n
                                #print("OperandType " + str(Calculator.OperandType))
                                
                            else:
                                #print("valore non accettato " + Cashed.dato)
                                temp.n = 1
                                OperandTypeFinder()
                        except Exception as e:
                            print(bcolors.RED + str(e) + bcolors.RESET)

                    def SecondNumberFinder():
                        Parser.Function.InfoFinder(Cashed.text,temp.nOperandType,True,True)

                        try:
                            if Cashed.dato.isnumeric():
                                Calculator.SecondNumber = float(Cashed.dato)
                                #print("SecondNumber  " + str(Calculator.SecondNumber))
                            else:
                                #print("valore non accettato " + Cashed.dato)
                                temp.nOperandType = 1
                                SecondNumberFinder()
                        except Exception as e:
                            print(bcolors.RED + str(e) + bcolors.RESET)
                    ########################

                    def Calc():
                        FirstNumberFinder()
                        OperandTypeFinder()
                        SecondNumberFinder()

                        try:

                            if Calculator.OperandType == '*':
                                risposta = Calculator.FirstNumber * Calculator.SecondNumber
                            if Calculator.OperandType == '+':
                                risposta = Calculator.FirstNumber + Calculator.SecondNumber
                            if Calculator.OperandType == '-':
                                risposta = Calculator.FirstNumber - Calculator.SecondNumber
                            if Calculator.OperandType == '**':
                                risposta = Calculator.FirstNumber ** Calculator.SecondNumber
                            if Calculator.OperandType == '/':
                                risposta = Calculator.FirstNumber / Calculator.SecondNumber
                        except Exception as e:
                            print(bcolors.RED + str(e) + bcolors.RESET)

                        def Response():
                            try:

                                Calculator.Request = str(Calculator.FirstNumber) + ' ' + str(Calculator.OperandType) + ' ' + str(Calculator.SecondNumber)
                                if " + " in Calculator.Request:
                                    Calculator.Request = str.strip(Calculator.Request.replace(" + "," piu "))
                                if " - " in Calculator.Request:
                                    Calculator.Request = str.strip(Calculator.Request.replace(" - "," meno "))          
                                if " * " in Calculator.Request:
                                    Calculator.Request = str.strip(Calculator.Request.replace(" * "," per "))
                                if " / " in Calculator.Request:
                                    Calculator.Request = str.strip(Calculator.Request.replace(" / "," diviso "))               
                                if " ** " in Calculator.Request:
                                    Calculator.Request = str.strip(Calculator.Request.replace(" ** "," elevato a "))
                                Parser.ForceUnParsing(Cashed.text,'<','>','_',False)
                                rispostadef = (Calculator.Request + ", e' uguale a " + str(risposta))
                                print(bcolors.GREEN + rispostadef + bcolors.RESET)
                                engine.say(rispostadef)
                                engine.runAndWait()
                            except Exception as e:
                                print(bcolors.RED + str(e) + bcolors.RESET)
                        Response()
                    Calc()

                    for parola in Alphabet.k:
                        Cashed.text = Cashed.text.replace(parola,"")

                #RIFARE# aggiungere il finder di funzione
                if any(parola in Cashed.text for parola in Alphabet.l):         #TTS
                    try:
                        for parola in ["_ripeti_","_siri_"]:
                            Cashed.text = str.strip(Cashed.text.replace(parola,""))

                        print(bcolors.GREEN + Cashed.text + bcolors.RESET)
                        engine.say(Cashed.text)
                        engine.runAndWait()
                    except:
                        print("non sono stata in grado di ripetere la frase")

                #COMPLETATO#
                if any(parola in Cashed.text for parola in Alphabet.m):         #SPEGNI
                    try:
                        for i in Alphabet.Caller:
                            if i in Cashed.text:         
                                print(str.strip(i.replace('_','').replace('ok','')) + " si sta spegnendo...")
                                engine.say ( str.strip(i.replace('_','').replace('ok','')) + " si sta spegnendo")
                                engine.runAndWait()
                                Cashed.loop = 0
                    except Exception as e:
                        print(bcolors.RED + str(e) + bcolors.RESET)
                    finally:
                        for parola in Alphabet.m:
                            Cashed.text = Cashed.text.replace(parola,"")
                        

                if any(parola in Cashed.text for parola in Alphabet.Alphabet):
                    try:
                        Attempt()
                    finally:
                        if any(parola in Cashed.TTS for parola in Alphabet.Caller):
                            if value.tempo_impiegato == "True":
                                Function.tempo_impiegato()
                                end = time.time()
                                time_passed = (end - Cashed.start)
                                print(bcolors.YELLOW + str(time_passed) + bcolors.RESET)
                            else:
                                pass
                               
                        if Cashed.loop == 1:
                            Listening()
                else:
                    pass            
            
            else:
                if Cashed.loop == 1:
                    Listening()

        if Cashed.request_name == 1:
            pass
        
        if Cashed.request_dialog == 1:
            pass

        if Cashed.request_saluto == 1:
            pass

        if Cashed.request_risposta == 1:
            pass

    except Exception as e:
        Cashed.request_name = 0
        Cashed.request_dialog = 0
        Cashed.request_text = 1

        print(bcolors.RED + str(e) + bcolors.RESET)  
    finally:
        if any(parola in Cashed.TTS for parola in Alphabet.Caller):
            if value.tempo_impiegato == "True":
                Function.tempo_impiegato()
                end = time.time()
                time_passed = round((end - Cashed.start),1)
                print(bcolors.YELLOW + (str(time_passed) + ' s' ) + bcolors.RESET)
            print(bcolors.ACQUA + '-----[Task Closed]-----' + bcolors.RESET + '\n')
        else:
            pass


        Cashed.request_saluto = 1
        Cashed.text = "NaN"
        Cashed.TTS = "NaN"
        Cashed.risposta = "NaN"
        Cashed.dato = "NaN"


        Parser.Function.e = 1
        Parser.Function.i = 0
        Parser.Function.inizio_funzione = 0


        temp.n = 1
        temp.nOperandType
        temp.loop = None
        temp.PreCashedDato = None
        

        if Cashed.loop == 1:
            Listening()

if Cashed.loop == 1:
    Listening()


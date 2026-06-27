from dataclasses import replace
from datetime import datetime
from importlib.machinery import PathFinder
from importlib.metadata import files
from importlib.resources import path
from pathlib import Path
import random
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
from pathlib import Path

# p.write('Hello world!', interval=0.25)
#
#
#
#
#
#
#

class bcolors:

    #colori background
    BBLACK = "\033[40m"  #NERO
    BRED = "\033[41m"    #ROSSO
    BGREEN = "\033[42m"  #VERDE
    BYELLOW = "\033[43m" #GIALLO
    BBLUE = "\033[44m"   #BLU
    BMAGENTA = "\033[45m"#MAGENTA
    BACQUA = "\033[46m"  #ACQUA
    BWHITE = "\033[47m"    #BIANCO

    #colori foreground
    BLACK = "\033[30m"   #NERO
    RED = "\033[31m"     #ROSSO
    GREEN = "\033[32m"   #VERDE
    YELLOW = "\033[33m"  #GIALLO
    BLUE = "\033[34m"    #BLU
    MAGENTA = "\033[35m" #MAGENTA
    ACQUA = "\033[36m"   #ACQUA
    WHITE = "\033[37m"   #BIANCO

    RESET = '\033[0m' #RESET COLOR
    BOLD = "\E[0;1m" #BOLD

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
    dato = "NaN"
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
    h = ["cerca"]
    i = ["apri", "esegui"]
    j = ["chiudi"]
    k = ["quanto fa"]
    l = ["ripeti"]
    m = ["spegniti","stop","exit"]



    null = '_'
    Alphabet = a + b + c + d + e + f + g + h + i + j + k + l + m
    accept_info = i + h + j + k + l
    accept_info.append(d[7])
    accept_info.append(d[0])
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

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
r = Recognizer()

try:
    ###Checking file location###
    try:
        path = Path(__file__).absolute().parent
        dr = pd.read_excel(path / 'Files/Settings.xlsx')
        ds = pd.read_excel(path / 'Files/CashedApp.xlsx')
    except FileNotFoundError as e:
        print(bcolors.RED + e + bcolors.RESET)
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
        engine.say (bcolors.YELLOW + inizio + bcolors.RESET)
        engine.runAndWait()

    def ascolto():
        ascolto =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
        ascolto = str.strip(ascolto.replace("Name: OBJECT, dtype: object",""))
        ascolto = ascolto[5::]
        print (bcolors.GREEN + ascolto + bcolors.RESET) 

    def richiesta():
        richiesta =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
        richiesta = str.strip(richiesta.replace("Name: OBJECT, dtype: object",""))
        richiesta = richiesta[5::]
        print (bcolors.GREEN + richiesta + bcolors.RESET)
        #print("")
        engine.say (richiesta)
        engine.runAndWait()

    def ripetere():
        ripetere =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RIPETERE" ]))
        ripetere = str.strip(ripetere.replace("Name: OBJECT, dtype: object",""))
        ripetere = ripetere[5::]
        print (bcolors.GREEN + ripetere + bcolors.RESET)
        engine.say(ripetere)
        engine.runAndWait()   

    def tempo_impiegato():
        tempoimp =(str(dt["OBJECT"] [dt["SETTING"] == "TEMPO IMPIEGATO" ]))
        tempoimp = str.strip(tempoimp.replace("Name: OBJECT, dtype: object",""))
        tempoimp = tempoimp[5::]
        print(bcolors.YELLOW + tempoimp + bcolors.RESET) 

    if value.inizio == "True" :
        inizio()
except:
    print(bcolors.RED + "controlla le impostazioni..." + bcolors.RESET)
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
            #audio = r.listen(source,timeout=3)
            #TTS = r.recognize_google(audio, language="it-IT").lower()
            TTS = "siri cerca giorgia meloni a letto con di maio"
            Cashed.text = TTS



            Parser.Parsing()
            #Parser.Function.FuncFinder()
            #print([Parser.Function.parola])
            #Parser.Function.IInfoFinder()
            #print([Cashed.dato])
            #Parser.Function.InfoFinder()
            #print([Cashed.dato])

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






class Parser():

    def Parsing():

        if Cashed.text.islower() == True:
            pass
        else:
            Cashed.text.lower()
        
        Cashed.text = '<' + Cashed.text + '>'
        Cashed.text = Cashed.text.replace(' ','_')

    def UnParsing():

        if Cashed.text.islower() == True:
            Cashed.text.lower()
            Cashed.text.capitalize()
        else:
            Cashed.text.lower()
            Cashed.text.capitalize()
        
        for i in ['<','>']:
            Cashed.text = Cashed.text.replace(i,'')
        for i in ['_']:
            Cashed.text = Cashed.text.replace(i,' ')

    class Function():

        parola = "NaN"
        loop = True
        i = 0
        e = 1
        ee = 0
    
        def IInfoFinder():
            Parser.Function.ee = Parser.Function.e + 1
            while True:
                Cashed.text[Parser.Function.e:Parser.Function.ee]
                if '>' in Cashed.text[Parser.Function.e:Parser.Function.ee]:
                    Parser.Function.ee = Parser.Function.ee - 1
                    Cashed.dato = Cashed.text[Parser.Function.e:Parser.Function.ee]
                    break                    
                else:
                    Parser.Function.ee = Parser.Function.ee+1
    
        def InfoFinder():
            Parser.Function.ee = Parser.Function.e + 1
            while True:
                Cashed.text[Parser.Function.e:Parser.Function.ee]
                if '_' in Cashed.text[Parser.Function.e:Parser.Function.ee]:
                    Parser.Function.ee = Parser.Function.ee - 1
                    Cashed.dato = Cashed.text[Parser.Function.e:Parser.Function.ee]
                    break
                if '>' in Cashed.text[Parser.Function.e:Parser.Function.ee]:
                    Parser.Function.ee = Parser.Function.ee - 1
                    Cashed.dato = Cashed.text[Parser.Function.e:Parser.Function.ee]
                    break                    
                else:
                    Parser.Function.ee = Parser.Function.ee+1    

        def FuncFinder():
            def WordFinder():
                    while Parser.Function.loop == True:
                        if parola in Cashed.text[Parser.Function.i:Parser.Function.e]:
                            Parser.Function.parola = parola
                            Parser.Function.loop = None
                            Parser.Function.e = Parser.Function.e +1
                            Parser.Function.ee = Parser.Function.e +1
                            break
                        else:
                            Parser.Function.e = Parser.Function.e+1
                        if '>' in Cashed.text[Parser.Function.i:Parser.Function.e]:
                            Parser.Function.e = 1
                            Parser.Function.loop = False  
            for parola in Alphabet.accept_info:
                WordFinder()
                if Parser.Function.loop == False:
                    Parser.Function.loop = True
                    WordFinder()


if Cashed.loop == 1:
    Listening()
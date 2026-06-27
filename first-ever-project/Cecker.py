
import asyncio
from pathlib import Path
from os import kill
import pyttsx3
from speech_recognition import Recognizer, Microphone
import pandas as pd
import sys

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
engine = pyttsx3.init()
sys.setrecursionlimit(10000)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
r = Recognizer()

class value:
    inizio = "NaN"
    ascolto = "NaN"
    richiesta = "NaN"
    ripetere = "NaN"
    tempo_impiegato = "NaN"


    var = [inizio,ascolto,richiesta,ripetere,tempo_impiegato] 




try:
    ###Checking file location###
    try:
        path = Path(__file__).absolute().parent
        dr = pd.read_excel(path / 'Files/Settings.xlsx')
        ds = pd.read_excel(path / 'Files/CashedApp.xlsx')
    except FileNotFoundError as e:
        print(bcolors.RED + str(e) + bcolors.RESET)
    except Exception as e:
        print(bcolors.RED + str(e) + bcolors.RESET)
    finally:
        try:
            dt = pd.DataFrame(dr)
            df = pd.DataFrame(ds)
        except Exception as e:
            print(bcolors.RED + str(e) + bcolors.RESET)
    ###Saved Bool###

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
except Exception as e:
    print(bcolors.RED + str(e) + bcolors.RESET)
    print(bcolors.RED + "errore di avvio, controlla le impostazioni e la posizione dei file" + bcolors.RESET)
    engine.say("errore di avvio, controlla le impostazioni e la posizione dei file")
    engine.runAndWait()

class Function:
    def inizio():
        inizio =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE INIZIALE" ]))
        inizio = str.strip(inizio.replace("Name: OBJECT, dtype: object",""))
        inizio = inizio[5::]
        print(inizio)
        #print("")
        engine.say(bcolors.YELLOW + inizio + bcolors.RESET)
        engine.runAndWait()
    def ascolto():
        ascolto =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE ASCOLTO" ]))
        ascolto = str.strip(ascolto.replace("Name: OBJECT, dtype: object",""))
        ascolto = ascolto[5::]
        print(bcolors.GREEN + ascolto + bcolors.RESET) 
    def richiesta():
        richiesta =(str(dt["OBJECT"] [dt["SETTING"] == "FRASE RICHIESTA" ]))
        richiesta = str.strip(richiesta.replace("Name: OBJECT, dtype: object",""))
        richiesta = richiesta[5::]
        print (bcolors.GREEN + richiesta + bcolors.RESET)
        #print("")
        engine.say(richiesta)
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
        print(bcolors.YELLOW + '\n\n\n' + tempoimp + bcolors.RESET) 


#print(f"INIZO: {value.inizio}")
#print(f"ASCOLTO: {value.ascolto}")
#print(F"RICHIESTA: {value.richiesta}")
#print(F"RIPETERE: {value.ripetere}")
#print(F"TEMPO IMPIEGATO: {value.tempo_impiegato}")
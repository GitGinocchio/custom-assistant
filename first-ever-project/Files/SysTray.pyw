
import sys
import pystray
from PIL import Image
from time import sleep
import os
import subprocess 
from pathlib import Path
import asyncio
import speech_recognition
import winsound



path = Path(__file__).absolute().parent
icon = Image.open(str(path) + '\ico-512.png')
pathSiri = str.strip(str(path).replace('Files',''))



class Pid:
    SiriPid = None



def Run(icon,item):
    try:

        if Pid.SiriPid == None:
            cmd = 'python Desktop\siri\Siri.py'
            pid = subprocess.Popen(cmd,start_new_session=True,restore_signals=True,shell=True).pid
            Pid.SiriPid = pid
        else:
            try:
                os.kill(Pid.SiriPid,0)
                Pid.SiriPid = None
            except Exception as e:
                st = 'python Desktop\siri\Files\SysTray.pyw'
                subprocess.Popen(st,start_new_session=True,restore_signals=True,shell=True)                

    except Exception as e:
        print(e)



def Exit(icon,item):
    if Pid.SiriPid != None:
        try:
            os.kill(Pid.SiriPid,0)
            Pid.SiriPid = None
        except Exception as e:
            print(e)
    else:
        pass
    
    SysTray.stop()



def Impostazioni(icon,item):
    pass


Menu = pystray.Menu(
    pystray.MenuItem('Siri(On/Off)', Run),
    pystray.MenuItem('Impostazioni',
    pystray.Menu(
        pystray.MenuItem('imp1',Impostazioni),
        pystray.MenuItem('imp2',Impostazioni),
        pystray.MenuItem('imp3',Impostazioni)
    )),
    pystray.MenuItem('Exit', Exit))



SysTray = pystray.Icon('Siri',icon=icon,menu=Menu,title='Siri.py')


def setup(icon):
    if icon.visible == True:
        icon.visible = False
    elif icon.visible == False:
        icon.visible = True

SysTray.run(setup)
from ai import Ai
#from say import TTS
from listen import Listener
#from NLPTS import NLPTS
import os,subprocess
os.chdir(os.path.dirname(__file__))

ai = Ai(datafp='.\models\data.pth',device='cpu')
#tts = TTS(device=None,lang='it',tld='com',slow=False)
listener = Listener(device=None,lang='it-IT')
#nlpts = NLPTS(datafp='.\data\data.pth',ignore_words=['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|'])

print('in ascolto...')
while True:
    data = listener.listen(triggers=['google','ehi google'],min_confidence=0.90,threshold_factor=0.05,silence_duration=1.5,timeout=5)
    print('input: ',data)
    if data[0] is not None:
        try:
            tag,prob = ai.process(data[0])
            cmd = [os.path.join(os.path.dirname(__file__),'commands/{}/cmd.bat'.format(tag)),data[0],tag]
            #p = subprocess.run(cmd, capture_output=True, text=True)
            
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            print(stdout,stderr)
        except subprocess.CalledProcessError as e:
            print("ProcessError: ",e)
        except Exception as e: 
            print("Exception: ",e)

        #print("Hai detto: \'{}\'".format(data[0]))
        #tts.say("Hai detto: \'{}\'".format(data[0]))

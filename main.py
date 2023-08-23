from ai import Ai
#from say import TTS
from listen import Listener
#from NLPTS import NLPTS
import os,subprocess,re
from jsonutils import jsonutils
os.chdir(os.path.dirname(__file__))

models = [model for model in os.listdir(os.path.join(os.path.dirname(__file__),'models'))]
models.sort(key=lambda x: str(os.path.basename(x)).split('.')[:2],reverse=True)

ai = Ai(datafp=os.path.join(os.path.dirname(__file__),'models',models[0]),device='cpu')
#tts = TTS(device=None,lang='it',tld='com',slow=False)
listener = Listener(device=None,lang='it-IT')
#nlpts = NLPTS(datafp='.\data\data.pth',ignore_words=['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|'])

print('in ascolto...')
while True:
    try:
        data = listener.listen(triggers=['google','ehi google'],min_confidence=0.90,threshold_factor=0.05,silence_duration=1.5,timeout=5)
        assert data[0] is not None, 'No input was passed...'        

        tag,prob = ai.process(data[0])
        content = jsonutils(os.path.join(os.path.dirname(__file__),'commands/{}/config.json'.format(tag))).content()
        print(data)
        if content['qualified']:
            cmd = [os.path.join(os.path.dirname(__file__),'commands/{}/{}'.format(tag,content['autorun'])),*content['args']]
            
            #p = subprocess.run(cmd, capture_output=True, text=True)
            #stdout,stderr = p.stdout,p.stderr

            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,shell=content['shell'])
            stdout, stderr = process.communicate()

            print(stdout,stderr)
    
    except subprocess.CalledProcessError as e: print("ProcessError: ",e)
    except AssertionError as e: pass
    except Exception as e: print("Exception: ",e)
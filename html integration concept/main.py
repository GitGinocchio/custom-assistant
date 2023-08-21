from flask import Flask, render_template, request, redirect
from jsonutils import jsonutils
import os
os.chdir(os.path.dirname(__file__))

app = Flask(__name__,static_folder='',template_folder='')

sections = []

def save_data(enabled, name,patterns,instructions):
    jsonutil = jsonutils(r"../commands/{}/config.json".format(name))
    try:
        os.mkdir(r"../commands/{}".format(name))
        with open(r"../commands/logs.log",'w') as log: log.close()
        
        with open(r"../commands/{}/cmd.bat".format(name),'w') as f: 
            for line in instructions: f.write(line)
        

        data = {
            'qualified': enabled,
            'shell' : True,
            'autorun' : "cmd.bat",
            'post-commands' : [],
            'patterns' : patterns
        }
        jsonutil.save_to_file(data)

    except FileExistsError:
        print(f"La cartella {name} esiste già.")
        return 1
    except Exception as e:
        print(e)
        return 1
    else:
        return 0


@app.route('/')
def index(): return render_template('index/index.html', sections=sections)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        cmd_enabled = request.form.get('enabled',type=bool)
        cmd_name = request.form.get('command-name',type=str).strip()
        cmd_patterns = request.form.get('patterns',type=str).splitlines()
        cmd_instructions = request.form.get('instructions',type=str).splitlines(True)

        if save_data(cmd_enabled,cmd_name,cmd_patterns,cmd_instructions) == 0:
            print('saved')
        else:
            print('not saved')
            return render_template('add/add.html')


        return redirect('/')


    if request.method == 'GET': pass

    return render_template('add/add.html')
    
    
    #return redirect('/')

if __name__ == '__main__':
    app.run()
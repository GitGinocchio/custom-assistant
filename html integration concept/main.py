from flask import Flask, render_template, request, redirect
from jsonutils import jsonutils
import os
os.chdir(os.path.dirname(__file__))

app = Flask(__name__,static_folder='',template_folder='')

sections = []

def save_data(enabled,name,patterns,autorun,args,shell,instructions,post_args):
    try:
        os.mkdir(r"../commands/{}".format(name))
        jsonutil = jsonutils(r"../commands/{}/config.json".format(name))
        with open(r"../commands/logs.log",'w') as log: log.close()
        
        with open(r"../commands/{}/cmd.bat".format(name),'w') as f: 
            for line in instructions: f.write(line)
        

        data = {
            'qualified': enabled,
            'shell' : shell,
            'autorun' : autorun,
            'args' : args,
            'post-commands' : post_args,
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
        autorun = request.form.get('autorun',type=str).strip()
        args = request.form.get('args',type=str).strip()
        shell = request.form.get('shell',type=bool)
        cmd_instructions = request.form.get('instructions',type=str).splitlines(True)
        pargs = request.form.get('pargs',type=str).strip()

        if save_data(cmd_enabled,cmd_name,cmd_patterns,autorun,args,shell,cmd_instructions,pargs) == 0:
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
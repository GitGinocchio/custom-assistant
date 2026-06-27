from flask import Flask, render_template, request, redirect
import socket
from jsonutils import jsonutils
import os
os.chdir(os.path.dirname(__file__))

app = Flask(__name__,static_folder='',template_folder='')

sections = []

def save_data(enabled,name,description,patterns,autorun,dir,args,shell,instructions):
    try:
        os.mkdir(r"../commands/{}".format(name))
        jsonutil = jsonutils(r"../commands/{}/config.json".format(name))
        with open(r"../commands/{}/logs.log".format(name),'w') as log: log.close()
        
        with open(r"../commands/{}/cmd.bat".format(name),'w') as f: 
            for line in instructions: f.write(line)
        

        data = {
            'qualified': enabled,
            'description': description,
            'shell' : shell,
            'autorun' : autorun,
            'dir' : dir,
            'args' : args,
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

def load_commands():
    sections.clear()
    for dir in os.listdir(f"..\commands"):
        content = jsonutils(f"..\commands\{dir}\config.json").content()
        cmd = {
            "enabled": content["qualified"],
            "name" : dir,
            "description" : content["description"],
        }
        sections.append(cmd)

@app.route('/')
def index():
    load_commands()
    return render_template('index/index.html', sections=sections)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        cmd_enabled = request.form.get('enabled',type=bool)
        print(cmd_enabled)
        cmd_name = request.form.get('command-name',type=str).strip()
        cmd_description = request.form.get('description',type=str).strip()
        cmd_patterns = request.form.get('patterns',type=str).splitlines()
        autorun = request.form.get('autorun',type=str).strip()
        args = request.form.get('args',type=str).strip()
        shell = request.form.get('shell',type=bool)
        cmd_instructions = request.form.get('instructions',type=str).splitlines(True)

        def save_data():
            try:
                os.mkdir(r"../commands/{}".format(cmd_name))
                jsonutil = jsonutils(r"../commands/{}/config.json".format(cmd_name))
                with open(r"../commands/{}/logs.log".format(cmd_name),'w') as log: log.close()
                
                with open(r"../commands/{}/cmd.bat".format(cmd_name),'w') as f: 
                    for line in cmd_instructions: f.write(line)
                

                data = {
                    'qualified': cmd_enabled,
                    'description': cmd_description,
                    'shell' : shell,
                    'autorun' : autorun,
                    'dir' : "",
                    'args' : args,
                    'patterns' : cmd_patterns
                }
                jsonutil.save_to_file(data)

            except FileExistsError:
                print(f"La cartella {cmd_name} esiste già.")
                return 1
            except Exception as e:
                print(e)
                return 1
            else:
                return 0


        if save_data() == 0:
            return redirect('/')
        else:
            return render_template('add/add.html')

    if request.method == 'GET': return render_template('add/add.html')


if __name__ == '__main__':
    load_commands()
    app.run(debug=False)
from PyQt5.QtCore import pyqtSignal, QThread
import time,subprocess



class StartProcessThread(QThread):
    processingthreadsignal = pyqtSignal(dict)
    def __init__(self,parent=None):
        super().__init__(parent)

    def process(self, data : tuple):
        timer = time.time()
        self.parent().socketserver.start()
        self.parent().animator.set_animation(r'D:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\ui\animations\loading.anim')
        try:
            tag,prob,info = self.parent().aithread.prediction(data[0])
            assert tag is not None, "tag is None"
            content = self.parent().jsonthread.jsonfile(r'..\commands\{}\config.json'.format(tag))
            assert content['enabled'], "command disabled."
            cmd = [r'..\commands\{}\{}'.format(tag,content['autorun']),data[0],info if info is not None else '',*list(content['args'])]
        except AssertionError: pass
        except Exception as e: print('preexec error:',e)
        else:
            try:
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True,shell=content['shell'])
                print('----------------------------------------------------------------')
                print("(autorun start execute) time: ",time.time() - timer)
                print(cmd)
                process.wait()
            except subprocess.CalledProcessError as e: print("Process error: ",e)
            except subprocess.TimeoutExpired as e: print("Timeout expired: ",e)
            except Exception as e: print("Anomalous error occurred {}".format(e))
            finally:
                #print("pid:",process.pid,"returncode:",process.returncode,"stderr:",process.stderr.read())
                try:
                    with open(r"..\commands\{}\logs.log".format(tag),'a',encoding='utf-8') as logfile:
                        log = "\n[{}] [pid: {}] [returncode: {}] : {}".format(time.strftime('%Y-%m-%d %H:%M:%S'),process.pid,process.returncode,str(process.stderr.read()).replace('\n',' '))
                        logfile.write(log)
                except Exception as e:
                    print('logerror:',e)

                print("(total execute) time: ",time.time() - timer)
                print('----------------------------------------------------------------')
        finally:
            self.parent().socketserver.stop()
            self.parent().animator.set_animation(r'D:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\ui\animations\threshold.tanim')
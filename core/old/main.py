from PyQt5.QtWidgets import QSystemTrayIcon,QApplication,QMenu, QAction
from PyQt5.QtGui import QIcon
from QDialogs import CreateCommand,EditCommand,Settings
from QThread_Ai import AiThread
from QThread_Connection import SocketConnection
from QThread_Json import JsonThread
from QThread_Listen import ListenThread
from QThread_Process import StartProcessThread
from QThread_Say import SayThread
from QThread_TrainAi import TrainAiThread
from QAnimations import Animator
import sys,os



#tray icon
class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self):
        super(SystemTrayIcon, self).__init__()
        self.setIcon(QIcon(r'../ui/icons/microphone.png'))

        self.menu = QMenu()
        self.create_command_action = QAction('Create Command', self.menu)
        self.open_settings = QAction('Settings', self.menu)
        self.exit_action = QAction('Exit', self.menu)

        self.menu.addActions([self.create_command_action, self.menu.addSeparator(), self.open_settings, self.exit_action])
        self.setContextMenu(self.menu)
        self.activated.connect(self.UserInputHandler)
        self.create_command_action.triggered.connect(self.create_command)
        self.exit_action.triggered.connect(self.exit)
        self.open_settings.triggered.connect(self.settings)

        self.create_command_dialog = None
        self.settings_dialog = None
        self.jsonthread = JsonThread(self)
        self.listenthread = ListenThread(self,device=None,lang='it-IT',triggers=["google","ehi google","ok google"],min_confidence=0.9,threshold_factor=0.7,silence_duration=1.5,timeout=5,min_time=1)
        self.saythread = SayThread(self,device=None,lang='it',tld='com')
        self.aithread = AiThread(self,device='cpu',model=0,language='Italian',ignore_words=['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|'])
        self.socketserver = SocketConnection(parent=self)
        self.startprocessthread = StartProcessThread(self)
        self.aitrain = TrainAiThread(self,r'D:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\commands',epochs=1000,lr=0.001,hidden_size=8,device='cpu')
        #self.aitrain.start()
        #self.aitrain.trainaithreadsignal.connect(print)

        self.animator = Animator(anim=r'D:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\ui\animations\threshold.tanim',color=(0,255,0),function=self.listenthread.get_microphone_threshold,parent=self)
        #self.loadinganim = Animation(self,'loading.anim',color=(0,255,0))
        #self.waveanim = Animation(self,'wave.anim',color=(0,255,0))
        #self.thresholdanim = ThresholdAnimation(self,'threshold.anim',color=(0,255,0),fn=self.listenthread.get_microphone_threshold,values=[0.007,0.01,0.03,0.05,0.07,0.1,0.3,0.5])

        self.listenthread.start()
        self.animator.start()
        self.saythread.start()
        self.listenthread.listenthreadsignal.connect(self.startprocessthread.process)
        self.show()

    def UserInputHandler(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            print("double click")
        if reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            print("middle click")
        if reason == QSystemTrayIcon.ActivationReason.Context:
            self.menu.show()
            #if self.menu_visible: self.menu.hide()
            #else: self.menu.show()
            #self.menu_visible = not self.menu_visible
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            print("Trigger click")
        if reason == QSystemTrayIcon.ActivationReason.Unknown:
            print("Unknown click")

    def create_command(self):
        if self.create_command_dialog is None:
            self.create_command_dialog = CreateCommand(self)
        else:
            if self.create_command_dialog.isHidden(): self.create_command_dialog.show()
            else: self.create_command_dialog.hide()

    def edit_command(self):
        if self.create_command_dialog is None:
            self.create_command_dialog = EditCommand(self)
        else:
            if self.create_command_dialog.isHidden(): self.create_command_dialog.show()
            else: self.create_command_dialog.hide()

    def settings(self):
        if self.settings_dialog is None:
            self.settings_dialog = Settings(self)
        else:
            if self.settings_dialog.isHidden(): self.settings_dialog.show()
            else: self.settings_dialog.hide()

    def exit(self):
        self.hide()
        self.deleteLater()
        sys.exit(0)



if __name__ == '__main__':
    os.chdir("D:\\Desktop\\Coding\\Python\\voice-assistant-projects\\customized-assistant\\tools")
    # Specifica il percorso della directory che desideri aggiungere
    #os.environ["PATH"] = f"{os.environ.get('PATH', '')};D:\\Desktop\\Coding\\Python\\voice-assistant-projects\\customized-assistant\\tools"
    #print(os.environ["PATH"])
    app = QApplication(sys.argv)
    assistant = SystemTrayIcon()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import QDialog, QInputDialog,QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.uic import loadUi
from jsonutils import jsonfile
import os



#dialogs
class CreateCommand(QDialog):
    createcommandsignal = pyqtSignal(dict)
    def __init__(self,parent=None):
        super(CreateCommand, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        loadUi("../ui/dialogs/add.ui", self)
        self._parent = parent
        self.newbutton.clicked.connect(self.new)
        self.editbutton.clicked.connect(self.edit)
        self.removebutton.clicked.connect(self.remove)
        self.importbutton.clicked.connect(self.importbatch)
        
        self.add.clicked.connect(self.save)
        self.show()

    def isvalid(self):
        assert self.nameinput.text().strip().lower() != '','Devi inserire un nome per questo comando!'
        assert all(self.nameinput.text().strip().lower() != name for name in os.listdir('../commands')),'Questo nome e\' gia\' presente!'
        assert self.description.toPlainText().strip().lower() != '','Devi inserire una descrizione per questo comando!'
        assert self.modelslist.count() > 0, 'Devi inserire almeno una frase al modello di frasi per questo comando!'
        assert self.autoexecinput.text().strip().lower() != '','Devi inserire un file in auto esecuzione per questo comando!'
        assert self.self.directory.text().strip() != '', 'Devi inserire una cartella!'

    def save(self):
        try:
            self.isvalid()
            command_name = self.nameinput.text().strip().lower()
            command_enabled = self.enable.isChecked()
            command_description = self.description.toPlainText()
            command_patterns = [self.modelslist.item(i).text() for i in range(self.modelslist.count()) if self.modelslist.item(i)]
            command_exec = self.autoexecinput.text().strip()
            command_dir = self.directory.text().strip()
            command_args = self.argsinput.text().strip()
            command_shell_enabled = self.shell.isChecked()
            command_istructions = self.instructions.toPlainText()
        except AssertionError as e: self.statuslabel.setText(f"<font color=\"red\">Errore: {e} </font>")
        else:
            try:
                os.mkdir(r"../commands/{}".format(command_name))
                content = jsonfile(r"../commands/{}/config.json".format(command_name))
                with open(r"../commands/{}/logs.log".format(command_name),'w') as log: log.close()
                with open(r"../commands/{}/cmd.bat".format(command_name),'w') as f: f.write(command_istructions)

                data = {
                    'enabled': command_enabled,
                    'description': command_description,
                    'shell' : command_shell_enabled,
                    'autorun' : command_exec,
                    'dir' : command_dir,
                    'args' : command_args,
                    'patterns' : command_patterns
                }
                content.save(data)
            except Exception as e: self.statuslabel.setText(f"<font color=\"red\">Errore: {e} </font>")
            else:
                self.reset()
                self.hide()
                self._parent.showMessage(f"Comando \"{command_name}\" creato con successo!",f"{command_description}",msecs=20000) #QIcon(r'../ui/icons/microphone.png')

    def new(self):
        currentIndex = self.modelslist.count()
        self.modelslist.setCurrentRow(currentIndex)
        text, ok  = QInputDialog.getText(self,"New","New pattern:",flags=self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        if ok and text != '':
            self.modelslist.insertItem(currentIndex,text)

    def edit(self):
        currentItem = self.modelslist.currentItem()
        if currentItem is not None:
            text, ok  = QInputDialog.getText(self,"Edit","Edit pattern:",flags=self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            if ok and text != '':
                currentItem.setText(text)

    def remove(self):
        currentIndex = self.modelslist.currentRow()
        if currentIndex != -1:
            #question = QMessageBox.question(self,'Remove pattern','Vuoi rimuovere il pattern: "{}"'.format(self.modelslist.currentItem().text()),QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            #if question == QMessageBox.Yes:
                #item = self.modelslist.takeItem(currentIndex)
                #del item
            item = self.modelslist.takeItem(currentIndex)
            del item

    def importbatch(self):
        file, _ = QFileDialog.getOpenFileName(self,"Load batch file:",options=QFileDialog.Options(),filter="Batch files (*.bat *.cmd)")
        if file != '':
            with open(file) as f: self.instructions.setPlainText(f.read())
        else: self.instructions.clear()

    def reset(self):
        self.nameinput.setText("")
        self.enable.setChecked(True)
        self.description.clear()
        self.modelslist.clear()
        self.autoexecinput.setText("cmd.bat")
        self.argsinput.setText("")
        self.shell.setChecked(False)
        self.instructions.clear()

    def closeEvent(self, event):
        # Nascondere la finestra di dialogo anziché chiuderla
        event.ignore()
        self.hide()

class EditCommand(CreateCommand):
    def __init__(self,parent=None):
        super(EditCommand, self).__init__(parent)

class ViewCommands: pass
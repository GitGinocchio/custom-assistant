from PyQt5.QtCore import QThread
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
import os,time,struct

class Animation:
    def __init__(self,frames : list[dict]):
        #Animation ha gli attributi:
        #   - frames
        #     {num : int, image : bytes, duration : float}
        
        #controllo se ogni frame e' un dizionario contenente le seguenti chiavi
        for frame in frames:
            assert all([True for i in ['num','image','duration'] if i in frame]), f'Invalid frame {frame} found!'
        self.frames = frames
    
    def keys(self):
        #Questa funzione restituisce le chiavi che ha il primo frame
        return self.frames[0].keys()

    def getDuration(self,*,frame : int = None):
        return sum([frame['duration'] for frame in self.frames]) if frame is None else self.__getitem__(frame)
        
    def __str__(self):
        return f'Animation: frames: {self.frames}; total duration: {self.total_duration}'

    def __len__(self):
        return len(self.frames)

    def __iter__(self):
        #Se viene iterata l'oggetto ritorno i frame dell'animazione
        return iter(self.frames)

    def __next__(self):
        raise StopIteration

    def __getitem__(self, __k : int):
        #Questa funzione restituisce un frame desiderato, ritorna un errore se si tenta di accedere ad un frame inesistente
        try: return self.frames[__k]
        except ValueError as e: print(f'Frame num {__k} not found in animation!')

class ThresholdAnimation(Animation):
    def __init__(self,frames):
        #Questo oggetto eredita e inizializza Animation
        super().__init__(frames)
        
        for frame in frames:
            assert all([True for i in ['num','image','duration','threshold'] if i in frame]), f'Invalid frame {frame} found!'
    
    def getThreshold(self, frame : int = None):
        #Questo metodo restituisce il valore di threshold per il frame desiderato
        return self.__getitem__(frame)['threshold'] if frame is not None else [self.__getitem__(i)['threshold'] for i in range(len(self.frames)-1)]

def load(animation : str):
    assert (animation.endswith('.tanim') or animation.endswith('.anim')) and os.path.exists(animation) if animation is str else True

    try:
        with open(animation, 'rb') as infile:
            num_frames = int.from_bytes(infile.read(4), byteorder='big')
            total_duration = struct.unpack('f', infile.read(4))[0]
            frames = []
            
            for _ in range(num_frames):
                imagedata = infile.read(int.from_bytes(infile.read(4), byteorder='big'))
                if animation.endswith('.tanim'): threshold = struct.unpack('f', infile.read(4))[0]
                duration = struct.unpack('f', infile.read(4))[0]
                frame = {'num': len(frames), 'imagedata': imagedata, 'duration': duration} #'threshold' : threshold
                if animation.endswith('.tanim'): frame.update([('threshold',threshold)])
                frames.append(frame)
    except Exception as e: raise RuntimeError(e)
    else: return ThresholdAnimation(frames) if animation.endswith('.tanim') else Animation(frames)

class Animator(QThread):
    def __init__(self, anim : str | Animation | ThresholdAnimation, color : tuple = (255,255,255),*,function : classmethod = None,parent):
        super().__init__(parent=parent)
        self.anim : Animation | ThresholdAnimation = load(anim) if type(anim) is str else anim
        self.color = QtGui.QColor(*color)
        self.function : classmethod = function
        self.active = True

    def getpixmap(self,imagedata : bytes):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(imagedata)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), self.color)
        painter.end()
        return pixmap
    def set_color(self, color : tuple): self.color = QtGui.QColor(*color)
    def set_animation(self, animation : str): self.anim = load(animation)
    def set_threshold_function(self, function : classmethod): self.function = function

    def run(self):
        self.active = True
        while self.active:
            if type(self.anim) is ThresholdAnimation and self.function is not None:
                threshold = self.function()
                
                if type(self.anim) is Animation: continue
                if threshold < min(self.anim.getThreshold()):
                    self.parent().setIcon(QIcon(self.getpixmap(self.anim[0]['imagedata'])))
                    time.sleep(float(self.anim[0]['duration']))
                    continue

                if type(self.anim) is Animation: continue
                indexes = [i for i,value in enumerate(self.anim.getThreshold()) if threshold > value][:len(self.anim)-1]
                self.parent().setIcon(QIcon(self.getpixmap(self.anim[indexes[-1]]['imagedata'])))
                time.sleep(float(self.anim[indexes[-1]]['duration']))

            elif type(self.anim) is Animation or (type(self.anim) is ThresholdAnimation and self.function is None):
                for frame in self.anim:
                    self.parent().setIcon(QIcon(self.getpixmap(frame['imagedata'])))
                    time.sleep(float(frame['duration']))

    def from_threshold(self,threshold : float):
        if threshold < min(self.anim.getThreshold()):
            self.parent().setIcon(QIcon(self.getpixmap(self.anim[0]['imagedata'])))
            time.sleep(float(self.anim[0]['duration']))
        else:
            indexes = [i for i,value in enumerate(self.anim.getThreshold()) if threshold > value][:len(self.anim)-1]
            self.parent().setIcon(QIcon(self.getpixmap(self.anim[indexes[-1]]['imagedata'])))
            time.sleep(float(self.anim[indexes[-1]]['duration']))

    def stop(self): self.active = False
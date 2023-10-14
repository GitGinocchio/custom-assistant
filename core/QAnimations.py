from PyQt5.QtCore import QThread
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
import os,time
from anim import dump

#animations
class Animation(QThread):
    def __init__(self,parent=None,anim : str = None,color : tuple[int] = (255,255,255)):
        super().__init__(parent)
        self.active = True
        self.animation = dump(os.path.join(r'../ui/animations',anim))
        self.color = QtGui.QColor(*color)

    def change_color(self, color : tuple[int] = (255,255,255)):
        self.color = color

    def change_anim(self,anim : str):
        self.animation = dump(os.path.join(r'../ui/animations',anim))

    def change_image_color(self,image_data, color : QtGui.QColor):
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image_data)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return pixmap

    def run(self):
        try:
            self.active = True
            
            while self.active:
                for frame in self.animation['frames']:
                    self.parent().setIcon(QIcon(self.change_image_color(frame['imagedata'],self.color)))
                    time.sleep(float(frame['duration']))

        except Exception as e:
            print(e)
        finally:
            self.active = False

    def animate(self, anim : str,color : tuple[int] = (255,255,255)):
        try:    
            animation = dump(os.path.join(r'../ui/animations',anim))
            self.active = True
            
            while self.active:
                for frame in animation['frames']:
                    self.parent().setIcon(QIcon(self.change_image_color(frame['imagedata'],color)))
                    time.sleep(float(frame['duration']))

        except Exception as e: print(e)
        finally: self.active = False

    def stop(self): self.active = False

class ThresholdAnimation(Animation):
    def __init__(self,parent=None,anim : str = None,color : tuple[int] = (255,255,255),fn = None, values : list[float | int] = []):
        super().__init__(parent,anim,color)
        #assert len(values) == len(self.animation['frames']),f'you have passed {len(values)}, but there are {len(self.animation["frames"])} frames'
        self.fn = fn
        self.values = sorted(values,reverse=False)

    def run(self):
        try:
            self.active = True

            while self.active:
                threshold = self.fn()

                if threshold < min(self.values):
                    self.parent().setIcon(QIcon(self.change_image_color(self.animation['frames'][0]['imagedata'],self.color)))
                    continue

                index = [i for i,value in enumerate(self.values) if threshold > value][:len(self.animation['frames'])-1]
                self.parent().setIcon(QIcon(self.change_image_color(self.animation['frames'][index[-1]]['imagedata'],self.color)))

        except Exception as e:
            print(e)
        finally:
            self.active = False
    
    def animate(self,anim : str,color : tuple[int] = (255,255,255),fn : classmethod = None):
        try:
            animation = dump(os.path.join(r'../ui/animations',anim))
            self.active = True

            while self.active:
                threshold = fn()

                if threshold < min(self.values):
                    self.parent().setIcon(QIcon(self.change_image_color(animation['frames'][0]['imagedata'],color)))
                    continue

                index = [i for i,value in enumerate(self.values) if threshold > value][:len(animation['frames'])-1]
                self.parent().setIcon(QIcon(self.change_image_color(animation['frames'][index[-1]]['imagedata'],color)))

        except Exception as e:
            print(e)
        finally:
            self.active = False

    def from_threshold(self, threshold : float | int, color : tuple[int] = None):
        if threshold < min(self.values):
            self.parent().setIcon(QIcon(self.change_image_color(self.animation['frames'][0]['imagedata'],QtGui.QColor(*color) if color is not None else self.color)))
        else:
            index = [i for i,value in enumerate(self.values) if threshold > value][:len(self.animation['frames'])-1]
            self.parent().setIcon(QIcon(self.change_image_color(self.animation['frames'][index[-1]]['imagedata'],QtGui.QColor(*color) if color is not None else self.color)))
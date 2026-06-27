import os,struct
from QAnimations import Animation,ThresholdAnimation

def dump(animation : str | Animation | ThresholdAnimation):
    assert animation.endswith('.anim') and os.path.exists(animation) if animation is str else True

    if type(animation) is str:
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
                    if animation.endswith('.tanim'):frame.update(('threshold',threshold))
                    frames.append(frame)
        except Exception as e: print(e)
        else:
            return {'num_frames': num_frames,'frames' : frames,'total_duration':total_duration}
    else:
        return {'num_frames': len(animation),'frames' : animation,'total_duration': animation.getDuration()}

def load(animation : str):
    assert (animation.endswith('.tanim') or animation.endswith('.anim')) and os.path.exists(animation) if animation is str else True

    if type(animation) is str:
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
                    if animation.endswith('.tanim'):frame.update(('threshold',threshold))
                    frames.append(frame)
        except Exception as e: print(e)
        else:
            return ThresholdAnimation(frames) if animation.endswith('.tanim') else Animation(frames)

class AnimationManager:
    def __init__(self,*,animation : str | Animation = None):
        assert animation.endswith('.anim') if animation is str else True
        self.animation : Animation
        if type(animation) is str: self.load(animation)
        elif animation is not None: self.animation = animation
        else: self.animation = Animation([])

    def load(self, animation : str | Animation):
        assert animation.endswith('.anim') and os.path.exists(animation) if animation is str else True

        if type(animation) is str:
            try:
                with open(animation, 'rb') as infile:
                    num_frames = int.from_bytes(infile.read(4), byteorder='big')
                    total_duration = struct.unpack('f', infile.read(4))[0]
                    frames = []
                
                    for _ in range(num_frames):
                        imagedata = infile.read(int.from_bytes(infile.read(4), byteorder='big'))
                        duration = struct.unpack('f', infile.read(4))[0]
                        frames.append({'num': len(frames), 'imagedata': imagedata, 'duration': duration})
            except Exception as e: print(e)
            else:
                self.animation = Animation(frames)
        else: self.animation = animation

    def new(self,image : str | bytes, duration : float):
        if type(image) is str:
            assert image.endswith('.png') and os.path.exists(image),'image must be a ".png" image and must exist'
            with open(image,'rb') as img_file: image = img_file.read()
        self.animation.frames.append({'num' : len(self.animation), 'imagedata' : image, 'duration' : duration})

    def edit(self,frame : int,*, image : str | bytes = None, duration : float = None):
        assert self.animation is not None, "You must load or create an Animation first"
        if type(image) is str:
            assert image.endswith('.png') and os.path.exists(image),'image must be a ".png" image and must exist'
            with open(image,'rb') as img_file: image = img_file.read()

        for name,key in [('image',image),('duration',duration)]:
            if key is not None: self.animation[frame][name] = key

    def dump(self):
        assert self.animation is not None, "You must load or create an Animation first"
        return {'num_frames': len(self.animation),'frames' : self.animation,'total_duration':self.animation.getDuration()}

    def save(self,filename : str):
        assert filename.endswith('.anim'), 'file must end with ".anim" extension.'
        assert self.animation is not None, "You must load or create an Animation first"

        with open(filename, 'wb') as outfile:
            outfile.write(int(len(self.animation)).to_bytes(4, byteorder='big'))
            outfile.write(struct.pack('f',self.animation.getDuration()))

            for frame in self.animation:
                outfile.write(len(frame['imagedata']).to_bytes(4, byteorder='big'))
                outfile.write(frame['imagedata'])
                outfile.write(struct.pack('f', frame['duration']))

class ThresholdAnimationManager(AnimationManager):
    def __init__(self,*,animation : str | ThresholdAnimation = None):
        super().__init__(animation=animation)
        assert animation.endswith('.tanim') if animation is str else True
        self.animation : ThresholdAnimation
        if type(animation) is str: self.load(animation)
        elif animation is not None: self.animation = animation
        else: self.animation = ThresholdAnimation([])
    
    def load(self, animation : str | ThresholdAnimation):
        assert animation.endswith('.tanim') and os.path.exists(animation) if animation is str else True

        if type(animation) is str:
            try:
                with open(animation, 'rb') as infile:
                    num_frames = int.from_bytes(infile.read(4), byteorder='big')
                    total_duration = struct.unpack('f', infile.read(4))[0]
                    frames = []
                
                    for _ in range(num_frames):
                        imagedata = infile.read(int.from_bytes(infile.read(4), byteorder='big'))
                        threshold = struct.unpack('f', infile.read(4))[0]
                        duration = struct.unpack('f', infile.read(4))[0]
                        frames.append({'num': len(frames), 'imagedata': imagedata, 'duration': duration,'threshold' : threshold})
            except Exception as e: print(e)
            else:
                self.animation = ThresholdAnimation(frames)
        else: self.animation = animation

    def new(self,image : str | bytes, duration : float,threshold : float):
        if type(image) is str:
            assert image.endswith('.png') and os.path.exists(image),'image must be a ".png" image and must exist'
            with open(image,'rb') as img_file: image = img_file.read()
        self.animation.frames.append({'num' : len(self.animation), 'imagedata' : image, 'duration' : duration,'threshold' : threshold})

    def edit(self,frame : int,*, image : str | bytes = None, duration : float = None,threshold : float = None):
        assert self.animation is not None, "You must load or create an Animation first"
        if type(image) is str:
            assert image.endswith('.png') and os.path.exists(image),'image must be a ".png" image and must exist'
            with open(image,'rb') as img_file: image = img_file.read()

        for name,key in [('image',image),('duration',duration),('threshold',threshold)]:
            if key is not None: self.animation[frame][name] = key

    def save(self,filename : str):
        assert filename.endswith('.tanim'), 'file must end with ".anim" extension.'
        assert self.animation is not None, "You must load or create an Animation first"

        with open(filename, 'wb') as outfile:
            outfile.write(int(len(self.animation)).to_bytes(4, byteorder='big'))
            outfile.write(struct.pack('f',self.animation.getDuration()))

            for frame in self.animation:
                outfile.write(len(frame['imagedata']).to_bytes(4, byteorder='big'))
                outfile.write(frame['imagedata'])
                outfile.write(struct.pack('f', frame['threshold']))
                outfile.write(struct.pack('f', frame['duration']))

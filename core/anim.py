import os,struct
from argparse import ArgumentParser
os.chdir(os.path.dirname(__file__))

"""
# Funzione per scrivere un'immagine PNG con intestazione di lunghezza
def write_image_with_length(outfile, image_file, duration_seconds):
    with open(image_file, 'rb') as image:
        image_data = image.read()
        image_length = len(image_data)
        # Scrivi la lunghezza dell'immagine come intestazione (4 byte)
        outfile.write(image_length.to_bytes(4, byteorder='big'))
        # Scrivi i dati dell'immagine
        outfile.write(image_data)
        # Scrivi la durata in secondi come intestazione (4 byte)
        outfile.write(int(duration_seconds).to_bytes(4, byteorder='big'))

# Directory contenente le immagini PNG dell'animazione
image_directory = r'D:\Desktop\Coding\Python\voice-assistant-projects\old\voice-assistant-without-ui\icons\animations\animation1'

# Nome del file .anim in cui salvare l'animazione
anim_file = 'animazione.anim'

# Elenco delle immagini PNG nell'ordine desiderato con le relative durate
image_info = [
    ('immagine1.png', 2.0),  # Durata 2 secondi
    ('immagine2.png', 3.0),  # Durata 3 secondi
    ('immagine3.png', 1.5)   # Durata 1.5 secondi
]

total_duration = sum(duration for _, duration in image_info)

with open(anim_file, 'wb') as outfile:
    # Scrivi il numero totale di immagini come metadato (4 byte)
    outfile.write(len(image_info).to_bytes(4, byteorder='big'))
    # Scrivi la durata complessiva in secondi come metadato (8 byte)
    outfile.write(int(total_duration).to_bytes(8, byteorder='big'))
    
    for image_file, duration in image_info:
        image_path = os.path.join(image_directory, image_file)
        write_image_with_length(outfile, image_path, duration)

print(f'File .anim "{anim_file}" creato con successo.')
"""


def dump(filename : str):
    assert filename.endswith('.anim') and os.path.exists(filename), 'File must end with ".anim" extension.'

    with open(filename, 'rb') as infile:
        # Leggi il numero totale di immagini dal metadato (4 byte)
        num_frames = int.from_bytes(infile.read(4), byteorder='big')
        # Leggi la durata complessiva in secondi dal metadato (4 byte)
        duration = struct.unpack('f', infile.read(4))[0]

        frames = []

        for _ in range(num_frames):
            # Leggi la lunghezza dell'immagine (4 byte)
            image_length = int.from_bytes(infile.read(4), byteorder='big')
            # Leggi i dati dell'immagine
            image_data = infile.read(image_length)
            # Leggi la durata dell'immagine (4 byte)
            image_duration = struct.unpack('f', infile.read(4))[0]

            # Puoi gestire l'immagine come preferisci, ad esempio, salvarla su disco o elaborarla direttamente.
            # In questo esempio, immaginiamo di salvarla temporaneamente su disco.
            #image_filename = f'temp_frame_{len(frames)}.png'
            #with open(image_filename, 'wb') as image_file:
                #image_file.write(image_data)

            frames.append({'num': len(frames), 'imagedata': image_data, 'duration': image_duration})
    
    return {'lenframes' : num_frames,'frames': frames, 'duration': duration}

class Animation:
    def __init__(self,dfduration : float | int = 2.0):
        self.dfduration = dfduration
        self.frames = []
        self.duration = 0.0

    def addframe(self,image : str, duration : float | int = None):
        assert image.endswith('.png') and os.path.exists(image), 'image must be a ".png" image and must exist'

        self.duration += float(duration if duration is not None else self.dfduration)
        self.frames.append({'num' : len(self.frames), 'image' : image, 'duration' : float(duration if duration is not None else self.dfduration)})

    def save(self,filename : str):
        assert filename.endswith('.anim'), 'file must end with ".anim" extension.'
        assert len(self.frames) > 0, 'first you have to add a new frame to the animation!'

        with open(filename, 'wb') as outfile:
            # Scrivi il numero totale di immagini come metadato (4 byte)
            outfile.write(int(len(self.frames)).to_bytes(4, byteorder='big'))
            # Scrivi la durata complessiva in secondi come metadato (4 byte)
            outfile.write(struct.pack('f',self.duration))

            for frame in self.frames:
                with open(frame['image'],'rb') as image:
                    imagedata = image.read()
                    outfile.write(len(imagedata).to_bytes(4, byteorder='big'))
                    outfile.write(imagedata)
                    outfile.write(struct.pack('f', frame['duration']))
        
        self.frames.clear()
        self.duration = 0.0


#animation = Animation()

#path = r'D:\Desktop\Coding\Python\voice-assistant-projects\old\voice-assistant-without-ui\icons\animations\loading'
#imgs = os.listdir(path)

#imgs = ['0.png','2.png','4.png','6.png','0.png','6.png','4.png','2.png']

#print(imgs)
#for image in imgs:
    #animation.addframe(os.path.join(path,image),duration=0.15)

#print(sorted(imgs,reverse=True)[1:-1])
#for image in sorted(imgs,reverse=True)[1:-1]:
    #animation.addframe(os.path.join(path,image),duration=0.15)

#animation.save('../ui/animations/loading.anim')

#data = dump('../ui/animations/loading.anim')

#print(data)

#for frame in data['frames']:
    #print(frame)
from PyQt5.QtCore import pyqtSignal, QThread
import nltk,torch,torch.nn as nn,numpy as np,os
from nltk.stem.porter import PorterStemmer



class AiThread(QThread):
    aithreadsignal = pyqtSignal(dict)
    def __init__(self,parent=None,device : str = 'cpu',model : int | str = 0,language : str = 'Italian',ignore_words : list[str] = []):
        super().__init__(parent)
        models = [model for model in os.listdir('../models')]
        models.sort(key=lambda x: str(os.path.basename(x)).split('.')[:2],reverse=True)
        if device == 'cuda' and not torch.cuda.is_available(): raise ValueError('Error: selected device is type CUDA but is not available.')
        print('Ai: using model:',os.path.join(r'..\models',models[model] if type(model) is int else model))
        self.data = torch.load(os.path.join(r'..\models',models[model] if type(model) is int else model),encoding='utf-8')
        self.ignore_words = ignore_words
        self.language = language
        self.device = torch.device('cuda' if device == 'cuda' and torch.cuda.is_available() else 'cpu')
        self.stemmer = PorterStemmer()
        self.model = self.NeuralNet(self.data["input_size"], self.data["hidden_size"], self.data["output_size"]).to(self.device)
        self.model.load_state_dict(self.data["model_state"])
        self.model.eval()

    class NeuralNet(nn.Module):
        def __init__(self, input_size, hidden_size, num_classes):
            super(AiThread.NeuralNet, self).__init__()
            self.flatten = nn.Flatten()
            self.l1 = nn.Linear(input_size, hidden_size) 
            self.l2 = nn.Linear(hidden_size, hidden_size)
            self.l3 = nn.Linear(hidden_size, num_classes)
            self.relu = nn.ReLU(True)
        
        def forward(self, x):
            out = self.l1(x)
            out = self.relu(out)
            out = self.l2(out)
            out = self.relu(out)
            out = self.l3(out)
            
            return out

    def prediction(self,sentence : str,*, min_prob : float = None,preserve_line : bool = True):
        #for word in self.data['intents']["Callers"]: Sentence = Sentence.replace(word,'').strip()
        
        for word in self.ignore_words: sentence = sentence.replace(word,'')
        sentence = nltk.word_tokenize(sentence.lower(),language=self.language,preserve_line=preserve_line)
        stemmed = [self.stemmer.stem(word) for word in sentence]
        X = np.zeros(len(self.data['all_words']), dtype=np.float32)
        for idx, w in enumerate(self.data['all_words']):
            if w in stemmed: X[idx] = 1
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.data['tags'][predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > min_prob if min_prob is not None else float(self.data['benchmark']['min_prob']):
            for intent in self.data['intents']:
                if tag == intent["tag"]:
                    tokenized = []
                    [[tokenized.append(word) for word in nltk.word_tokenize(str(pattern).lower(),language=self.language,preserve_line=True) if word not in tokenized] for pattern in intent['patterns']]#lemmatizer.lemmatize(word)
                    stemmed = [self.stemmer.stem(word,to_lowercase=True) for word in tokenized]

                    for index in range(-1, -len(sentence)-1, -1):
                        if any(w == sentence[index] for w in tokenized) and any(sentence[index].find(w) for w in stemmed): # or any(sentence[index].find(w) for w in stemmed)
                            if index + 1 in range(-1,-len(sentence)-1,-1): 
                                return str(intent['tag']), float(prob.item()),' '.join(sentence[index + 1::])
                            else: 
                                return str(intent['tag']), float(prob.item()), None

        return None, float(prob.item()), None
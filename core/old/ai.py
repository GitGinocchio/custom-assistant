import nltk,torch,torch.nn as nn,numpy as np
from nltk.stem.porter import PorterStemmer

class Ai:
    def __init__(self,datafp : str, device : str = 'cpu'):
        if device == 'cuda' and not torch.cuda.is_available(): raise ValueError('Error: selected device is type CUDA but is not available.')
        self.data = torch.load(datafp,encoding='utf-8')
        self.device = torch.device('cuda' if device == 'cuda' and torch.cuda.is_available() else 'cpu')
        self.stemmer = PorterStemmer()
        self.model = self.NeuralNet(self.data["input_size"], self.data["hidden_size"], self.data["output_size"]).to(self.device)
        self.model.load_state_dict(self.data["model_state"])
        self.model.eval()

    class NeuralNet(nn.Module):
        def __init__(self, input_size, hidden_size, num_classes):
            super(Ai.NeuralNet, self).__init__()
            #self.flatten = nn.Flatten()
            self.l1 = nn.Linear(input_size, hidden_size) 
            self.l2 = nn.Linear(hidden_size, hidden_size)
            self.l3 = nn.Linear(hidden_size, num_classes)
            self.relu = nn.ReLU()
        
        def forward(self, x):
            out = self.l1(x)
            out = self.relu(out)
            out = self.l2(out)
            out = self.relu(out)
            out = self.l3(out)

            # no activation and no softmax at the end
            return out

    def bag_of_words(self, tokenized : list[str], words : list[str]):
        sentence_words = [self.stemmer.stem(word.lower()) for word in tokenized]
        bag = np.zeros(len(words), dtype=np.float32)
        for idx, w in enumerate(words):
            if w in sentence_words: 
                bag[idx] = 1
        return bag

    def prediction(self,Sentence : str, min_prob : float = None):
        #for word in self.data['intents']["Callers"]: Sentence = Sentence.replace(word,'').strip()
        
        Sentence = nltk.word_tokenize(Sentence.lower(),language='Italian',preserve_line=True)
        X = self.bag_of_words(Sentence, self.data['all_words'])
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
                    return str(intent['tag']), float(prob.item())
            else:
                return None, float(prob.item())
        else:
            return None, float(prob.item())

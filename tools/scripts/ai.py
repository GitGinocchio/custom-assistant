import nltk,os,torch,torch.nn as nn,numpy as np,json
os.chdir(os.path.dirname(__file__))

class utils:
    def tokenize(sentence):
        """
        split sentence into array of words/tokens
        a token can be a word or punctuation character, or number
        """
        return nltk.word_tokenize(sentence,language='Italian',preserve_line=True)

    def stem(word):
        
        """
        stemming = find the root form of the word
        examples:
        words = ["organize", "organizes", "organizing"]
        words = [stem(w) for w in words]
        -> ["organ", "organ", "organ"]
        """
        from nltk.stem.porter import PorterStemmer
        return PorterStemmer().stem(word.lower())

    def bag_of_words(tokenized_sentence, words):
        """
        return bag of words array:
        1 for each known word that exists in the sentence, 0 otherwise
        example:
        sentence = ["hello", "how", "are", "you"]
        words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
        bag   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
        """
        # stem each word
        sentence_words = [utils.stem(word) for word in tokenized_sentence]
        # initialize bag with 0 for each word
        bag = np.zeros(len(words), dtype=np.float32)
        for idx, w in enumerate(words):
            if w in sentence_words: 
                bag[idx] = 1
            #print(idx, w)
        #print(bag)
        return bag

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
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

class Ai:
    def __init__(self,datafp : str, device : str):
        if device == 'cuda' and not torch.cuda.is_available(): raise ValueError('Error: selected device is type CUDA but is not available.')
        self.data = torch.load(datafp,encoding='utf-8')
        self.device = torch.device('cuda' if device == 'cuda' and torch.cuda.is_available() else 'cpu')
        self.model = NeuralNet(self.data["input_size"], self.data["hidden_size"], self.data["output_size"]).to(self.device)
        self.model.load_state_dict(self.data["model_state"])
        self.model.eval()

    def process(self,Sentence : str, min_prob : float = None):
        #for word in self.data['intents']["Callers"]: Sentence = Sentence.replace(word,'').strip()
        
        Sentence = utils.tokenize(Sentence.lower())
        X = utils.bag_of_words(Sentence, self.data['all_words'])
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.data['tags'][predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() >  min_prob if min_prob is not None else float(self.data['benchmark']['min_prob']):
            for intent in self.data['intents']['intents']:
                if tag == intent["tag"]:
                    return str(intent['tag']), float(prob.item())
            else:
                return None, float(prob.item())
        else:
            return None, float(prob.item())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Interazione con modello AI.')

    # Argomento per inserire la frase da elaborare
    parser.add_argument('sentence', type=str, help='Frase da sottoporre all\'AI per l\'elaborazione.')

    # Argomento per specificare il dispositivo di calcolo (CPU o CUDA)
    parser.add_argument('-device', type=str, default='cpu', choices=('cpu', 'cuda'),help='Dispositivo di calcolo da utilizzare (\'cpu\' o \'cuda\'). Default: cpu.')

    # Argomento per specificare un valore di soglia per l\'elaborazione
    parser.add_argument('-cutoff', type=float, default=None,help='Valore di soglia. Se la probabilità supera questo valore, verrà restituito un risultato.')

    # Argomento per specificare il percorso del modello
    parser.add_argument('-model', type=str, default='./data/data.pth',help='Percorso del file del modello AI pre-addestrato. Default: \'./data/data.pth\'.')

    args = parser.parse_args()

    try:
        ai = Ai(args.model,args.device)
        tag, prob = ai.process(args.sentence,args.cutoff)
        print(json.dumps({'tag':tag,'prob':prob}))
    except Exception as e:
        print(e.with_traceback(None))
        #input("Premi un tasto per uscire...")
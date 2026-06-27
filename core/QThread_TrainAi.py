from PyQt5.QtCore import pyqtSignal, QThread
import nltk,torch,torch.nn as nn,numpy as np,os
from datetime import datetime
from torch.utils.data import Dataset, DataLoader




class TrainAiThread(QThread):
    trainaithreadsignal = pyqtSignal(dict)
    def __init__(self,parent, commandspath : str,*,epochs : int, lr : float, hidden_size : int, device : str):
        super().__init__(parent)
        self.intents,self.tags,self.words,self.xy,self.x,self.y = [],[],[],[],[],[]
        for dir in os.listdir(commandspath):
            if os.path.isdir(os.path.join(commandspath,dir)):
                content = self.parent().jsonthread.jsonfile(os.path.join(commandspath,dir,'config.json'))
                self.intents.append({'tag' : dir,'patterns' : content['patterns']})
                self.tags.append(dir)
                for pattern in content['patterns']:
                    words = nltk.word_tokenize(pattern,language=self.parent().aithread.language,preserve_line=True)
                    self.words.extend(words)
                    self.xy.append((words, dir))
        self.words = sorted(set([self.parent().aithread.stemmer.stem(w) for w in self.words if w not in self.parent().aithread.ignore_words]))
        self.tags = sorted(set(self.tags))
        for (pattern_sentence, tag) in self.xy:
            bag = np.zeros(len(self.words), dtype=np.float32)
            for idx, w in enumerate(self.words):
                if w in [self.parent().aithread.stemmer.stem(word) for word in pattern_sentence]: bag[idx] = 1
            self.x.append(bag)
            self.y.append(self.tags.index(tag))
        #----------------------------------------------------------------
        self.epochs = epochs
        self.learning_rate = lr
        self.batch_size = int(len(np.array(self.x)[0]) ** 0.5)
        self.input_size = len(np.array(self.x)[0])
        self.hidden_size = hidden_size
        self.output_size = len(self.tags)
        #----------------------------------------------------------------
        self.device = torch.device('cuda' if device.lower() == 'cuda' and torch.cuda.is_available() else 'cpu')
        self.model = self.parent().aithread.NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.traindataset = DataLoader(dataset=self.ChatDataset(np.array(self.x),np.array(self.y)),batch_size=self.batch_size,shuffle=True,num_workers=0)
        self.testdataset = DataLoader(dataset=self.ChatDataset(np.array(self.x),np.array(self.y)),batch_size=self.batch_size,shuffle=True,num_workers=0)
        self.loss_params = {}
        self.loss = nn.CrossEntropyLoss(*self.loss_params)
        self.optim_params = {"lr" : self.learning_rate,"betas" : (0.9, 0.999),"eps" : 0.00000001,"weight_decay" : 0.01,"amsgrad" : True}
        self.optim = torch.optim.AdamW(params=self.model.parameters(),**self.optim_params)

    def run(self):
        total_labels = 0
        correct_labels = 0
        train_loss = 0
        test_loss = 0
        sumprobs = 0
        accuracy = 0

        for epoch in range(1,self.epochs + 1):
            for batch, (inputs, labels) in enumerate(self.traindataset):
                self.model.train()
                inputs = inputs.to(self.device)
                labels = labels.to(dtype=torch.long).to(self.device)

                outputs = self.model(inputs)
                loss = self.loss(outputs, labels)

                self.optim.zero_grad()
                loss.backward()
                self.optim.step()

                l, current = loss.item(), (batch + 1) * len(inputs)
                train_loss += loss.item()
                train_loss /= len(self.traindataset)

            with torch.no_grad():
                self.model.eval()
                for inputs, labels in self.testdataset:
                    inputs = inputs.to(self.device)
                    labels = labels.to(dtype=torch.long).to(self.device)

                    outputs = self.model(inputs)

                    loss = self.loss(outputs, labels)

                    test_loss += loss.item()

                    _, predicted = torch.max(outputs.data, dim=1)
                    total_labels += labels.size(0)
                    correct_labels += (predicted == labels).sum().item()
            
            sentence = nltk.word_tokenize('',language=self.parent().aithread.language,preserve_line=True)
            X = np.zeros(len(self.words), dtype=np.float32)
            for idx, w in enumerate(self.words):
                if w in [self.parent().aithread.stemmer.stem(word) for word in sentence]: X[idx] = 1
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(self.device)
            output = self.model(X)
            _, predicted = torch.max(output, dim=1)
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            sumprobs += prob.item()

            test_loss /= len(self.testdataset)
            accuracy = correct_labels / total_labels * 100
            
            data = {'epoch' : epoch,'train_loss' : train_loss,'test_loss' : test_loss,'min_prob' : sumprobs / epoch,'accuracy' : accuracy,'total_labels' : total_labels,'correct_labels' : correct_labels}
            self.trainaithreadsignal.emit(data)

        data = {'epoch' : self.epochs,'train_loss' : train_loss,'test_loss' : test_loss,'min_prob' : sumprobs / self.epochs,'accuracy' : accuracy,'total_labels' : total_labels,'correct_labels' : correct_labels}
        self.trainaithreadsignal.emit(data)
        self.save(finaldata=data)

    class ChatDataset(Dataset):
        def __init__(self,X_train,Y_train):
            self.n_samples = len(X_train)
            self.x_data = X_train
            self.y_data = Y_train

        # support indexing such that dataset[i] can be used to get i-th sample
        def __getitem__(self, index):
            return self.x_data[index], self.y_data[index]

        # we can call len(dataset) to return the size
        def __len__(self):
            return self.n_samples

    def save(self, filename : str = None,*,finaldata : dict):
        data = {
        "intents" : self.intents,
        "model_state": self.model.state_dict(),
        "input_size": self.input_size,
        "hidden_size": self.hidden_size,
        "output_size": self.output_size,
        "all_words": self.words,
        "tags": self.tags,
        "benchmark": {
            "num_epochs" : finaldata['epoch'],
            "learning_rate" : self.learning_rate,
            "final_train_loss" : finaldata['train_loss'], 
            "final_test_loss" : finaldata['test_loss'],
            "accuracy" : f"{finaldata['accuracy']}%",
            "min_prob" : finaldata['min_prob'],
            "total_labels" : finaldata['total_labels'],
            "correct_labels" : finaldata['correct_labels'],
            },
        "metadata" : {
            "datetime" : datetime.now().strftime('%d/%m%Y - %H:%M:%S')
        },
        "spec" : {
            "criterion" : str(type(self.loss)),
            "optimizer" : str(type(self.optim)),
            "criterion_params" : self.loss_params,
            "optimizer_params" : self.optim_params,
            "cuda_available" : torch.cuda.is_available(),
            "device_spec" : {"index" : self.device.index, "type" : self.device.type,"name" : ""}
        }

        }
        try:
            torch.save(data, "../models/{}.{}.{}.pth".format(datetime.now().day,datetime.now().month,datetime.now().year) if filename is None else filename)
        except Exception as e: print(e)

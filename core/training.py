from ai import NeuralNet,stem,tokenize,bag_of_words
import torch
import datetime,time
import numpy as np
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from colorama import Fore
from jsonutils import jsonutils
import os
os.chdir(os.path.dirname(__file__))

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

# - Model Training and Evaluation - 
class MTE:
    def __init__(self,epochs : int,lr : float = 0.001,hidden_size : int = 8,device : str = 'cpu',*,ignore_words : list[str],last_dataset : str = None,commandspath : str):
        self.commandspath = commandspath
        self.ignore_words = ignore_words
        if last_dataset is None:
            self.all_words,self.tags,self.xy,self.x,self.y,self.intents = [],[],[],[],[],[]
        else:
            data = torch.load(last_dataset,encoding='utf-8')
            self.all_words,self.tags,self.xy,self.x,self.y,self.intents = data['all_words'],data['tags'],[],[],[],data['intents']
        
        for dir in os.listdir(self.commandspath):
            if os.path.isdir(os.path.join(self.commandspath,dir)):
                content = jsonutils(os.path.join(self.commandspath,dir,'config.json')).content()
                self.intents.append({'tag' : dir,'patterns' : content['patterns']})
                self.tags.append(dir)
                for pattern in content['patterns']:
                    words = tokenize(pattern)
                    self.all_words.extend(words)
                    self.xy.append((words, dir))
        self.all_words = sorted(set([stem(w) for w in self.all_words if w not in self.ignore_words]))
        self.tags = sorted(set(self.tags))
        for (pattern_sentence, tag) in self.xy:
            # X: bag of words for each pattern_sentence
            bag = bag_of_words(pattern_sentence, self.all_words)
            self.x.append(bag)
            # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
            label = self.tags.index(tag)
            self.y.append(label)
        #----------------------------------------------------------------
        self.epochs = epochs
        self.learning_rate = lr
        self.batch_size = int(len(np.array(self.x)[0]) ** 0.5)
        self.input_size = len(np.array(self.x)[0])
        self.hidden_size = hidden_size
        self.output_size = len(self.tags)
        #----------------------------------------------------------------
        self.device = torch.device('cuda' if device == 'cuda' and torch.cuda.is_available() else 'cpu')
        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.traindataset = DataLoader(dataset=ChatDataset(np.array(self.x),np.array(self.y)),batch_size=self.batch_size,shuffle=True,num_workers=0)
        self.testdataset = DataLoader(dataset=ChatDataset(np.array(self.x),np.array(self.y)),batch_size=self.batch_size,shuffle=True,num_workers=0)
        self.loss_params = {}
        self.loss = nn.CrossEntropyLoss(*self.loss_params)
        self.optim_params = {"lr" : self.learning_rate,"betas" : (0.9, 0.999),"eps" : 0.00000001,"weight_decay" : 0.01,"amsgrad" : True}
        self.optim = torch.optim.AdamW(params=self.model.parameters(),**self.optim_params)
        #----------------------------------------------------------------
        self.nepoch = 0
        self.train_loss = 0.0
        self.test_loss = 0.0
        self.accuracy = 0.0
        self.total_labels = 0
        self.correct_labels = 0
        self.probs_list = []

    def set_loss(self, loss,params):
        self.loss_params = params
        self.loss = loss

    def set_optim(self, optim,params):
        self.optim_params = params
        self.optim = optim

    def epoch(self, train : bool, test : bool,printall : bool = True,returndata : bool = False):
        self.nepoch += 1
        
        self.train_loss = 0.0
        self.test_loss = 0.0
        self.correct_labels = 0
        self.total_labels = 0

        if train:
            self.model.train()
            if printall: print(f"loss values     batch size / input size \n")
            
            for batch, (inputs, labels) in enumerate(self.traindataset):
                inputs = inputs.to(self.device)
                labels = labels.to(dtype=torch.long).to(self.device)

                outputs = self.model(inputs)
                loss = self.loss(outputs, labels)

                self.optim.zero_grad()
                loss.backward()
                self.optim.step()

                if batch % 100 == 0:
                    l, current = loss.item(), (batch + 1) * len(inputs)
                    if printall: print(f"loss: {l:>7f}  [{current:>10d}/{len(self.traindataset.dataset):>10d}]")
                else:
                    l, current = loss.item(), (batch + 1) * len(inputs)
                    if printall: print(f"loss: {l:>7f}  [{current:>10d}/{len(self.traindataset.dataset):>10d}]")
                self.train_loss += loss.item()

            self.train_loss /= len(self.traindataset)

        if test:
            self.model.eval()

            with torch.no_grad():
                for inputs, labels in self.testdataset:
                    inputs = inputs.to(self.device)
                    labels = labels.to(dtype=torch.long).to(self.device)

                    outputs = self.model(inputs)

                    loss = self.loss(outputs, labels)

                    self.test_loss += loss.item()

                    _, predicted = torch.max(outputs.data, dim=1)
                    self.total_labels += labels.size(0)
                    self.correct_labels += (predicted == labels).sum().item()

                    #print(f"Total: {total}",f"Correct: {correct}")
            
            Sentence = tokenize(''.lower())
            X = bag_of_words(Sentence, self.all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(self.device)
            output = self.model(X)
            _, predicted = torch.max(output, dim=1)
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            self.probs_list.append(prob.item())

            self.test_loss /= len(self.testdataset)
            self.accuracy = 100 * self.correct_labels / self.total_labels  #(correct):>0.1f
            if printall: print(f"\nEpoch Test: \n Total: {self.total_labels} Correct: {self.correct_labels} \n Accuracy: {self.accuracy}%, Avg loss: {self.test_loss:>8f}, Min Prob: {float(sum(self.probs_list)/len(self.probs_list)):>8f} \n")
        
        if returndata: return {
            'train' : {'train_loss' : self.train_loss},
            'test' : {'test_loss' : self.test_loss,'min_prob' : float(sum(self.probs_list)/len(self.probs_list)),'accuracy' : self.accuracy,'total_labels' : self.total_labels,'correct_labels' : self.correct_labels}}

    def save(self,path : str = None):
        self.nepochs = 0

        data = {
        "intents" : self.intents,
        "model_state": self.model.state_dict(),
        "input_size": self.input_size,
        "hidden_size": self.hidden_size,
        "output_size": self.output_size,
        "all_words": self.all_words,
        "tags": self.tags,
        "benchmark": {
            "num_epochs" : self.epochs,
            "learning_rate" : self.learning_rate,
            "final_train_loss" : self.train_loss, 
            "final_test_loss" : self.test_loss,
            "accuracy" : f"{self.accuracy}%",
            "min_prob" : float(sum(self.probs_list)/len(self.probs_list)),
            "total_labels" : self.total_labels,
            "correct_labels" : self.correct_labels
            },
        "metadata" : {
            "datetime" : datetime.datetime.now().strftime('%d/%m%Y - %H:%M:%S')
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
            torch.save(data, "../models/{}.{}.{}.pth".format(datetime.datetime.now().day,datetime.datetime.now().month,datetime.datetime.now().year) if path is None else path)
        except Exception as e: print(e)



if __name__ == '__main__':
    os.system('cls') if os.name in ('nt', 'dos') else os.system('clear')
    from colorama import Fore,Back
    import keyboard
    mte = MTE(1000,ignore_words=['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|'],commandspath=r'../commands') #last_dataset="./models/data.pth"
    bar_length = 100
    t = 1.0
    def keyboard_callback(key):
        global t
        if key == 'up':
            if t > 0.1: t -= 0.1
        elif key == 'down':
            if t < 3.0: t += 0.1
    keyboard.add_hotkey(hotkey='up',callback=keyboard_callback,trigger_on_release=False,args=['up'])
    keyboard.add_hotkey(hotkey='down',callback=keyboard_callback,trigger_on_release=False,args=['down'])

    print(len(mte.xy), "patterns")
    print(len(mte.tags), "tags") #print(len(tags), "tags:", tags)
    print(len(mte.all_words), "unique stemmed words.",'\n') #print(len(all_words), "unique stemmed words:", all_words)
    print("num epochs:",mte.epochs)
    print("learning rate:",mte.learning_rate)
    print("bach_size:",mte.batch_size,"input_size:",mte.input_size,"output_size:",mte.output_size,"hidden_size:",mte.hidden_size,'\n')

    input(Fore.GREEN + "Premi un tasto per continuare..." + Fore.RESET)

    for epoch in range(mte.epochs):
        print(Fore.GREEN + '[ ↑ ] : speed up all processes | [ ↓ ] : slow down all processes | [ ] : print more specific information \n' + Fore.RESET)                                                                         
        loading_bar = '[' + f'{Fore.GREEN}={Fore.RESET}' * int(round(bar_length * epoch/mte.epochs)) + f'=' * (bar_length - int(round(bar_length * epoch/mte.epochs))) + ']'
        print("Progress: ",loading_bar,f" {epoch/mte.epochs*100:.2f}","%",' - ',f"Epoch: {epoch}/{mte.epochs}")
        data = mte.epoch(True,True,True,True)
        print(Fore.GREEN +f"time for each epoch: {round(t,1)}" + Fore.RESET)

        time.sleep(t)
        os.system('cls') if os.name in ('nt', 'dos') else os.system('clear')

    print("Progress: ",loading_bar,f" {epoch/mte.epochs*100:.2f}","%",' - ',f"Epoch: {epoch}/{mte.epochs}")
    print(f'final loss: {data["train"]["train_loss"]}')
    print(f"\nFinal Test: \n Accuracy: {data['test']['accuracy']}%, Avg loss: {data['test']['test_loss']} \n")

    mte.save()

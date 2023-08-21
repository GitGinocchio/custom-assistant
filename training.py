from ai import NeuralNet,utils
import torch
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

def create_dataset(ignore_words : list[str]):
    all_words = []
    tags = []
    xy = []

    for dir in os.listdir(os.path.join(os.path.dirname(__file__),'commands')):
        if os.path.isdir(os.path.join(os.path.dirname(__file__),'commands',dir)):
            content = jsonutils(os.path.join(os.path.dirname(__file__),'commands',dir,'config.json')).content()
            tags.append(dir)
            for pattern in content['patterns']:
                words = utils.tokenize(pattern)
                all_words.extend(words)
                xy.append((words, dir))

    all_words = sorted(set([utils.stem(w) for w in all_words if w not in ignore_words]))
    tags = sorted(set(tags))

    x_train = []
    y_train = []
    for (pattern_sentence, tag) in xy:
        # X: bag of words for each pattern_sentence
        bag = utils.bag_of_words(pattern_sentence, all_words)
        x_train.append(bag)
        # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
        label = tags.index(tag)
        y_train.append(label)

    return {
        'dataset': ChatDataset(np.array(x_train),np.array(y_train)),
        'x' : np.array(x_train),
        'y' : np.array(y_train),
        'tags' : tags,
        'all_words' : all_words,
        'xy' : xy
        }
data = create_dataset(ignore_words=['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|'])

# Hyper-parameters 
num_epochs = 10000
batch_size = int(len(data['x'][0]) ** 0.5)
learning_rate = 0.001
input_size = len(data['x'][0])
hidden_size = 8
output_size = len(data['tags'])



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

loss = nn.CrossEntropyLoss()
optimizer_params = {"lr" : learning_rate,"betas" : (0.9, 0.999),"eps" : 0.00000001,"weight_decay" : 0.01,"amsgrad" : True}
optimizer = torch.optim.AdamW(params=model.parameters(),**optimizer_params) #optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate,betas=(0.9, 0.999),eps=0.00000001,weight_decay=0,amsgrad=True) #default

train_loader = DataLoader(dataset=data['dataset'],batch_size=batch_size,shuffle=True,num_workers=0)
test_loader = DataLoader(dataset=data['dataset'],batch_size=batch_size,shuffle=True,num_workers=0)

def train_model(model, optimizer, criterion, train_loader, device):
    model.train()  # impostiamo il modello in modalità "train"
    train_loss = 0.0
    print(f"loss values     batch size / input size \n")
    for batch, (inputs, labels) in enumerate(train_loader):
        inputs = inputs.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        outputs = model(inputs)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            l, current = loss.item(), (batch + 1) * len(inputs)
            print(f"loss: {l:>7f}  [{current:>10d}/{len(train_loader.dataset):>10d}]")
        else:
            l, current = loss.item(), (batch + 1) * len(inputs)
            print(f"loss: {l:>7f}  [{current:>10d}/{len(train_loader.dataset):>10d}]")
        train_loss += loss.item()

    train_loss /= len(train_loader)

    return train_loss

probs_list = []

def test_model(model, criterion, test_loader, device):
    model.eval()  # impostiamo il modello in modalità "eval"
    test_loss = 0.0
    correct = 0
    total = 0


    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            labels = labels.to(dtype=torch.long).to(device)

            outputs = model(inputs)

            loss = criterion(outputs, labels)

            test_loss += loss.item()

            _, predicted = torch.max(outputs.data, dim=1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            #print(f"Total: {total}",f"Correct: {correct}")
    
    Sentence = utils.tokenize(''.lower())
    X = utils.bag_of_words(Sentence, data['all_words'])
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    probs_list.append(prob.item())

    test_loss /= len(test_loader)
    accuracy = 100 * correct / total    #(correct):>0.1f
    print(f"\nEpoch Test: \n Total: {total} Correct: {correct} \n Accuracy: {accuracy}%, Avg loss: {test_loss:>8f}, Min Prob: {float(sum(probs_list)/len(probs_list)):>8f} \n")

    return test_loss, accuracy,total, correct

class Training_and_Evaluation:
    def __init__(self):
        pass



if __name__ == '__main__':
    pass

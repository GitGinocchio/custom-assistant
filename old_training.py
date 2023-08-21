import numpy as np
import random
import os
import time
from datetime import datetime
import json
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltk_utils import bag_of_words, tokenize, stem
from model import NeuralNet
from colorama import Fore
CurrentPath = Path(__file__).absolute().parent

def clearConsole():
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        os.system('cls')
    else:
        os.system('clear')

with open(str(CurrentPath) + '\intents.json', 'r',encoding='utf-8') as f: intents = json.load(f)

all_words = []
tags = []
xy = []

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))

# stem and lower each word
ignore_words = ['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|']
all_words = [stem(w) for w in all_words if w not in ignore_words]
# remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

print(len(xy), "patterns")
print(len(tags), "tags") #print(len(tags), "tags:", tags)
print(len(all_words), "unique stemmed words.") #print(len(all_words), "unique stemmed words:", all_words)

# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 10000 #5000 #10000
batch_size = int(len(X_train[0]) ** 0.5) #10
learning_rate = 0.001 #0.001
input_size = len(X_train[0])
hidden_size = 8 #8
output_size = len(tags)
print("num epochs:",num_epochs)
print("learning rate:",learning_rate)
print("bach_size:",batch_size,"input_size:",input_size,"output_size:",output_size,"hidden_size:",hidden_size)

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

dataset = ChatDataset(X_train,y_train)



train_loader = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)

test_loader = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss
criterion = nn.CrossEntropyLoss()
# Optimization
optimizer_params = {
    "lr" : learning_rate,
    "betas" : (0.9, 0.999),
    "eps" : 0.00000001,
    "weight_decay" : 0.01,
    "amsgrad" : True
}
optimizer = torch.optim.AdamW(params=model.parameters(),**optimizer_params) #Actualy the best
#optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate,betas=(0.9, 0.999),eps=0.00000001,weight_decay=0,amsgrad=True) #default

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
    
    Sentence = tokenize(''.lower())
    X = bag_of_words(Sentence, all_words)
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




import keyboard
time_to_sleep = 1.0

def keyboard_callback(key):
    global time_to_sleep
    if key == 'up':
        if round(time_to_sleep,1) > 0.0:
            time_to_sleep -= 0.1
    elif key == 'down':
        time_to_sleep = time_to_sleep + 0.1

def run_training_and_evaluation_test():
    keyboard.add_hotkey(hotkey='up',callback=keyboard_callback,trigger_on_release=False,args=['up'])
    keyboard.add_hotkey(hotkey='down',callback=keyboard_callback,trigger_on_release=False,args=['down'])

    for epoch in range(num_epochs):
        clearConsole()
        print(Fore.GREEN + '[ ↑ ] : speed up all processes | [ ↓ ] : slow up all processes | [ ] : print more specific information \n' + Fore.RESET)
        print(f"Epoch {epoch+1}/{num_epochs}\n----------------------------------")
        train_loss = train_model(model,optimizer,criterion,train_loader,device)
        test_loss, accuracy, total, correct = test_model(model,criterion,test_loader,device)
        print(f"time for each epoch: {round(time_to_sleep,1)}")
        print(f"----------------------------------")
        time.sleep(round(time_to_sleep,1))

    clearConsole()
    print(f'final loss: {train_loss}')
    print(f"\nFinal Test Error: \n Accuracy: {accuracy}%, Avg loss: {test_loss} \n")
    FILE = str(CurrentPath) + "\data.pth"
    data = {
    "intents" : intents,
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags,
    "benchmark": {
        "num_epochs" : num_epochs,
        "learning_rate" : learning_rate,
        "final_train_loss" : train_loss, 
        "final_test_loss" : test_loss,
        "accuracy" : f"{accuracy}%",
        "min_prob" : float(sum(probs_list)/len(probs_list)),
        "total_labels" : total,
        "correct_labels" : correct
        },
    "metadata" : {
        "datetime" : datetime.now().strftime('%d/%m%Y - %H:%M:%S')
    },
    "spec" : {
        "criterion" : str(type(criterion)),
        "optimizer" : str(type(optimizer)),
        "optimizer_params" : optimizer_params,
        "cuda_available" : torch.cuda.is_available(),
        "device_spec" : {"index" : device.index, "type" : device.type}
    }

    }
    #print(f"\ntraining and evaluation completed...")
    #print(f"Saving results to {FILE}...")
    torch.save(data, FILE)
    #print(f'file saved to {FILE}...')
    #print('\n')
    #print(data["benchmark"])
    #print('\n')
    #print(data["metadata"])
    #print('\n')
    #print(data["spec"])
    #print('\n')


    time.sleep(10)

print(f"--------------------------------\n")
print("Running training and evaluation tests...")
time.sleep(5)
run_training_and_evaluation_test()

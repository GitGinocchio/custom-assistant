from ai import NeuralNet,utils
import torch
import numpy as np
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from colorama import Fore
from jsonutils import jsonutils
import os
os.chdir(os.path.dirname(__file__))

all_words = []
tags = []
xy = []

def import_pattern():
    global all_words,tags,xy
    
    for dir in os.listdir(os.path.join(os.path.dirname(__file__),'commands')):
        if os.path.isdir(os.path.join(os.path.dirname(__file__),'commands',dir)):
            content = jsonutils(os.path.join(os.path.dirname(__file__),'commands',dir,'config.json')).content()
            tags.append(dir)
            for pattern in content['patterns']:
                words = utils.tokenize(pattern)
                all_words.extend(words)
                xy.append((words, dir))

    ignore_words = ['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|']
    all_words = [utils.stem(w) for w in all_words if w not in ignore_words]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = utils.bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)
X_train = np.array(X_train)
y_train = np.array(y_train)
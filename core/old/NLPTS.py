import nltk,torch,os
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
#Natural Language Parsing and Tagging System

class NLPTS:
    def __init__(self,datafp : str,ignore_words : list[str] = []):
        self.intents = torch.load(datafp,encoding='ascii')['intents']
        self.ignore_words = ignore_words

    def parse(self,sentence : str, sep : str = ' ',maxsplit : int = -1,ignore_words : list[str] = []):
        ignore_words.extend(self.ignore_words)
        for word in ignore_words: sentence = sentence.replace(word,'')
        return sentence.lower().split(sep, maxsplit)

    def parse_and_tokenize(self,sentence : str,language : str = 'Italian', preserve_line : bool = True,ignore_words : list[str] = []):
        ignore_words.extend(self.ignore_words)
        return nltk.word_tokenize(sentence.lower(),language=language,preserve_line=preserve_line)

    def unparse(self,words : list, sep : str = ' '): return f'{sep}'.join(words).lower()

    def find(self, phrase_words : list, tag : str):
        """
            for a given 'parsed phrase' or 'phrase_words', parsed with 'parse_and_tokenize' or 'parse' method
            and a given tag, return the data finded in that phrase.

            if unparse is True then return a string instead of a list of string.

        """
        try:
            assert tag is not None
            tag_pos = [index for index,name in enumerate(self.intents,0) if name['tag'] == tag][0]
        except AssertionError: pass
        except IndexError: tag_pos = None

        tokenized = []
        for words in [intent['patterns'] for intent in self.intents][tag_pos]: 
            [tokenized.append(word) for word in self.parse_and_tokenize(words) if word not in tokenized] #lemmatizer.lemmatize(word)
        stemmed_pattern = [stemmer.stem(word,to_lowercase=True) for word in tokenized]
        print(stemmed_pattern)

        for index in range(-1, -len(phrase_words)-1, -1):
            if any(w == phrase_words[index] for w in stemmed_pattern): # or any(phrase_words[index].find(w) for w in stemmed_pattern)
                if index + 1 in range(-1,-len(phrase_words)-1,-1):
                    return phrase_words[index + 1::]
                else:
                    #raise IndexError("No data was found for this phrase.")
                    return None

nltps = NLPTS(r'D:\Desktop\Coding\Python\voice-assistant-projects\customized-assistant\models\15.9.2023.pth')
dato = nltps.find(nltps.parse_and_tokenize('Google che ore sono?',preserve_line=True),tag='hours')
print(dato)
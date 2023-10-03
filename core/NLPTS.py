import nltk,torch,os
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
os.chdir(os.path.dirname(__file__))
#Natural Language Parsing and Tagging System

class NLPTS:
    def __init__(self,datafp : str,ignore_words : list[str] = []):
        self.intents = torch.load(datafp,encoding='utf-8')['intents']
        self.ignore_words = ignore_words

    def parse(self,sentence : str, sep : str = ' ',maxsplit : int = -1,ignore_words : list[str] = []):
        ignore_words.extend(self.ignore_words)
        for word in ignore_words: sentence = sentence.replace(word,'')
        return sentence.lower().split(sep, maxsplit)

    def parse_and_tokenize(self,sentence : str,language : str = 'Italian', preserve_line : bool = True,ignore_words : list[str] = []):
        ignore_words.extend(self.ignore_words)
        for word in ignore_words: sentence = sentence.replace(word,'')
        return nltk.word_tokenize(sentence.lower(),language=language,preserve_line=preserve_line)

    def unparse(self,words : list, sep : str = ' '): return f'{sep}'.join(words).lower()

    def findindextagbytag(self,tag : str):
        """
            if tag (str) is specified, return the corresponding index into the intents file and if that tag accepts info.
            else if tag is None, search for tag using a stem function and the words in the pattern dictionary from intents file

            return the corresponding index and if that tag accepts info

        """
        try:
            tag_pos = [index for index,name in enumerate(self.intents,0) if name['tag'] == tag][0]
        except IndexError:
            return None
        else:
            return tag_pos

    def find(self, phrase_words : list, tag : str = None, unparse : bool = True,lemm : bool = False):
        """
            for a given 'parsed phrase' or 'phrase_words', parsed with 'parse_and_tokenize' or 'parse' method
            and a given tag, return the data finded in that phrase.

            if unparse is True then return a string instead of a list of string.

        """
        if tag is not None:
            tag_position = self.findindextagbytag(tag=tag)
        else:
            pass

        tokenized = []
        for words in [intent['patterns'] for intent in self.intents][tag_position]: 
            tokenized_words = self.parse_and_tokenize(words)
            [tokenized.append(lemmatizer.lemmatize(word,'v') if lemm else word) for word in tokenized_words if word not in tokenized] #lemmatizer.lemmatize(word)
        stemmed_pattern = [stemmer.stem(word,to_lowercase=True) for word in tokenized]
        #print(stemmed_pattern)

        for index in range(-1, -len(phrase_words)-1, -1):
            #print(index)
            if any(w == phrase_words[index] for w in stemmed_pattern): # or any(phrase_words[index].find(w) for w in stemmed_pattern)
                if index + 1 in range(-1,-len(phrase_words)-1,-1):
                    if unparse:
                        return self.unparse(phrase_words[index + 1::])
                    else:
                        return phrase_words[index + 1::]
                else:
                    return None
                    #raise IndexError("No data was found for this phrase.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Interazione con NLPTS (Natural Language Parsing and Tagging System).')

    parser.add_argument('sentence', type=str, help='Frase da cui estrapolare informazioni.')
    parser.add_argument('-tag','-t', type=str,required=True, help='Il tag (categoria di frasi) al quale la frase fa parte.')
    parser.add_argument('-model', type=str, default='./data/data.pth',help='Percorso del file del modello AI pre-addestrato. Default: \'./data/data.pth\'.')
    parser.add_argument('-mode','-m', type=str, default='pt',choices=('p','pt'), help='Metodo di preprocesso (parsifica | parsifica e tokenizzazione). Default: \'pt\'')
    parser.add_argument('-parsed','-p', action='store_true',default=False, help='Se ritornare una versione non parsificata o parsificata della frase data in input. Default: True')
    parser.add_argument('-ignore','-i',nargs='*',type=str, default=['?', '.', '!',',',';',':','[', ']', '{', '}', '}', '(','<', '>', '/','\\','|'], help='Una lista di stringhe che non vengono considerate ed eliminate durante la fase di elaborazione.')

    args = parser.parse_args()

    nlpts = NLPTS(args.model,args.ignore)
    phrase_words = nlpts.parse(args.sentence) if args.mode == 'p' else nlpts.parse_and_tokenize(args.sentence)
    result = nlpts.find(phrase_words,args.tag,not args.parsed)
    print(result)
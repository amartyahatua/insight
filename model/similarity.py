from __future__ import print_function
import os
# import sys
import numpy as np
import pandas as pd
import pickle
# from nltk.stem import WordNetLemmatizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction import stop_words
# from nltk.stem import PorterStemmer
# from nltk.stem import LancasterStemmer
# from gensim.models import KeyedVectors
from sklearn.neighbors import KNeighborsClassifier
# from sklearn import metrics

class Similarity:
    def __init__(self):
        self.BASE_DIR = ''
        self.GLOVE_DIR = os.path.join(self.BASE_DIR, 'glove')
        self.TEXT_DATA_DIR = os.path.join(self.BASE_DIR, '20_newsgroup')
        self.MAX_SEQUENCE_LENGTH = 1000
        self.MAX_NUM_WORDS = 20000
        self.EMBEDDING_DIM = 100
        self.VALIDATION_SPLIT = 0.2
        self.embeddings_index = {}
        
    def similarity(self):
        print("hello")
        with open(os.path.join(self.GLOVE_DIR, 'glove.6B.100d.txt'), encoding="utf8") as f:
            for line in f:
                word, coefs = line.split(maxsplit=1)
                coefs = np.fromstring(coefs, 'f', sep=' ')
                self.embeddings_index[word] = coefs
        print('Found %s word vectors.' % len(self.embeddings_index))


        data = pd.read_csv("..\\data\\temp_data.csv",  encoding="utf8")
        text = data['label']
        cls = data['type']
        
        for i in range(len(text)):
            temp = text[i]
            temp = temp.split(" ")
            preprocessed = ''
            for word in temp:
                word = word.lower()                
                if(len(preprocessed) == 0):
                    preprocessed = word 
                else:
                    preprocessed = preprocessed +" "+ word
                
            
            text[i] = preprocessed
            
        embed = np.zeros((len(text), 500))
        
        for i in range(len(text)):
            temp = text[i]
            temp = temp.split(" ")
            for j in range(len(temp)):
                x = temp[j]
                if(len(x) > 0):
                    p = self.embeddings_index[x]
                    embed[i][(j*100):((j+1)*100)] = p
        
        
        knn = KNeighborsClassifier(n_neighbors=10)
        cls = cls.to_numpy()
        knn.fit(embed, cls)
        #pickle.dumps(knn,'model')
        
        return self.embeddings_index, knn
        
        
        
        
        

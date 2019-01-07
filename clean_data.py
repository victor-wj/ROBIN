import re
import os
import sys
import pandas as pd # provide sql-like data manipulation tools. very handy.
pd.options.mode.chained_assignment = None
import numpy as np # high dimensional vector computing library.
from copy import deepcopy
from string import punctuation
from random import shuffle
import gensim
from gensim.models.word2vec import Word2Vec # the word2vec model gensim class
LabeledSentence = gensim.models.doc2vec.LabeledSentence 
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
from nltk.tokenize import TweetTokenizer # a tweet tokenizer from nltk.
tokenizer = TweetTokenizer()
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


class Clean_Data:
    def __init__(self):
        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.csv_file = 'news_label_topic.csv'        

    def clean(self):
        data = pd.read_csv(self.csv_file, encoding ='latin1')
        for i in range(len(data["topic"])):
            try:
                data["topic_clean"][i] = data["topic"][i].replace("BRIEF",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("CORRECTED",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("RPT",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("PRESS DIGEST",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("BAY STREET",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("CANADA STOCKS",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("PREVIEW",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("Analysis:",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("New Issue",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("COMPANY VIEW",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("Insight:",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("Exclusive:",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("Fitch:",'')
                data["topic_clean"][i] = data["topic_clean"][i].lower()
                data["topic_clean"][i] = data["topic_clean"][i].replace('moves-','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('deals of the day --','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update -','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 1','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 2','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 3','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 4','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 5','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 6','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 7','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 8','')
                data["topic_clean"][i] = data["topic_clean"][i].replace('update 9','')
                data["topic_clean"][i] = data["topic_clean"][i].replace(' is ',' be ')
                data["topic_clean"][i] = data["topic_clean"][i].replace(' are ',' be ')
                data["topic_clean"][i] = data["topic_clean"][i].replace("'s",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("breakingviews ",'')
                data["topic_clean"][i] = data["topic_clean"][i].replace("can't",'cannot')
                data["topic_clean"][i] = data["topic_clean"][i].replace("won't",'will not')
                data["topic_clean"][i] = data["topic_clean"][i].replace("%",' percentage')

                # remove all non-ANSI character in topic column data["topic"][i]
                regex1 = re.compile('[^a-zA-Z0-9 ]')
                data["topic_clean"][i] = regex1.sub('', data["topic_clean"][i])

                # more: reports -> report;  lawmakers ->  lawmaker
                if (data["topic_clean"][i].find(' ') == 0):
                    data["topic_clean"][i] = data["topic_clean"][i].replace(' ','',1)
            except Exception as e:
                print (e)
                break
        data.to_csv(self.csv_file)

def main():
    clean_data = Clean_Data()
    clean_data.clean()

if __name__ == "__main__":
    main()

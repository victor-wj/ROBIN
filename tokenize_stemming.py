import pandas as pd 
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re, string, unicodedata
import nltk
from nltk.stem import LancasterStemmer, WordNetLemmatizer

class Clean_Data:
    def __init__(self):

        self.csv_file = 'news_label_topic_after_cleaning.csv'        
    
    def tokenize(self, text):

        """ # 1 .Stemming (including tokenize)
        st = LancasterStemmer()
        stemmedWords = [st.stem(word) for word in word_tokenize(text)]
        print ("stemmedWords: ", stemmedWords) """

        # or. lemmatize_verbs Lemmatization is a more effective option than stemming because it converts the word into its root word, rather than just stripping the suffices. It makes use of the vocabulary and does a morphological analysis to obtain the root word. Therefore, we usually prefer using lemmatization over stemming.
        lemmatizer = WordNetLemmatizer()
        lemmatizerWords_adj = [lemmatizer.lemmatize(word, pos='a') for word in word_tokenize(text)]
        lemmatizerWords_non = [lemmatizer.lemmatize(word, pos='n') for word in lemmatizerWords_adj]
        lemmatizerWords_verb = [lemmatizer.lemmatize(word, pos='v') for word in lemmatizerWords_non]
        print ("lemmatizerWords: ", lemmatizerWords_verb)

        # 3. Removing stopwords
        customStopWords2 = set(stopwords.words('english')+list(punctuation))
        wordsWOStopwords2 = [word for word in lemmatizerWords_verb if word not in customStopWords2]
        print ("wordsWOStopwords2: ", wordsWOStopwords2)
        return wordsWOStopwords2


def main():
    clean_data = Clean_Data()
    data = pd.read_csv(clean_data.csv_file, encoding ='latin1')

    for i in range(len(data["topic"])):
        data["topic_tokenized"][i] = clean_data.tokenize(data["topic"][i])

    data.to_csv(clean_data.csv_file)

if __name__ == "__main__":
    main()


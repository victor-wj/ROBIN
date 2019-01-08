# https://github.com/giuseppebonaccorso/twitter_sentiment_analysis_word2vec_convnet/blob/master/Twitter%20Sentiment%20Analysis%20with%20Word2Vec%20and%20Convnets.ipynb
import pandas as pd 
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
import re, string, unicodedata
import nltk
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import keras.backend as K
import multiprocessing
import tensorflow as tf
from gensim.models.word2vec import Word2Vec
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv1D
from keras.optimizers import Adam
from nltk.tokenize import RegexpTokenizer     
import dill
import numpy as np

np.random.seed(1000)

tokenized_corpus = []
labels = []

data = pd.read_csv('news_label_topic_cleaning_tokenized.csv', encoding ='latin1')

for i in range(len(data["topic"])):
    labels.append(data["label"][i])
    tokenized_corpus.append(data["topic_tokenized"][i].strip())

with open( 'tokenized_corpus.dill', 'wb') as f:
    dill.dump(tokenized_corpus, f)

with open('tokenized_corpus.dill', 'rb') as f:
    tokenized_corpus = dill.load(f)

vector_size = 512
window_size = 10
word2vec = Word2Vec(sentences=tokenized_corpus,
                size=vector_size, 
                window=window_size, 
                negative=20,
                iter=50,
                seed=1000,
                workers=multiprocessing.cpu_count())
word2vec.save('word2vec.model')        
word2vec = Word2Vec.load('word2vec.model') 

word2vec.save('word2vec.model')

word2vec = Word2Vec.load('word2vec.model')

X_vecs = word2vec.wv
train_size = 40000
test_size = 4226
avg_length = 0.0
max_length = 0
for news in tokenized_corpus:
    if len(news) > max_length:
        max_length = len(news)
    avg_length += float(len(news))
max_tweet_length = 20
indexes = np.random.choice(len(tokenized_corpus), train_size + test_size, replace=False)

X_train = np.zeros((train_size, max_tweet_length, vector_size), dtype=K.floatx())
Y_train = np.zeros((train_size, 2), dtype=np.int32)
X_test = np.zeros((test_size, max_tweet_length, vector_size), dtype=K.floatx())
Y_test = np.zeros((test_size, 2), dtype=np.int32)

for i, index in enumerate(indexes):
    for t, token in enumerate(tokenized_corpus[index]):
        if t >= max_tweet_length:
            break
        
        if token not in X_vecs:
            continue
    
        if i < train_size:
            X_train[i, t, :] = X_vecs[token]
        else:
            X_test[i - train_size, t, :] = X_vecs[token]
            
    if i < train_size:
        Y_train[i, :] = [1.0, 0.0] if labels[index] == 0 else [0.0, 1.0]
    else:
        Y_test[i - train_size, :] = [1.0, 0.0] if labels[index] == 0 else [0.0, 1.0]

batch_size = 32
nb_epochs = 100
model = Sequential()

model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same', input_shape=(max_tweet_length, vector_size)))
model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same'))
model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same'))
model.add(Conv1D(32, kernel_size=3, activation='elu', padding='same'))
model.add(Dropout(0.25))

model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
model.add(Conv1D(32, kernel_size=2, activation='elu', padding='same'))
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(256, activation='tanh'))
model.add(Dense(256, activation='tanh'))
model.add(Dropout(0.5))

model.add(Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=0.0001, decay=1e-6),
              metrics=['accuracy'])

# Fit the model

model.fit(X_train, Y_train,
          batch_size=batch_size,
          shuffle=True,
          epochs=nb_epochs,
          validation_data=(X_test, Y_test),
          callbacks=[EarlyStopping(min_delta=0.00025, patience=2)])
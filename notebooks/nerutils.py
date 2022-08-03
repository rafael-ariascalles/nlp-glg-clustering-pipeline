import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import LSTM, Embedding, Dense
from tensorflow.keras.layers import TimeDistributed, SpatialDropout1D, Bidirectional
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from sklearn.metrics import classification_report

class NERTextPrepper():
    def __init__(self, data, max_len=50, case="lower", punctuation="trailing"):
        self.data = data

        #
        # Text regularization
        #
        if case == "lower":
            data['Word'] = data['Word'].str.lower()

        if punctuation == "trailing":
            data['Word'] = data['Word'].str.replace("\([a-z0-9]+\)(\.|,|!|\?)\+", "\1", regex=True)
            data['Word'] = data['Word'].str.replace("~", "", regex=True)
        elif punctuation == "all":
            data['Word'] = data['Word'].str.replace("[^a-z0-9]", " ", regex=True)

        #
        # Create vocabulary
        #
        self.words = list(set(self.data['Word'].values))
        self.words.append("<unk>")
        self.words.append("ENDPAD")
        self.num_words = len(self.words) + 1


        # Create tag list

        # We do not have enough 'nat', 'art' or 'eve' tags to predict them
        # with any meaningful accuracy, so we will create a new 'misc' category
        self.data['Tag'] = self.data['Tag'].str.replace("(nat|art|eve)", "misc", regex=True)

        self.tags = list(set(self.data['Tag'].values))
        self.num_tags = len(self.tags)
        

        # Create vocab and tag dictionary for word -> integer lookup

        self.word2idx =  {w : i+1 for i,w in enumerate(self.words)}
        self.tag2idx  =  {t : i for i,t in enumerate(self.tags)}
        


        # Split 'Word' series to arrays of sentences

        self.data['Sentence #'] = self.data['Sentence #'].fillna(method='ffill')
        agg_func = lambda s:[(w,t) for w,t in zip(s['Word'].tolist(),s['Tag'].tolist())]
        self.grouped = self.data.groupby("Sentence #").apply(agg_func)
        self.sentences = [s for s in self.grouped]
        

        # Convert data to form needed by Tensorflow model

        self.max_len = 50
        
        self.X = [[self.word2idx[w[0]] for w in s]for s in self.sentences]
        self.X = pad_sequences(maxlen=self.max_len , sequences=self.X, padding='post', value=self.num_words-1)

        self.y = [[self.tag2idx[w[1]] for w in s]for s in self.sentences]
        self.y = pad_sequences(maxlen=max_len , sequences=self.y, padding='post', value=self.tag2idx["O"])
        self.y = [to_categorical(i, num_classes=self.num_tags) for i in self.y]

    def fit(self, x_train, y_train, epochs=10):
        
        # Layers

        input_word = Input(shape = (self.max_len,))
        self.model = Embedding(input_dim=self.num_words,output_dim=self.max_len,input_length=self.max_len)(input_word)
        self.model = SpatialDropout1D(0.1)(self.model)
        self.model = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.1))(self.model)
        out = TimeDistributed(Dense(self.num_tags,activation='softmax'))(self.model)
        self.model = Model(input_word,out)
        self.model.summary()

        # Compile

        self.model.compile(optimizer="adam",loss='categorical_crossentropy',metrics=['accuracy'])

        # Fit controls and start fit

        early_stopping = EarlyStopping(monitor='val_accuracy',patience=1,verbose=0,mode='max',restore_best_weights=True)
        callbacks = [early_stopping]

        history = self.model.fit(x_train,np.array(y_train), validation_split = 0.2, batch_size = 64, epochs = epochs, verbose = 1,
            callbacks=callbacks)

        return history
   
    def evaluate(self, x_test, y_test):

        self.model.evaluate(x_test, np.array(y_test))

        # Convert y_true and model predictions to integers that
        # match our tag2idx dictionary

        y_pred_probs = self.model.predict(np.array(x_test))
        y_true = np.argmax(np.array(y_test), axis=-1)
        y_true_flat = [item for sublist in y_true for item in sublist]

        y_pred = np.argmax(y_pred_probs, axis=-1)
        y_pred = [item for sublist in y_pred for item in sublist]

        print(self.tags)
        print(classification_report(y_true_flat, y_pred, target_names=self.tags))

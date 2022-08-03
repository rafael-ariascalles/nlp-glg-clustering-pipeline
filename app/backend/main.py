from html import entities
from pydoc_data.topics import topics
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

import tensorflow as tf
import pandas as pd
import numpy as np

def string2Vector(str_in, word2idx_dict, max_len=50):
    """
    Process sentences so they are ready
       to pass to the LSTM prediction model
    """
    
    # Fill vector with end padding value
    str_vec = [word2idx_dict["ENDPAD"]] * max_len
   

    # Fill vector with integer representation
    # of the word if found in the dictionary,
    # otherwise use index for "unknown" character
    for i, s in enumerate(str_in.lower().split()):
        if s in word2idx_dict.keys():
            str_vec[i] = word2idx_dict[s]
        else:
            str_vec[i] = word2idx_dict["<unk>"]
            
        # If string is too long, truncate it
        if i == max_len-1:
            break
            
    return str_in.split(), np.reshape(str_vec, (1,max_len))


app = FastAPI()

####################
# Load assets     
####################
# Load NER model and keep it in RAM
data_dir = "./models/"
ner_model = tf.keras.models.load_model(data_dir + 'ner-lstm-3')

# Dictionaries that map words and tag text to
# the integer representation used by the TF model
word = pd.read_csv(data_dir + "word2dict.csv")
word2idx_dict = pd.Series(word['values'].values, index=word['words']).to_dict()

tags = pd.read_csv(data_dir + "tag2dict.csv")
tag2idx_dict = pd.Series(tags['values'].values, index=tags['tag']).to_dict()


# pydantic models
class SubmitedText(BaseModel):
    text: str

class SubmitedTextOut(SubmitedText):
    entities: dict
    topics: dict

@app.post("/predict", response_model=SubmitedTextOut, status_code=200)
def get_prediction(payload: SubmitedText):
    
    text = payload.text
    
    # Convers text to numeric input for TF model
    text_tokens, text_vector = string2Vector(text, word2idx_dict)

    
    # Load model and predict
    ner_preds = ner_model.predict(text_vector)

    # Convert prediction probabilities to text tag labels
    ner_preds = np.argmax(ner_preds, axis=-1)
    ner_preds = [item for sublist in ner_preds for item in sublist]
    tag_names = list(tag2idx_dict.keys())

    entities = {}
    for i, ner_pred_i in enumerate(ner_preds):
        tag_i = tag_names[ner_pred_i]
        if tag_i != "O":
            entities[text_tokens[i]] = tag_i

    response_object = SubmitedTextOut(text=text
        , entities=entities
        , topics={"Topic 1": [], "Topic 2": [], "Topic 3": [], "Topic 4": [], "Topic 5": []}
    )

    return response_object
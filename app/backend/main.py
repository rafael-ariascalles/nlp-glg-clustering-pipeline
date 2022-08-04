from html import entities
from pydoc_data.topics import topics
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

import tensorflow as tf
import pandas as pd
import numpy as np
import re
# import logging

def string2Vector(str_in, word2idx_dict, max_len=50):
    """
    Process sentences so they are ready
       to pass to the LSTM prediction model
    """
    
    # Fill vector with end padding value
    str_vec = [word2idx_dict["ENDPAD"]] * max_len
   
    str_clean = str_in.replace("'s", "");
    str_clean = re.sub("([a-zA-Z0-9])(\.|,|!|\?)", "\g<1>", str_clean)
    str_clean = str_clean.replace("~", "");

    # Fill vector with integer representation
    # of the word if found in the dictionary,
    # otherwise use index for "unknown" character
    for i, s in enumerate(str_clean.lower().split()):
        if s in word2idx_dict.keys():
            str_vec[i] = word2idx_dict[s]
        else:
            str_vec[i] = word2idx_dict["<unk>"]
            
        # If string is too long, truncate it
        if i == max_len-1:
            break
            
    return str_clean.split(), np.reshape(str_vec, (1,max_len))


app = FastAPI()

####################
# Load assets     
####################
# Load NER model and keep it in RAM
data_dir = "./models/"
ner_model = tf.keras.models.load_model(data_dir + 'ner-lstm-no-trailing-punct-misc')

# Dictionaries that map words and tag text to
# the integer representation used by the TF model
word = pd.read_csv(data_dir + "word2dict.csv")
word2idx_dict = pd.Series(word['values'].values, index=word['words']).to_dict()

tags = pd.read_csv(data_dir + "tag2dict.csv")
tag2idx_dict = pd.Series(tags['values'].values, index=tags['tag']).to_dict()
tag_names = list(tag2idx_dict.keys())

bio2readable_tag = {'B-per': 'Person', 'I-per': 'Person'
                    , 'B-geo': 'Location', 'I-geo': 'Location'
                    , 'B-gpe': 'Geopolitical entity', 'I-gpe': 'Geopolitical entity'
                    , 'B-org': 'Organization', 'I-org': 'Organization'
                    , 'B-misc': 'Misc', 'I-misc': 'Misc'
                    , 'B-tim': 'Time', 'I-tim': 'Time'
                    }

def assign_entities(ner_preds, tag_names, text_tokens):
    entities={'Person': '', 'Location': '', 'Organization': '', 'Geopolitical entity': '', 'Time': '', 'Misc': ''}
    last_tag = ""
    for i, ner_pred_i in enumerate(ner_preds):
        tag_i = tag_names[ner_pred_i]
        sep = "";
        if tag_i != "O":
            # entities[text_tokens[i]+str(i)] = tag_i
            tag_readable_i = bio2readable_tag[tag_i]
            if entities[tag_readable_i] != "":
                sep = ", "
            if tag_i.startswith('I') and last_tag == tag_readable_i:
                entities[tag_readable_i] = entities[tag_readable_i] + ' ' + text_tokens[i]
            else:
                entities[tag_readable_i] = entities[tag_readable_i] + sep +  text_tokens[i]
            last_tag = tag_readable_i

    return entities

def get_predicted_classes(ner_pred_probs):
    ner_preds = np.argmax(ner_pred_probs, axis=-1)
    ner_preds = [item for sublist in ner_preds for item in sublist]

    return ner_preds

# pydantic models
class SubmitedText(BaseModel):
    text: str

class SubmitedTextOut(SubmitedText):
    entities: dict
    topics: dict

@app.post("/predict", response_model=SubmitedTextOut, status_code=200)
def get_prediction(payload: SubmitedText):
    
    # logging.debug('This message should go to the log file')
    text = payload.text
    
    # Convers text to numeric input for TF model
    text_tokens, text_vector = string2Vector(text, word2idx_dict)

    # Get predicted tag probabilities
    ner_pred_probs = ner_model.predict(text_vector)

    # Convert prediction probabilities to integer class labels
    ner_preds = get_predicted_classes(ner_pred_probs)
    
    # Convert integer class labels to friendly tag names
    # and assign tagged words to the predicted dictionary location
    entities = assign_entities(ner_preds, tag_names, text_tokens)

    response_object = SubmitedTextOut(text=text
        , entities=entities
        , topics={"Topic 1": [], "Topic 2": [], "Topic 3": [], "Topic 4": [], "Topic 5": []}
    )

    return response_object
from html import entities
from pydoc_data.topics import topics
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

import pandas as pd
import numpy as np

from flair.data import Sentence
from flair.models import SequenceTagger


app = FastAPI()

####################
# Load assets     
####################
# Load NER model and keep it in RAM
data_dir = "./models/"

# load tagger
tagger = SequenceTagger.load("flair/ner-english-ontonotes-fast")

def get_entities(text):
    # make example sentence
    sentence = Sentence(text)

    # predict NER tags
    tagger.predict(sentence)

    # print predicted NER spans
    # print('The following NER tags are found:')
    # iterate over entities and print
    entities = {}
    for entity in sentence.get_spans('ner'):
        # entities[entity.text] = entity.tag
        if entity.tag in entities:
            entities[entity.tag] = entities[entity.tag] + ", " + entity.text
        else:
            entities[entity.tag] = entity.text

    return entities


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

    entities = get_entities(text)

    response_object = SubmitedTextOut(text=text
        , entities=entities
        , topics={"Topic 1": [], "Topic 2": [], "Topic 3": [], "Topic 4": [], "Topic 5": []}
    )

    return response_object

from html import entities
from pydoc_data.topics import topics
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from topic_service import TopicService
from ner_service import NERService

import pandas as pd
import numpy as np



app = FastAPI()

####################
# Load assets     
####################

# load tagger
#tagger = SequenceTagger.load("flair/ner-english-ontonotes-fast")
ner_service = NERService()
topic_service = TopicService()


# pydantic models
class SubmitedText(BaseModel):
    text: str

class SubmitedTextOut(SubmitedText):
    entities: dict
    topics: List[dict]

@app.post("/predict", response_model=SubmitedTextOut, status_code=200)
def get_prediction(payload: SubmitedText):
    
    # logging.debug('This message should go to the log file')
    text = payload.text

    entities = ner_service.get_entities(text)
    topics = topic_service.predict_topic([text])

    response_object = SubmitedTextOut(text=text
        , entities=entities
        , topics=topics
    )

    return response_object

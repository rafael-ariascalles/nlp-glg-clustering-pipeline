from html import entities
from pydoc_data.topics import topics
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel



app = FastAPI()

# pydantic models
class SubmitedText(BaseModel):
    text: str

class SubmitedTextOut(SubmitedText):
    entities: dict
    topics: dict

@app.post("/predict", response_model=SubmitedTextOut, status_code=200)
def get_prediction(payload: SubmitedText):
    text = payload.text


    response_object = SubmitedTextOut(text=text
        , entities={"PERSON": [], "LOCATION": [], "ORGANIZATION": [], "MONEY": [], "PERCENT": [], "DATE": [], "TIME": [], "MISC": []}
        , topics={"Topic 1": [], "Topic 2": [], "Topic 3": [], "Topic 4": [], "Topic 5": []}
    )

    return response_object
from collections import defaultdict
from flair.data import Sentence
from flair.models import SequenceTagger
import numpy as np

class NERService:

    def __init__(self):
        self.ner_tagger_model = SequenceTagger.load("flair/ner-english-ontonotes-fast")

    def get_entities(self, text):
        sentence = Sentence(text)

        # predict NER tags
        self.ner_tagger_model.predict(sentence)

        # iterate over entities and put them
        # in a dictionary with the tag as the key
        # but do not add duplicate values
        entities = defaultdict(set)
        for entity in sentence.get_spans('ner'):
                entities[entity.tag].add(entity.text)

        return { k: list(v) for k,v in entities.items() }


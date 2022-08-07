from flair.data import Sentence
from flair.models import SequenceTagger

class NERService:

    def __init__(self):
        self.ner_tagger_model = SequenceTagger.load("flair/ner-english-ontonotes-fast")

    def get_entities(self, text):
        sentence = Sentence(text)

        # predict NER tags
        self.ner_tagger_model.predict(sentence)

        # iterate over entities and put them
        # in a dictionary with the tag as the key
        entities = {}
        for entity in sentence.get_spans('ner'):
            # entities[entity.text] = entity.tag
            if entity.tag in entities:
                entities[entity.tag] = entities[entity.tag] + ", " + entity.text
            else:
                entities[entity.tag] = entity.text

        return entities


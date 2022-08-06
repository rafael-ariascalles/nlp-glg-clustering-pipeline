import joblib
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Class for topic service
# This class is used to predict the topic of a given text, it use sentence embedding to predict the topic
# 1. Load the model sentence-transformers using huggingface library
# 2. Load the Kmeans minibatch kmeans model using joblib
# 3. Predict the topic of a given text
class TopicService:

    # Constructor
    # 1. Load the model sentence-transformers using huggingface library
    # 2. Load the Kmeans minibatch kmeans model using joblib
    def __init__(self):
        self.encoder_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.cluster_model = joblib.load('./models/kmeans_model.pkl')

    # Predict the topic of a given text
    # 1. Get the embedding of the text
    # 2. Predict the topic of the text
    # 3. Return the topic
    def predict_topic(self, text):
        embedding = self.encoder_model.encode(text)

        distances = self.kmean_model.transform(embedding)
        cluster = self.kmean_model.predict(embedding)
        cluster_distances = np.min(distances,axis=1)
        topic = [c if d < 0.9 else 37 for c,d in zip(cluster,cluster_distances)]
        return topic[0]
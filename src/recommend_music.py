import pandas as pd
from sentence_transformers import SentenceTransformer, util
import streamlit as st

class MusicRecommendationSystem:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.df = None
        self.emb = None

    def initialize(self):
        try:
            self.df = pd.read_csv(self.csv_path)
            required = ['Title','Mood','Genre','Language']
            if any(c not in self.df.columns for c in required):
                return "Columns missing"
            texts = (self.df['Title'] + ' ' + self.df['Mood'] +
                     ' ' + self.df['Genre'] + ' ' + self.df['Language'])
            self.emb = self.model.encode(texts.tolist(), convert_to_tensor=True)
            return None
        except:
            return "CSV load error"

    def get_unique_genres(self):
        return sorted(self.df['Genre'].dropna().unique())

    def recommend(self, caption, genre, top=5):
        query = f"{caption} {genre}"
        q_emb = self.model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(q_emb, self.emb)[0]
        idx = scores.argsort(descending=True)[:top].cpu().numpy()
        return self.df.iloc[idx], self.df.iloc[idx]['Mood'].mode()[0]

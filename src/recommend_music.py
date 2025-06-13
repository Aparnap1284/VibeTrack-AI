import pandas as pd
from sentence_transformers import SentenceTransformer, util

class MusicRecommendationSystem:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.embeddings = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def initialize(self):
        try:
            self.df = pd.read_csv(self.csv_path)
            required_cols = ['Title', 'Mood', 'Genre', 'Language']
            missing = [col for col in required_cols if col not in self.df.columns]
            if missing:
                return f"Missing columns: {missing}"

            self.df['full_text'] = (
                self.df['Title'].astype(str) + " " +
                self.df['Mood'].astype(str) + " " +
                self.df['Genre'].astype(str) + " " +
                self.df['Language'].astype(str)
            )

            self.embeddings = self.model.encode(self.df['full_text'].tolist(), convert_to_tensor=True)
        except Exception as e:
            return str(e)

    def detect_mood(self, caption):
        # Map mood keywords manually (quick and effective)
        mood_keywords = {
            "happy": ["celebration", "birthday", "smile", "joy", "friends"],
            "sad": ["tears", "cry", "alone", "breakup"],
            "romantic": ["love", "kiss", "valentine", "romance", "candlelight"],
            "dreamy": ["stars", "sleep", "dream", "moonlight"],
            "energetic": ["dance", "party", "gym", "hype"],
            "angry": ["fight", "rage", "angry", "revenge"]
        }

        caption_lower = caption.lower()
        for mood, keywords in mood_keywords.items():
            if any(word in caption_lower for word in keywords):
                return mood.capitalize()

        return "Neutral"

    def get_unique_genres(self):
        return sorted(self.df['Genre'].dropna().unique()) if self.df is not None else []

    def recommend(self, caption, genre, top_k=5):
        mood = self.detect_mood(caption)
        query = f"{caption} {mood} {genre}"
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, self.embeddings)[0]
        top_indices = scores.argsort(descending=True)[:top_k]
        return self.df.iloc[top_indices.cpu().numpy()], mood

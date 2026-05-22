import pandas as pd
import random
from sentence_transformers import SentenceTransformer, util
import streamlit as st


class MusicRecommendationSystem:

    def __init__(self, csv_path):

        self.csv_path = csv_path

        self.model = SentenceTransformer(
            'all-MiniLM-L6-v2'
        )

        self.df = None
        self.emb = None

    # ---------------------------------------------------
    # DETECT MOOD FROM CAPTION
    # ---------------------------------------------------
    def detect_caption_mood(self, caption):

        caption = caption.lower()

        mood_keywords = {

            "Energetic": [
                "party",
                "dance",
                "dj",
                "club",
                "celebration",
                "festival",
                "fun",
                "friends",
                "farewell",
                "wedding",
                "beats",
                "crazy"
            ],

            "Romantic": [
                "love",
                "romantic",
                "couple",
                "date",
                "kiss",
                "heart",
                "stars",
                "together"
            ],

            "Sad": [
                "alone",
                "broken",
                "cry",
                "pain",
                "heartbreak",
                "lost",
                "miss"
            ],

            "Peaceful": [
                "beach",
                "sunset",
                "nature",
                "mountains",
                "calm",
                "relax",
                "ocean",
                "seashore"
            ],

            "Motivational": [
                "gym",
                "workout",
                "success",
                "motivation",
                "winner",
                "hustle",
                "beast",
                "hero"
            ],

            "Melancholic": [
                "rain",
                "night",
                "lonely",
                "dark",
                "memories",
                "silent"
            ]
        }

        for mood, keywords in mood_keywords.items():

            for word in keywords:

                if word in caption:
                    return mood

        return "Romantic"

    # ---------------------------------------------------
    # INITIALIZE
    # ---------------------------------------------------
    def initialize(self):

        try:

            self.df = pd.read_csv(
                self.csv_path,
                sep=None,
                engine='python'
            )

            self.df.columns = (
                self.df.columns.str.strip()
            )

            required = [
                'Title',
                'Composer',
                'Singer',
                'Mood',
                'Genre',
                'Language'
            ]

            missing = [

                col for col in required
                if col not in self.df.columns

            ]

            if missing:
                return f"Columns missing: {missing}"

            self.df = self.df.fillna('')

            # -----------------------------------------
            # SMART SEMANTIC TEXTS
            # -----------------------------------------
            texts = (

                "Song: " +
                self.df['Title'].astype(str) + ". " +

                "Singer: " +
                self.df['Singer'].astype(str) + ". " +

                "Composer: " +
                self.df['Composer'].astype(str) + ". " +

                "Mood: " +
                self.df['Mood'].astype(str) + ". " +

                "Genre: " +
                self.df['Genre'].astype(str) + ". " +

                "Language: " +
                self.df['Language'].astype(str)

            )

            self.emb = self.model.encode(
                texts.tolist(),
                convert_to_tensor=True
            )

            return None

        except Exception as e:

            return f"CSV load error: {str(e)}"

    # ---------------------------------------------------
    # GET GENRES
    # ---------------------------------------------------
    def get_unique_genres(self):

        return sorted(

            self.df['Genre']
            .dropna()
            .astype(str)
            .unique()
            .tolist()

        )

    # ---------------------------------------------------
    # GET LANGUAGES
    # ---------------------------------------------------
    def get_unique_languages(self):

        return sorted(

            self.df['Language']
            .dropna()
            .astype(str)
            .unique()
            .tolist()

        )

    # ---------------------------------------------------
    # RECOMMEND
    # ---------------------------------------------------
    def recommend(
        self,
        caption,
        genre,
        language=None,
        top=5
    ):

        try:

            # -----------------------------------------
            # DETECT MOOD
            # -----------------------------------------
            detected_mood = self.detect_caption_mood(
                caption
            )

            # -----------------------------------------
            # BETTER QUERY
            # -----------------------------------------
            query = f"""
            Video vibe: {caption}

            Preferred genre: {genre}

            Preferred language: {language}

            Mood: {detected_mood}

            Recommend emotionally matching songs.
            """

            q_emb = self.model.encode(
                query,
                convert_to_tensor=True
            )

            scores = util.cos_sim(
                q_emb,
                self.emb
            )[0]

            self.df['score'] = (
                scores.cpu().numpy()
            )

            # -----------------------------------------
            # STRICT FILTERING
            # -----------------------------------------
            filtered_df = self.df[

                self.df['Genre']
                .str.contains(
                    genre,
                    case=False,
                    na=False
                )

            ].copy()

            if language != "Any":

                filtered_df = filtered_df[

                    filtered_df['Language']
                    .str.contains(
                        language,
                        case=False,
                        na=False
                    )

                ]

            # -----------------------------------------
            # MOOD BOOSTING
            # -----------------------------------------
            filtered_df['mood_bonus'] = filtered_df[
                'Mood'
            ].apply(

                lambda x: 0.15
                if str(x).lower() ==
                detected_mood.lower()
                else 0

            )

            filtered_df['final_score'] = (

                filtered_df['score'] +
                filtered_df['mood_bonus']

            )

            # -----------------------------------------
            # SORT
            # -----------------------------------------
            filtered_df = filtered_df.sort_values(
                by='final_score',
                ascending=False
            )

            # -----------------------------------------
            # TOP CANDIDATES
            # -----------------------------------------
            top_candidates = filtered_df.head(15)

            # -----------------------------------------
            # DIVERSITY
            # -----------------------------------------
            recommendations = top_candidates.sample(

                n=min(top, len(top_candidates)),

                random_state=random.randint(
                    1,
                    99999
                )

            )

            recommendations = recommendations.sort_values(
                by='final_score',
                ascending=False
            )

            return (
                recommendations,
                detected_mood
            )

        except Exception as e:

            st.error(
                f"Recommendation error: {str(e)}"
            )

            return (
                pd.DataFrame(),
                "Unknown"
            )
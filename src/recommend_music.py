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
    # INITIALIZE DATASET + EMBEDDINGS
    # ---------------------------------------------------
    def initialize(self):

        try:

            # Auto detect CSV separator
            self.df = pd.read_csv(
                self.csv_path,
                sep=None,
                engine='python'
            )

            # Clean column names
            self.df.columns = (
                self.df.columns.str.strip()
            )

            print("\nDetected Columns:\n")
            print(self.df.columns.tolist())

            # Required columns
            required = [
                'Title',
                'Composer',
                'Singer',
                'Mood',
                'Genre',
                'Language'
            ]

            # Check missing columns
            missing = [
                col for col in required
                if col not in self.df.columns
            ]

            if missing:
                return f"Columns missing: {missing}"

            # Fill empty values
            self.df = self.df.fillna('')

            # ---------------------------------------------------
            # SMART SEMANTIC EMBEDDINGS
            # ---------------------------------------------------
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

            # Generate embeddings
            self.emb = self.model.encode(
                texts.tolist(),
                convert_to_tensor=True
            )

            return None

        except Exception as e:

            return f"CSV load error: {str(e)}"

    # ---------------------------------------------------
    # GET UNIQUE GENRES
    # ---------------------------------------------------
    def get_unique_genres(self):

        try:

            genres = sorted(

                self.df['Genre']
                .dropna()
                .astype(str)
                .unique()
                .tolist()

            )

            return genres

        except Exception:

            return []

    # ---------------------------------------------------
    # GET UNIQUE LANGUAGES
    # ---------------------------------------------------
    def get_unique_languages(self):

        try:

            languages = sorted(

                self.df['Language']
                .dropna()
                .astype(str)
                .unique()
                .tolist()

            )

            return languages

        except Exception:

            return []

    # ---------------------------------------------------
    # MAIN RECOMMENDATION FUNCTION
    # ---------------------------------------------------
    def recommend(
        self,
        caption,
        genre,
        language="Any",
        top=5
    ):

        try:

            # ---------------------------------------------------
            # BETTER QUERY ENGINEERING
            # ---------------------------------------------------
            query = f"""
            A music recommendation for:
            {caption}

            The music should match the emotional vibe,
            atmosphere, energy, and feeling of the scene.

            Preferred genre: {genre}
            Preferred language: {language}

            Mood relevance is more important than exact genre.
            """

            # Encode query
            q_emb = self.model.encode(
                query,
                convert_to_tensor=True
            )

            # Similarity scores
            scores = util.cos_sim(
                q_emb,
                self.emb
            )[0]

            # ---------------------------------------------------
            # CREATE SAFE COPY
            # ---------------------------------------------------
            filtered_df = self.df.copy()

            # Add scores
            filtered_df['score'] = (
                scores.cpu().numpy()
            )

            # ---------------------------------------------------
            # STRICT GENRE FILTERING
            # ---------------------------------------------------
            genre_filtered = filtered_df[

                filtered_df['Genre']
                .str.contains(
                    genre,
                    case=False,
                    na=False
                )

            ].copy()

            # Use genre filter if enough results exist
            if len(genre_filtered) >= 5:

                filtered_df = genre_filtered

            # ---------------------------------------------------
            # LANGUAGE FILTER
            # ---------------------------------------------------
            if language != "Any":

                language_filtered = filtered_df[

                    filtered_df['Language']
                    .str.contains(
                        language,
                        case=False,
                        na=False
                    )

                ].copy()

                # Keep language filter only if enough songs
                if len(language_filtered) >= 3:

                    filtered_df = language_filtered

            # ---------------------------------------------------
            # FINAL SORTING
            # ---------------------------------------------------
            filtered_df = filtered_df.sort_values(
                by='score',
                ascending=False
            )

            # ---------------------------------------------------
            # DETECTED MOOD
            # ---------------------------------------------------
            detected_mood = (
                filtered_df.iloc[0]['Mood']
            )

            # ---------------------------------------------------
            # TOP CANDIDATES
            # ---------------------------------------------------
            top_candidates = (
                filtered_df.head(12)
            )

            # ---------------------------------------------------
            # SLIGHT DIVERSITY
            # ---------------------------------------------------
            recommendations = top_candidates.sample(

                n=min(top, len(top_candidates)),

                random_state=random.randint(
                    1,
                    10000
                )

            )

            # Remove duplicates
            recommendations = (
                recommendations
                .drop_duplicates(
                    subset=['Title']
                )
            )

            # Final sorting
            recommendations = (
                recommendations
                .sort_values(
                    by='score',
                    ascending=False
                )
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
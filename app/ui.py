import streamlit as st
import urllib.parse
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recommend_music import MusicRecommendationSystem


# 🔧 Load mood image from assets/
def load_mood_image(mood):
    mood = mood.strip().lower()
    
    # Resolve path from ui.py (which is inside /app/)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    image_path = os.path.join(base_dir, 'assets', f"{mood}.jpg")
    default_path = os.path.join(base_dir, 'assets', "default.jpg")

    if os.path.exists(image_path):
        return image_path, f"{mood.title()} Vibes"
    else:
        return default_path, "Default Vibe"


# Page setup
st.set_page_config(page_title="VibeTrack AI", page_icon="🎵", layout="wide")

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Custom styles
st.markdown("""
    <style>
    .container {
        max-width: 1100px;
        margin: auto;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #5b21b6;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize recommender
recommender = MusicRecommendationSystem("dataset/reels_dataset.csv")
error = recommender.initialize()
if error:
    st.error(error)
    st.stop()

# UI layout
with st.container():
    st.markdown("""
    <div class="header" style="text-align:center;">
        <h1>🎵 VibeTrack AI</h1>
        <p>Let your vibe choose the tune</p>
    </div>
    """, unsafe_allow_html=True)

    # User input
    with st.form("recommender_form"):
        caption = st.text_area("🎙️ Describe your video", "a romantic walk under stars", height=100)
        genre = st.selectbox("🎶 Preferred music genre", recommender.get_unique_genres())
        submit = st.form_submit_button("🔍 Recommend")

    if submit:
        with st.spinner("Detecting mood and recommending tracks..."):
            results, detected_mood = recommender.recommend(caption, genre)

        st.markdown("---")

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader(f"🎧 AI Recommended Tracks for mood: `{detected_mood.title()}`")

            if not results.empty:
                for _, row in results.iterrows():
                    title = row['Title']
                    mood = row['Mood'].title()
                    genre = row['Genre']
                    language = row['Language']
                    spotify_url = row.get('SpotifyLink', f"https://open.spotify.com/search/{urllib.parse.quote(title)}")
                    youtube_url = row.get('YouTubeLink', f"https://www.youtube.com/results?search_query={urllib.parse.quote(title)}")

                    st.markdown(f"""
                        <div class="music-card">
                            <h4>{title}</h4>
                            <p>{genre} – {mood} – {language}</p>
                            <a href="{spotify_url}" target="_blank">🎧 Spotify</a>
                            <a href="{youtube_url}" target="_blank">▶ YouTube</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("No matching tracks found.")

        with col_right:
            st.subheader("🌈 AI Detected Mood Preview")
            st.markdown(f"**Detected Mood:** `{detected_mood.title()}`")

            # Load image dynamically
            img_path, img_caption = load_mood_image(detected_mood)
            st.image(img_path, caption=img_caption, use_container_width=True)
            st.text(f"[DEBUG] Mood image path resolved: {img_path}")

    # Footer
    st.markdown("""
    <hr style='margin-top:2rem; margin-bottom:1rem'>
    <p style='text-align: center; color: pink'>
    Made with 💜 by Aparna | VibeTrack AI © 2025
    </p>
    """, unsafe_allow_html=True)

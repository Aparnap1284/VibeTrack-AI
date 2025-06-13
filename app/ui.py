import streamlit as st
import urllib.parse
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recommend_music import MusicRecommendationSystem

# Load mood image helper
def load_mood_image(mood):
    mood = mood.strip().lower()
    # asset path relative to project base
    img = os.path.join(os.path.dirname(__file__), '..', 'assets', f'{mood}.jpg')
    if os.path.exists(img):
        return img, f"{mood.title()} Vibes"
    # fallback
    default = os.path.join(os.path.dirname(__file__), '..', 'assets', 'default.jpg')
    return default, "Default Vibe"

# Page setup
st.set_page_config(page_title="VibeTrack AI", page_icon="🎵", layout="wide")

# Load CSS
css_file = os.path.join(os.path.dirname(__file__), 'styles.css')
if os.path.exists(css_file):
    st.markdown(f"<style>{open(css_file).read()}</style>", unsafe_allow_html=True)

# Initialize recommender
recommender = MusicRecommendationSystem("dataset/reels_dataset.csv")
if recommender.initialize():
    st.error("Failed loading dataset.")
    st.stop()

# Main container
with st.container():
    st.markdown("""
    <div class="header">
        <h1>🎵 VibeTrack AI</h1>
        <p>Let your vibe choose the tune</p>
    </div>
    """, unsafe_allow_html=True)

    # Input form
    with st.form("form"):
        caption = st.text_area("🎙️ Describe your video", height=100)
        genre = st.selectbox("🎶 Preferred music genre", recommender.get_unique_genres())
        submit = st.form_submit_button("🔍 Recommend")

    if submit:
        with st.spinner("Processing..."):
            results, mood = recommender.recommend(caption, genre)
        st.markdown("---")

        lcol, rcol = st.columns([2, 1])

        # Left pane: songs
        with lcol:
            st.subheader(f"🎧 Recommendations for **{mood.title()}** vibe")
            if results.empty:
                st.error("No tracks found.")
            else:
                for _, r in results.iterrows():
                    title, m, g, lang = r['Title'], r['Mood'], r['Genre'], r['Language']
                    spt = r.get('SpotifyLink', f"https://open.spotify.com/search/{urllib.parse.quote(title)}")
                    yt = r.get('YouTubeLink', f"https://www.youtube.com/results?search_query={urllib.parse.quote(title)}")
                    st.markdown(f"""
                    <div class="music-card">
                      <h4>{title}</h4>
                      <p>{g} – {m} – {lang}</p>
                      <a href="{spt}" target="_blank">🎧 Spotify</a>
                      <a href="{yt}" target="_blank">▶ YouTube</a>
                    </div>
                    """, unsafe_allow_html=True)

        # Right pane: mood image
        with rcol:
            st.subheader("🌈 Mood Preview")
            img_path, caption_text = load_mood_image(mood)
            st.image(img_path, caption=caption_text, use_container_width=True)

    # Footer
    st.markdown("""
    <hr>
    <p class="footer">Made with 💜 by Aparna | VibeTrack AI © 2025</p>
    """, unsafe_allow_html=True)

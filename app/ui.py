import streamlit as st
import urllib.parse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))
from src.recommend_music import MusicRecommendationSystem

# Constants
ASSETS_DIR = Path(__file__).parent.parent / "assets"
DEFAULT_IMAGE = ASSETS_DIR / "default.jpg"

def load_mood_image(mood: str) -> tuple[str, str]:
    """Load mood image with proper path handling.
    
    Args:
        mood: The detected mood (case insensitive)
    
    Returns:
        tuple: (image_path, caption)
    """
    mood = mood.strip().lower()
    image_path = ASSETS_DIR / f"{mood}.jpg"
    
    if image_path.exists():
        return str(image_path), f"{mood.title()} Vibes"
    
    return str(DEFAULT_IMAGE), "Default Vibe"

def setup_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="VibeTrack AI",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def load_custom_styles() -> None:
    """Load custom CSS styles."""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Additional inline styles
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
        .music-card {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            background: rgba(245, 245, 245, 0.8);
            transition: transform 0.2s;
        }
        .music-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .music-card a {
            margin-right: 1rem;
            text-decoration: none;
            color: #5b21b6;
            font-weight: 500;
        }
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            color: #5b21b6;
            font-size: 0.9rem;
        }
        .stTextArea textarea {
            min-height: 100px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header() -> None:
    """Render the application header."""
    st.markdown("""
    <div class="header" style="text-align:center; margin-bottom:2rem;">
        <h1 style="color:#5b21b6; font-size:2.5rem;">🎵 VibeTrack AI</h1>
        <p style="font-size:1.1rem; color:#6b7280;">Let your vibe choose the tune</p>
    </div>
    """, unsafe_allow_html=True)

def render_recommendation_results(results, detected_mood: str) -> None:
    """Render the recommendation results section.
    
    Args:
        results: DataFrame containing recommended tracks
        detected_mood: The detected mood from user input
    """
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
                spotify_url = row.get('SpotifyLink', 
                    f"https://open.spotify.com/search/{urllib.parse.quote(title)}")
                youtube_url = row.get('YouTubeLink', 
                    f"https://www.youtube.com/results?search_query={urllib.parse.quote(title)}")

                st.markdown(f"""
                    <div class="music-card">
                        <h4 style="margin-bottom:0.5rem;">{title}</h4>
                        <p style="color:#6b7280; margin-bottom:0.5rem;">
                            {genre} – {mood} – {language}
                        </p>
                        <div style="margin-top:0.5rem;">
                            <a href="{spotify_url}" target="_blank">🎧 Spotify</a>
                            <a href="{youtube_url}" target="_blank">▶ YouTube</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching tracks found. Try adjusting your description or genre.")

    with col_right:
        st.subheader("🌈 AI Detected Mood Preview")
        st.markdown(f"**Detected Mood:** `{detected_mood.title()}`")

        img_path, caption = load_mood_image(detected_mood)
        st.image(
            img_path,
            caption=caption,
            use_column_width=True,
            output_format="auto"
        )

def render_footer() -> None:
    """Render the application footer."""
    st.markdown("""
    <hr style='margin-top:2rem; margin-bottom:1rem; border-color:#e5e7eb'>
    <p style='text-align: center; color: #7c3aed; font-size:0.9rem;'>
    Made with 💜 by Aparna | VibeTrack AI © 2025
    </p>
    """, unsafe_allow_html=True)

def main() -> None:
    """Main application function."""
    setup_page()
    load_custom_styles()

    # Initialize recommender system
    try:
        recommender = MusicRecommendationSystem("dataset/reels_dataset.csv")
        if error := recommender.initialize():
            st.error(f"Initialization error: {error}")
            st.stop()
    except Exception as e:
        st.error(f"Failed to initialize recommender: {str(e)}")
        st.stop()

    # Main UI container
    with st.container():
        render_header()

        # Input form
        with st.form("recommender_form"):
            caption = st.text_area(
                "🎙️ Describe your video",
                "a romantic walk under stars",
                help="Describe the mood or scene of your video"
            )
            
            genre = st.selectbox(
                "🎶 Preferred music genre",
                recommender.get_unique_genres(),
                help="Select your preferred music genre"
            )

            submit = st.form_submit_button(
                "🔍 Recommend",
                use_container_width=True
            )

        if submit:
            with st.spinner("🎶 Detecting mood and recommending tracks..."):
                try:
                    results, detected_mood = recommender.recommend(caption, genre)
                    render_recommendation_results(results, detected_mood)
                except Exception as e:
                    st.error(f"Error generating recommendations: {str(e)}")

        render_footer()

if __name__ == "__main__":
    main()
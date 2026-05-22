import streamlit as st
import urllib.parse
import sys
import os

# Add src path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from src.recommend_music import MusicRecommendationSystem


# Load mood image
def load_mood_image(mood):

    mood = str(mood).strip().lower()

    image_filename = f"{mood}.jpg"

    image_path = os.path.join(
        "assets",
        image_filename
    )

    if os.path.exists(image_path):
        return image_path, f"{mood.title()} Vibes"

    return os.path.join(
        "assets",
        "default.jpg"
    ), "Default Vibe"


# Streamlit config
st.set_page_config(
    page_title="VibeTrack AI",
    page_icon="🎵",
    layout="wide"
)

# Load CSS
css_path = os.path.join(
    os.path.dirname(__file__),
    "styles.css"
)

if os.path.exists(css_path):

    with open(css_path, "r", encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# Initialize recommender
recommender = MusicRecommendationSystem(
    "dataset/reels_dataset.csv"
)

error = recommender.initialize()

if error:
    st.error(error)
    st.stop()


# HEADER
st.markdown(
    """
    <div class="header">
        <h1>🎵 VibeTrack AI</h1>
        <p>Let your vibe choose the tune</p>
    </div>
    """,
    unsafe_allow_html=True
)

# FORM
with st.form("recommend_form"):

    caption = st.text_area(
        "🎙️ Describe your video",
        "a romantic walk under stars",
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:

        genre = st.selectbox(
            "🎶 Preferred Genre",
            recommender.get_unique_genres()
        )

    with col2:

        language = st.selectbox(
            "🌍 Preferred Language",
            ["Any"] + recommender.get_unique_languages()
        )

    submit = st.form_submit_button(
        "✨ Recommend Songs"
    )

# RESULTS
if submit:

    with st.spinner(
        "Finding songs matching your vibe..."
    ):

        results, detected_mood = recommender.recommend(
            caption,
            genre,
            language
        )

    st.markdown("---")

    left_col, right_col = st.columns([2, 1])

    # LEFT SIDE
    with left_col:

        st.subheader(
            f"🎧 Recommended Tracks • Mood: {detected_mood.title()}"
        )

        if not results.empty:

            for _, row in results.iterrows():

                title = str(row['Title'])
                mood = str(row['Mood'])
                genre_name = str(row['Genre'])
                language_name = str(row['Language'])

                spotify_url = (
                    "https://open.spotify.com/search/" +
                    urllib.parse.quote(title)
                )

                youtube_url = (
                    "https://www.youtube.com/results?search_query=" +
                    urllib.parse.quote(title)
                )

                # CLEAN HTML
                st.markdown(f"""
<div class="music-card">

<h3>{title}</h3>

<p>
🎭 {mood} |
🎼 {genre_name} |
🌍 {language_name}
</p>

<div class="button-row">

<a href="{spotify_url}" target="_blank">
🎧 Spotify
</a>

<a href="{youtube_url}" target="_blank">
▶ YouTube
</a>

</div>

</div>
""", unsafe_allow_html=True)

        else:

            st.warning(
                "No matching songs found."
            )

    # RIGHT SIDE
    with right_col:

        st.subheader("🌈 Mood Preview")

        st.markdown(
            f"### {detected_mood.title()} Vibes"
        )

        img_path, caption_text = load_mood_image(
            detected_mood
        )

        st.image(
            img_path,
            caption=caption_text,
            use_container_width=True
        )

# FOOTER
st.markdown(
    """
    <hr>

    <p class="footer">
        Made with 💜 by Aparna • VibeTrack AI © 2025
    </p>
    """,
    unsafe_allow_html=True
)